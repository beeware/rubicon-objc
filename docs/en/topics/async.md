# Asynchronous Programming with Rubicon { #async-rubicon }

One of the banner features of Python 3 is the introduction of native asynchronous programming, implemented in [`asyncio`][].

For an introduction to the use of asynchronous programming, see [the documentation for the asyncio module][asyncio].

## Integrating asyncio with CoreFoundation

The [`asyncio`][] module provides an event loop to coordinate asynchronous features. However, if you're running an Objective-C GUI application, you probably already have an event loop - the one provided by CoreFoundation. This CoreFoundation event loop is then wrapped by `NSApplication` or `UIApplication` in end-user code.

However, you can't have two event loops running at the same time, so you need a way to integrate the two. Luckily, [`asyncio`][] provides a way to customize its event loop so it can be integrated with other event sources.

It does this using a custom event loop. Rubicon provides a `RubiconEventLoop` that inserts Core Foundation event handling into the asyncio event loop.

To use asyncio in a pure Core Foundation application, do the following:

```python
# Import the Event Loop
from rubicon.objc.eventloop import RubiconEventLoop

# Create an event loop, and run it!
loop = RubiconEventLoop()
loop.run_forever()
```

The last call (`loop.run_forever()`) will, as the name suggests, run forever - or, at least, until an event handler calls `loop.stop()` to terminate the event loop.

## Integrating asyncio with AppKit and NSApplication

If you're using AppKit and NSApplication, you don't just need to start the CoreFoundation event loop - you need to start the full `NSApplication` life cycle. To do this, you pass the application instance into the call to `loop.run_forever()`:

```python
# Import the Event Loop and lifecycle
from rubicon.objc.eventloop import RubiconEventLoop, CocoaLifecycle

# Get a handle to the shared NSApplication
from ctypes import cdll, util
from rubicon.objc import ObjCClass

appkit = cdll.LoadLibrary(util.find_library("AppKit"))
NSApplication = ObjCClass("NSApplication")
NSApplication.declare_class_property("sharedApplication")
app = NSApplication.sharedApplication

# Create an event loop, and run it, using the NSApplication!
loop = RubiconEventLoop()
loop.run_forever(lifecycle=CocoaLifecycle(app))
```

Again, this will run "forever" -- until either `loop.stop()` is called, or `terminate:` is invoked on the NSApplication.

## Integrating asyncio with iOS and UIApplication

If you're embedding Python in a UIKit application, use `run_forever_cooperatively()` with an `iOSLifecycle`. This registers asyncio callbacks and returns control to the native launcher, which calls `UIApplicationMain`:

```python
# Import the Event Loop and lifecycle
from rubicon.objc.eventloop import RubiconEventLoop, iOSLifecycle

# Register asyncio callbacks before the native launcher starts UIApplicationMain.
loop = RubiconEventLoop()
loop.run_forever_cooperatively(lifecycle=iOSLifecycle())
```

By default, `iOSLifecycle` starts a nested `NSRunLoop` when UIKit first processes the registered callbacks. This preserves compatibility with older native launchers that hold Python's global interpreter lock (GIL) while running `UIApplicationMain`. Entering the nested loop releases the GIL, allowing background Python threads to run. However, `NSRunLoop.run()` uses the default run-loop mode, preventing UIKit from selecting its tracking mode during scrolling.

### Using the UIKit run loop directly

If your native launcher releases the GIL around `UIApplicationMain`, disable the nested loop:

```python
loop = RubiconEventLoop()
loop.run_forever_cooperatively(lifecycle=iOSLifecycle(nested=False))
```

UIKit then controls the run-loop modes, and Rubicon's callbacks continue to run in the common modes, including the tracking mode. The native application retains ownership of its event loop and application lifetime.

The native Objective-C launcher must detach Python's thread state before entering `UIApplicationMain`, and restore it before using Python's C API again. For example:

```objective-c
PyThreadState *thread_state = PyEval_SaveThread();
@try {
    UIApplicationMain(argc, argv, nil, @"PythonAppDelegate");
}
@finally {
    PyEval_RestoreThread(thread_state);
}
```

The `@finally` block also restores the thread state if an Objective-C exception leaves `UIApplicationMain`. Rubicon's ctypes callbacks acquire the GIL when calling into Python.

Do not set `nested=False` with a launcher that still holds the GIL: background threads can stall until an unrelated main-thread callback gives them an opportunity to run. Waking the run loop cannot release the GIL. Changing Rubicon alone does not update an existing application's native launcher; inspect and rebuild the generated application as well. See [Python's thread-state documentation](https://docs.python.org/3/c-api/threads.html#detaching-the-thread-state-from-extension-code) for details.
