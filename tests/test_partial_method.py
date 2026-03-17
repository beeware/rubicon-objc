from __future__ import annotations

from ctypes import (
    byref,
    create_string_buffer,
)

import pytest

from rubicon.objc import (
    NSRange,
    NSUInteger,
    ObjCClass,
    at,
)


def test_no_args():
    Example = ObjCClass("Example")
    assert Example.overloaded() == 0


def test_one_arg():
    Example = ObjCClass("Example")
    assert Example.overloaded(42) == 42


def test_two_args():
    Example = ObjCClass("Example")
    assert Example.overloaded(12, extraArg=34) == (12 + 34)


def test_lots_of_args():
    pystring = "Uñîçö∂€"
    pybytestring = pystring.encode("utf-8")
    nsstring = at(pystring)
    buf = create_string_buffer(len(pybytestring) + 1)
    usedLength = NSUInteger()
    remaining = NSRange(0, 0)
    nsstring.getBytes(
        buf,
        maxLength=32,
        usedLength=byref(usedLength),
        encoding=4,  # NSUTF8StringEncoding
        options=0,
        range=NSRange(0, 7),
        remainingRange=byref(remaining),
    )
    assert buf.value.decode("utf-8") == pystring


def test_arg_order():
    Example = ObjCClass("Example")

    assert Example.overloaded(3, extraArg1=5, extraArg2=7) == (3 + 5 + 7)
    assert Example.overloaded(3, extraArg2=5, extraArg1=7) == (3 * 5 * 7)

    # Although the arguments are a unique match, they're not in the right order.
    with pytest.raises(ValueError):
        Example.overloaded(0, orderedArg2=0, orderedArg1=0)


def test_duplicate_arg_names():
    Example = ObjCClass("Example")
    assert Example.overloaded(24, duplicateArg__a=16, duplicateArg__b=6) == (
        24 + 2 * 16 + 3 * 6
    )


def test_exception():
    Example = ObjCClass("Example")
    with pytest.raises(
        ValueError,
        match=(
            r"Invalid selector overloaded:invalidArgument:. Available selectors are: "
            r"overloaded, overloaded:, overloaded:extraArg:, "
            r"overloaded:extraArg1:extraArg2:, overloaded:extraArg2:extraArg1:, "
            r"overloaded:orderedArg1:orderedArg2:, "
            r"overloaded:duplicateArg:duplicateArg:"
        ),
    ):
        Example.overloaded(0, invalidArgument=0)


def test_with_override():
    """If one method in a partial is overridden, that doesn't impact lookup of other
    partial targets."""
    SpecificExample = ObjCClass("SpecificExample")

    obj = SpecificExample.alloc().init()

    # The subclass implementation is invoked, not the base
    obj.method(2, withArg=3)
    assert obj.baseIntField == 5

    # The base class implementation can still be found an invoked.
    obj.method(2)
    assert obj.baseIntField == 2
