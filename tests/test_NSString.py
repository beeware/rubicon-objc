from __future__ import annotations

import os
import unittest

from rubicon.objc import ns_from_py, py_from_ns
from rubicon.objc.api import NSString


class NSStringTests(unittest.TestCase):
    TEST_STRINGS = ("", "abcdef", "Uñîçö∂€")
    HAYSTACK = "abcdabcdabcdef"
    NEEDLES = ["", "a", "bcd", "def", HAYSTACK, "nope", "dcb"]
    RANGES = [(None, None), (None, 6), (6, None), (4, 10)]

    def assert_method(self, py_value, method, *args, **kwargs):
        ns_value = ns_from_py(py_value)

        try:
            py_method = getattr(py_value, method)
        except AttributeError:
            self.fail(f"Python type '{type(py_value)}' does not have method '{method}'")

        try:
            ns_method = getattr(ns_value, method)
        except AttributeError:
            self.fail(
                f"Rubicon analog for type '{type(py_value)}' does not have method '{method}'"
            )

        try:
            py_result = py_method(*args, **kwargs)
            py_exception = None
        except Exception as e:
            py_exception = e
            py_result = None

        try:
            ns_result = ns_method(*args, **kwargs)
            ns_exception = None
        except Exception as e:
            ns_exception = e
            ns_result = None

        if py_exception is None and ns_exception is None:
            self.assertEqual(
                py_result,
                ns_result,
                f"Different results for {method}: Python = {py_result}; ObjC = {ns_result}",
            )
        elif py_exception is not None:
            if ns_exception is not None:
                self.assertEqual(
                    type(py_exception),
                    type(ns_exception),
                    f"Different exceptions for {method}: Python = {py_result}; ObjC = {ns_result}",
                )
            else:
                self.fail(
                    f"Python call for {method} raised {type(py_exception)}, but ObjC did not"
                )
        else:
            self.fail(
                f"ObjC call for {method} raised {type(py_exception)}, but Python did not"
            )

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

        first = ns_from_py("first")
        second = ns_from_py("second")

        self.assertEqual(first, first)
        self.assertNotEqual(first, second)
        self.assertEqual(second, second)

    def test_str_eq_nsstring(self):
        """A Python str and a NSString can be checked for equality."""

        py_first = "first"
        py_second = "second"
        ns_first = ns_from_py(py_first)
        ns_second = ns_from_py(py_second)

        self.assertEqual(py_first, ns_first)
        self.assertEqual(ns_first, py_first)
        self.assertNotEqual(py_first, ns_second)
        self.assertNotEqual(ns_first, py_second)
        self.assertEqual(py_second, ns_second)
        self.assertEqual(ns_second, py_second)

    def test_nsstring_as_fspath(self):
        """An NSString can be interpreted as a 'path-like' object."""

        # os.path.dirname requires a 'path-like' object.
        self.assertEqual(os.path.dirname(ns_from_py("/path/base/leaf")), "/path/base")

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
                        self.assertEqual(
                            ns_haystack.index(ns_needle, start, end), index
                        )

                    try:
                        rindex = py_haystack.rindex(py_needle, start, end)
                    except ValueError:
                        with self.assertRaises(ValueError):
                            ns_haystack.rindex(ns_needle, start, end)
                    else:
                        self.assertEqual(
                            ns_haystack.rindex(ns_needle, start, end), rindex
                        )

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
        self.assert_method("lower, UPPER & Mixed!", "capitalize")

    def test_nsstring_casefold(self):
        self.assert_method("lower, UPPER & Mixed!", "casefold")

    def test_nsstring_center(self):
        self.assert_method("hello", "center", 20)
        self.assert_method("hello", "center", 20, "*")

    def test_nsstring_count(self):
        self.assert_method("hello world", "count", "x")
        self.assert_method("hello world", "count", "l")

    def test_nsstring_encode(self):
        self.assert_method("Uñîçö∂€ string", "encode", "utf-8")
        self.assert_method("Uñîçö∂€ string", "encode", "utf-16")
        self.assert_method("Uñîçö∂€ string", "encode", "ascii")
        self.assert_method("Uñîçö∂€ string", "encode", "ascii", "ignore")

    def test_nsstring_endswith(self):
        self.assert_method("world", "endswith")
        self.assert_method("cake", "endswith")

    def test_nsstring_expandtabs(self):
        self.assert_method(
            "hello\tworld",
            "expandtabs",
        )
        self.assert_method("hello\tworld", "expandtabs", 4)
        self.assert_method("hello\tworld", "expandtabs", 10)

    def test_nsstring_format(self):
        self.assert_method("hello {}", "format", "world")

    def test_nsstring_format_map(self):
        self.assert_method("hello {name}", "format_map", {"name": "world"})

    def test_nsstring_isalnum(self):
        self.assert_method("abcd", "isalnum")
        self.assert_method("1234", "isalnum")
        self.assert_method("abcd1234", "isalnum")

    def test_nsstring_isalpha(self):
        self.assert_method("abcd", "isalpha")
        self.assert_method("1234", "isalpha")
        self.assert_method("abcd1234", "isalpha")

    def test_nsstring_isdecimal(self):
        self.assert_method("abcd", "isdecimal")
        self.assert_method("1234", "isdecimal")
        self.assert_method("abcd1234", "isdecimal")

    def test_nsstring_isdigit(self):
        self.assert_method("abcd", "isdigit")
        self.assert_method("1234", "isdigit")
        self.assert_method("abcd1234", "isdigit")

    def test_nsstring_isidentifier(self):
        self.assert_method("def", "isidentifier")
        self.assert_method("class", "isidentifier")
        self.assert_method("hello", "isidentifier")
        self.assert_method("boo!", "isidentifier")

    def test_nsstring_islower(self):
        self.assert_method("abcd", "islower")
        self.assert_method("ABCD", "islower")
        self.assert_method("1234", "islower")
        self.assert_method("abcd1234", "islower")
        self.assert_method("ABCD1234", "islower")

    def test_nsstring_isnumeric(self):
        self.assert_method("abcd", "isdigit")
        self.assert_method("1234", "isdigit")
        self.assert_method("abcd1234", "isdigit")

    def test_nsstring_isprintable(self):
        self.assert_method("\x09", "isprintable")
        self.assert_method("Hello", "isprintable")

    def test_nsstring_isspace(self):
        self.assert_method(" ", "isspace")
        self.assert_method("   ", "isspace")
        self.assert_method("Hello world", "isspace")
        self.assert_method("Hello", "isspace")

    def test_nsstring_istitle(self):
        self.assert_method("Hello World", "istitle")
        self.assert_method("hello world", "istitle")
        self.assert_method("Hello world", "istitle")
        self.assert_method("Hello WORLD", "istitle")
        self.assert_method("HELLO WORLD", "istitle")

    def test_nsstring_isupper(self):
        self.assert_method("abcd", "isupper")
        self.assert_method("ABCD", "isupper")
        self.assert_method("1234", "isupper")
        self.assert_method("abcd1234", "isupper")
        self.assert_method("ABCD1234", "isupper")

    def test_nsstring_join(self):
        self.assert_method(":", "join", ["aa", "bb", "cc"])

    def test_nsstring_ljust(self):
        self.assert_method("123", "ljust", 5)
        self.assert_method("123", "ljust", 5, "*")

    def test_nsstring_lower(self):
        self.assert_method(
            "lower, UPPER & Mixed!",
            "lower",
        )

    def test_nsstring_lstrip(self):
        self.assert_method(
            "   hello   ",
            "lstrip",
        )
        self.assert_method(
            "...hello...",
            "lstrip",
        )
        self.assert_method("...hello...", "lstrip", ".")

    def test_nsstring_maketrans(self):
        self.assert_method("hello", "maketrans", "lo", "g!")

    def test_nsstring_partition(self):
        self.assert_method("hello new world", "partition", " ")
        self.assert_method("hello new world", "partition", "l")

    def test_nsstring_replace(self):
        self.assert_method("hello new world", "replace", "new", "old")
        self.assert_method("hello new world", "replace", "l", "!")
        self.assert_method("hello new world", "replace", "l", "!", 2)

    def test_nsstring_rjust(self):
        self.assert_method("123", "rjust", 5)
        self.assert_method("123", "rjust", 5, "*")

    def test_nsstring_rpartition(self):
        self.assert_method("hello new world", "rpartition", " ")
        self.assert_method("hello new world", "rpartition", "l")

    def test_nsstring_rsplit(self):
        self.assert_method("hello new world", "rsplit")
        self.assert_method("hello new world", "rsplit", " ", 1)
        self.assert_method("hello new world", "rsplit", "l")
        self.assert_method("hello new world", "rsplit", "l", 2)

    def test_nsstring_rstrip(self):
        self.assert_method("   hello   ", "rstrip")
        self.assert_method("...hello...", "rstrip")
        self.assert_method("...hello...", "rstrip", ".")

    def test_nsstring_split(self):
        self.assert_method("hello new world", "split")
        self.assert_method("hello new world", "split", " ", 1)
        self.assert_method("hello new world", "split", "l")
        self.assert_method("hello new world", "split", "l", 2)

    def test_nsstring_splitlines(self):
        self.assert_method("Hello\nnew\nworld\n", "splitlines")

    def test_nsstring_strip(self):
        self.assert_method("   hello   ", "strip")
        self.assert_method("...hello...", "strip")
        self.assert_method("...hello...", "strip", ".")

    def test_nsstring_swapcase(self):
        self.assert_method("lower, UPPER & Mixed!", "swapcase")

    def test_nsstring_title(self):
        self.assert_method("lower, UPPER & Mixed!", "title")

    def test_nsstring_translate(self):
        self.assert_method("hello", "translate", {108: "g", 111: "!!"})

    def test_nsstring_upper(self):
        self.assert_method("lower, UPPER & Mixed!", "upper")

    def test_nsstring_zfill(self):
        self.assert_method("123", "zfill", 5)
