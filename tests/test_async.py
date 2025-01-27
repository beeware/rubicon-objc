from __future__ import annotations

import asyncio
import sys
import time
import unittest

from rubicon.objc.eventloop import RubiconEventLoop


# Some coroutines with known behavior for testing purposes.
async def do_stuff(results, x):
    for i in range(0, x):
        results.append(i)
        await asyncio.sleep(0.1)


async def stop_loop(loop, delay):
    await asyncio.sleep(delay)
    loop.stop()


class AsyncRunTests(unittest.TestCase):
    def setUp(self):
        self.loop = RubiconEventLoop()

    def tearDown(self):
        if sys.version_info < (3, 14):
            asyncio.set_event_loop_policy(None)
        self.loop.close()

    def test_run_until_complete(self):
        results = []
        start = time.time()
        self.loop.run_until_complete(do_stuff(results, 5))
        end = time.time()

        # The co-routine should have accumulated 5 values,
        # and taken at least 0.1*5 == 0.5 seconds to run.
        self.assertEqual(results, [0, 1, 2, 3, 4])
        self.assertGreaterEqual(end - start, 0.5)

    def test_run_forever(self):
        results1 = []
        results2 = []
        start = time.time()
        self.loop.create_task(do_stuff(results1, 3))
        self.loop.create_task(do_stuff(results2, 4))
        self.loop.create_task(stop_loop(self.loop, 0.6))
        self.loop.run_forever()
        end = time.time()

        # The co-routine should have accumulated two
        # independent sets of values (of different lengths).
        # The run duration is controlled by the stop task.
        self.assertEqual(results1, [0, 1, 2])
        self.assertEqual(results2, [0, 1, 2, 3])
        self.assertGreaterEqual(end - start, 0.6)


class AsyncCallTests(unittest.TestCase):
    def setUp(self):
        self.loop = RubiconEventLoop()

    def tearDown(self):
        if sys.version_info < (3, 14):
            asyncio.set_event_loop_policy(None)
        self.loop.close()

    def test_call_soon(self):
        start = time.time()
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()
        end = time.time()

        # The co-routine will be queued immediately,
        # and stop the loop immediately.
        self.assertLessEqual(end - start, 0.05)

    def test_call_later(self):
        start = time.time()
        self.loop.call_later(0.2, self.loop.stop)
        self.loop.run_forever()
        end = time.time()

        # The co-routine will be queued after 0.2 seconds.
        self.assertGreaterEqual(end - start, 0.2)
        self.assertLess(end - start, 0.4)

    def test_call_at(self):
        start = time.time()
        when = self.loop.time() + 0.2
        self.loop.call_at(when, self.loop.stop)
        self.loop.run_forever()
        end = time.time()

        # The co-routine will be queued after 0.2 seconds.
        self.assertGreaterEqual(end - start, 0.2)
        self.assertLess(end - start, 0.4)


class AsyncReaderWriterTests(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        self.server = None

    def tearDown(self):
        # Close the server
        if self.server:
            self.server.close()
            self.loop.run_until_complete(self.server.wait_closed())
        self.loop.close()

    def test_tcp_echo(self):
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

        self.server = self.loop.run_until_complete(
            asyncio.start_server(echo_server, "127.0.0.1", 3742)
        )

        client_messages = []

        async def echo_client(message):
            reader, writer = await asyncio.open_connection("127.0.0.1", 3742)

            writer.write(message.encode())

            data = await reader.read(100)
            client_messages.append(data.decode())

            writer.close()

        self.loop.run_until_complete(echo_client("Hello, World!"))
        self.loop.run_until_complete(echo_client("Goodbye, World!"))

        self.assertEqual(server_messages, ["Hello, World!", "Goodbye, World!"])
        self.assertEqual(client_messages, ["Hello, World!", "Goodbye, World!"])


class AsyncSubprocessTests(unittest.TestCase):
    def setUp(self):
        self.loop = RubiconEventLoop()

    def tearDown(self):
        if sys.version_info < (3, 14):
            asyncio.set_event_loop_policy(None)
        self.loop.close()

    def test_subprocess(self):
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

        task = asyncio.ensure_future(list_dir(), loop=self.loop)
        self.loop.run_until_complete(task)

        # Check for some files that should exist.
        # Everything in the sample set, less everything from the result,
        # should be an empty set.
        self.assertEqual(
            {"README.rst"} - task.result(),
            set(),
        )
