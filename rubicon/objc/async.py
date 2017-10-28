"""PEP 3156 event loop based on CoreFoundation"""

import threading
from asyncio import DefaultEventLoopPolicy, coroutines, events, tasks, unix_events
from ctypes import CFUNCTYPE, POINTER, Structure, c_double, c_long, c_ulong, c_void_p

from .runtime import objc_const, objc_id
from .core_foundation import CFStringRef, libcf

###########################################################################
# CoreFoundation types and constants needed for async handlers
###########################################################################
CFRunLoopRef = objc_id
CFTimeInterval = c_double
CFAbsoluteTime = CFTimeInterval
CFRunLoopTimerRef = objc_id
CFAllocatorRef = objc_id
CFOptionFlags = c_ulong
CFIndex = c_long
CFRunLoopTimerCallBack = CFUNCTYPE(None, CFRunLoopTimerRef, c_void_p)
CFRunLoopMode = CFStringRef


class CFRunLoopTimerContext(Structure):
    _fields_ = [
        ('copyDescription', CFUNCTYPE(CFStringRef, c_void_p)),  # CFStringRef (*copyDescription)(const void *info)
        ('info', c_void_p),
        ('release', CFUNCTYPE(None, c_void_p)),  # void (*release)(const void *info)
        ('retain', CFUNCTYPE(None, c_void_p)),  # const void *(*retain)(const void *info)
        ('version', CFIndex),
    ]


kCFAllocatorDefault = objc_const(libcf, 'kCFAllocatorDefault')
kCFRunLoopCommonModes = objc_const(libcf, 'kCFRunLoopCommonModes')


###########################################################################
# CoreFoundation methods for async handlers
###########################################################################

libcf.CFRunLoopGetMain.restype = CFRunLoopRef
libcf.CFRunLoopGetMain.argtypes = []

libcf.CFAbsoluteTimeGetCurrent.restype = CFAbsoluteTime
libcf.CFAbsoluteTimeGetCurrent.argtypes = []

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

libcf.CFRunLoopAddTimer.restype = None
libcf.CFRunLoopAddTimer.argtypes = [CFRunLoopRef, CFRunLoopTimerRef, CFRunLoopMode]

libcf.CFRunLoopRemoveTimer.restype = None
libcf.CFRunLoopRemoveTimer.argtypes = [CFRunLoopRef, CFRunLoopTimerRef, CFRunLoopMode]


###########################################################################
# CoreFoundation types needed for async handlers
###########################################################################

class CFTimerHandle(events.Handle):
    # __slots__ = ('_source', '_repeat')

    def __init__(self, *, loop, timeout, repeat, callback, args):
        super().__init__(callback, args, loop)

        self._timeout = timeout
        self._repeat = repeat

        # Retain a reference to the Handle
        loop._handlers.add(self)

        # Compute when the timer will fire
        fire_time = libcf.CFAbsoluteTimeGetCurrent() + timeout

        def cfcallback(cftimer, extra):
            callback(*args)

        self._cfcallback = CFRunLoopTimerCallBack(cfcallback)

        self.timer = libcf.CFRunLoopTimerCreate(
            kCFAllocatorDefault,
            fire_time,
            0,  # interval
            0,  # flags
            0,  # order
            self._cfcallback,  # callout
            None,  # context
        )

        libcf.CFRunLoopAddTimer(self._loop._cfrunloop, self.timer, kCFRunLoopCommonModes)

    def cancel(self):
        super().cancel()
        libcf.CFRunLoopRemoveTimer(self._loop._cfrunloop, self.timer, kCFRunLoopCommonModes)
        self._loop._handlers.discard(self)


class CFEventLoop(unix_events.SelectorEventLoop):
    def __init__(self, application=None):
        self._application = application
        self._cfrunloop = libcf.CFRunLoopGetMain()
        self._running = False

        self._handlers = set()
        self._accept_futures = {}

        super().__init__()

    def _check_not_coroutine(self, callback, name):
        """Check whether the given callback is a coroutine or not."""
        if (coroutines.iscoroutine(callback) or coroutines.iscoroutinefunction(callback)):
            raise TypeError("coroutines cannot be used with {}()".format(name))

    def is_running(self):  ###
        return self._running

    def run(self):
        recursive = self.is_running()
        if not recursive and hasattr(events, "_get_running_loop") and events._get_running_loop():
            raise RuntimeError('Cannot run the event loop while another loop is running')

        if not recursive:
            self._running = True
            if hasattr(events, "_set_running_loop"):
                events._set_running_loop(self)

        try:
            self._application.run()
        finally:
            if not recursive:
                self._running = False
                if hasattr(events, "_set_running_loop"):
                    events._set_running_loop(None)

    def run_until_complete(self, future, **kw):
        """Run the event loop until a Future is done.
        Return the Future's result, or raise its exception.
        """
        def stop(f):
            self.stop()

        future = tasks.async(future, loop=self)
        future.add_done_callback(stop)
        try:
            self.run_forever(**kw)
        finally:
            future.remove_done_callback(stop)

        if not future.done():
            raise RuntimeError('Event loop stopped before Future completed.')

        return future.result()

    def run_forever(self, application=None):  ###
        """Run the event loop until stop() is called."""
        if application is not None:
            self.set_application(application)

        if self.is_running():
            raise RuntimeError(
                "Recursively calling run_forever is forbidden. "
                "To recursively run the event loop, call run().")

        try:
            self.run()
        finally:
            self.stop()

    # Methods scheduling callbacks.  All these return Handles.
    def call_soon(self, callback, *args):  ###
        self._check_not_coroutine(callback, 'call_soon')

        return CFTimerHandle(
            loop=self,
            timeout=0,
            repeat=False,
            callback=callback,
            args=args
        )

    call_soon_threadsafe = call_soon  ##

    def call_later(self, delay, callback, *args):  ###
        self._check_not_coroutine(callback, 'call_later')

        return CFTimerHandle(
            loop=self,
            timeout=delay,
            repeat=False,
            callback=callback,
            args=args
        )

    def call_at(self, when, callback, *args):  ###
        self._check_not_coroutine(callback, 'call_at')

        return CFTimerHandle(
            loop=self,
            timeout=when - self.time(),
            repeat=False,
            callback=callback,
            args=args
        )

    def time(self):  ###
        return libcf.CFAbsoluteTimeGetCurrent()

    def stop(self):  ###
        """Stop the inner-most invocation of the event loop.
        Typically, this will mean stopping the event loop completely.
        Note that due to the nature of CF's main loop, stopping may not be
        immediate.
        """
        if self._application is not None:
            self._application.terminate(None)

    def close(self):
        for future in self._accept_futures.values():
            future.cancel()
        self._accept_futures.clear()

        for s in self._handlers:
            s.cancel()
        self._handlers.clear()

        super().close()

    def set_application(self, application):
        if self._application is not None:
            raise ValueError("application is already set")
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
    def __init__(self, application=None):
        self._default_loop = None
        self._application = application
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
            loop = CFEventLoop()
        loop._policy = self

        return loop

    def get_default_loop(self):
        """Get the default event loop."""
        if not self._default_loop:
            self._default_loop = self._new_default_loop()
        return self._default_loop

    def _new_default_loop(self):
        loop = CFEventLoop(application=self._application)
        loop._policy = self
        return loop
