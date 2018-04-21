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
