from __future__ import annotations

import math
from ctypes import (
    c_double,
    c_float,
    c_int,
)

import pytest

from rubicon.objc import (
    SEL,
    ObjCClass,
    ObjCInstance,
    at,
    send_message,
)
from rubicon.objc.runtime import objc_id

from .conftest import (
    NSString,
    struct_int_sized,
    struct_large,
    struct_oddly_sized,
)


def test_sel_by_name():
    assert SEL(b"foobar").name == b"foobar"


def test_sel_null():
    with pytest.raises(ValueError):
        _ = SEL(None).name


def test_sel_repr():
    """Test SEL.__repr__ (line 275)"""
    # Null selector
    sel_null = SEL(None)
    assert repr(sel_null) == "rubicon.objc.runtime.SEL(None)"

    # Registered selector
    sel = SEL(b"init")
    assert repr(sel) == "rubicon.objc.runtime.SEL(b'init')"


def test_method_incorrect_argument_count_send():
    """Attempting to call a method with send_message with an incorrect number of
    arguments throws an exception."""

    Example = ObjCClass("Example")
    obj = Example.alloc().init()

    with pytest.raises(TypeError):
        send_message(
            obj,
            "accessIntField",
            "extra argument 1",
            restype=c_int,
            argtypes=[],
        )

    with pytest.raises(TypeError):
        send_message(
            obj,
            "mutateIntFieldWithValue:",
            restype=None,
            argtypes=[c_int],
        )

    with pytest.raises(TypeError):
        send_message(
            obj,
            "mutateIntFieldWithValue:",
            123,
            "extra_argument",
            restype=None,
            argtypes=[c_int],
        )


def test_method_varargs_send():
    """A variadic method can be called using send_message."""
    formatted = send_message(
        NSString,
        "stringWithFormat:",
        at("This is a %@ with %@"),
        varargs=[at("string"), at("placeholders")],
        restype=objc_id,
        argtypes=[objc_id],
    )
    assert str(ObjCInstance(formatted)) == "This is a string with placeholders"


def test_method_send():
    """An instance method can be invoked with send_message."""
    Example = ObjCClass("Example")

    obj = Example.alloc().init()

    assert (
        send_message(
            obj,
            "accessBaseIntField",
            restype=c_int,
            argtypes=[],
        )
        == 22
    )
    assert (
        send_message(
            obj,
            "accessIntField",
            restype=c_int,
            argtypes=[],
        )
        == 33
    )

    send_message(
        obj,
        "mutateBaseIntFieldWithValue:",
        8888,
        restype=None,
        argtypes=[c_int],
    )
    send_message(
        obj,
        "mutateIntFieldWithValue:",
        9999,
        restype=None,
        argtypes=[c_int],
    )

    assert (
        send_message(
            obj,
            "accessBaseIntField",
            restype=c_int,
            argtypes=[],
        )
        == 8888
    )
    assert (
        send_message(
            obj,
            "accessIntField",
            restype=c_int,
            argtypes=[],
        )
        == 9999
    )


def test_send_sel():
    """send_message accepts a SEL object as the selector parameter."""
    Example = ObjCClass("Example")

    obj = Example.alloc().init()

    assert (
        send_message(
            obj,
            SEL("accessIntField"),
            restype=c_int,
            argtypes=[],
        )
        == 33
    )


def test_float_method_send():
    """A method with a float argument can be handled by send_message."""
    Example = ObjCClass("Example")
    example = Example.alloc().init()
    assert send_message(
        example,
        "areaOfSquare:",
        1.5,
        restype=c_float,
        argtypes=[c_float],
    ) == pytest.approx(2.25)


def test_double_method_send():
    """A method with a double argument can be handled by send_message."""
    Example = ObjCClass("Example")
    example = Example.alloc().init()
    assert send_message(
        example,
        "areaOfCircle:",
        1.5,
        restype=c_double,
        argtypes=[c_double],
    ) == pytest.approx(1.5 * math.pi)


def test_struct_return_send():
    """Methods returning structs of different sizes by value can be handled when using
    send_message."""
    Example = ObjCClass("Example")
    example = Example.alloc().init()

    assert (
        send_message(
            example,
            "intSizedStruct",
            restype=struct_int_sized,
            argtypes=[],
        ).x
        == b"abc"
    )
    assert (
        send_message(
            example,
            "oddlySizedStruct",
            restype=struct_oddly_sized,
            argtypes=[],
        ).x
        == b"abcd"
    )
    assert (
        send_message(
            example,
            "largeStruct",
            restype=struct_large,
            argtypes=[],
        ).x
        == b"abcdefghijklmnop"
    )


def test_send_message_invalid_receiver():
    """Test send_message invalid receiver (line 917)"""
    with pytest.raises(TypeError, match="Receiver must be an ObjCInstance or objc_id"):
        send_message(123, "init", restype=objc_id)
