from __future__ import annotations

import os

import pytest

from rubicon.objc import ns_from_py, py_from_ns
from rubicon.objc.api import NSString

TEST_STRINGS = ("", "abcdef", "Uñîçö∂€")
HAYSTACK = "abcdabcdabcdef"
NEEDLES = ["", "a", "bcd", "def", HAYSTACK, "nope", "dcb"]
RANGES = [(None, None), (None, 6), (6, None), (4, 10)]


def assert_method(py_value, method, *args, **kwargs):
    ns_value = ns_from_py(py_value)

    try:
        py_method = getattr(py_value, method)
    except AttributeError:
        pytest.fail(f"Python type '{type(py_value)}' does not have method '{method}'")

    try:
        ns_method = getattr(ns_value, method)
    except AttributeError:
        pytest.fail(
            f"Rubicon analog for type '{type(py_value)}' does not have "
            f"method '{method}'"
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
        assert py_result == ns_result, (
            f"Different results for {method}: Python = {py_result}; ObjC = {ns_result}"
        )

    elif py_exception is not None:
        if ns_exception is not None:
            assert type(py_exception) is type(ns_exception), (
                f"Different exceptions for {method}: Python = {py_result}; "
                f"ObjC = {ns_result}"
            )

        else:
            pytest.fail(
                f"Python call for {method} raised {type(py_exception)}, "
                f"but ObjC did not"
            )
    else:
        pytest.fail(
            f"ObjC call for {method} raised {type(py_exception)}, but Python did not"
        )


@pytest.mark.parametrize("pystr", TEST_STRINGS)
def test_str_nsstring_conversion(pystr):
    """Python str and NSString can be converted to each other manually."""

    nsstr = ns_from_py(pystr)
    assert isinstance(nsstr, NSString)
    assert str(nsstr) == pystr
    assert py_from_ns(nsstr) == pystr


def test_nsstring_eq_nsstring():
    """Two NSStrings can be checked for equality."""

    first = ns_from_py("first")
    second = ns_from_py("second")

    assert first == first
    assert first != second
    assert second == second


def test_str_eq_nsstring():
    """A Python str and a NSString can be checked for equality."""

    py_first = "first"
    py_second = "second"
    ns_first = ns_from_py(py_first)
    ns_second = ns_from_py(py_second)

    assert py_first == ns_first
    assert ns_first == py_first
    assert py_first != ns_second
    assert ns_first != py_second
    assert py_second == ns_second
    assert ns_second == py_second


def test_nsstring_as_fspath():
    """An NSString can be interpreted as a 'path-like' object."""

    # os.path.dirname requires a 'path-like' object.
    assert os.path.dirname(ns_from_py("/path/base/leaf")) == "/path/base"


@pytest.mark.parametrize("py_left", TEST_STRINGS)
@pytest.mark.parametrize("py_right", TEST_STRINGS)
def test_nsstring_compare(py_left, py_right):
    """A NSString can be compared to other strings."""

    ns_left = ns_from_py(py_left)
    ns_right = ns_from_py(py_right)

    assert (ns_left < ns_right) == (py_left < py_right)
    assert (ns_left <= ns_right) == (py_left <= py_right)
    assert (ns_left >= ns_right) == (py_left >= py_right)
    assert (ns_left > ns_right) == (py_left > py_right)


@pytest.mark.parametrize("py_needle", NEEDLES)
def test_nsstring_in(py_needle):
    """The in operator works on NSString."""

    py_haystack = HAYSTACK
    ns_haystack = ns_from_py(py_haystack)
    ns_needle = ns_from_py(py_needle)
    if py_needle in py_haystack:
        assert ns_needle in ns_haystack
    else:
        assert ns_needle not in ns_haystack


@pytest.mark.parametrize("pystr", TEST_STRINGS)
def test_nsstring_len(pystr):
    """``len()`` works on NSString."""

    nsstr = ns_from_py(pystr)
    assert len(nsstr) == len(pystr)


@pytest.mark.parametrize("pystr", TEST_STRINGS)
def test_nsstring_getitem_index(pystr):
    """The individual elements of a NSString can be accessed."""

    nsstr = ns_from_py(pystr)
    for i, pychar in enumerate(pystr):
        assert nsstr[i] == pychar


@pytest.mark.parametrize("pystr", TEST_STRINGS)
@pytest.mark.parametrize("step", (None, 1, 2, -1, -2))
def test_nsstring_getitem_slice(pystr, step):
    """A NSString can be sliced."""

    nsstr = ns_from_py(pystr)
    assert nsstr[::step] == pystr[::step]
    assert nsstr[:3:step] == pystr[:3:step]
    assert nsstr[2::step] == pystr[2::step]
    assert nsstr[1:4:step] == pystr[1:4:step]


@pytest.mark.parametrize("pystr", TEST_STRINGS)
def test_nsstring_iter(pystr):
    """A NSString can be iterated over."""

    nsstr = ns_from_py(pystr)
    for nschar, pychar in zip(nsstr, pystr, strict=True):
        assert nschar == pychar


@pytest.mark.parametrize("py_needle", NEEDLES)
@pytest.mark.parametrize(("start", "end"), RANGES)
def test_nsstring_find_rfind(py_needle, start, end):
    """The find and rfind methods work on NSString."""

    py_haystack = HAYSTACK
    ns_haystack = ns_from_py(py_haystack)
    ns_needle = ns_from_py(py_needle)
    assert ns_haystack.find(ns_needle, start, end) == py_haystack.find(
        py_needle, start, end
    )
    assert ns_haystack.rfind(ns_needle, start, end) == py_haystack.rfind(
        py_needle, start, end
    )


@pytest.mark.parametrize("py_needle", NEEDLES)
@pytest.mark.parametrize(("start", "end"), RANGES)
def test_nsstring_index_rindex(py_needle, start, end):
    """The index and rindex methods work on NSString."""

    py_haystack = HAYSTACK
    ns_haystack = ns_from_py(py_haystack)
    ns_needle = ns_from_py(py_needle)

    try:
        index = py_haystack.index(py_needle, start, end)
    except ValueError:
        with pytest.raises(ValueError):
            ns_haystack.index(ns_needle, start, end)
    else:
        assert ns_haystack.index(ns_needle, start, end) == index

    try:
        rindex = py_haystack.rindex(py_needle, start, end)
    except ValueError:
        with pytest.raises(ValueError):
            ns_haystack.rindex(ns_needle, start, end)
    else:
        assert ns_haystack.rindex(ns_needle, start, end) == rindex


@pytest.mark.parametrize("py_left", TEST_STRINGS)
@pytest.mark.parametrize("py_right", TEST_STRINGS)
def test_nsstring_add_radd(py_left, py_right):
    """The + operator works on NSString."""

    ns_left = ns_from_py(py_left)
    ns_right = ns_from_py(py_right)
    py_concat = py_left + py_right
    ns_concat = ns_from_py(py_concat)
    assert (ns_left + ns_right) == ns_concat
    assert (py_left + ns_right) == ns_concat
    assert (ns_left + py_right) == ns_concat


@pytest.mark.parametrize("py_str", TEST_STRINGS)
@pytest.mark.parametrize("n", (-5, 0, 1, 2, 5))
def test_nsstring_mul_rmul(py_str, n):
    """The * operator works on NSString."""

    ns_str = ns_from_py(py_str)
    py_repeated = py_str * n
    ns_repeated = ns_from_py(py_repeated)
    assert (ns_str * n) == ns_repeated
    assert (n * ns_str) == ns_repeated


def test_nsstring_capitalize():
    """The capitalize method works on NSString."""
    assert_method("lower, UPPER & Mixed!", "capitalize")


def test_nsstring_casefold():
    """The casefold method works on NSString."""
    assert_method("lower, UPPER & Mixed!", "casefold")


def test_nsstring_center():
    """The center method works on NSString."""
    assert_method("hello", "center", 20)
    assert_method("hello", "center", 20, "*")


def test_nsstring_count():
    """The count method works on NSString."""
    assert_method("hello world", "count", "x")
    assert_method("hello world", "count", "l")


def test_nsstring_encode():
    """The encode method works on NSString."""
    assert_method("Uñîçö∂€ string", "encode", "utf-8")
    assert_method("Uñîçö∂€ string", "encode", "utf-16")
    assert_method("Uñîçö∂€ string", "encode", "ascii")
    assert_method("Uñîçö∂€ string", "encode", "ascii", "ignore")


def test_nsstring_endswith():
    """The endswith method works on NSString."""
    assert_method("world", "endswith")
    assert_method("cake", "endswith")


def test_nsstring_expandtabs():
    """The expandtabs method works on NSString."""
    assert_method("hello\tworld", "expandtabs")
    assert_method("hello\tworld", "expandtabs", 4)
    assert_method("hello\tworld", "expandtabs", 10)


def test_nsstring_format():
    """The format method works on NSString."""
    assert_method("hello {}", "format", "world")


def test_nsstring_format_map():
    """The format_map method works on NSString."""
    assert_method("hello {name}", "format_map", {"name": "world"})


def test_nsstring_isalnum():
    """The isalnum method works on NSString."""
    assert_method("abcd", "isalnum")
    assert_method("1234", "isalnum")
    assert_method("abcd1234", "isalnum")


def test_nsstring_isalpha():
    """The isalpha method works on NSString."""
    assert_method("abcd", "isalpha")
    assert_method("1234", "isalpha")
    assert_method("abcd1234", "isalpha")


def test_nsstring_isdecimal():
    """The isdecimal method works on NSString."""
    assert_method("abcd", "isdecimal")
    assert_method("1234", "isdecimal")
    assert_method("abcd1234", "isdecimal")


def test_nsstring_isdigit():
    """The isdigit method works on NSString."""
    assert_method("abcd", "isdigit")
    assert_method("1234", "isdigit")
    assert_method("abcd1234", "isdigit")


def test_nsstring_isidentifier():
    """The isidentifier method works on NSString."""
    assert_method("def", "isidentifier")
    assert_method("class", "isidentifier")
    assert_method("hello", "isidentifier")
    assert_method("boo!", "isidentifier")


def test_nsstring_islower():
    """The islower method works on NSString."""
    assert_method("abcd", "islower")
    assert_method("ABCD", "islower")
    assert_method("1234", "islower")
    assert_method("abcd1234", "islower")
    assert_method("ABCD1234", "islower")


def test_nsstring_isnumeric():
    """The isnumeric method works on NSString."""
    assert_method("abcd", "isnumeric")
    assert_method("1234", "isnumeric")
    assert_method("三", "isnumeric")
    assert_method("½", "isnumeric")


def test_nsstring_isprintable():
    """The isprintable method works on NSString."""
    assert_method("\x09", "isprintable")
    assert_method("Hello", "isprintable")


def test_nsstring_isspace():
    """The isspace method works on NSString."""
    assert_method(" ", "isspace")
    assert_method("   ", "isspace")
    assert_method("Hello world", "isspace")
    assert_method("Hello", "isspace")


def test_nsstring_istitle():
    """The istitle method works on NSString."""
    assert_method("Hello World", "istitle")
    assert_method("hello world", "istitle")
    assert_method("Hello world", "istitle")
    assert_method("Hello WORLD", "istitle")
    assert_method("HELLO WORLD", "istitle")


def test_nsstring_isupper():
    """The isupper method works on NSString."""
    assert_method("abcd", "isupper")
    assert_method("ABCD", "isupper")
    assert_method("1234", "isupper")
    assert_method("abcd1234", "isupper")
    assert_method("ABCD1234", "isupper")


def test_nsstring_join():
    """The join method works on NSString."""
    assert_method(":", "join", ["aa", "bb", "cc"])


def test_nsstring_ljust():
    """The ljust method works on NSString."""
    assert_method("123", "ljust", 5)
    assert_method("123", "ljust", 5, "*")


def test_nsstring_lower():
    """The lower method works on NSString."""
    assert_method("lower, UPPER & Mixed!", "lower")


def test_nsstring_lstrip():
    """The lstrip method works on NSString."""
    assert_method("   hello   ", "lstrip")
    assert_method("...hello...", "lstrip")
    assert_method("...hello...", "lstrip", ".")


def test_nsstring_maketrans():
    """The maketrans method works on NSString."""
    assert_method("hello", "maketrans", "lo", "g!")


def test_nsstring_partition():
    """The partition method works on NSString."""
    assert_method("hello new world", "partition", " ")
    assert_method("hello new world", "partition", "l")


def test_nsstring_replace():
    """The replace method works on NSString."""
    assert_method("hello new world", "replace", "new", "old")
    assert_method("hello new world", "replace", "l", "!")
    assert_method("hello new world", "replace", "l", "!", 2)


def test_nsstring_rjust():
    """The rjust method works on NSString."""
    assert_method("123", "rjust", 5)
    assert_method("123", "rjust", 5, "*")


def test_nsstring_rpartition():
    """The rpartition method works on NSString."""
    assert_method("hello new world", "rpartition", " ")
    assert_method("hello new world", "rpartition", "l")


def test_nsstring_rsplit():
    """The rsplit method works on NSString."""
    assert_method("hello new world", "rsplit")
    assert_method("hello new world", "rsplit", " ", 1)
    assert_method("hello new world", "rsplit", "l")
    assert_method("hello new world", "rsplit", "l", 2)


def test_nsstring_rstrip():
    """The rstrip method works on NSString."""
    assert_method("   hello   ", "rstrip")
    assert_method("...hello...", "rstrip")
    assert_method("...hello...", "rstrip", ".")


def test_nsstring_split():
    """The split method works on NSString."""
    assert_method("hello new world", "split")
    assert_method("hello new world", "split", " ", 1)
    assert_method("hello new world", "split", "l")
    assert_method("hello new world", "split", "l", 2)


def test_nsstring_splitlines():
    """The splitlines method works on NSString."""
    assert_method("Hello\nnew\nworld\n", "splitlines")


def test_nsstring_strip():
    """The strip method works on NSString."""
    assert_method("   hello   ", "strip")
    assert_method("...hello...", "strip")
    assert_method("...hello...", "strip", ".")


def test_nsstring_swapcase():
    """The swapcase method works on NSString."""
    assert_method("lower, UPPER & Mixed!", "swapcase")


def test_nsstring_title():
    """The title method works on NSString."""
    assert_method("lower, UPPER & Mixed!", "title")


def test_nsstring_translate():
    """The translate method works on NSString."""
    assert_method("hello", "translate", {108: "g", 111: "!!"})


def test_nsstring_upper():
    """The upper method works on NSString."""
    assert_method("lower, UPPER & Mixed!", "upper")


def test_nsstring_zfill():
    """The zfill method works on NSString."""
    assert_method("123", "zfill", 5)
