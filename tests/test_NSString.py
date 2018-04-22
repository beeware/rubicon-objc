import faulthandler
import unittest
from ctypes import CDLL, util

from rubicon.objc import ns_from_py, py_from_ns
from rubicon.objc.runtime import NSString

try:
    import platform
    OSX_VERSION = tuple(int(v) for v in platform.mac_ver()[0].split('.')[:2])
except Exception:
    OSX_VERSION = None


# Load the test harness library
rubiconharness_name = util.find_library('rubiconharness')
if rubiconharness_name is None:
    raise RuntimeError("Couldn't load Rubicon test harness library. Have you set DYLD_LIBRARY_PATH?")
rubiconharness = CDLL(rubiconharness_name)

faulthandler.enable()


class NSStringTests(unittest.TestCase):
    TEST_STRINGS = ('', 'abcdef', 'Uñîçö∂€')
    HAYSTACK = 'abcdabcdabcdef'
    NEEDLES = ['', 'a', 'bcd', 'def', HAYSTACK, 'nope', 'dcb']
    RANGES = [(None, None), (None, 6), (6, None), (4, 10)]

    def test_str_nsstring_conversion(self):
        """Python str and NSString can be converted to each other manually."""

        for pystr in type(self).TEST_STRINGS:
            with self.subTest(pystr=pystr):
                nsstr = ns_from_py(pystr)
                self.assertIsInstance(nsstr, NSString)
                self.assertEqual(str(nsstr), pystr)
                self.assertEqual(py_from_ns(nsstr), pystr)

    def test_nsstring_eq_nsstring(self):
        """Two NSStrings can be checked for equality."""

        first = ns_from_py('first')
        second = ns_from_py('second')

        self.assertEqual(first, first)
        self.assertNotEqual(first, second)
        self.assertEqual(second, second)

    def test_str_eq_nsstring(self):
        """A Python str and a NSString can be checked for equality."""

        py_first = 'first'
        py_second = 'second'
        ns_first = ns_from_py(py_first)
        ns_second = ns_from_py(py_second)

        self.assertEqual(py_first, ns_first)
        self.assertEqual(ns_first, py_first)
        self.assertNotEqual(py_first, ns_second)
        self.assertNotEqual(ns_first, py_second)
        self.assertEqual(py_second, ns_second)
        self.assertEqual(ns_second, py_second)

    def test_nsstring_in(self):
        """The in operator works on NSString."""

        py_haystack = type(self).HAYSTACK
        ns_haystack = ns_from_py(py_haystack)
        for py_needle in type(self).NEEDLES:
            with self.subTest(py_needle=py_needle):
                ns_needle = ns_from_py(py_needle)
                if py_needle in py_haystack:
                    self.assertIn(ns_needle, ns_haystack)
                else:
                    self.assertNotIn(ns_needle, ns_haystack)

    def test_nsstring_len(self):
        """len() works on NSString."""

        for pystr in type(self).TEST_STRINGS:
            with self.subTest(pystr=pystr):
                nsstr = ns_from_py(pystr)
                self.assertEqual(len(nsstr), len(pystr))

    def test_nsstring_getitem_index(self):
        """The individual elements of a NSString can be accessed."""

        for pystr in type(self).TEST_STRINGS:
            with self.subTest(pystr=pystr):
                nsstr = ns_from_py(pystr)
                for i, pychar in enumerate(pystr):
                    self.assertEqual(nsstr[i], pychar)

    def test_nsstring_getitem_slice(self):
        """A NSString can be sliced."""

        for pystr in type(self).TEST_STRINGS:
            for step in (None, 1, 2, -1, -2):
                with self.subTest(pystr=pystr, step=step):
                    nsstr = ns_from_py(pystr)
                    self.assertEqual(nsstr[::step], pystr[::step])
                    self.assertEqual(nsstr[:3:step], pystr[:3:step])
                    self.assertEqual(nsstr[2::step], pystr[2::step])
                    self.assertEqual(nsstr[1:4:step], pystr[1:4:step])

    def test_nsstring_iter(self):
        """A NSString can be iterated over."""

        for pystr in type(self).TEST_STRINGS:
            with self.subTest(pystr=pystr):
                nsstr = ns_from_py(pystr)
                for nschar, pychar in zip(nsstr, pystr):
                    self.assertEqual(nschar, pychar)

    def test_nsstring_find_rfind(self):
        """The find and rfind methods work on NSString."""

        py_haystack = type(self).HAYSTACK
        ns_haystack = ns_from_py(py_haystack)
        for py_needle in type(self).NEEDLES:
            for start, end in type(self).RANGES:
                with self.subTest(py_needle=py_needle, start=start, end=end):
                    ns_needle = ns_from_py(py_needle)
                    self.assertEqual(
                        ns_haystack.find(ns_needle, start, end),
                        py_haystack.find(py_needle, start, end),
                    )
                    self.assertEqual(
                        ns_haystack.rfind(ns_needle, start, end),
                        py_haystack.rfind(py_needle, start, end),
                    )

    def test_nsstring_index_rindex(self):
        """The index and rindex methods work on NSString."""

        py_haystack = type(self).HAYSTACK
        ns_haystack = ns_from_py(py_haystack)
        for py_needle in type(self).NEEDLES:
            for start, end in type(self).RANGES:
                with self.subTest(py_needle=py_needle, start=start, end=end):
                    ns_needle = ns_from_py(py_needle)

                    try:
                        index = py_haystack.index(py_needle, start, end)
                    except ValueError:
                        with self.assertRaises(ValueError):
                            ns_haystack.index(ns_needle, start, end)
                    else:
                        self.assertEqual(ns_haystack.index(ns_needle, start, end), index)

                    try:
                        rindex = py_haystack.rindex(py_needle, start, end)
                    except ValueError:
                        with self.assertRaises(ValueError):
                            ns_haystack.rindex(ns_needle, start, end)
                    else:
                        self.assertEqual(ns_haystack.rindex(ns_needle, start, end), rindex)

    def test_nsstring_add_radd(self):
        """The + operator works on NSString."""

        for py_left in type(self).TEST_STRINGS:
            for py_right in type(self).TEST_STRINGS:
                with self.subTest(py_left=py_left, py_right=py_right):
                    ns_left = ns_from_py(py_left)
                    ns_right = ns_from_py(py_right)
                    py_concat = py_left + py_right
                    ns_concat = ns_from_py(py_concat)
                    self.assertEqual(ns_left + ns_right, ns_concat)
                    self.assertEqual(py_left + ns_right, ns_concat)
                    self.assertEqual(ns_left + py_right, ns_concat)

    def test_nsstring_mul_rmul(self):
        """The * operator works on NSString."""

        for py_str in type(self).TEST_STRINGS:
            for n in (-5, 0, 1, 2, 5):
                with self.subTest(py_str=py_str, n=n):
                    ns_str = ns_from_py(py_str)
                    py_repeated = py_str * n
                    ns_repeated = ns_from_py(py_repeated)
                    self.assertEqual(ns_str * n, ns_repeated)
                    self.assertEqual(n * ns_str, ns_repeated)
