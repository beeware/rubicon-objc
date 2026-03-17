from __future__ import annotations

import pytest

from rubicon.objc import (
    NSObject,
    ObjCClass,
    ObjCMetaClass,
)
from rubicon.objc.runtime import libobjc


def test_by_name():
    """An Objective-C metaclass can be looked up by name."""

    Example = ObjCClass("Example")
    ExampleMeta = ObjCMetaClass("Example")

    assert ExampleMeta.name == "Example"
    assert ExampleMeta == Example.objc_class


def test_caching():
    """ObjCMetaClass instances are cached."""

    ExampleMeta1 = ObjCMetaClass("Example")
    ExampleMeta2 = ObjCMetaClass("Example")

    assert ExampleMeta1 is ExampleMeta2


def test_by_pointer():
    """An Objective-C metaclass can be created from a pointer."""

    examplemeta_ptr = libobjc.objc_getMetaClass(b"Example")
    ExampleMeta = ObjCMetaClass(examplemeta_ptr)
    assert ExampleMeta == ObjCMetaClass("Example")


def test_nonexistant():
    """A NameError is raised if a metaclass doesn't exist."""

    with pytest.raises(NameError):
        ObjCMetaClass("DoesNotExist")


def test_meta():
    """The class of a metaclass can be looked up."""

    ExampleMeta = ObjCMetaClass("Example")
    ExampleMetaMeta = ExampleMeta.objc_class

    assert isinstance(ExampleMetaMeta, ObjCMetaClass)
    assert ExampleMetaMeta == NSObject.objc_class


def test_requires_metaclass():
    """ObjCMetaClass only accepts metaclass pointers."""

    random_obj = NSObject.alloc().init()
    with pytest.raises(ValueError):
        ObjCMetaClass(random_obj.ptr)

    with pytest.raises(ValueError):
        ObjCMetaClass(NSObject.ptr)


def test_superclass():
    """An ObjCMetaClass's superclass can be looked up."""

    Example = ObjCClass("Example")
    BaseExample = ObjCClass("BaseExample")

    assert Example.objc_class.superclass == BaseExample.objc_class
    assert BaseExample.objc_class.superclass == NSObject.objc_class
    assert NSObject.objc_class.superclass == NSObject
