from __future__ import annotations

from ctypes import c_int

import pytest

from rubicon.objc import (
    NSMakeRect,
    NSObject,
    NSObjectProtocol,
    NSRect,
    NSSize,
    ObjCClass,
    ObjCProtocol,
    at,
    objc_classmethod,
    objc_method,
    objc_property,
    py_from_ns,
    send_super,
)
from rubicon.objc.runtime import libobjc

from .conftest import NSString


def test_by_name():
    """An Objective-C protocol can be looked up by name."""

    ExampleProtocol = ObjCProtocol("ExampleProtocol")
    assert ExampleProtocol.name == "ExampleProtocol"


def test_caching():
    """ObjCProtocol instances are cached."""

    ExampleProtocol1 = ObjCProtocol("ExampleProtocol")
    ExampleProtocol2 = ObjCProtocol("ExampleProtocol")

    assert ExampleProtocol1 is ExampleProtocol2


def test_by_pointer():
    """An Objective-C protocol can be created from a pointer."""

    example_protocol_ptr = libobjc.objc_getProtocol(b"ExampleProtocol")
    ExampleProtocol = ObjCProtocol(example_protocol_ptr)
    assert ExampleProtocol == ObjCProtocol("ExampleProtocol")


def test_nonexistant_protocol():
    """A NameError is raised if a protocol doesn't exist."""

    with pytest.raises(NameError):
        ObjCProtocol("DoesNotExist")


def test_requires_protocol():
    """ObjCProtocol only accepts protocol pointers."""

    random_obj = NSObject.alloc().init()
    with pytest.raises(ValueError):
        ObjCProtocol(random_obj.ptr)


def test_derived_protocols():
    """An ObjCProtocol's protocols can be looked up."""

    DerivedProtocol = ObjCProtocol("DerivedProtocol")
    BaseProtocolOne = ObjCProtocol("BaseProtocolOne")
    BaseProtocolTwo = ObjCProtocol("BaseProtocolTwo")

    assert DerivedProtocol.protocols, (BaseProtocolOne, BaseProtocolTwo)


def test_instancecheck():
    """``isinstance()`` works with an ObjCProtocol as the second argument."""

    NSCoding = ObjCProtocol("NSCoding")
    NSSecureCoding = ObjCProtocol("NSSecureCoding")

    assert isinstance(at(""), NSSecureCoding)
    assert isinstance(at(""), NSCoding)

    assert not isinstance(object(), NSSecureCoding)
    assert not isinstance(NSObject.new(), NSSecureCoding)


def test_subclasscheck():
    """``issubclass()`` works with an ObjCProtocol as the second argument."""
    NSCopying = ObjCProtocol("NSCopying")
    NSCoding = ObjCProtocol("NSCoding")
    NSSecureCoding = ObjCProtocol("NSSecureCoding")

    assert issubclass(NSObject, NSObjectProtocol)
    assert issubclass(NSString, NSObjectProtocol)
    assert issubclass(NSSecureCoding, NSSecureCoding)
    assert issubclass(NSSecureCoding, NSCoding)

    assert not issubclass(NSObject, NSSecureCoding)
    assert not issubclass(NSCoding, NSSecureCoding)
    assert not issubclass(NSCopying, NSSecureCoding)

    with pytest.raises(TypeError):
        issubclass(object(), NSSecureCoding)
    with pytest.raises(TypeError):
        issubclass(object, NSSecureCoding)
    with pytest.raises(TypeError):
        issubclass(NSObject.new(), NSSecureCoding)


def test_auto_rename_global():
    """Test the global automatic renaming option of ObjCProtocol."""

    try:
        ObjCProtocol.auto_rename = True

        class TestGlobalRenamedProtocol(metaclass=ObjCProtocol):
            pass

        protocol1 = TestGlobalRenamedProtocol

        class TestGlobalRenamedProtocol_2(metaclass=ObjCProtocol):
            pass

        class TestGlobalRenamedProtocol(metaclass=ObjCProtocol):
            pass

        # Check that the protocol was renamed
        assert TestGlobalRenamedProtocol.name == "TestGlobalRenamedProtocol_3"
        assert protocol1 is not TestGlobalRenamedProtocol

    finally:
        ObjCProtocol.auto_rename = False


def test_auto_rename_per_class():
    """Test the per-protocol automatic renaming option of ObjCProtocol."""

    class TestLocalRenamedProtocol(metaclass=ObjCProtocol):
        pass

    protocol1 = TestLocalRenamedProtocol

    class TestLocalRenamedProtocol_2(metaclass=ObjCProtocol):
        pass

    class TestLocalRenamedProtocol(
        metaclass=ObjCProtocol,
        auto_rename=True,
    ):
        pass

    # Check that the protocol was renamed
    assert TestLocalRenamedProtocol.name == "TestLocalRenamedProtocol_3"
    assert protocol1 is not TestLocalRenamedProtocol


def test_no_duplicate_protocols():
    """An Objective-C class cannot adopt a protocol more than once."""

    with pytest.raises(ValueError):

        class DuplicateProtocol(
            NSObject, protocols=[NSObjectProtocol, NSObjectProtocol]
        ):
            pass


def test_def_empty():
    """An empty ObjCProtocol can be defined."""

    class EmptyProtocol(metaclass=ObjCProtocol):
        pass


def test_def_methods():
    """An ObjCProtocol with method definitions can be defined."""

    class ProtocolWithSomeMethods(metaclass=ObjCProtocol):
        @objc_classmethod
        def class_method(self, param) -> c_int:
            pass

        @objc_method
        def instance_method(self, param) -> c_int:
            pass

    # TODO Test that the methods are actually defined


def test_def_property():
    """An ObjCProtocol with a property definition can be defined."""

    class ProtocolWithAProperty(metaclass=ObjCProtocol):
        prop = objc_property()

    # TODO Test that the property is actually defined


def test_def_extends():
    """An ObjCProtocol that extends other protocols can be defined."""

    ExampleProtocol = ObjCProtocol("ExampleProtocol")

    class ProtocolExtendsProtocols(NSObjectProtocol, ExampleProtocol):
        pass

    assert ProtocolExtendsProtocols.protocols == (NSObjectProtocol, ExampleProtocol)


def test_repr():
    """Test ObjCProtocol repr return correct value."""

    assert repr(NSObjectProtocol) == "<ObjCProtocol: NSObject>"


def test_interface():
    """An ObjC protocol implementation can be defined in Python."""

    Callback = ObjCProtocol("Callback")
    results = {}

    class Handler(NSObject, protocols=[Callback]):
        @objc_method
        def initWithValue_(self, value: int):
            self.value = value
            return self

        @objc_method
        def peek_withValue_(self, example, value: int) -> None:
            results["string"] = example.toString() + " peeked"
            results["int"] = value + self.value

        @objc_method
        def poke_withValue_(self, example, value: int) -> None:
            results["string"] = example.toString() + " poked"
            results["int"] = value + self.value

        @objc_method
        def reverse_(self, input):
            return "".join(reversed(input))

        @objc_method
        def message(self):
            return "Alea iacta est."

        @objc_classmethod
        def fiddle_(cls, value: int) -> None:
            results["string"] = "Fiddled with it"
            results["int"] = value

    # Check that the protocol is adopted.
    assert Handler.protocols == (Callback,)

    # Create two handler instances so we can check the right one
    # is being invoked.
    handler1 = Handler.alloc().initWithValue_(5)
    handler2 = Handler.alloc().initWithValue_(10)

    # Create an Example object, and register a handler with it.
    Example = ObjCClass("Example")
    example = Example.alloc().init()
    example.callback = handler2

    # Check some Python-side attributes
    assert handler1.value == 5
    assert handler2.value == 10

    # Invoke the callback; check that the results have been peeked as expected
    example.testPeek_(42)

    assert results["string"] == "This is an ObjC Example object peeked"
    assert results["int"] == 52

    example.testPoke_(37)

    assert results["string"] == "This is an ObjC Example object poked"
    assert results["int"] == 47

    assert example.getMessage() == "Alea iacta est."

    assert example.reverseIt_("Alea iacta est.") == ".tse atcai aelA"

    Handler.fiddle_(99)

    assert results["string"] == "Fiddled with it"
    assert results["int"] == 99


def test_interface_return_struct():
    """An ObjC protocol implementation that returns values by struct can be defined in
    Python."""

    results = {}
    Thing = ObjCClass("Thing")

    class StructReturnHandler(Thing):
        @objc_method
        def initWithValue_(self, value):
            self.value = py_from_ns(value)
            return self

        @objc_method
        def computeSize_(self, input: NSSize) -> NSSize:
            results["size"] = True
            sup = send_super(
                __class__,
                self,
                "computeSize:",
                input,
                restype=NSSize,
                argtypes=[NSSize],
            )
            return NSSize(input.width + self.value, sup.height)

        @objc_method
        def computeRect_(self, input: NSRect) -> NSRect:
            results["rect"] = True
            sup = send_super(
                __class__,
                self,
                "computeRect:",
                input,
                restype=NSRect,
                argtypes=[NSRect],
            )
            return NSMakeRect(
                input.origin.y + self.value,
                sup.origin.x,
                input.size.height + self.value,
                sup.size.width,
            )

        # Register a second method returning NSSize. Don't
        # have to use it - just have to register that it exists.
        @objc_method
        def origin(self) -> NSSize:
            return NSSize(0, 0)

    # Create two handler instances so we can check the right one
    # is being invoked.
    handler1 = StructReturnHandler.alloc().initWithValue_(5)
    handler2 = StructReturnHandler.alloc().initWithValue_(10)

    outSize = handler1.computeSize(NSSize(20, 30))
    assert outSize.width == 25
    assert outSize.height == 90
    assert results.get("size")

    outRect = handler2.computeRect(NSMakeRect(10, 20, 30, 40))
    assert outRect.origin.x == 30
    assert outRect.origin.y == 110
    assert outRect.size.width == 50
    assert outRect.size.height == 60
    assert results.get("rect")

    # Invoke a method through an interface.
    Example = ObjCClass("Example")
    obj = Example.alloc().init()

    # Test the base class directly
    thing1 = Thing.alloc().init()
    obj.thing = thing1
    outSize = obj.testThing(10)
    assert outSize.width == 0
    assert outSize.height == 30

    # Test the python handler
    obj.thing = handler1
    outSize = obj.testThing(15)
    assert outSize.width == 5
    assert outSize.height == 45
