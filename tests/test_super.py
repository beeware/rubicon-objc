from __future__ import annotations

from ctypes import c_int

import pytest

from rubicon.objc import (
    SEL,
    ObjCClass,
    send_super,
)


def test_send():
    """An instance method of the super class can be invoked."""
    SpecificExample = ObjCClass("SpecificExample")

    obj = SpecificExample.alloc().init()

    send_super(
        SpecificExample,
        obj,
        "method:withArg:",
        2,
        5,
        restype=None,
        argtypes=[c_int, c_int],
    )

    assert obj.baseIntField == 10


def test_send_sel():
    """send_super accepts a SEL object as the selector parameter."""
    SpecificExample = ObjCClass("SpecificExample")

    obj = SpecificExample.alloc().init()

    send_super(
        SpecificExample,
        obj,
        SEL("method:withArg:"),
        2,
        5,
        restype=None,
        argtypes=[c_int, c_int],
    )

    assert obj.baseIntField == 10


def test_send_incorrect_argument_count():
    """Attempting to call a method with send_super with an incorrect number of arguments
    throws an exception."""
    SpecificExample = ObjCClass("SpecificExample")

    obj = SpecificExample.alloc().init()

    with pytest.raises(TypeError):
        send_super(
            SpecificExample,
            obj,
            "method:withArg:",
            2,
            restype=None,
            argtypes=[],
        )

    with pytest.raises(TypeError):
        send_super(
            SpecificExample,
            obj,
            "method:withArg:",
            restype=None,
            argtypes=[c_int, c_int],
        )

    with pytest.raises(TypeError):
        send_super(
            SpecificExample,
            obj,
            "method:withArg:",
            2,
            5,
            6,
            "extra argument",
            restype=None,
            argtypes=[c_int, c_int],
        )


def test_send_varargs():
    """A variadic method can be called using send_super."""
    SpecificExample = ObjCClass("SpecificExample")

    obj = SpecificExample.alloc().init()
    send_super(
        SpecificExample,
        obj,
        "methodWithArgs:",
        2,
        varargs=[5, 6],
        argtypes=[c_int],
        restype=None,
    )

    assert obj.accessBaseIntField() == 11
