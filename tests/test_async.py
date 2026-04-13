from __future__ import annotations

import asyncio
import sys
import time

import pytest

from rubicon.objc import NSMakePoint, ObjCClass
from rubicon.objc.eventloop import CFLifecycle, CocoaLifecycle, RubiconEventLoop, libcf

NSApplication = ObjCClass("NSApplication")
NSEvent = ObjCClass("NSEvent")


# Some coroutines with known behavior for testing purposes.
async def do_stuff(results, x):
    for i in range(0, x):
        results.append(i)
        await asyncio.sleep(0.1)


async def stop_loop(loop, delay):
    await asyncio.sleep(delay)
    loop.stop()


@pytest.fixture
def loop():
    loop = RubiconEventLoop()
    yield loop
    if sys.version_info < (3, 14):
        asyncio.set_event_loop_policy(None)
    loop.close()


def test_run_until_complete(loop):
    results = []
    start = time.time()
    loop.run_until_complete(do_stuff(results, 5))
    end = time.time()

    # The co-routine should have accumulated 5 values,
    # and taken at least 0.1*5 == 0.5 seconds to run.
    assert results == [0, 1, 2, 3, 4]
    assert (end - start) >= 0.5


def test_run_forever(loop):
    results1 = []
    results2 = []
    start = time.time()
    loop.create_task(do_stuff(results1, 3))
    loop.create_task(do_stuff(results2, 4))
    loop.create_task(stop_loop(loop, 0.6))
    loop.run_forever()
    end = time.time()

    # The co-routine should have accumulated two
    # independent sets of values (of different lengths).
    # The run duration is controlled by the stop task.
    assert results1 == [0, 1, 2]
    assert results2 == [0, 1, 2, 3]
    assert (end - start) >= 0.6


def test_tcp_echo(loop):
    """A simple TCP Echo client/server works as expected."""
    # This tests that you can:
    # * create a TCP server
    # * create a TCP client
    # * write to a socket
    # * read from a socket
    # * be notified of updates on a socket when data arrives.

    # Requires that port 3742 is available for use.

    server_messages = []

    async def echo_server(reader, writer):
        data = await reader.read(100)
        message = data.decode()
        server_messages.append(message)

        writer.write(data)
        await writer.drain()

        writer.close()

    server = None
    try:
        server = loop.run_until_complete(
            asyncio.start_server(echo_server, "127.0.0.1", 3742)
        )

        client_messages = []

        async def echo_client(message):
            reader, writer = await asyncio.open_connection("127.0.0.1", 3742)

            writer.write(message.encode())

            data = await reader.read(100)
            client_messages.append(data.decode())

            writer.close()

        loop.run_until_complete(echo_client("Hello, World!"))
        loop.run_until_complete(echo_client("Goodbye, World!"))

        assert server_messages == ["Hello, World!", "Goodbye, World!"]
        assert client_messages == ["Hello, World!", "Goodbye, World!"]
    finally:
        if server:
            server.close()
            loop.run_until_complete(server.wait_closed())


def test_call_soon(loop):
    start = time.time()
    loop.call_soon(loop.stop)
    loop.run_forever()
    end = time.time()

    # The co-routine will be queued immediately,
    # and stop the loop immediately.
    assert (end - start) <= 0.05


def test_call_later(loop):
    start = time.time()
    loop.call_later(0.2, loop.stop)
    loop.run_forever()
    end = time.time()

    # The co-routine will be queued after 0.2 seconds.
    assert (end - start) >= 0.2
    assert (end - start) < 0.4


def test_call_at(loop):
    start = time.time()
    when = loop.time() + 0.2
    loop.call_at(when, loop.stop)
    loop.run_forever()
    end = time.time()

    # The co-routine will be queued after 0.2 seconds.
    assert (end - start) >= 0.2
    assert (end - start) < 0.4


def test_subprocess(loop):
    async def list_dir():
        proc = await asyncio.create_subprocess_shell(
            "ls",
            stdout=asyncio.subprocess.PIPE,
        )

        entries = set()
        line = await proc.stdout.readline()
        while line:
            entries.add(line.decode("utf-8").strip())
            line = await proc.stdout.readline()

        # Cleanup - close the transport.
        proc._transport.close()
        return entries

    task = asyncio.ensure_future(list_dir(), loop=loop)
    loop.run_until_complete(task)

    # Check for some files that should exist.
    # Everything in the sample set, less everything from the result,
    # should be an empty set.
    assert ({"README.md"} - task.result()) == set()


def test_cf_lifecycle(loop):
    """The simple CFLifecycle works."""
    loop.create_task(stop_loop(loop, 0.6))
    loop.run_forever(lifecycle=CFLifecycle())


def test_cf_lifecycle_explicit(loop):
    """The simple CFLifecycle works with an explicit event loop."""
    loop.create_task(stop_loop(loop, 0.6))
    loop.run_forever(lifecycle=CFLifecycle(libcf.CFRunLoopGetMain()))


def test_cocoa_lifecycle(loop):
    """The full Cocoa Lifecycle works."""

    # Shutting down the Cooca event loop needs a followup event to ensure that
    # post-stop processing occurs.
    async def shutdown(delay):
        await asyncio.sleep(delay)
        loop.stop()
        event = NSEvent.otherEventWithType(
            15,
            location=NSMakePoint(0, 0),
            modifierFlags=0,
            timestamp=0,
            windowNumber=0,
            context=None,
            subtype=0,
            data1=0,
            data2=0,
        )
        NSApplication.sharedApplication.postEvent(event, atStart=True)

    loop.create_task(shutdown(0.6))

    loop.run_forever(lifecycle=CocoaLifecycle(NSApplication.sharedApplication))
