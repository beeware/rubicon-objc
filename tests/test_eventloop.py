from __future__ import annotations

import asyncio
import contextlib
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


def test_socket_handle_ignores_notification_for_unknown_fd(loop, sock):
    handle = CFSocketHandle(loop=loop, fd=sock.fileno())
    del loop._sockets[sock.fileno()]

    handle._cf_socket_callback(
        handle._cf_socket, kCFSocketReadCallBack, None, None, None
    )

    assert handle._src is None
    libcf.CFSocketInvalidate(handle._cf_socket)


def test_socket_handle_cancel_is_noop_while_reader_active(loop, sock):
    """cancel() only tears down the socket once both reader and writer are
    disabled."""
    fd = sock.fileno()
    handle = CFSocketHandle(loop=loop, fd=fd)
    handle.enable_read(lambda: None, ())

    handle.cancel()

    assert fd in loop._sockets
    handle.disable_read()


def test_add_reader_and_remove_reader(loop, sock):
    fd = sock.fileno()
    loop.add_reader(fd, lambda: None)
    assert fd in loop._sockets

    loop.remove_reader(fd)
    assert fd not in loop._sockets


def test_add_writer(loop, sock):
    fd = sock.fileno()
    loop.add_writer(fd, lambda: None)
    assert fd in loop._sockets
    loop.remove_writer(fd)


def test_remove_reader_for_unregistered_fd_returns_false(loop):
    assert loop._remove_reader(99999) is False


def test_call_soon_rejects_coroutine_function(loop):
    async def coro():
        pass

    with pytest.raises(TypeError, match="coroutines cannot be used"):
        loop.call_soon(coro)


def test_run_raises_if_another_loop_is_running(loop):
    sentinel = object()
    events._set_running_loop(sentinel)
    try:
        with pytest.raises(RuntimeError, match="another loop is running"):
            loop.run()
    finally:
        events._set_running_loop(None)


def test_run_supports_recursive_invocation(loop):
    """Unlike run_forever(), run() can be called recursively (e.g. for a
    modal event loop)."""
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


def test_run_until_complete_raises_if_loop_stopped_early(loop):
    future = loop.create_future()
    loop.call_soon(loop.stop)

    with pytest.raises(RuntimeError, match="stopped before Future completed"):
        loop.run_until_complete(future)


def test_run_forever_raises_if_already_running(loop):
    def inner():
        with pytest.raises(RuntimeError, match="Recursively calling run_forever"):
            loop.run_forever()
        loop.stop()

    loop.call_soon(inner)
    loop.run_forever()


def test_run_forever_cooperatively_defers_lifecycle_start(loop):
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


def test_close_cancels_pending_timers(loop):
    handle = loop.call_later(5, lambda: None)
    assert handle in loop._timers

    loop.close()

    assert handle._cancelled
    assert not loop._timers


def test_set_lifecycle_twice_raises_value_error(loop):
    loop._set_lifecycle(CFLifecycle())

    with pytest.raises(ValueError, match="already set"):
        loop._set_lifecycle(CFLifecycle())


def test_set_lifecycle_while_running_raises_runtime_error(loop):
    loop._lifecycle = None
    loop._running = True
    try:
        with pytest.raises(RuntimeError, match="already running"):
            loop._set_lifecycle(CFLifecycle())
    finally:
        loop._running = False


def test_add_callback_skips_cancelled_handle(loop):
    handle = loop.call_soon(lambda: None)
    handle.cancel()

    loop._add_callback(handle)

    assert handle not in loop._timers


def test_new_event_loop_creates_independent_loops(policy):
    default_loop = policy.new_event_loop()
    other_loop = policy.new_event_loop()
    try:
        assert other_loop is not default_loop
        assert isinstance(other_loop, CFEventLoop)
    finally:
        other_loop.close()


def test_get_default_loop_is_memoized(policy):
    assert policy.get_default_loop() is policy.get_default_loop()


@pytest.mark.skipif(
    sys.version_info >= (3, 14),
    reason="Child watcher support was removed in Python 3.14",
)
def test_get_child_watcher_is_memoized(policy):
    policy.get_default_loop()

    with tolerating_child_watcher_deprecation():
        watcher = policy.get_child_watcher()

    assert policy.get_child_watcher() is watcher


@pytest.mark.skipif(
    sys.version_info >= (3, 14),
    reason="Child watcher support was removed in Python 3.14",
)
def test_set_child_watcher_closes_previous_watcher(policy):
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
def test_set_child_watcher_without_existing_watcher(policy):
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
def test_init_watcher_skips_attach_loop_off_main_thread(policy):
    """A watcher created off the main thread is left unattached."""
    policy.get_default_loop()

    def create_watcher():
        with tolerating_child_watcher_deprecation():
            policy.get_child_watcher()

    thread = threading.Thread(target=create_watcher)
    thread.start()
    thread.join()

    assert policy._watcher is not None
