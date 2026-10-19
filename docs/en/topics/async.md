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

By default, `iOSLifecycle` checks the native launcher's capability flag, `sys._ios_app_main_releases_gil`. If the flag is exactly `True`, UIKit owns the run loop and can select its tracking mode during scrolling. Rubicon's callbacks continue to run in the common modes, including the tracking mode. The native application retains ownership of its event loop and application lifetime.

If the flag is absent or is not `True`, `iOSLifecycle` starts a nested `NSRunLoop` when UIKit first processes the registered callbacks. This preserves compatibility with older native launchers that hold Python's global interpreter lock (GIL) while running `UIApplicationMain`. Entering the nested loop releases the GIL, allowing background Python threads to run. However, `NSRunLoop.run()` uses the default run-loop mode, preventing UIKit from selecting its tracking mode during scrolling.

Updating Rubicon alone preserves nesting with an older launcher. Updating the launcher alone preserves nesting with older Rubicon versions. Updating both automatically uses the UIKit loop through the existing `iOSLifecycle()` call; no Toga or application code change is required. Existing applications must regenerate or patch their native launcher and rebuild it to pick up the launcher change. Updating Python dependencies alone does not replace the native code.

### Native launcher capability

The flag is a promise made by the native launcher, not a Python version check or a statement that the GIL is currently released. After initializing Python and before importing application code, a launcher that releases the GIL around `UIApplicationMain` advertises this capability:

```objective-c
if (PySys_SetObject("_ios_app_main_releases_gil", Py_True) < 0) {
    // Abort startup using the launcher's error handling.
    PyErr_Print();
    return 1;
}
```

After application code returns, the launcher must detach Python's thread state before entering `UIApplicationMain`, and restore it before using Python's C API again:

```objective-c
PyThreadState *thread_state = PyEval_SaveThread();
@try {
    UIApplicationMain(argc, argv, nil, @"PythonAppDelegate");
}
@finally {
    PyEval_RestoreThread(thread_state);
}
```

The `@finally` block also restores the thread state if an Objective-C exception leaves `UIApplicationMain`. Rubicon's ctypes callbacks acquire the GIL when calling into Python. `PySys_SetObject` keeps a reference to the capability value; the launcher does not transfer ownership of `Py_True` or retain an Objective-C application object for this capability.

Do not set this flag in application code to bypass detection. A launcher that still holds the GIL must leave the flag absent or set it to `False`: otherwise background threads can stall until an unrelated main-thread callback gives them an opportunity to run. Waking the run loop cannot release the GIL. See [Python's thread-state documentation](https://docs.python.org/3/c-api/threads.html#detaching-the-thread-state-from-extension-code) for details.

### Overriding automatic detection

`iOSLifecycle(nested=True)` always uses the nested loop. `iOSLifecycle(nested=False)` always uses the UIKit loop, and is only suitable for a native launcher known to release the GIL, even if it does not advertise the capability. Omitting `nested`, or passing `None`, selects the automatic behavior.
