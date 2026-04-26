from __future__ import annotations

import gc
import uuid
import weakref
from collections.abc import Callable

import pytest

from rubicon.objc import (
    NSMutableArray,
    NSObject,
    ObjCClass,
    ObjCInstance,
    ObjCMetaClass,
    ObjCProtocol,
    objc_method,
    objc_property,
)
from rubicon.objc.runtime import autoreleasepool, libobjc

from .conftest import (
    NSImage,
    NSString,
)


class ObjcWeakref(NSObject):
    weak_property = objc_property(weak=True)


def assert_lifecycle(object_constructor: Callable[[], ObjCInstance]) -> None:
    obj = object_constructor()

    wr = ObjcWeakref.alloc().init()
    wr.weak_property = obj

    with autoreleasepool():
        del obj
        gc.collect()

        assert wr.weak_property is not None, (
            "object was deallocated before end of autorelease pool"
        )

    assert wr.weak_property is None, "object was not deallocated"


def test_can_produce_objcclass():
    """Creating an ObjCInstance for a class pointer gives an ObjCClass."""
    example_ptr = libobjc.objc_getClass(b"Example")
    Example = ObjCInstance(example_ptr)
    assert Example == ObjCClass("Example")
    assert isinstance(Example, ObjCClass)


def test_can_produce_objcmetaclass():
    """Creating an ObjCInstance for a metaclass pointer gives an ObjCMetaClass."""
    examplemeta_ptr = libobjc.objc_getMetaClass(b"Example")
    ExampleMeta = ObjCInstance(examplemeta_ptr)
    assert ExampleMeta == ObjCMetaClass("Example")
    assert isinstance(ExampleMeta, ObjCMetaClass)


def test_can_produce_objcprotocol():
    """Creating an ObjCInstance for a protocol pointer gives an ObjCProtocol."""
    example_protocol_ptr = libobjc.objc_getProtocol(b"ExampleProtocol")
    ExampleProtocol = ObjCInstance(example_protocol_ptr)
    assert ExampleProtocol == ObjCProtocol("ExampleProtocol")
    assert isinstance(ExampleProtocol, ObjCProtocol)


def test_str_repr():
    """An ObjCInstance's str and repr contain the object's description and
    debugDescription, respectively."""
    DescriptionTester = ObjCClass("DescriptionTester")
    py_description_string = "normal description string"
    py_debug_description_string = "debug description string"
    tester = DescriptionTester.alloc().initWithDescriptionString(
        py_description_string,
        debugDescriptionString=py_debug_description_string,
    )

    # Check str
    assert str(tester) == py_description_string

    # Check repr
    assert (
        repr(tester) == f"<ObjCInstance: DescriptionTester at {hex(id(tester))}: "
        f"{py_debug_description_string}>"
    )


def test_str_repr_with_nil_descriptions():
    """An ObjCInstance's str and repr work even if description and debugDescription are
    nil."""
    DescriptionTester = ObjCClass("DescriptionTester")
    tester = DescriptionTester.alloc().initWithDescriptionString(
        None, debugDescriptionString=None
    )
    assert str(tester) is not None
    assert repr(tester) is not None


def test_python_attribute():
    """Python attributes can be added to an ObjCInstance."""
    Thing = ObjCClass("Thing")
    thing = Thing.alloc().init()

    # Use objects that don't have an obvious Objective-C equivalent,
    # to ensure that the actual Python objects are being stored,
    # and not converted Objective-C versions.
    thing.python_object_1 = range(2, 8)
    thing.python_object_2 = type
    assert thing.python_object_1 == range(2, 8)
    assert thing.python_object_2 is type

    # Test deleting Python attribute.

    del thing.python_object_1

    with pytest.raises(AttributeError):
        _ = thing.python_object_1


def test_python_attribute_keep_alive():
    """Python attributes on an ObjCInstance are kept even if the object temporarily has
    no Python references."""
    Example = ObjCClass("Example")
    example = Example.alloc().init()
    Thing = ObjCClass("Thing")
    thing = Thing.alloc().init()

    # Use objects that don't have an obvious Objective-C equivalent,
    # to ensure that the actual Python objects are being stored,
    # and not converted Objective-C versions.
    python_object_1 = range(2, 8)
    python_object_2 = type

    # Remember the objects' IDs to allow checking that the objects retrieved
    # later are identical without keeping an actual reference to the objects.
    python_object_1_id = id(python_object_1)
    python_object_2_id = id(python_object_2)

    # Add our Python attributes to the Objective-C object.
    thing.python_object_1 = python_object_1
    thing.python_object_2 = python_object_2

    # Store the object in an Objective-C property.
    # This creates a reference in Objective-C, but not in Python.
    example.setThing(thing)

    # Delete all of our Python references to the ObjCInstance and the
    # objects stored on it.
    del python_object_1
    del python_object_2
    del thing

    # Try to force Python to destroy any no longer referenced objects.
    gc.collect()

    # Get our object back from Objective-C.
    thing = example.thing

    # Check that our Python attributes are still there.
    assert thing.python_object_1 == range(2, 8)
    assert thing.python_object_2 is type

    # Check that these are exactly the same objects that we stored before.
    assert id(thing.python_object_1) == python_object_1_id
    assert id(thing.python_object_2) == python_object_2_id


def test_python_attribute_freed():
    """Python attributes on an ObjCInstance are freed after the instance is released."""
    with autoreleasepool():
        obj = NSObject.alloc().init()

        # Use a custom object as attribute value so that we can keep
        # a weak reference.

        class TestO:
            pass

        python_object = TestO()

        wr_python_object = weakref.ref(python_object)

        # Add our Python attribute to the Objective-C object.
        obj.python_object = python_object

        # Delete all of Python references to the Python object.
        del python_object

        # Try to force Python to destroy any no longer referenced objects.
        gc.collect()

        # Check that our Python attributes are still there.
        assert obj.python_object is wr_python_object()

        # Make sure that all Python objects are freed.
        del obj
        gc.collect()

    assert wr_python_object() is None


def test_returned_lifecycle():
    """An object is retained when creating an ObjCInstance for it without implicit
    ownership.

    It is autoreleased when the ObjCInstance is garbage collected.
    """

    def create_object():
        with autoreleasepool():
            return NSString.stringWithString(str(uuid.uuid4()))

    assert_lifecycle(create_object)


def test_alloc_lifecycle():
    """We properly retain and release objects that are allocated but never
    initialized."""

    def create_object():
        with autoreleasepool():
            return NSObject.alloc()

    assert_lifecycle(create_object)


def test_alloc_init_lifecycle():
    """An object is not additionally retained when we create and initialize it through
    an alloc().init() chain.

    It is autoreleased when the ObjCInstance is garbage collected.
    """

    def create_object():
        return NSObject.alloc().init()

    assert_lifecycle(create_object)


def test_new_lifecycle():
    """An object is not additionally retained when we create and initialize it with a
    new call.

    It is autoreleased when the ObjCInstance is garbage collected.
    """

    def create_object():
        return NSObject.new()

    assert_lifecycle(create_object)


def test_copy_lifecycle():
    """An object is not additionally retained when we create and initialize it with a
    copy call.

    It is autoreleased when the ObjCInstance is garbage collected.
    """

    def create_object():
        obj = NSMutableArray.alloc().init()
        copy = obj.copy()

        # Check that the copy is a new object.
        assert obj is not copy
        assert obj.ptr.value != copy.ptr.value

        return copy

    assert_lifecycle(create_object)


def test_mutable_copy_lifecycle():
    """An object is not additionally retained when we create and initialize it with a
    mutableCopy call.

    It is autoreleased when the ObjCInstance is garbage collected.
    """

    def create_object():
        obj = NSMutableArray.alloc().init()
        copy = obj.mutableCopy()

        # Check that the copy is a new object.
        assert obj is not copy
        assert obj.ptr.value != copy.ptr.value

        return copy

    assert_lifecycle(create_object)


def test_immutable_copy_lifecycle():
    """If the same object is returned from multiple creation methods, it is still freed
    on Python garbage collection."""

    def create_object():
        with autoreleasepool():
            obj = NSString.stringWithString(str(uuid.uuid4()))
            copy = obj.copy()

        # Check that the copy the same object as the original.
        assert obj is copy
        assert obj.ptr.value == copy.ptr.value

        return obj

    assert_lifecycle(create_object)


def test_init_change_lifecycle():
    """We do not leak memory if init returns a different object than it received in
    alloc."""

    def create_object():
        with autoreleasepool():
            obj_allocated = NSString.alloc()
            obj_initialized = obj_allocated.initWithString(str(uuid.uuid4()))

        # Check that the initialized object is a different one than the allocated.
        assert obj_allocated is not obj_initialized
        assert obj_allocated.ptr.value != obj_initialized.ptr.value

        return obj_initialized

    assert_lifecycle(create_object)


def test_init_none():
    """We do not segfault if init returns nil."""
    with autoreleasepool():
        image = NSImage.alloc().initWithContentsOfFile("/no/file/here")

    assert image is None


def test_dealloc():
    class DeallocTester(NSObject):
        did_dealloc = False

        attr0 = objc_property()
        attr1 = objc_property(weak=True)

        @objc_method
        def dealloc(self):
            DeallocTester.did_dealloc = True

    obj = DeallocTester.alloc().init()

    attr0 = NSObject.alloc().init()
    attr1 = NSObject.alloc().init()

    obj.attr0 = attr0
    obj.attr1 = attr1

    assert attr0.retainCount() == 2
    assert attr1.retainCount() == 1

    # Delete the Python wrapper and ensure that the Objective-C object is
    # deallocated after ``autorelease`` on garbage collection. This will also
    # trigger a decrement in the retain count of attr0.
    with autoreleasepool():
        del obj
        gc.collect()

    assert DeallocTester.did_dealloc, "custom dealloc did not run"
    assert attr0.retainCount() == 1, "strong property value was not released"
    assert attr1.retainCount() == 1, "weak property value was released"


def test_polymorphic_constructor():
    """Check that the right constructor is activated based on arguments used."""
    Example = ObjCClass("Example")

    obj1 = Example.alloc().init()
    obj2 = Example.alloc().initWithIntValue_(2242)
    obj3 = Example.alloc().initWithBaseIntValue_intValue_(3342, 3337)

    assert obj1.baseIntField == 22
    assert obj1.intField == 33

    assert obj2.baseIntField == 44
    assert obj2.intField == 2242

    assert obj3.baseIntField == 3342
    assert obj3.intField == 3337

    # Protected constructors can't be invoked
    with pytest.raises(AttributeError):
        Example.alloc().initWithString_("Hello")
