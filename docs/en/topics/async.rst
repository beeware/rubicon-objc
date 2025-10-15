=====================================
Asynchronous Programming with Rubicon
=====================================

One of the banner features of Python 3 is the introduction of native
asynchronous programming, implemented in :mod:`asyncio`.

For an introduction to the use of asynchronous programming, see `the
documentation for the asyncio module
<https://docs.python.org/3/library/asyncio.html>`__.

Integrating asyncio with CoreFoundation
=======================================

The :mod:`asyncio` module provides an event loop to coordinate asynchronous
features. However, if you're running an Objective C GUI application, you
probably already have an event loop - the one provided by CoreFoundation.
This CoreFoundation event loop is then wrapped by ``NSApplication`` or
``UIApplication`` in end-user code.

However, you can't have two event loops running at the same time, so you need
a way to integrate the two. Luckily, :mod:`asyncio` provides a way to customize
it's event loop so it can be integrated with other event sources.

It does this using a custom event loop. Rubicon provides a ``RubiconEventLoop``
that inserts Core Foundation event handling into the asyncio event loop.

To use asyncio in a pure Core Foundation application, do the following::

    # Import the Event Loop
    from rubicon.objc.eventloop import RubiconEventLoop

    # Create an event loop, and run it!
    loop = RubiconEventLoop()
    loop.run_forever()

The last call (``loop.run_forever()``) will, as the name suggests, run forever
- or, at least, until an event handler calls ``loop.stop()`` to terminate the
event loop.

Integrating asyncio with AppKit and ``NSApplication``
=====================================================

If you're using AppKit and NSApplication, you don't just need to start the
CoreFoundation event loop - you need to start the full ``NSApplication``
life cycle. To do this, you pass the application instance into the call to
``loop.run_forever()``::

    # Import the Event Loop and lifecycle
    from rubicon.objc.eventloop import RubiconEventLoop, CocoaLifecycle

    # Get a handle to the shared NSApplication
    from ctypes import cdll, util
    from rubicon.objc import ObjCClass

    appkit = cdll.LoadLibrary(util.find_library('AppKit'))
    NSApplication = ObjCClass('NSApplication')
    NSApplication.declare_class_property('sharedApplication')
    app = NSApplication.sharedApplication

    # Create an event loop, and run it, using the NSApplication!
    loop = RubiconEventLoop()
    loop.run_forever(lifecycle=CocoaLifecycle(app))

Again, this will run "forever" -- until either ``loop.stop()`` is called, or
``terminate:`` is invoked on the NSApplication.

Integrating asyncio with iOS and UIApplication
==============================================

If you're using UIKit and UIApplication on iOS, you need to use the iOS
life cycle. To do this, you pass an ``iOSLifecycle`` object into the call to
``loop.run_forever()``::

    # Import the Event Loop and lifecycle
    from rubicon.objc.eventloop import RubiconEventLoop, iOSLifecycle

    # Create an event loop, and run it, using the UIApplication!
    loop = RubiconEventLoop()
    loop.run_forever(lifecycle=iOSLifecycle())

Again, this will run "forever" -- until either ``loop.stop()`` is called, or
``terminate:`` is invoked on the UIApplication.
