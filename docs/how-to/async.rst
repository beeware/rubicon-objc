=====================================
Asynchronous Programming with Rubicon
=====================================

One of the banner features of Python 3 is the introduction of native
asychronous programming, implemented in the `asyncio`.

For an introduction to the use of asynchronous programming, see `the
documentation for the asyncio module
<https://docs.python.org/3/library/asyncio.html>`, or `this introductory
tutorial to asynchronous programming with asyncio
<http://asyncio.readthedocs.io/en/latest/index.html>`.

Integrating asyncio with CoreFoundation
---------------------------------------

The asyncio module provides an event loop to coordinate asynchronous features.
However, if you're running an Objective C GUI applicaiton, you probably
already have an event loop - the one provided by CoreFoundation. This
CoreFoundation event loop is then wrapped by `NSApplication` or
`UIApplication` in end-user code.

However, you can't have two event loops running at the same time, so you need
a way to integrate the two. Luckily, `asyncio` provides a way to customize
it's event loop so it can be integrated with other event sources.

It does this using an Event Loop Policy. Rubicon provides an Core Foundation
Event Loop Policy that inserts Core Foundation event handling into the asyncio
event loop.

To use asyncio in a pure Core Foundation application, do the following::

    # Import the Event Loop Policy
    from rubicon.objc.async import EventLoopPolicy

    # Install the event loop policy
    asyncio.set_event_loop_policy(EventLoopPolicy())

    # Get an event loop, and run it!
    loop = asyncio.get_event_loop()
    loop.run_forever()

The last call (``loop.run_forever()``) will, as the name suggests, run forever
- or, at least, until an event handler calls ``loop.stop()`` to terminate the
event loop.

Integrating asyncio with AppKit and NSApplication
-------------------------------------------------

If you're using AppKit and NSApplication, you don't just need to start the
CoreFoundation event loop - you need to start the full NSApplication
lifecycle. To do this, you pass the application instance into the call to
``loop.run_forever()``::

    # Import the Event Loop Policy and lifecycle
    from rubicon.objc.async import EventLoopPolicy, CocoaLifecycle

    # Install the event loop policy
    asyncio.set_event_loop_policy(EventLoopPolicy())

    # Get a handle to the shared NSApplication
    from ctypes import cdll, util
    from rubicon.objc import ObjCClass

    appkit = cdll.LoadLibrary(util.find_library('AppKit'))
    NSApplication = ObjCClass('NSApplication')
    app = NSApplication.sharedApplication()

    # Get an event loop, and run it, using the NSApplication!
    loop = asyncio.get_event_loop()
    loop.run_forever(lifecycle=CocoaLifecycle(app))

Again, this will run "forever" -- until either ``loop.stop()`` is called, or
``terminate:`` is invoked on the NSApplication.

.. FIXME once this actually works...
.. Integrating asyncio with iOS and UIApplication
.. ----------------------------------------------

.. If you're using UIKit and UIApplication on iOS, you need to use the iOS
.. lifecycle. To do this, you pass an ``iOSLifecycle`` object into the call to
.. ``loop.run_forever()``::

..     # Import the Event Loop Policy and lifecycle
..     from rubicon.objc.async import EventLoopPolicy, iOSLifecycle

..     # Install the event loop policy
..     asyncio.set_event_loop_policy(EventLoopPolicy())

..     # Get a handle to the shared NSApplication
..     from ctypes import cdll, util
..     from rubicon.objc import ObjCClass

..     appkit = cdll.LoadLibrary(util.find_library('AppKit'))
..     NSApplication = ObjCClass('NSApplication')
..     app = NSApplication.sharedApplication()

..     # Get an event loop, and run it, using the NSApplication!
..     loop = asyncio.get_event_loop()
..     loop.run_forever(lifecycle=iOSLifecycle(app))

.. Again, this will run "forever" -- until either ``loop.stop()`` is called, or
.. ``terminate:`` is invoked on the NSApplication.
