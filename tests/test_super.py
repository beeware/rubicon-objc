from __future__ import annotations

from ctypes import c_int

import pytest

from rubicon.objc import (
    SEL,
    ObjCClass,
    send_super,
)
from rubicon.objc.runtime import objc_id, Class
from unittest.mock import MagicMock, patch
from ctypes import c_void_p


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


def test_send_super_invalid_cls():
    """Test send_super invalid cls (line 1039)"""
    with pytest.raises(TypeError, match="Missing or invalid cls argument"):
        send_super(123, MagicMock(spec=objc_id), "init")


def test_send_super_dealloc_warning():
    """Test send_super dealloc warning (line 1048-1054)"""
    cls = MagicMock(spec=Class)
    receiver = MagicMock(spec=objc_id)
    with pytest.warns(
        UserWarning, match="You should not call the superclass dealloc manually"
    ):
        result = send_super(cls, receiver, "dealloc")
        assert result is None


def test_send_super_root_class():
    """Test send_super root class (line 1073-1074)"""
    # We need to mock libobjc.class_getSuperclass to return NULL
    with patch("rubicon.objc.runtime.libobjc") as mock_libobjc:
        mock_libobjc.class_getSuperclass.return_value = c_void_p(None)
        mock_libobjc.class_getName.return_value = b"NSObject"

        cls = MagicMock(spec=Class)
        receiver = MagicMock(spec=objc_id)
        with pytest.raises(ValueError, match="The specified class 'NSObject' is a root class"):
            send_super(cls, receiver, "init")
