from __future__ import annotations

import pytest

from rubicon.objc import ObjCClass


def test_field():
    """A field on an instance can be accessed and mutated."""
    Example = ObjCClass("Example")

    obj = Example.alloc().init()

    assert obj.baseIntField == 22
    assert obj.intField == 33

    obj.baseIntField = 8888
    obj.intField = 9999

    assert obj.baseIntField == 8888
    assert obj.intField == 9999


def test_static():
    """A static field on a class can be accessed and mutated."""
    Example = ObjCClass("Example")

    Example.mutateStaticBaseIntFieldWithValue_(1)
    Example.mutateStaticIntFieldWithValue_(11)

    assert Example.staticBaseIntField == 1
    assert Example.staticIntField == 11

    Example.staticBaseIntField = 1188
    Example.staticIntField = 1199

    assert Example.staticBaseIntField == 1188
    assert Example.staticIntField == 1199


def test_non_existent():
    """An attribute error is raised if you invoke a non-existent field."""
    Example = ObjCClass("Example")

    obj1 = Example.alloc().init()

    # Non-existent fields raise an error.
    with pytest.raises(AttributeError):
        _ = obj1.field_doesnt_exist

    # Cache warming doesn't affect anything.
    with pytest.raises(AttributeError):
        _ = obj1.field_doesnt_exist


def test_non_existent_static():
    """An attribute error is raised if you invoke a non-existent static field."""
    Example = ObjCClass("Example")

    # Non-existent fields raise an error.
    with pytest.raises(AttributeError):
        _ = Example.static_field_doesnt_exist

    # Cache warming doesn't affect anything.
    with pytest.raises(AttributeError):
        _ = Example.static_field_doesnt_exist


def test_static_access_non_static():
    """An instance field/method cannot be accessed from the static context."""
    Example = ObjCClass("Example")

    obj = Example.alloc().init()

    with pytest.raises(AttributeError):
        _ = obj.staticIntField

    with pytest.raises(AttributeError):
        obj.get_staticIntField()


def test_non_static_access_static():
    """A static field/method cannot be accessed from an instance context."""
    Example = ObjCClass("Example")

    with pytest.raises(AttributeError):
        _ = Example.intField

    with pytest.raises(AttributeError):
        Example.accessIntField()
