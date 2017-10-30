"""PEP 3156 event loop based on CoreFoundation"""

from asyncio import (
    DefaultEventLoopPolicy, coroutines, events, tasks, unix_events
)
from ctypes import (
    CFUNCTYPE, POINTER, Structure, c_double, c_int, c_long, c_ulong, c_void_p
)
import threading

from .core_foundation import (
    CFAbsoluteTime, CFAllocatorRef, CFDataRef, CFOptionFlags,
    CFStringRef, CFTimeInterval, kCFAllocatorDefault, libcf
)
from .runtime import objc_const, objc_id
from .types import CFIndex

###########################################################################
# CoreFoundation types and constants needed for async handlers
###########################################################################

CFRunLoopRef = objc_id
CFRunLoopMode = CFStringRef
CFRunLoopSourceRef = objc_id

CFRunLoopTimerRef = objc_id
CFRunLoopTimerCallBack = CFUNCTYPE(None, CFRunLoopTimerRef, c_void_p)

CFSocketRef = objc_id
CFSocketCallbackType = c_int
CFSocketCallback = CFUNCTYPE(None, CFSocketRef, CFSocketCallbackType, CFDataRef, c_void_p, c_void_p)
CFSocketNativeHandle = c_int


class CFRunLoopTimerContext(Structure):
    _fields_ = [
        ('copyDescription', CFUNCTYPE(CFStringRef, c_void_p)),  # CFStringRef (*copyDescription)(const void *info)
        ('info', c_void_p),
        ('release', CFUNCTYPE(None, c_void_p)),  # void (*release)(const void *info)
        ('retain', CFUNCTYPE(None, c_void_p)),  # const void *(*retain)(const void *info)
        ('version', CFIndex),
    ]


kCFRunLoopCommonModes = objc_const(libcf, 'kCFRunLoopCommonModes')

kCFSocketNoCallBack = 0
kCFSocketReadCallBack = 1
kCFSocketAcceptCallBack = 2
kCFSocketDataCallBack = 3
kCFSocketConnectCallBack = 4
kCFSocketWriteCallBack = 8

kCFSocketAutomaticallyReenableReadCallBack = 1
kCFSocketAutomaticallyReenableWriteCallBack = 8


###########################################################################
# CoreFoundation methods for async handlers
###########################################################################

class CFSocketContext(Structure):
    _fields_ = [
        ('copyDescription', CFUNCTYPE(CFStringRef, c_void_p)),  # CFStringRef (*copyDescription)(const void *info)
        ('info', c_void_p),
        ('release', CFUNCTYPE(None, c_void_p)),  # void (*release)(const void *info)
        ('retain', CFUNCTYPE(None, c_void_p)),  # const void *(*retain)(const void *info)
        ('version', CFIndex),
    ]


libcf.CFAbsoluteTimeGetCurrent.restype = CFAbsoluteTime
libcf.CFAbsoluteTimeGetCurrent.argtypes = []

libcf.CFRunLoopAddSource.restype = None
libcf.CFRunLoopAddSource.argtypes = [CFRunLoopRef, CFRunLoopSourceRef, CFRunLoopMode]

libcf.CFRunLoopAddTimer.restype = None
libcf.CFRunLoopAddTimer.argtypes = [CFRunLoopRef, CFRunLoopTimerRef, CFRunLoopMode]

libcf.CFRunLoopRemoveSource.restype = None
libcf.CFRunLoopRemoveSource.argtypes = [CFRunLoopRef, CFRunLoopSourceRef, CFRunLoopMode]

libcf.CFRunLoopRemoveTimer.restype = None
libcf.CFRunLoopRemoveTimer.argtypes = [CFRunLoopRef, CFRunLoopTimerRef, CFRunLoopMode]

libcf.CFRunLoopRun.restype = None
libcf.CFRunLoopRun.argtypes = []

libcf.CFRunLoopStop.restype = None
libcf.CFRunLoopStop.argtypes = [CFRunLoopRef]

libcf.CFRunLoopTimerCreate.restype = CFRunLoopTimerRef
libcf.CFRunLoopTimerCreate.argtypes = [
    CFAllocatorRef,
    CFAbsoluteTime,
    CFTimeInterval,
    CFOptionFlags,
    CFIndex,
    CFRunLoopTimerCallBack,
    POINTER(CFRunLoopTimerContext),
]

libcf.CFSocketCreateRunLoopSource.restype = CFRunLoopSourceRef
libcf.CFSocketCreateRunLoopSource.argtypes = [CFAllocatorRef, CFSocketRef, CFIndex]

libcf.CFSocketCreateWithNative.restype = CFSocketRef
libcf.CFSocketCreateWithNative.argtypes = [
    CFAllocatorRef,
    CFSocketNativeHandle,
    CFOptionFlags,
    CFSocketCallback,
    POINTER(CFSocketContext)
]

libcf.CFSocketDisableCallBacks.restype = None
libcf.CFSocketDisableCallBacks.argtypes = [CFSocketRef, CFOptionFlags]

libcf.CFSocketEnableCallBacks.restype = None
libcf.CFSocketEnableCallBacks.argtypes = [CFSocketRef, CFOptionFlags]

libcf.CFSocketInvalidate.restype = None
libcf.CFSocketInvalidate.argtypes = [CFSocketRef]

libcf.CFSocketSetSocketFlags.restype = None
libcf.CFSocketSetSocketFlags.argtypes = [CFSocketRef, CFOptionFlags]


###########################################################################
# CoreFoundation types needed for async handlers
###########################################################################

class CFTimerHandle(events.TimerHandle):
    def _cf_timer_callback(self, callback, args):
        # Create a CF-compatible callback for a timer event
        def cf_timer_callback(cftimer, extra):
            callback(*args)
        return CFRunLoopTimerCallBack(cf_timer_callback)

    def __init__(self, *, loop, timeout, repeat, callback, args):
        super().__init__(
            libcf.CFAbsoluteTimeGetCurrent() + timeout,
            self._cf_timer_callback(callback, args),
            None,
            loop
        )

        self._timeout = timeout
        self._repeat = repeat

        # Retain a reference to the Handle
        self._loop._timers.add(self)

        # Create the timer event, and add it to the run loop.
        self._timer = libcf.CFRunLoopTimerCreate(
            kCFAllocatorDefault,
            self._when,
            0,  # interval
            0,  # flags
            0,  # order
            self._callback,  # callout
            None,  # context
        )

        libcf.CFRunLoopAddTimer(self._loop._cfrunloop, self._timer, kCFRunLoopCommonModes)

    def cancel(self):
        super().cancel()
        libcf.CFRunLoopRemoveTimer(self._loop._cfrunloop, self._timer, kCFRunLoopCommonModes)
        self._loop._timers.discard(self)


class CFSocketHandle(events.Handle):
    # Create a CF-compatible callback for a source event
    def _cf_socket_callback(self, cfSocket, callbackType,
                            ignoredAddress, ignoredData, context):
        if self._fd not in self._loop._sockets:
            # Spurious notifications seem to be generated sometimes if you
            # CFSocketDisableCallBacks in the middle of an event.  I don't know
            # about this FD, any more, so let's get rid of it.
            libcf.CFRunLoopRemoveSource(
                self._loop._cfrunloop, self._src, kCFRunLoopCommonModes
            )
            return

        if callbackType == kCFSocketReadCallBack:
            callback, args = self._reader
        elif callbackType == kCFSocketWriteCallBack:
            callback, args = self._writer
        else:
            callback = None

        if callback:
            callback(*args)

    def __init__(self, *, loop, fd):
        """
        Register a file descriptor with the C{CFRunLoop}, or modify its state
        so that it's listening for both notifications (read and write) rather
        than just one; used to implement C{addReader} and C{addWriter}.
        @param fd: The file descriptor.
        @type fd: L{int}
        @param descr: the L{IReadDescriptor} or L{IWriteDescriptor}
        @param flag: the flag to register for callbacks on, either
            C{kCFSocketReadCallBack} or C{kCFSocketWriteCallBack}
        """
        super().__init__(CFSocketCallback(self._cf_socket_callback), None, loop)

        # Retain a reference to the Handle
        self._loop._sockets[fd] = self
        self._reader = None
        self._writer = None

        self._fd = fd
        self._cf_socket = libcf.CFSocketCreateWithNative(
            kCFAllocatorDefault, self._fd,
            kCFSocketReadCallBack | kCFSocketWriteCallBack |
            kCFSocketConnectCallBack,
            self._callback,
            None
        )
        libcf.CFSocketSetSocketFlags(
            self._cf_socket,
            kCFSocketAutomaticallyReenableReadCallBack |
            kCFSocketAutomaticallyReenableWriteCallBack

            # # This extra flag is to ensure that CF doesn't (destructively,
            # # because destructively is the only way to do it) retrieve
            # # SO_ERROR
            # 1 << 6
        )
        self._src = libcf.CFSocketCreateRunLoopSource(kCFAllocatorDefault, self._cf_socket, 0)
        libcf.CFRunLoopAddSource(self._loop._cfrunloop, self._src, kCFRunLoopCommonModes)
        libcf.CFSocketDisableCallBacks(
            self._cf_socket,
            kCFSocketReadCallBack | kCFSocketWriteCallBack |
            kCFSocketConnectCallBack
        )

    def enable_read(self, callback, args):
        libcf.CFSocketEnableCallBacks(self._cf_socket, kCFSocketReadCallBack)
        self._reader = (callback, args)

    def disable_read(self):
        libcf.CFSocketDisableCallBacks(self._cf_socket, kCFSocketReadCallBack)
        self._reader = None
        self.cancel()

    def enable_write(self, callback, args):
        libcf.CFSocketEnableCallBacks(self._cf_socket, kCFSocketWriteCallBack)
        self._writer = (callback, args)

    def disable_write(self):
        libcf.CFSocketDisableCallBacks(self._cf_socket, kCFSocketWriteCallBack)
        self._writer = None
        self.cancel()

    def cancel(self):
        """
        """
        if self._reader is None and self._writer is None:
            super().cancel()
            del self._loop._sockets[self._fd]

            libcf.CFRunLoopRemoveSource(self._loop._cfrunloop, self._src, kCFRunLoopCommonModes)
            libcf.CFSocketInvalidate(self._cf_socket)


class CFEventLoop(unix_events.SelectorEventLoop):
    def __init__(self, application=None):
        self._application = application
        self._cfrunloop = libcf.CFRunLoopGetMain()
        self._running = False

        self._timers = set()
        self._accept_futures = {}
        self._sockets = {}

        super().__init__()

    def _add_reader(self, fd, callback, *args):
        try:
            handle = self._sockets[fd]
        except KeyError:
            handle = CFSocketHandle(loop=self, fd=fd)
            self._sockets[fd] = handle

        handle.enable_read(callback, args)

    def add_reader(self, fd, callback, *args):
        """Add a reader callback."""
        self._ensure_fd_no_transport(fd)
        self._add_reader(fd, callback, *args)

    def _remove_reader(self, fd):
        self._ensure_fd_no_transport(fd)

        try:
            self._sockets[fd].disable_read()
            return True
        except KeyError:
            return False

    def remove_reader(self, fd):
        """Remove a reader callback."""
        self._ensure_fd_no_transport(fd)
        self._remove_reader(self, fd)

    def _add_writer(self, fd, callback, *args):
        self._ensure_fd_no_transport(fd)

        try:
            handle = self._sockets[fd]
        except KeyError:
            handle = CFSocketHandle(loop=self, fd=fd)
            self._sockets[fd] = handle

        handle.enable_write(callback, args)

    def add_writer(self, fd, callback, *args):
        """Add a writer callback.."""
        self._add_writer(fd, callback, *args)

    def _remove_writer(self, fd):
        self._ensure_fd_no_transport(fd)

        try:
            self._sockets[fd].disable_write()
            return True
        except KeyError:
            return False

    def remove_writer(self, fd):
        """Remove a writer callback."""
        self._ensure_fd_no_transport(fd)
        self._remove_writer(fd)

    ######################################################################
    # Lifecycle and execution
    ######################################################################
    def _check_not_coroutine(self, callback, name):
        """Check whether the given callback is a coroutine or not."""
        if (coroutines.iscoroutine(callback) or coroutines.iscoroutinefunction(callback)):
            raise TypeError("coroutines cannot be used with {}()".format(name))

    def is_running(self):
        """Returns True if the event loop is running."""
        return self._running

    def run(self):
        """Internal implementatin of run using the CoreFoundation event loop."""
        recursive = self.is_running()
        if not recursive and hasattr(events, "_get_running_loop") and events._get_running_loop():
            raise RuntimeError('Cannot run the event loop while another loop is running')

        if not recursive:
            self._running = True
            if hasattr(events, "_set_running_loop"):
                events._set_running_loop(self)

        try:
            if self._application:
                self._application.run()
            else:
                libcf.CFRunLoopRun()
        finally:
            if not recursive:
                self._running = False
                if hasattr(events, "_set_running_loop"):
                    events._set_running_loop(None)

    def run_until_complete(self, future, **kw):
        """Run until the Future is done.

        If the argument is a coroutine, it is wrapped in a Task.

        WARNING: It would be disastrous to call run_until_complete()
        with the same coroutine twice -- it would wrap it in two
        different Tasks and that can't be good.

        Return the Future's result, or raise its exception.
        """
        def stop(f):
            self.stop()

        future = tasks.ensure_future(future, loop=self)
        future.add_done_callback(stop)
        try:
            self.run_forever(**kw)
        finally:
            future.remove_done_callback(stop)

        if not future.done():
            raise RuntimeError('Event loop stopped before Future completed.')

        return future.result()

    def run_forever(self, application=None):
        """Run until stop() is called."""
        self.set_application(application)

        if self.is_running():
            raise RuntimeError(
                "Recursively calling run_forever is forbidden. "
                "To recursively run the event loop, call run().")

        try:
            self.run()
        finally:
            self.stop()

    def call_soon(self, callback, *args):
        """Arrange for a callback to be called as soon as possible.

        This operates as a FIFO queue: callbacks are called in the
        order in which they are registered.  Each callback will be
        called exactly once.

        Any positional arguments after the callback will be passed to
        the callback when it is called.
        """
        self._check_not_coroutine(callback, 'call_soon')

        return CFTimerHandle(
            loop=self,
            timeout=0,
            repeat=False,
            callback=callback,
            args=args
        )

    call_soon_threadsafe = call_soon

    def call_later(self, delay, callback, *args):
        """Arrange for a callback to be called at a given time.

        Return a Handle: an opaque object with a cancel() method that
        can be used to cancel the call.

        The delay can be an int or float, expressed in seconds.  It is
        always relative to the current time.

        Each callback will be called exactly once.  If two callbacks
        are scheduled for exactly the same time, it undefined which
        will be called first.

        Any positional arguments after the callback will be passed to
        the callback when it is called.
        """
        self._check_not_coroutine(callback, 'call_later')

        return CFTimerHandle(
            loop=self,
            timeout=delay,
            repeat=False,
            callback=callback,
            args=args
        )

    def call_at(self, when, callback, *args):
        """Like call_later(), but uses an absolute time.

        Absolute time corresponds to the event loop's time() method.
        """
        self._check_not_coroutine(callback, 'call_at')

        return CFTimerHandle(
            loop=self,
            timeout=when - self.time(),
            repeat=False,
            callback=callback,
            args=args
        )

    def time(self):
        """Return the time according to the event loop's clock.

        This is a float expressed in seconds since an epoch, but the
        epoch, precision, accuracy and drift are unspecified and may
        differ per event loop.
        """
        return libcf.CFAbsoluteTimeGetCurrent()

    def stop(self):
        """Stop running the event loop.

        Every callback already scheduled will still run.  This simply informs
        run_forever to stop looping after a complete iteration.
        """
        if self._application:
            self._application.terminate()
        else:
            libcf.CFRunLoopStop(self._cfrunloop)

    def close(self):
        """Close the event loop.

        This clears the queues and shuts down the executor,
        but does not wait for the executor to finish.

        The event loop must not be running.
        """
        while self._accept_futures:
            future = self._accept_futures.pop()
            future.cancel()

        while self._timers:
            handler = self._timers.pop()
            handler.cancel()

        super().close()

    def set_application(self, application):
        """Set the application that is controlling this loop.
        """
        if self._application is not None:
            raise ValueError("Application is already set")
        if self.is_running():
            raise RuntimeError("You can't add the application to a loop that's already running.")
        self._application = application
        self._policy._application = application


class CFEventLoopPolicy(events.AbstractEventLoopPolicy):
    """Default CF event loop policy
    In this policy, each thread has its own event loop. However, we only
    automatically create an event loop by default for the main thread; other
    threads by default have no event loop.
    """
    def __init__(self):
        self._application = None
        self._default_loop = None
        self._watcher_lock = threading.Lock()
        self._watcher = None
        self._policy = DefaultEventLoopPolicy()
        self._policy.new_event_loop = self.new_event_loop
        self.get_event_loop = self._policy.get_event_loop
        self.set_event_loop = self._policy.set_event_loop

    def get_child_watcher(self):
        raise NotImplementedError()
        # if self._watcher is None:
        #     with self._watcher_lock:
        #         if self._watcher is None:
        #             self._watcher = CFChildWatcher()
        # return self._watcher

    def set_child_watcher(self, watcher):
        raise NotImplementedError()
        """Set a child watcher.

        Must be an an instance of CFChildWatcher, as it ties in with CF
        appropriately.
        """

        # if watcher is not None and not isinstance(watcher, CFChildWatcher):
        #     raise TypeError("Only CFChildWatcher is supported!")

        # with self._watcher_lock:
        #     self._watcher = watcher

    def new_event_loop(self):
        """Create a new event loop and return it."""
        if not self._default_loop and isinstance(threading.current_thread(), threading._MainThread):
            loop = self.get_default_loop()
        else:
            loop = CFEventLoop(self._application)
        loop._policy = self

        return loop

    def get_default_loop(self):
        """Get the default event loop."""
        if not self._default_loop:
            self._default_loop = self._new_default_loop()
        return self._default_loop

    def _new_default_loop(self):
        loop = CFEventLoop(self._application)
        loop._policy = self
        return loop
