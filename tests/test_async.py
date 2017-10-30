import asyncio
import time
import unittest

from rubicon.objc.async import EventLoopPolicy


# Some coroutines with known behavior for testing purposes.
@asyncio.coroutine
def do_stuff(results, x):
    for i in range(0, x):
        results.append(i)
        yield from asyncio.sleep(0.1)


@asyncio.coroutine
def stop_loop(loop, delay):
    yield from asyncio.sleep(delay)
    loop.stop()


class AsyncRunTests(unittest.TestCase):
    def setUp(self):
        asyncio.set_event_loop_policy(EventLoopPolicy())
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
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
        self.loop.create_task(stop_loop(self.loop, 0.5))
        self.loop.run_forever()
        end = time.time()

        # The co-routine should have accumulated two
        # independent sets of values (of different lengths).
        # The run duration is controlled by the stop task.
        self.assertEqual(results1, [0, 1, 2])
        self.assertEqual(results2, [0, 1, 2, 3])
        self.assertGreaterEqual(end - start, 0.5)


class AsyncCallTests(unittest.TestCase):
    def setUp(self):
        asyncio.set_event_loop_policy(EventLoopPolicy())
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
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
        self.assertLess(end - start, 0.3)

    def test_call_at(self):
        start = time.time()
        when = self.loop.time() + 0.2
        self.loop.call_at(when, self.loop.stop)
        self.loop.run_forever()
        end = time.time()

        # The co-routine will be queued after 0.2 seconds.
        self.assertGreaterEqual(end - start, 0.2)
        self.assertLess(end - start, 0.3)


class AsyncReaderWriterTests(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.server = None

    def tearDown(self):
        # Close the server
        if self.server:
            self.server.close()
            self.loop.run_until_complete(self.server.wait_closed())

    def test_tcp_echo(self):
        """A simple TCP Echo client/server works as expected"""
        # This tests that you can:
        # * create a TCP server
        # * create a TCP client
        # * write to a socket
        # * read from a socket
        # * be notified of updates on a socket when data arrives.

        # Requires that port 3742 is available for use.

        server_messages = []

        @asyncio.coroutine
        def echo_server(reader, writer):
            data = yield from reader.read(100)
            message = data.decode()
            server_messages.append(message)

            writer.write(data)
            yield from writer.drain()

            writer.close()

        self.server = self.loop.run_until_complete(
            asyncio.start_server(echo_server, '127.0.0.1', 3742, loop=self.loop)
        )

        client_messages = []

        @asyncio.coroutine
        def echo_client(message, loop):
            reader, writer = yield from asyncio.open_connection('127.0.0.1', 3742,
                                                                loop=loop)

            writer.write(message.encode())

            data = yield from reader.read(100)
            client_messages.append(data.decode())

            writer.close()

        self.loop.run_until_complete(echo_client('Hello, World!', self.loop))
        self.loop.run_until_complete(echo_client('Goodbye, World!', self.loop))

        self.assertEqual(server_messages, ['Hello, World!', 'Goodbye, World!'])
        self.assertEqual(client_messages, ['Hello, World!', 'Goodbye, World!'])
