from __future__ import annotations

import asyncio
import contextlib
import importlib
import socket
import sys
import threading
import warnings
from asyncio import events

import pytest

from rubicon.objc.eventloop import (
    CFEventLoop,
    CFLifecycle,
    CFSocketHandle,
    EventLoopPolicy,
    RubiconEventLoop,
    kCFSocketReadCallBack,
    libcf,
)


@pytest.fixture
def loop():
    loop = RubiconEventLoop()
    yield loop
    if sys.version_info < (3, 14):
        asyncio.set_event_loop_policy(None)
    loop.close()


@pytest.fixture
def policy():
    with pytest.warns(DeprecationWarning):
        policy = EventLoopPolicy()
    yield policy
    if policy._default_loop is not None:
        policy._default_loop.close()


@pytest.fixture
def sock():
    sock = socket.socket()
    yield sock
    sock.close()


@contextlib.contextmanager
def tolerating_child_watcher_deprecation():
    """SafeChildWatcher only emits a DeprecationWarning on Python 3.12+;
    tolerate it either way instead of asserting it must occur."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        yield


@pytest.mark.skipif(
    sys.platform not in ("darwin", "ios"),
    reason="Requires Apple Objective-C runtime",
)
def test_ios_has_no_nsevent():
    """Re-importing eventloop with sys.platform set to iOS must not define NSEvent."""
    name = "rubicon.objc.eventloop"
    saved_platform = sys.platform
    try:
        sys.platform = "ios"
        sys.modules.pop(name, None)
        module = importlib.import_module(name)
        assert not hasattr(module, "NSEvent")
    finally:
        sys.platform = saved_platform
        sys.modules.pop(name, None)
        importlib.import_module(name)


def test_socket_handle_unknown_fd(loop, sock):
    """A notification for an fd the loop no longer tracks is ignored."""
    handle = CFSocketHandle(loop=loop, fd=sock.fileno())
    del loop._sockets[sock.fileno()]

    handle._cf_socket_callback(
        handle._cf_socket, kCFSocketReadCallBack, None, None, None
    )

    assert handle._src is None
    libcf.CFSocketInvalidate(handle._cf_socket)


def test_socket_handle_cancel_partial(loop, sock):
    """Cancelling a socket handle is a no-op while a reader/writer is active."""
    fd = sock.fileno()
    handle = CFSocketHandle(loop=loop, fd=fd)
    handle.enable_read(lambda: None, ())

    handle.cancel()

    assert fd in loop._sockets
    handle.disable_read()


def test_add_remove_reader(loop, sock):
    """Adding and removing a reader registers and deregisters its socket."""
    fd = sock.fileno()
    loop.add_reader(fd, lambda: None)
    assert fd in loop._sockets

    loop.remove_reader(fd)
    assert fd not in loop._sockets


def test_add_remove_writer(loop, sock):
    """Adding and removing a writer registers and deregisters its socket."""
    fd = sock.fileno()
    loop.add_writer(fd, lambda: None)
    assert fd in loop._sockets
    loop.remove_writer(fd)


def test_remove_reader_unregistered(loop):
    """Removing a reader for an unregistered file descriptor reports failure."""
    assert loop._remove_reader(99999) is False


def test_call_soon_coroutine_rejected(loop):
    """call_soon() rejects coroutine functions."""

    async def coro():
        pass

    with pytest.raises(TypeError, match="coroutines cannot be used"):
        loop.call_soon(coro)


def test_run_nested_loop_error(loop):
    """run() refuses to start while another event loop is already running."""
    sentinel = object()
    events._set_running_loop(sentinel)
    try:
        with pytest.raises(RuntimeError, match="another loop is running"):
            loop.run()
    finally:
        events._set_running_loop(None)


def test_run_recursive(loop):
    """run() can be invoked recursively, e.g. to drive a modal event loop."""
    order = []

    def inner():
        order.append("inner-start")
        loop.call_soon(loop.stop)
        loop.run()
        order.append("inner-end")
        loop.stop()

    loop.call_soon(inner)
    loop.run_forever()

    assert order == ["inner-start", "inner-end"]


def test_run_until_complete_stopped_early(loop):
    """run_until_complete() raises if the loop stops before the future completes."""
    future = loop.create_future()
    loop.call_soon(loop.stop)

    with pytest.raises(RuntimeError, match="stopped before Future completed"):
        loop.run_until_complete(future)


def test_run_forever_recursive_error(loop):
    """run_forever() refuses to be called recursively."""

    def inner():
        with pytest.raises(RuntimeError, match="Recursively calling run_forever"):
            loop.run_forever()
        loop.stop()

    loop.call_soon(inner)
    loop.run_forever()


def test_run_forever_cooperatively(loop):
    """run_forever_cooperatively() marks the loop as running without blocking."""
    assert not loop.is_running()

    loop.run_forever_cooperatively()

    assert loop.is_running()
    assert isinstance(loop._lifecycle, CFLifecycle)

    with pytest.raises(RuntimeError, match="Recursively calling run_forever"):
        loop.run_forever_cooperatively()

    # Nothing pumps the CFRunLoop in this test, so the deferred
    # lifecycle.start() callback never fires. Reset the state it left
    # behind so the fixture's teardown can close the loop.
    loop._running = False
    events._set_running_loop(None)


def test_close_cancels_timers(loop):
    """Closing the loop cancels any pending timers."""
    handle = loop.call_later(5, lambda: None)
    assert handle in loop._timers

    loop.close()

    assert handle._cancelled
    assert not loop._timers


def test_close_cancels_accept_futures(loop):
    """Closing the loop cancels any pending accept() futures."""
    future = loop.create_future()
    loop._accept_futures = {future}

    loop.close()

    assert future.cancelled()
    assert not loop._accept_futures


def test_set_lifecycle_twice(loop):
    """Setting the lifecycle a second time is rejected."""
    loop._set_lifecycle(CFLifecycle())

    with pytest.raises(ValueError, match="already set"):
        loop._set_lifecycle(CFLifecycle())


def test_set_lifecycle_while_running(loop):
    """Setting the lifecycle while the loop is running is rejected."""
    loop._lifecycle = None
    loop._running = True
    try:
        with pytest.raises(RuntimeError, match="already running"):
            loop._set_lifecycle(CFLifecycle())
    finally:
        loop._running = False


def test_add_callback_cancelled(loop):
    """Adding a cancelled callback handle does not schedule it."""
    handle = loop.call_soon(lambda: None)
    handle.cancel()

    loop._add_callback(handle)

    assert handle not in loop._timers


def test_new_event_loop(policy):
    """Each additional call to new_event_loop() returns an independent loop."""
    default_loop = policy.new_event_loop()
    other_loop = policy.new_event_loop()
    try:
        assert other_loop is not default_loop
        assert isinstance(other_loop, CFEventLoop)
    finally:
        other_loop.close()


def test_get_default_loop_is_memoized(policy):
    """get_default_loop() returns the same loop instance on repeated calls."""
    assert policy.get_default_loop() is policy.get_default_loop()


@pytest.mark.skipif(
    sys.version_info >= (3, 14),
    reason="Child watcher support was removed in Python 3.14",
)
def test_get_child_watcher_is_memoized(policy):
    """get_child_watcher() returns the same watcher instance on repeated calls."""
    policy.get_default_loop()

    with tolerating_child_watcher_deprecation():
        watcher = policy.get_child_watcher()

    assert policy.get_child_watcher() is watcher


@pytest.mark.skipif(
    sys.version_info >= (3, 14),
    reason="Child watcher support was removed in Python 3.14",
)
def test_set_child_watcher_replaces(policy):
    """Setting a new child watcher closes the previous one."""
    from asyncio import SafeChildWatcher

    policy.get_default_loop()
    with tolerating_child_watcher_deprecation():
        policy.get_child_watcher()
        new_watcher = SafeChildWatcher()

    policy.set_child_watcher(new_watcher)

    assert policy._watcher is new_watcher


@pytest.mark.skipif(
    sys.version_info >= (3, 14),
    reason="Child watcher support was removed in Python 3.14",
)
def test_set_child_watcher_first(policy):
    """Setting a child watcher works even when none was previously set."""
    from asyncio import SafeChildWatcher

    assert policy._watcher is None

    with tolerating_child_watcher_deprecation():
        watcher = SafeChildWatcher()
    policy.set_child_watcher(watcher)

    assert policy._watcher is watcher


@pytest.mark.skipif(
    sys.version_info >= (3, 14),
    reason="Child watcher support was removed in Python 3.14",
)
def test_init_watcher_off_main_thread(policy):
    """A watcher created off the main thread is left unattached to a loop."""
    policy.get_default_loop()

    def create_watcher():
        with tolerating_child_watcher_deprecation():
            policy.get_child_watcher()

    thread = threading.Thread(target=create_watcher)
    thread.start()
    thread.join()

    assert policy._watcher is not None


def test_eventloop_import_without_policy(monkeypatch):
    """Python 3.16 drops EventLoopPolicy; RubiconEventLoop becomes CFEventLoop."""
    name = "rubicon.objc.eventloop"

    if sys.version_info >= (3, 16):
        import rubicon.objc.eventloop as module

        assert module.RubiconEventLoop is module.CFEventLoop
        assert not hasattr(module, "EventLoopPolicy")
        return

    monkeypatch.setattr(sys, "version_info", (3, 16, 0, "final", 0))
    sys.modules.pop(name, None)
    try:
        module = importlib.import_module(name)
        assert module.RubiconEventLoop is module.CFEventLoop
        assert not hasattr(module, "EventLoopPolicy")
    finally:
        sys.modules.pop(name, None)
        importlib.import_module(name)
