import faulthandler
import os
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

    def test_nsstring_as_fspath(self):
        """An NSString can be interpreted as a 'path-like' object"""

        # os.path.dirname requires a 'path-like' object.
        self.assertEqual(
            os.path.dirname(ns_from_py('/path/base/leaf')),
            '/path/base'
        )

    def test_nsstring_compare(self):
        """A NSString can be compared to other strings."""

        for py_left in type(self).TEST_STRINGS:
            for py_right in type(self).TEST_STRINGS:
                with self.subTest(py_left=py_left, py_right=py_right):
                    ns_left = ns_from_py(py_left)
                    ns_right = ns_from_py(py_right)

                    self.assertEqual(ns_left < ns_right, py_left < py_right)
                    self.assertEqual(ns_left <= ns_right, py_left <= py_right)
                    self.assertEqual(ns_left >= ns_right, py_left >= py_right)
                    self.assertEqual(ns_left > ns_right, py_left > py_right)

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

    def test_nsstring_capitalize(self):
        ns_str = ns_from_py('lower, UPPER & Mixed!')
        self.assertEqual(ns_str.capitalize(), 'Lower, upper & mixed!')

    def test_nsstring_casefold(self):
        ns_str = ns_from_py('lower, UPPER & Mixed!')
        self.assertEqual(ns_str.casefold(), 'lower, upper & mixed!')

    def test_nsstring_center(self):
        ns_str = ns_from_py('hello')
        self.assertEqual(ns_str.center(20), '       hello        ')
        self.assertEqual(ns_str.center(20, '*'), '*******hello********')

    def test_nsstring_count(self):
        ns_str = ns_from_py('hello world')
        self.assertEqual(ns_str.count('x'), 0)
        self.assertEqual(ns_str.count('l'), 3)
        self.assertEqual(ns_str.count('l', start=5), 1)
        self.assertEqual(ns_str.count('l', end=8), 2)
        self.assertEqual(ns_str.count('l', start=4, end=8), 0)

    def test_nsstring_encode(self):
        ns_str = ns_from_py('Uñîçö∂€ string')
        self.assertEqual(
            ns_str.encode('utf-8'),
            b'U\xc3\xb1\xc3\xae\xc3\xa7\xc3\xb6\xe2\x88\x82\xe2\x82\xac string'
        )
        self.assertEqual(
            ns_str.encode('utf-16'),
            b'\xff\xfeU\x00\xf1\x00\xee\x00\xe7\x00\xf6\x00\x02"\xac  \x00s\x00t\x00r\x00i\x00n\x00g\x00'
        )

        with self.assertRaises(UnicodeEncodeError):
            ns_str.encode('ascii')
        self.assertEqual(ns_str.encode('ascii', 'ignore'), b'U string')

    def test_nsstring_endswith(self):
        ns_str = ns_from_py('Hello world')
        self.assertTrue(ns_str.endswith('world'))
        self.assertFalse(ns_str.endswith('cake'))

    def test_nsstring_expandtabs(self):
        ns_str = ns_from_py('hello\tworld')
        self.assertEqual(ns_str.expandtabs(), 'hello   world')
        self.assertEqual(ns_str.expandtabs(4), 'hello   world')
        self.assertEqual(ns_str.expandtabs(10), 'hello     world')

    def test_nsstring_format(self):
        ns_str = ns_from_py('hello {}')
        self.assertEqual(ns_str.format('world'), 'hello world')

    def test_nsstring_format_map(self):
        ns_str = ns_from_py('hello {name}')
        self.assertEqual(ns_str.format_map({'name': 'world'}), 'hello world')

    def test_nsstring_isalnum(self):
        self.assertTrue(ns_from_py('abcd').isalnum())
        self.assertTrue(ns_from_py('1234').isalnum())
        self.assertTrue(ns_from_py('abcd1234').isalnum())

    def test_nsstring_isalpha(self):
        self.assertTrue(ns_from_py('abcd').isalpha())
        self.assertFalse(ns_from_py('1234').isalpha())
        self.assertFalse(ns_from_py('abcd1234').isalpha())

    def test_nsstring_isdecimal(self):
        self.assertFalse(ns_from_py('abcd').isdecimal())
        self.assertTrue(ns_from_py('1234').isdecimal())
        self.assertFalse(ns_from_py('abcd1234').isdecimal())

    def test_nsstring_isdigit(self):
        self.assertFalse(ns_from_py('abcd').isdigit())
        self.assertTrue(ns_from_py('1234').isdigit())
        self.assertFalse(ns_from_py('abcd1234').isdigit())

    def test_nsstring_isidentifier(self):
        self.assertTrue(ns_from_py('def').isidentifier())
        self.assertTrue(ns_from_py('class').isidentifier())
        self.assertTrue(ns_from_py('hello').isidentifier())
        self.assertFalse(ns_from_py('boo!').isidentifier())

    def test_nsstring_islower(self):
        self.assertTrue(ns_from_py('abcd').islower())
        self.assertFalse(ns_from_py('ABCD').islower())
        self.assertFalse(ns_from_py('1234').islower())
        self.assertTrue(ns_from_py('abcd1234').islower())
        self.assertFalse(ns_from_py('ABCD1234').islower())

    def test_nsstring_isnumeric(self):
        self.assertFalse(ns_from_py('abcd').isdigit())
        self.assertTrue(ns_from_py('1234').isdigit())
        self.assertFalse(ns_from_py('abcd1234').isdigit())

    def test_nsstring_isprintable(self):
        self.assertFalse(ns_from_py('\x09').isprintable())
        self.assertTrue(ns_from_py('Hello').isprintable())

    def test_nsstring_isspace(self):
        self.assertTrue(ns_from_py(' ').isspace())
        self.assertTrue(ns_from_py('   ').isspace())
        self.assertFalse(ns_from_py('Hello world').isspace())
        self.assertFalse(ns_from_py('Hello').isspace())

    def test_nsstring_istitle(self):
        self.assertTrue(ns_from_py('Hello World').istitle())
        self.assertFalse(ns_from_py('hello world').istitle())
        self.assertFalse(ns_from_py('Hello world').istitle())
        self.assertFalse(ns_from_py('Hello WORLD').istitle())
        self.assertFalse(ns_from_py('HELLO WORLD').istitle())

    def test_nsstring_isupper(self):
        self.assertFalse(ns_from_py('abcd').isupper())
        self.assertTrue(ns_from_py('ABCD').isupper())
        self.assertFalse(ns_from_py('1234').isupper())
        self.assertFalse(ns_from_py('abcd1234').isupper())
        self.assertTrue(ns_from_py('ABCD1234').isupper())

    def test_nsstring_join(self):
        ns_str = ns_from_py(':')
        self.assertEqual(ns_str.join(['aa', 'bb', 'cc']), 'aa:bb:cc')

    def test_nsstring_ljust(self):
        ns_str = ns_from_py('123')
        self.assertEqual(ns_str.ljust(5), '123  ')
        self.assertEqual(ns_str.ljust(5, '*'), '123**')

    def test_nsstring_lower(self):
        ns_str = ns_from_py('lower, UPPER & Mixed!')
        self.assertEqual(ns_str.lower(), 'lower, upper & mixed!')

    def test_nsstring_lstrip(self):
        ns_str = ns_from_py('   hello   ')
        self.assertEqual(ns_str.lstrip(), 'hello   ')

        ns_str = ns_from_py('...hello...')
        self.assertEqual(ns_str.lstrip('.'), 'hello...')

    def test_nsstring_maketrans(self):
        ns_str = ns_from_py('hello')
        self.assertEqual(ns_str.maketrans('lo', 'g!'), {108: 103, 111: 33})

    def test_nsstring_partition(self):
        ns_str = ns_from_py('hello new world')
        self.assertEqual(ns_str.partition(' '), ('hello', ' ', 'new world'))
        self.assertEqual(ns_str.partition('l'), ('he', 'l', 'lo new world'))

    def test_nsstring_replace(self):
        ns_str = ns_from_py('hello new world')
        self.assertEqual(ns_str.replace('new', 'old'), 'hello old world')
        self.assertEqual(ns_str.replace('l', '!'), 'he!!o new wor!d')
        self.assertEqual(ns_str.replace('l', '!', 2), 'he!!o new world')

    def test_nsstring_rjust(self):
        ns_str = ns_from_py('123')
        self.assertEqual(ns_str.rjust(5), '  123')
        self.assertEqual(ns_str.rjust(5, '*'), '**123')

    def test_nsstring_rpartition(self):
        ns_str = ns_from_py('hello new world')
        self.assertEqual(ns_str.rpartition(' '), ('hello new', ' ', 'world'))
        self.assertEqual(ns_str.rpartition('l'), ('hello new wor', 'l', 'd'))

    def test_nsstring_rsplit(self):
        ns_str = ns_from_py('hello new world')
        self.assertEqual(ns_str.rsplit(), ['hello', 'new', 'world'])
        self.assertEqual(ns_str.rsplit(' ', 1), ['hello new', 'world'])
        self.assertEqual(ns_str.rsplit('l'), ['he', '', 'o new wor', 'd'])
        self.assertEqual(ns_str.rsplit('l', 2), ['hel', 'o new wor', 'd'])

    def test_nsstring_rstrip(self):
        ns_str = ns_from_py('   hello   ')
        self.assertEqual(ns_str.rstrip(), '   hello')

        ns_str = ns_from_py('...hello...')
        self.assertEqual(ns_str.rstrip('.'), '...hello')

    def test_nsstring_split(self):
        ns_str = ns_from_py('hello new world')
        self.assertEqual(ns_str.split(), ['hello', 'new', 'world'])
        self.assertEqual(ns_str.split(' ', 1), ['hello', 'new world'])
        self.assertEqual(ns_str.split('l'), ['he', '', 'o new wor', 'd'])
        self.assertEqual(ns_str.split('l', 2), ['he', '', 'o new world'])

    def test_nsstring_splitlines(self):
        ns_str = ns_from_py('Hello\nnew\nworld\n')
        self.assertEqual(ns_str.splitlines(), ['Hello', 'new', 'world'])

    def test_nsstring_strip(self):
        ns_str = ns_from_py('   hello   ')
        self.assertEqual(ns_str.strip(), 'hello')

        ns_str = ns_from_py('...hello...')
        self.assertEqual(ns_str.strip('.'), 'hello')

    def test_nsstring_swapcase(self):
        ns_str = ns_from_py('lower, UPPER & Mixed!')
        self.assertEqual(ns_str.swapcase(), 'LOWER, upper & mIXED!')

    def test_nsstring_title(self):
        ns_str = ns_from_py('lower, UPPER & Mixed!')
        self.assertEqual(ns_str.title(), 'Lower, Upper & Mixed!')

    def test_nsstring_translate(self):
        ns_str = ns_from_py('hello')
        self.assertEqual(ns_str.translate({108: 'g', 111: '!!'}), 'hegg!!')

    def test_nsstring_upper(self):
        ns_str = ns_from_py('lower, UPPER & Mixed!')
        self.assertEqual(ns_str.upper(), 'LOWER, UPPER & MIXED!')

    def test_nsstring_zfill(self):
        ns_str = ns_from_py('123')
        self.assertEqual(ns_str.zfill(5), '00123')
