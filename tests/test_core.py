from __future__ import annotations

import functools
import gc
import math
import sys
import threading
import unittest
import uuid
import weakref
from ctypes import (
    ArgumentError,
    Structure,
    byref,
    c_char,
    c_double,
    c_float,
    c_int,
    c_void_p,
    cast,
    create_string_buffer,
)
from decimal import Decimal
from enum import Enum
from typing import Callable

from rubicon.objc import (
    SEL,
    CFRange,
    CGPoint,
    CGRect,
    CGSize,
    NSEdgeInsets,
    NSEdgeInsetsMake,
    NSMakeRect,
    NSMutableArray,
    NSObject,
    NSObjectProtocol,
    NSPoint,
    NSRange,
    NSRect,
    NSSize,
    NSUInteger,
    ObjCClass,
    ObjCInstance,
    ObjCMetaClass,
    ObjCProtocol,
    UIEdgeInsets,
    at,
    objc_classmethod,
    objc_const,
    objc_ivar,
    objc_method,
    objc_property,
    py_from_ns,
    send_message,
    send_super,
    types,
)
from rubicon.objc.api import get_method_family
from rubicon.objc.runtime import (
    autoreleasepool,
    get_ivar,
    libobjc,
    load_library,
    objc_id,
    set_ivar,
)
from rubicon.objc.types import __LP64__

from . import OSX_VERSION, rubiconharness

appkit = load_library("AppKit")

NSArray = ObjCClass("NSArray")
NSImage = ObjCClass("NSImage")
NSString = ObjCClass("NSString")


class ObjcWeakref(NSObject):
    weak_property = objc_property(weak=True)


class struct_int_sized(Structure):
    _fields_ = [("x", c_char * 4)]


class struct_oddly_sized(Structure):
    _fields_ = [("x", c_char * 5)]


class struct_large(Structure):
    _fields_ = [("x", c_char * 17)]


def assert_lifecycle(
    test: unittest.TestCase, object_constructor: Callable[[], ObjCInstance]
) -> None:
    obj = object_constructor()

    wr = ObjcWeakref.alloc().init()
    wr.weak_property = obj

    with autoreleasepool():
        del obj
        gc.collect()

        test.assertIsNotNone(
            wr.weak_property,
            "object was deallocated before end of autorelease pool",
        )

    test.assertIsNone(wr.weak_property, "object was not deallocated")


class RubiconTest(unittest.TestCase):
    def test_sel_by_name(self):
        self.assertEqual(SEL(b"foobar").name, b"foobar")

    def test_sel_null(self):
        with self.assertRaises(ValueError):
            SEL(None).name

    def test_class_by_name(self):
        """An Objective-C class can be looked up by name."""

        Example = ObjCClass("Example")
        self.assertEqual(Example.name, "Example")

    def test_objcclass_caching(self):
        """ObjCClass instances are cached."""

        Example1 = ObjCClass("Example")
        Example2 = ObjCClass("Example")

        self.assertIs(Example1, Example2)

    def test_class_by_pointer(self):
        """An Objective-C class can be created from a pointer."""

        example_ptr = libobjc.objc_getClass(b"Example")
        Example = ObjCClass(example_ptr)
        self.assertEqual(Example, ObjCClass("Example"))

    def test_nonexistant_class(self):
        """A NameError is raised if a class doesn't exist."""

        with self.assertRaises(NameError):
            ObjCClass("DoesNotExist")

    def test_metaclass_by_name(self):
        """An Objective-C metaclass can be looked up by name."""

        Example = ObjCClass("Example")
        ExampleMeta = ObjCMetaClass("Example")

        self.assertEqual(ExampleMeta.name, "Example")
        self.assertEqual(ExampleMeta, Example.objc_class)

    def test_objcmetaclass_caching(self):
        """ObjCMetaClass instances are cached."""

        ExampleMeta1 = ObjCMetaClass("Example")
        ExampleMeta2 = ObjCMetaClass("Example")

        self.assertIs(ExampleMeta1, ExampleMeta2)

    def test_metaclass_by_pointer(self):
        """An Objective-C metaclass can be created from a pointer."""

        examplemeta_ptr = libobjc.objc_getMetaClass(b"Example")
        ExampleMeta = ObjCMetaClass(examplemeta_ptr)
        self.assertEqual(ExampleMeta, ObjCMetaClass("Example"))

    def test_nonexistant_metaclass(self):
        """A NameError is raised if a metaclass doesn't exist."""

        with self.assertRaises(NameError):
            ObjCMetaClass("DoesNotExist")

    def test_metametaclass(self):
        """The class of a metaclass can be looked up."""

        ExampleMeta = ObjCMetaClass("Example")
        ExampleMetaMeta = ExampleMeta.objc_class

        self.assertIsInstance(ExampleMetaMeta, ObjCMetaClass)
        self.assertEqual(ExampleMetaMeta, NSObject.objc_class)

    def test_protocol_by_name(self):
        """An Objective-C protocol can be looked up by name."""

        ExampleProtocol = ObjCProtocol("ExampleProtocol")
        self.assertEqual(ExampleProtocol.name, "ExampleProtocol")

    def test_protocol_caching(self):
        """ObjCProtocol instances are cached."""

        ExampleProtocol1 = ObjCProtocol("ExampleProtocol")
        ExampleProtocol2 = ObjCProtocol("ExampleProtocol")

        self.assertIs(ExampleProtocol1, ExampleProtocol2)

    def test_protocol_by_pointer(self):
        """An Objective-C protocol can be created from a pointer."""

        example_protocol_ptr = libobjc.objc_getProtocol(b"ExampleProtocol")
        ExampleProtocol = ObjCProtocol(example_protocol_ptr)
        self.assertEqual(ExampleProtocol, ObjCProtocol("ExampleProtocol"))

    def test_nonexistant_protocol(self):
        """A NameError is raised if a protocol doesn't exist."""

        with self.assertRaises(NameError):
            ObjCProtocol("DoesNotExist")

    def test_objcinstance_can_produce_objcclass(self):
        """Creating an ObjCInstance for a class pointer gives an ObjCClass."""

        example_ptr = libobjc.objc_getClass(b"Example")
        Example = ObjCInstance(example_ptr)
        self.assertEqual(Example, ObjCClass("Example"))
        self.assertIsInstance(Example, ObjCClass)

    def test_objcinstance_can_produce_objcmetaclass(self):
        """Creating an ObjCInstance for a metaclass pointer gives an
        ObjCMetaClass."""

        examplemeta_ptr = libobjc.objc_getMetaClass(b"Example")
        ExampleMeta = ObjCInstance(examplemeta_ptr)
        self.assertEqual(ExampleMeta, ObjCMetaClass("Example"))
        self.assertIsInstance(ExampleMeta, ObjCMetaClass)

    def test_objcclass_can_produce_objcmetaclass(self):
        """Creating an ObjCClass for a metaclass pointer gives an
        ObjCMetaclass."""

        examplemeta_ptr = libobjc.objc_getMetaClass(b"Example")
        ExampleMeta = ObjCClass(examplemeta_ptr)
        self.assertEqual(ExampleMeta, ObjCMetaClass("Example"))
        self.assertIsInstance(ExampleMeta, ObjCMetaClass)

    def test_objcinstance_can_produce_objcprotocol(self):
        """Creating an ObjCInstance for a protocol pointer gives an
        ObjCProtocol."""

        example_protocol_ptr = libobjc.objc_getProtocol(b"ExampleProtocol")
        ExampleProtocol = ObjCInstance(example_protocol_ptr)
        self.assertEqual(ExampleProtocol, ObjCProtocol("ExampleProtocol"))
        self.assertIsInstance(ExampleProtocol, ObjCProtocol)

    def test_objcclass_requires_class(self):
        """ObjCClass only accepts class pointers."""

        random_obj = NSObject.alloc().init()
        with self.assertRaises(ValueError):
            ObjCClass(random_obj.ptr)

    def test_objcmetaclass_requires_metaclass(self):
        """ObjCMetaClass only accepts metaclass pointers."""

        random_obj = NSObject.alloc().init()
        with self.assertRaises(ValueError):
            ObjCMetaClass(random_obj.ptr)

        with self.assertRaises(ValueError):
            ObjCMetaClass(NSObject.ptr)

    def test_objcprotocol_requires_protocol(self):
        """ObjCProtocol only accepts protocol pointers."""

        random_obj = NSObject.alloc().init()
        with self.assertRaises(ValueError):
            ObjCProtocol(random_obj.ptr)

    def test_objcclass_superclass(self):
        """An ObjCClass's superclass can be looked up."""

        Example = ObjCClass("Example")
        BaseExample = ObjCClass("BaseExample")

        self.assertEqual(Example.superclass, BaseExample)
        self.assertEqual(BaseExample.superclass, NSObject)
        self.assertIsNone(NSObject.superclass)

    def test_objcmetaclass_superclass(self):
        """An ObjCMetaClass's superclass can be looked up."""

        Example = ObjCClass("Example")
        BaseExample = ObjCClass("BaseExample")

        self.assertEqual(Example.objc_class.superclass, BaseExample.objc_class)
        self.assertEqual(BaseExample.objc_class.superclass, NSObject.objc_class)
        self.assertEqual(NSObject.objc_class.superclass, NSObject)

    def test_objcclass_protocols(self):
        """An ObjCClass's protocols can be looked up."""

        BaseExample = ObjCClass("BaseExample")
        ExampleProtocol = ObjCProtocol("ExampleProtocol")
        DerivedProtocol = ObjCProtocol("DerivedProtocol")

        self.assertEqual(BaseExample.protocols, (ExampleProtocol, DerivedProtocol))

    def test_objcprotocol_protocols(self):
        """An ObjCProtocol's protocols can be looked up."""

        DerivedProtocol = ObjCProtocol("DerivedProtocol")
        BaseProtocolOne = ObjCProtocol("BaseProtocolOne")
        BaseProtocolTwo = ObjCProtocol("BaseProtocolTwo")

        self.assertEqual(DerivedProtocol.protocols, (BaseProtocolOne, BaseProtocolTwo))

    def test_objcclass_instancecheck(self):
        """isinstance works with an ObjCClass as the second argument."""
        self.assertIsInstance(NSObject.new(), NSObject)
        self.assertIsInstance(at(""), NSString)
        self.assertIsInstance(at(""), NSObject)
        self.assertIsInstance(NSObject, NSObject)
        self.assertIsInstance(NSObject, NSObject.objc_class)

        self.assertNotIsInstance(object(), NSObject)
        self.assertNotIsInstance(NSObject.new(), NSString)
        self.assertNotIsInstance(NSArray.array, NSString)

    def test_objcclass_subclasscheck(self):
        """issubclass works with an ObjCClass as the second argument."""
        self.assertTrue(issubclass(NSObject, NSObject))
        self.assertTrue(issubclass(NSString, NSObject))
        self.assertTrue(issubclass(NSObject.objc_class, NSObject))
        self.assertTrue(issubclass(NSObject.objc_class, NSObject.objc_class))

        self.assertFalse(issubclass(NSObject, NSString))
        self.assertFalse(issubclass(NSArray, NSString))

        with self.assertRaises(TypeError):
            issubclass(object(), NSObject)
        with self.assertRaises(TypeError):
            issubclass(object, NSObject)
        with self.assertRaises(TypeError):
            issubclass(NSObject.new(), NSObject)
        with self.assertRaises(TypeError):
            issubclass(NSObjectProtocol, NSObject)

    def test_objcprotocol_instancecheck(self):
        """isinstance works with an ObjCProtocol as the second argument."""

        NSCoding = ObjCProtocol("NSCoding")
        NSSecureCoding = ObjCProtocol("NSSecureCoding")

        self.assertIsInstance(at(""), NSSecureCoding)
        self.assertIsInstance(at(""), NSCoding)

        self.assertNotIsInstance(object(), NSSecureCoding)
        self.assertNotIsInstance(NSObject.new(), NSSecureCoding)

    def test_objcprotocol_subclasscheck(self):
        """issubclass works with an ObjCProtocol as the second argument."""
        NSCopying = ObjCProtocol("NSCopying")
        NSCoding = ObjCProtocol("NSCoding")
        NSSecureCoding = ObjCProtocol("NSSecureCoding")

        self.assertTrue(issubclass(NSObject, NSObjectProtocol))
        self.assertTrue(issubclass(NSString, NSObjectProtocol))
        self.assertTrue(issubclass(NSSecureCoding, NSSecureCoding))
        self.assertTrue(issubclass(NSSecureCoding, NSCoding))

        self.assertFalse(issubclass(NSObject, NSSecureCoding))
        self.assertFalse(issubclass(NSCoding, NSSecureCoding))
        self.assertFalse(issubclass(NSCopying, NSSecureCoding))

        with self.assertRaises(TypeError):
            issubclass(object(), NSSecureCoding)
        with self.assertRaises(TypeError):
            issubclass(object, NSSecureCoding)
        with self.assertRaises(TypeError):
            issubclass(NSObject.new(), NSSecureCoding)

    def test_field(self):
        """A field on an instance can be accessed and mutated"""

        Example = ObjCClass("Example")

        obj = Example.alloc().init()

        self.assertEqual(obj.baseIntField, 22)
        self.assertEqual(obj.intField, 33)

        obj.baseIntField = 8888
        obj.intField = 9999

        self.assertEqual(obj.baseIntField, 8888)
        self.assertEqual(obj.intField, 9999)

    def test_method(self):
        """An instance method can be invoked."""
        Example = ObjCClass("Example")

        obj = Example.alloc().init()

        self.assertEqual(obj.accessBaseIntField(), 22)
        self.assertEqual(obj.accessIntField(), 33)

        obj.mutateBaseIntFieldWithValue_(8888)
        obj.mutateIntFieldWithValue_(9999)

        self.assertEqual(obj.accessBaseIntField(), 8888)
        self.assertEqual(obj.accessIntField(), 9999)

    def test_method_incorrect_argument_count(self):
        """Attempting to call a method with an incorrect number of arguments
        throws an exception."""

        Example = ObjCClass("Example")
        obj = Example.alloc().init()

        with self.assertRaises(TypeError):
            obj.accessIntField("extra argument 1")

        with self.assertRaises(TypeError):
            obj.mutateIntFieldWithValue_()

        with self.assertRaises(TypeError):
            obj.mutateIntFieldWithValue_(123, "extra argument")

    def test_method_incorrect_argument_type(self):
        """Attempting to call a method with the wrong type of argument throws an exception."""

        Example = ObjCClass("Example")
        obj = Example.alloc().init()

        with self.assertRaisesRegex(
            ArgumentError,
            r"mutateIntFieldWithValue: argument 3: "
            + (
                r"TypeError: 'float' object cannot be interpreted as an integer; argtypes: c_int"
                if sys.version_info >= (3, 12)
                else (
                    r"TypeError: wrong type; argtypes: c_int"
                    if sys.version_info >= (3, 10)
                    else r"<class 'TypeError'>: wrong type; argtypes: c_int"
                )
            ),
        ):
            obj.mutateIntFieldWithValue_(1.234)

    def test_method_incorrect_argument_count_send(self):
        """Attempting to call a method with send_message with an incorrect
        number of arguments throws an exception."""

        Example = ObjCClass("Example")
        obj = Example.alloc().init()

        with self.assertRaises(TypeError):
            send_message(
                obj, "accessIntField", "extra argument 1", restype=c_int, argtypes=[]
            )

        with self.assertRaises(TypeError):
            send_message(
                obj, "mutateIntFieldWithValue:", restype=None, argtypes=[c_int]
            )

        with self.assertRaises(TypeError):
            send_message(
                obj,
                "mutateIntFieldWithValue:",
                123,
                "extra_argument",
                restype=None,
                argtypes=[c_int],
            )

    def test_method_varargs_send(self):
        """A variadic method can be called using send_message."""
        formatted = send_message(
            NSString,
            "stringWithFormat:",
            at("This is a %@ with %@"),
            varargs=[at("string"), at("placeholders")],
            restype=objc_id,
            argtypes=[objc_id],
        )
        self.assertEqual(
            str(ObjCInstance(formatted)), "This is a string with placeholders"
        )

    def test_method_send(self):
        """An instance method can be invoked with send_message."""
        Example = ObjCClass("Example")

        obj = Example.alloc().init()

        self.assertEqual(
            send_message(obj, "accessBaseIntField", restype=c_int, argtypes=[]), 22
        )
        self.assertEqual(
            send_message(obj, "accessIntField", restype=c_int, argtypes=[]), 33
        )

        send_message(
            obj, "mutateBaseIntFieldWithValue:", 8888, restype=None, argtypes=[c_int]
        )
        send_message(
            obj, "mutateIntFieldWithValue:", 9999, restype=None, argtypes=[c_int]
        )

        self.assertEqual(
            send_message(obj, "accessBaseIntField", restype=c_int, argtypes=[]), 8888
        )
        self.assertEqual(
            send_message(obj, "accessIntField", restype=c_int, argtypes=[]), 9999
        )

    def test_send_sel(self):
        """send_message accepts a SEL object as the selector parameter."""
        Example = ObjCClass("Example")

        obj = Example.alloc().init()

        self.assertEqual(
            send_message(obj, SEL("accessIntField"), restype=c_int, argtypes=[]), 33
        )

    def test_send_super(self):
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

        self.assertEqual(obj.baseIntField, 10)

    def test_send_super_sel(self):
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

        self.assertEqual(obj.baseIntField, 10)

    def test_send_super_incorrect_argument_count(self):
        """Attempting to call a method with send_super with an incorrect number
        of arguments throws an exception."""
        SpecificExample = ObjCClass("SpecificExample")

        obj = SpecificExample.alloc().init()

        with self.assertRaises(TypeError):
            send_super(
                SpecificExample, obj, "method:withArg:", 2, restype=None, argtypes=[]
            )

        with self.assertRaises(TypeError):
            send_super(
                SpecificExample,
                obj,
                "method:withArg:",
                restype=None,
                argtypes=[c_int, c_int],
            )

        with self.assertRaises(TypeError):
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

    def test_send_super_varargs(self):
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

        self.assertEqual(obj.accessBaseIntField(), 11)

    def test_static_field(self):
        """A static field on a class can be accessed and mutated"""
        Example = ObjCClass("Example")

        Example.mutateStaticBaseIntFieldWithValue_(1)
        Example.mutateStaticIntFieldWithValue_(11)

        self.assertEqual(Example.staticBaseIntField, 1)
        self.assertEqual(Example.staticIntField, 11)

        Example.staticBaseIntField = 1188
        Example.staticIntField = 1199

        self.assertEqual(Example.staticBaseIntField, 1188)
        self.assertEqual(Example.staticIntField, 1199)

    def test_static_method(self):
        """A static method on a class can be invoked."""
        Example = ObjCClass("Example")

        Example.mutateStaticBaseIntFieldWithValue_(2288)
        Example.mutateStaticIntFieldWithValue_(2299)

        self.assertEqual(Example.accessStaticBaseIntField(), 2288)
        self.assertEqual(Example.accessStaticIntField(), 2299)

    def test_mutator_like_method(self):
        """A method that looks like a mutator doesn't confuse issues."""
        Example = ObjCClass("Example")

        obj1 = Example.alloc().init()

        # setSpecialValue: looks like it might be a mutator
        # for a specialValue property, but this property doesn't exist.

        # We can invoke the method directly...
        obj1.setSpecialValue_(42)

        # ... but retrieving like a property is an error
        with self.assertRaises(AttributeError):
            obj1.specialValue

        # ...until you set it explicitly...
        obj1.specialValue = 37

        # ...at which point it's fair game to be retrieved.
        self.assertEqual(obj1.specialValue, 37)

    def test_property_forcing(self):
        """An instance or property method can be explicitly declared as a property."""
        Example = ObjCClass("Example")
        Example.declare_class_property("classMethod")
        Example.declare_class_property("classAmbiguous")
        Example.declare_property("instanceMethod")
        Example.declare_property("instanceAmbiguous")

        # A class method can be turned into a property
        self.assertEqual(Example.classMethod, 37)

        # An actual class property can be accessed as a property
        self.assertEqual(Example.classAmbiguous, 37)

        # An instance property can be accessed
        obj1 = Example.alloc().init()

        # An instance method can be turned into a property
        self.assertEqual(obj1.instanceMethod, 42)

        # An actual property can be accessed as a property
        self.assertEqual(obj1.instanceAmbiguous, 42)

        # Practical example: In Sierra, mainBundle was turned into a class property.
        # Previously, it was a method.
        NSBundle = ObjCClass("NSBundle")
        NSBundle.declare_class_property("mainBundle")
        self.assertFalse(
            callable(NSBundle.mainBundle), "NSBundle.mainBundle should not be a method"
        )

    def test_non_existent_field(self):
        """An attribute error is raised if you invoke a non-existent field."""
        Example = ObjCClass("Example")

        obj1 = Example.alloc().init()

        # Non-existent fields raise an error.
        with self.assertRaises(AttributeError):
            obj1.field_doesnt_exist

        # Cache warming doesn't affect anything.
        with self.assertRaises(AttributeError):
            obj1.field_doesnt_exist

    def test_non_existent_method(self):
        """An attribute error is raised if you invoke a non-existent method."""
        Example = ObjCClass("Example")

        obj1 = Example.alloc().init()

        # Non-existent methods raise an error.
        with self.assertRaises(AttributeError):
            obj1.method_doesnt_exist()

        # Cache warming doesn't affect anything.
        with self.assertRaises(AttributeError):
            obj1.method_doesnt_exist()

    def test_non_existent_static_field(self):
        """An attribute error is raised if you invoke a non-existent static field."""
        Example = ObjCClass("Example")

        # Non-existent fields raise an error.
        with self.assertRaises(AttributeError):
            Example.static_field_doesnt_exist

        # Cache warming doesn't affect anything.
        with self.assertRaises(AttributeError):
            Example.static_field_doesnt_exist

    def test_non_existent_static_method(self):
        """An attribute error is raised if you invoke a non-existent static method."""
        Example = ObjCClass("Example")

        # Non-existent methods raise an error.
        with self.assertRaises(AttributeError):
            Example.static_method_doesnt_exist()

        # Cache warming doesn't affect anything.
        with self.assertRaises(AttributeError):
            Example.static_method_doesnt_exist()

    def test_polymorphic_constructor(self):
        """Check that the right constructor is activated based on arguments used"""
        Example = ObjCClass("Example")

        obj1 = Example.alloc().init()
        obj2 = Example.alloc().initWithIntValue_(2242)
        obj3 = Example.alloc().initWithBaseIntValue_intValue_(3342, 3337)

        self.assertEqual(obj1.baseIntField, 22)
        self.assertEqual(obj1.intField, 33)

        self.assertEqual(obj2.baseIntField, 44)
        self.assertEqual(obj2.intField, 2242)

        self.assertEqual(obj3.baseIntField, 3342)
        self.assertEqual(obj3.intField, 3337)

        # Protected constructors can't be invoked
        with self.assertRaises(AttributeError):
            Example.alloc().initWithString_("Hello")

    def test_static_access_non_static(self):
        """An instance field/method cannot be accessed from the static context"""
        Example = ObjCClass("Example")

        obj = Example.alloc().init()

        with self.assertRaises(AttributeError):
            obj.staticIntField

        with self.assertRaises(AttributeError):
            obj.get_staticIntField()

    def test_non_static_access_static(self):
        """A static field/method cannot be accessed from an instance context"""
        Example = ObjCClass("Example")

        with self.assertRaises(AttributeError):
            Example.intField

        with self.assertRaises(AttributeError):
            Example.accessIntField()

    def test_string_argument(self):
        """A method with a string argument can be passed."""
        Example = ObjCClass("Example")
        example = Example.alloc().init()
        self.assertEqual(example.duplicateString_("Wagga"), "WaggaWagga")

    def test_enum_argument(self):
        """An enumerated type can be used as an argument."""
        Example = ObjCClass("Example")

        obj = Example.alloc().init()

        self.assertEqual(obj.accessBaseIntField(), 22)
        self.assertEqual(obj.accessIntField(), 33)

        class MyEnum(Enum):
            value1 = 8888
            value2 = 9999
            value3 = 3333
            value4 = 4444

        obj.mutateBaseIntFieldWithValue_(MyEnum.value1)
        obj.mutateIntFieldWithValue_(MyEnum.value2)

        self.assertEqual(obj.accessBaseIntField(), MyEnum.value1.value)
        self.assertEqual(obj.accessIntField(), MyEnum.value2.value)

        obj.baseIntField = MyEnum.value3
        obj.intField = MyEnum.value4

        self.assertEqual(obj.accessBaseIntField(), MyEnum.value3.value)
        self.assertEqual(obj.accessIntField(), MyEnum.value4.value)

    def test_string_return(self):
        """If a method or field returns a string, you get a Python string back"""
        Example = ObjCClass("Example")
        example = Example.alloc().init()
        self.assertEqual(example.toString(), "This is an ObjC Example object")

    def test_constant_string_return(self):
        """If a method or field returns a *constant* string, you get a Python string back"""
        Example = ObjCClass("Example")
        example = Example.alloc().init()
        self.assertEqual(example.smiley(), "%-)")

    def test_number_return(self):
        """If a method or field returns a NSNumber, it is not automatically converted to a Python number."""
        Example = ObjCClass("Example")
        example = Example.alloc().init()

        answer = example.theAnswer()
        self.assertIsInstance(answer, ObjCInstance)
        self.assertEqual(py_from_ns(answer), 42)
        tau = example.twopi()
        self.assertIsInstance(tau, ObjCInstance)
        self.assertAlmostEqual(py_from_ns(tau), 2.0 * math.pi, 5)

    def test_float_method(self):
        """A method with a float argument can be handled."""
        Example = ObjCClass("Example")
        example = Example.alloc().init()
        self.assertEqual(example.areaOfSquare_(1.5), 2.25)

    def test_float_method_send(self):
        """A method with a float argument can be handled by send_message."""
        Example = ObjCClass("Example")
        example = Example.alloc().init()
        self.assertEqual(
            send_message(
                example, "areaOfSquare:", 1.5, restype=c_float, argtypes=[c_float]
            ),
            2.25,
        )

    def test_double_method(self):
        """A method with a double argument can be handled."""
        Example = ObjCClass("Example")
        example = Example.alloc().init()
        self.assertAlmostEqual(example.areaOfCircle_(1.5), 1.5 * math.pi, 5)

    def test_double_method_send(self):
        """A method with a double argument can be handled by send_message."""
        Example = ObjCClass("Example")
        example = Example.alloc().init()
        self.assertAlmostEqual(
            send_message(
                example, "areaOfCircle:", 1.5, restype=c_double, argtypes=[c_double]
            ),
            1.5 * math.pi,
            5,
        )

    @unittest.skipIf(
        OSX_VERSION and OSX_VERSION < (10, 10),
        "Property handling doesn't work on OS X 10.9 (Mavericks) and earlier",
    )
    def test_decimal_method(self):
        """A method with a NSDecimalNumber arguments can be handled."""
        Example = ObjCClass("Example")
        example = Example.alloc().init()

        result = example.areaOfTriangleWithWidth_andHeight_(
            Decimal("3.0"), Decimal("4.0")
        )
        self.assertIsInstance(result, ObjCClass("NSDecimalNumber"))
        self.assertEqual(py_from_ns(result), Decimal("6.0"))

    def test_auto_struct_creation(self):
        """Structs from method signatures are created automatically."""
        Example = ObjCClass("Example")

        types.unregister_encoding_all(b"{simple=ii}")
        types.unregister_encoding_all(b"{simple}")
        types.unregister_encoding_all(b"{complex=[4s]^?{simple=ii}^{complex}}")
        types.unregister_encoding_all(b"{complex}")

        # Look up the method, so the return/argument types are decoded and the structs are registered.
        Example.doStuffWithStruct_

        struct_simple = types.ctype_for_encoding(b"{simple=ii}")
        self.assertEqual(struct_simple, types.ctype_for_encoding(b"{simple}"))

        simple = struct_simple(123, 456)
        ret = Example.doStuffWithStruct_(simple)
        struct_complex = types.ctype_for_encoding(
            b"{complex=[4s]^?{simple=ii}^{complex}}"
        )
        self.assertIsInstance(ret, struct_complex)
        self.assertEqual(struct_complex, types.ctype_for_encoding(b"{complex}"))
        self.assertEqual(list(ret.field_0), [1, 2, 3, 4])
        self.assertEqual(ret.field_1.value, None)
        self.assertEqual(ret.field_2.field_0, 123)
        self.assertEqual(ret.field_2.field_1, 456)
        self.assertEqual(cast(ret.field_3, c_void_p).value, None)

    def test_sequence_arg_to_struct(self):
        """Sequence arguments are converted to structures."""
        Example = ObjCClass("Example")

        ret = Example.extractSimpleStruct(([9, 8, 7, 6], None, (987, 654), None))
        struct_simple = types.ctype_for_encoding(b"{simple=ii}")
        self.assertIsInstance(ret, struct_simple)
        self.assertEqual(ret.field_0, 987)
        self.assertEqual(ret.field_1, 654)

    def test_struct_return(self):
        """Methods returning structs of different sizes by value can be handled."""
        Example = ObjCClass("Example")
        example = Example.alloc().init()

        types.register_encoding(b"{int_sized=[4c]}", struct_int_sized)
        self.assertEqual(example.intSizedStruct().x, b"abc")

        types.register_encoding(b"{oddly_sized=[5c]}", struct_oddly_sized)
        self.assertEqual(example.oddlySizedStruct().x, b"abcd")

        types.register_encoding(b"{large=[17c]}", struct_large)
        self.assertEqual(example.largeStruct().x, b"abcdefghijklmnop")

    def test_struct_return_send(self):
        """Methods returning structs of different sizes by value can be handled when using send_message."""
        Example = ObjCClass("Example")
        example = Example.alloc().init()

        self.assertEqual(
            send_message(
                example, "intSizedStruct", restype=struct_int_sized, argtypes=[]
            ).x,
            b"abc",
        )
        self.assertEqual(
            send_message(
                example, "oddlySizedStruct", restype=struct_oddly_sized, argtypes=[]
            ).x,
            b"abcd",
        )
        self.assertEqual(
            send_message(example, "largeStruct", restype=struct_large, argtypes=[]).x,
            b"abcdefghijklmnop",
        )

    def test_object_return(self):
        """If a method or field returns an object, you get an instance of that type returned"""
        Example = ObjCClass("Example")
        example = Example.alloc().init()

        Thing = ObjCClass("Thing")
        thing = Thing.alloc().initWithName_value_("This is thing", 2)

        example.thing = thing

        the_thing = example.thing
        self.assertEqual(the_thing.toString(), "This is thing 2")

    def test_no_convert_return(self):
        Example = ObjCClass("Example")
        example = Example.alloc().init()

        res = example.toString(convert_result=False)
        self.assertNotIsInstance(res, ObjCInstance)
        self.assertEqual(str(ObjCInstance(res)), "This is an ObjC Example object")

    def test_partial_method_no_args(self):
        Example = ObjCClass("Example")
        self.assertEqual(Example.overloaded(), 0)

    def test_partial_method_one_arg(self):
        Example = ObjCClass("Example")
        self.assertEqual(Example.overloaded(42), 42)

    def test_partial_method_two_args(self):
        Example = ObjCClass("Example")
        self.assertEqual(Example.overloaded(12, extraArg=34), 12 + 34)

    def test_partial_method_lots_of_args(self):
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
        self.assertEqual(buf.value.decode("utf-8"), pystring)

    def test_partial_method_arg_order(self):
        Example = ObjCClass("Example")

        self.assertEqual(Example.overloaded(3, extraArg1=5, extraArg2=7), 3 + 5 + 7)
        self.assertEqual(Example.overloaded(3, extraArg2=5, extraArg1=7), 3 * 5 * 7)

        # Although the arguments are a unique match, they're not in the right order.
        with self.assertRaises(ValueError):
            Example.overloaded(0, orderedArg2=0, orderedArg1=0)

    def test_partial_method_duplicate_arg_names(self):
        Example = ObjCClass("Example")
        self.assertEqual(
            Example.overloaded(24, duplicateArg__a=16, duplicateArg__b=6),
            24 + 2 * 16 + 3 * 6,
        )

    def test_partial_method_exception(self):
        Example = ObjCClass("Example")
        with self.assertRaisesRegex(
            ValueError,
            "Invalid selector overloaded:invalidArgument:. Available selectors are: "
            "overloaded, overloaded:, overloaded:extraArg:, "
            "overloaded:extraArg1:extraArg2:, overloaded:extraArg2:extraArg1:, "
            "overloaded:orderedArg1:orderedArg2:, overloaded:duplicateArg:duplicateArg:",
        ):
            Example.overloaded(0, invalidArgument=0)

    def test_objcmethod_str_repr(self):
        """Test ObjCMethod, ObjCPartialMethod, and ObjCBoundMethod str and repr"""

        obj = NSObject.new()

        # ObjCMethod
        self.assertEqual(repr(obj.init.method), "<ObjCMethod: init @16@0:8>")
        self.assertEqual(str(obj.init.method), "<ObjCMethod: init @16@0:8>")

        # ObjCBoundMethod
        self.assertRegex(
            repr(obj.init),
            r"ObjCBoundMethod\(<ObjCMethod: init @16@0:8>, <NSObject: 0x[0-9a-f]+>\)",
        )
        self.assertRegex(
            str(obj.init),
            r"ObjCBoundMethod\(<ObjCMethod: init @16@0:8>, <NSObject: 0x[0-9a-f]+>\)",
        )

        # ObjCPartialMethod
        self.assertEqual(
            repr(obj.performSelector.method), "ObjCPartialMethod('performSelector')"
        )
        self.assertEqual(
            str(obj.performSelector.method), "ObjCPartialMethod('performSelector')"
        )

    def test_objcinstance_str_repr(self):
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
        self.assertEqual(str(tester), py_description_string)

        # Check repr
        self.assertEqual(
            repr(tester),
            f"<ObjCInstance: DescriptionTester at {hex(id(tester))}: {py_debug_description_string}>",
        )

    def test_objcinstance_str_repr_with_nil_descriptions(self):
        """An ObjCInstance's str and repr work even if description and
        debugDescription are nil."""

        DescriptionTester = ObjCClass("DescriptionTester")
        tester = DescriptionTester.alloc().initWithDescriptionString(
            None, debugDescriptionString=None
        )
        self.assertIsNot(str(tester), None)
        self.assertIsNot(repr(tester), None)

    def test_objcclass_repr(self):
        """Test ObjCClass repr and str return correct value."""

        self.assertEqual(repr(NSObject), "<ObjCClass: NSObject>")
        self.assertEqual(str(NSObject), "ObjCClass('NSObject')")

    def test_objcprotocol_repr(self):
        """Test ObjCProtocol repr return correct value."""

        self.assertEqual(repr(NSObjectProtocol), "<ObjCProtocol: NSObject>")

    def test_nspoint_repr(self):
        """Test NSPoint repr and str returns correct value."""

        my_point = NSPoint(10, 20)
        self.assertEqual(repr(my_point), "<NSPoint(10.0, 20.0)>")
        self.assertEqual(str(my_point), "(10.0, 20.0)")

    def test_cgpoint_repr(self):
        """Test CGPoint repr and str returns correct value."""

        my_point = CGPoint(10, 20)
        if __LP64__:
            self.assertEqual(repr(my_point), "<NSPoint(10.0, 20.0)>")
        else:
            self.assertEqual(repr(my_point), "<CGPoint(10.0, 20.0)>")
        self.assertEqual(str(my_point), "(10.0, 20.0)")

    def test_nsrect_repr(self):
        """Test NSRect repr and str returns correct value."""

        my_rect = NSRect(NSPoint(10, 20), NSSize(5, 15))
        self.assertEqual(
            repr(my_rect),
            "<NSRect(NSPoint(10.0, 20.0), NSSize(5.0, 15.0))>",
        )
        self.assertEqual(str(my_rect), "5.0 x 15.0 @ (10.0, 20.0)")

    def test_cgrect_repr(self):
        """Test CGRect repr and str returns correct value."""

        my_rect = CGRect(CGPoint(10, 20), CGSize(5, 15))
        if __LP64__:
            self.assertEqual(
                repr(my_rect),
                "<NSRect(NSPoint(10.0, 20.0), NSSize(5.0, 15.0))>",
            )
        else:
            self.assertEqual(
                repr(my_rect),
                "<CGRect(CGPoint(10.0, 20.0), CGSize(5.0, 15.0))>",
            )

        self.assertEqual(str(my_rect), "5.0 x 15.0 @ (10.0, 20.0)")

    def test_nssize_repr(self):
        """Test NSSize repr and str returns correct value."""

        my_size = NSSize(5, 15)
        self.assertEqual(repr(my_size), "<NSSize(5.0, 15.0)>")
        self.assertEqual(str(my_size), "5.0 x 15.0")

    def test_cgsize_repr(self):
        """Test NSSize repr and str returns correct value."""

        my_size = CGSize(5, 15)
        if __LP64__:
            self.assertEqual(repr(my_size), "<NSSize(5.0, 15.0)>")
        else:
            self.assertEqual(repr(my_size), "<CGSize(5.0, 15.0)>")
        self.assertEqual(str(my_size), "5.0 x 15.0")

    def test_nsrange_repr(self):
        """Test NSRange repr and str returns correct value."""

        my_range = NSRange(5, 6)
        self.assertEqual(repr(my_range), "<NSRange(5, 6)>")
        self.assertEqual(str(my_range), "location=5, length=6")

    def test_cfrange_repr(self):
        """Test NSRange repr and str returns correct value."""

        my_range = CFRange(5, 6)
        self.assertEqual(repr(my_range), "<CFRange(5, 6)>")
        self.assertEqual(str(my_range), "location=5, length=6")

    def test_nsedgeinsets_repr(self):
        """Test NSRange repr and str returns correct value."""

        my_edge_insets = NSEdgeInsets(4, 5, 6, 7)
        self.assertEqual(repr(my_edge_insets), "<NSEdgeInsets(4.0, 5.0, 6.0, 7.0)>")
        self.assertEqual(
            str(my_edge_insets), "top=4.0, left=5.0, bottom=6.0, right=7.0"
        )

    def test_uiedgeinsets_repr(self):
        """Test NSRange repr and str returns correct value."""

        my_edge_insets = UIEdgeInsets(4, 5, 6, 7)
        self.assertEqual(repr(my_edge_insets), "<UIEdgeInsets(4.0, 5.0, 6.0, 7.0)>")
        self.assertEqual(
            str(my_edge_insets), "top=4.0, left=5.0, bottom=6.0, right=7.0"
        )

    def test_duplicate_class_registration(self):
        """If you define a class name twice in the same runtime, you get an error."""

        # First definition should work.
        class MyClass(NSObject):
            pass

        # Second definition will raise an error.
        # Without protection, this is a segfault.
        with self.assertRaises(RuntimeError):

            class MyClass(NSObject):  # noqa: F811
                pass

    def test_class_auto_rename_global(self):
        """Test the global automatic renaming option of ObjCClass."""

        try:
            ObjCClass.auto_rename = True

            class TestGlobalRenamedClass(NSObject):
                @objc_method
                def oldMethod(self):
                    pass

            class1 = TestGlobalRenamedClass

            class TestGlobalRenamedClass_2(NSObject):
                pass

            class TestGlobalRenamedClass(NSObject):  # noqa: F811
                @objc_method
                def testMethod(self):
                    return "TEST1"

            # Check that the class was renamed
            self.assertEqual(TestGlobalRenamedClass.name, "TestGlobalRenamedClass_3")
            self.assertIsNot(class1, TestGlobalRenamedClass)

            # Check that methods are updated
            obj = TestGlobalRenamedClass.new()
            with self.assertRaises(AttributeError):
                obj.oldMethod()
            self.assertEqual(obj.testMethod(), "TEST1")

        finally:
            ObjCClass.auto_rename = False

    def test_class_auto_rename_per_class(self):
        """Test the per-class automatic renaming option of ObjCClass."""

        class TestLocalRenamedClass(NSObject):
            @objc_method
            def oldMethod(self):
                pass

        class1 = TestLocalRenamedClass

        class TestLocalRenamedClass_2(NSObject):
            pass

        class TestLocalRenamedClass(NSObject, auto_rename=True):  # noqa: F811
            @objc_method
            def testMethod(self):
                return "TEST2"

        # Check that the class was renamed
        self.assertEqual(TestLocalRenamedClass.name, "TestLocalRenamedClass_3")
        self.assertIsNot(class1, TestLocalRenamedClass)

        # Check that methods are updated
        obj = TestLocalRenamedClass.new()
        with self.assertRaises(AttributeError):
            obj.oldMethod()
        self.assertEqual(obj.testMethod(), "TEST2")

    def test_protocol_auto_rename_global(self):
        """Test the global automatic renaming option of ObjCProtocol."""

        try:
            ObjCProtocol.auto_rename = True

            class TestGlobalRenamedProtocol(metaclass=ObjCProtocol):
                pass

            protocol1 = TestGlobalRenamedProtocol

            class TestGlobalRenamedProtocol_2(metaclass=ObjCProtocol):
                pass

            class TestGlobalRenamedProtocol(metaclass=ObjCProtocol):  # noqa: F811
                pass

            # Check that the protocol was renamed
            self.assertEqual(
                TestGlobalRenamedProtocol.name, "TestGlobalRenamedProtocol_3"
            )
            self.assertIsNot(protocol1, TestGlobalRenamedProtocol)

        finally:
            ObjCProtocol.auto_rename = False

    def test_protocol_auto_rename_per_class(self):
        """Test the per-protocol automatic renaming option of ObjCProtocol."""

        class TestLocalRenamedProtocol(metaclass=ObjCProtocol):
            pass

        protocol1 = TestLocalRenamedProtocol

        class TestLocalRenamedProtocol_2(metaclass=ObjCProtocol):
            pass

        class TestLocalRenamedProtocol(
            metaclass=ObjCProtocol,
            auto_rename=True,
        ):  # noqa: F811
            pass

        # Check that the protocol was renamed
        self.assertEqual(TestLocalRenamedProtocol.name, "TestLocalRenamedProtocol_3")
        self.assertIsNot(protocol1, TestLocalRenamedProtocol)

    def test_interface(self):
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
        self.assertSequenceEqual(Handler.protocols, (Callback,))

        # Create two handler instances so we can check the right one
        # is being invoked.
        handler1 = Handler.alloc().initWithValue_(5)
        handler2 = Handler.alloc().initWithValue_(10)

        # Create an Example object, and register a handler with it.
        Example = ObjCClass("Example")
        example = Example.alloc().init()
        example.callback = handler2

        # Check some Python-side attributes
        self.assertEqual(handler1.value, 5)
        self.assertEqual(handler2.value, 10)

        # Invoke the callback; check that the results have been peeked as expected
        example.testPeek_(42)

        self.assertEqual(results["string"], "This is an ObjC Example object peeked")
        self.assertEqual(results["int"], 52)

        example.testPoke_(37)

        self.assertEqual(results["string"], "This is an ObjC Example object poked")
        self.assertEqual(results["int"], 47)

        self.assertEqual(example.getMessage(), "Alea iacta est.")

        self.assertEqual(example.reverseIt_("Alea iacta est."), ".tse atcai aelA")

        Handler.fiddle_(99)

        self.assertEqual(results["string"], "Fiddled with it")
        self.assertEqual(results["int"], 99)

    def test_no_duplicate_protocols(self):
        """An Objective-C class cannot adopt a protocol more than once."""

        with self.assertRaises(ValueError):

            class DuplicateProtocol(
                NSObject, protocols=[NSObjectProtocol, NSObjectProtocol]
            ):
                pass

    def test_class_ivars(self):
        """An Objective-C class can have instance variables."""

        class Ivars(NSObject):
            object = objc_ivar(objc_id)
            int = objc_ivar(c_int)
            rect = objc_ivar(NSRect)

        ivars = Ivars.alloc().init()

        set_ivar(ivars, "object", at("foo").ptr)
        set_ivar(ivars, "int", c_int(12345))
        set_ivar(ivars, "rect", NSMakeRect(12, 34, 56, 78))

        s = ObjCInstance(get_ivar(ivars, "object"))
        self.assertEqual(str(s), "foo")

        i = get_ivar(ivars, "int")
        self.assertEqual(i.value, 12345)

        r = get_ivar(ivars, "rect")
        self.assertEqual(r.origin.x, 12)
        self.assertEqual(r.origin.y, 34)
        self.assertEqual(r.size.width, 56)
        self.assertEqual(r.size.height, 78)

    def test_class_properties(self):
        """A Python class can have ObjC properties with synthesized getters and setters
        of ObjCInstance type."""

        NSURL = ObjCClass("NSURL")

        class URLBox(NSObject):
            url = objc_property(ObjCInstance)
            data = objc_property(ObjCInstance)

            @objc_method
            def getSchemeIfPresent(self):
                if self.url is not None:
                    return self.url.scheme
                return None

        box = URLBox.alloc().init()

        # Default property value is None
        self.assertIsNone(box.url)

        # Assign an object via synthesized property setter and call method that uses synthesized property getter
        url = NSURL.alloc().initWithString_("https://www.google.com")
        box.url = url
        self.assertEqual(box.getSchemeIfPresent(), "https")

        # Assign None to dealloc property and see if method returns expected None
        box.url = None
        self.assertIsNone(box.getSchemeIfPresent())

        # Try composing URLs using constructors
        base = NSURL.URLWithString("https://beeware.org")
        full = NSURL.URLWithString("contributing/", relativeToURL=base)

        self.assertEqual(
            f"Visit {full.absoluteURL} for details",
            "Visit https://beeware.org/contributing/ for details",
        )

        # ObjC type conversions are performed on property assignment.
        box.data = "Jabberwock"
        self.assertEqual(box.data, "Jabberwock")

        Example = ObjCClass("Example")
        example = Example.alloc().init()
        box.data = example
        self.assertEqual(box.data, example)

        box.data = None
        self.assertIsNone(box.data)

    def test_class_python_properties(self):
        """A Python class can have ObjC properties with synthesized getters and setters
        of Python type."""

        class PythonObjectProperties(NSObject):
            object = objc_property(object)

        class PythonObject:
            pass

        properties = PythonObjectProperties.alloc().init()

        o = PythonObject()
        wr = weakref.ref(o)

        properties.object = o

        # Test that Python object is properly stored.
        self.assertIs(properties.object, o)

        # Test that Python object is retained by the property.
        del o
        gc.collect()

        self.assertIs(properties.object, wr())

        # Test that Python object is released by the property.
        properties.object = None
        gc.collect()
        self.assertIsNone(wr())

        # Test that Python object is released by dealloc.

        o = PythonObject()
        wr = weakref.ref(o)

        properties.object = o
        self.assertIs(properties.object, o)

        with autoreleasepool():
            del o
            del properties
            gc.collect()

        self.assertIsNone(wr())

    def test_class_python_properties_weak(self):
        class WeakPythonObjectProperties(NSObject):
            object = objc_property(object, weak=True)

        class PythonObject:
            pass

        properties = WeakPythonObjectProperties.alloc().init()

        o = PythonObject()
        wr = weakref.ref(o)

        properties.object = o

        # Test that Python object is properly stored.
        self.assertIs(properties.object, o)

        # Test that Python object is not retained by the property.
        del o
        gc.collect()

        self.assertIsNone(properties.object)
        self.assertIsNone(wr())

    def test_class_nonobject_properties(self):
        """An Objective-C class can have properties of non-object types."""

        class NonObjectProperties(NSObject):
            object = objc_property(ObjCInstance)
            int = objc_property(c_int)
            rect = objc_property(NSRect)

        properties = NonObjectProperties.alloc().init()

        properties.object = at("foo")
        properties.int = 12345
        properties.rect = NSMakeRect(12, 34, 56, 78)

        self.assertEqual(properties.object, "foo")
        self.assertEqual(properties.int, 12345)

        r = properties.rect
        self.assertEqual(r.origin.x, 12)
        self.assertEqual(r.origin.y, 34)
        self.assertEqual(r.size.width, 56)
        self.assertEqual(r.size.height, 78)

    def test_class_nonobject_properties_weak(self):
        with self.assertRaises(TypeError):

            class WeakNonObjectProperties(NSObject):
                int = objc_property(c_int, weak=True)

    def test_class_properties_lifecycle_strong(self):
        class StrongObjectProperties(NSObject):
            object = objc_property(ObjCInstance)

        with autoreleasepool():
            properties = StrongObjectProperties.alloc().init()

            obj = NSObject.alloc().init()
            obj_pointer = obj.ptr.value  # store the object pointer for future use

            properties.object = obj

            del obj
            gc.collect()

        # assert that the object was retained by the property
        self.assertEqual(properties.object.ptr.value, obj_pointer)

    def test_class_properties_lifecycle_weak(self):
        class WeakObjectProperties(NSObject):
            object = objc_property(ObjCInstance, weak=True)

        with autoreleasepool():
            properties = WeakObjectProperties.alloc().init()

            obj = NSObject.alloc().init()
            properties.object = obj

            self.assertIs(properties.object, obj)

            del obj
            gc.collect()

        self.assertIsNone(properties.object)

    def test_class_with_wrapped_methods(self):
        """An ObjCClass can have wrapped methods."""

        def deco(f):
            @functools.wraps(f)
            def _wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            return _wrapper

        class SimpleMath(NSObject):
            @objc_method
            @deco
            def addOne_(self, num: c_int) -> c_int:
                return num + 1

            @objc_classmethod
            @deco
            def subtractOne_(cls, num: c_int) -> c_int:
                return num - 1

        simplemath = SimpleMath.alloc().init()
        self.assertEqual(simplemath.addOne_(254), 255)
        self.assertEqual(SimpleMath.subtractOne_(75), 74)

    def test_protocol_def_empty(self):
        """An empty ObjCProtocol can be defined."""

        class EmptyProtocol(metaclass=ObjCProtocol):
            pass

    def test_protocol_def_methods(self):
        """An ObjCProtocol with method definitions can be defined."""

        class ProtocolWithSomeMethods(metaclass=ObjCProtocol):
            @objc_classmethod
            def class_method(self, param) -> c_int:
                pass

            @objc_method
            def instance_method(self, param) -> c_int:
                pass

        # TODO Test that the methods are actually defined

    def test_protocol_def_property(self):
        """An ObjCProtocol with a property definition can be defined."""

        class ProtocolWithAProperty(metaclass=ObjCProtocol):
            prop = objc_property()

        # TODO Test that the property is actually defined

    def test_protocol_def_extends(self):
        """An ObjCProtocol that extends other protocols can be defined."""

        ExampleProtocol = ObjCProtocol("ExampleProtocol")

        class ProtocolExtendsProtocols(NSObjectProtocol, ExampleProtocol):
            pass

        self.assertSequenceEqual(
            ProtocolExtendsProtocols.protocols, [NSObjectProtocol, ExampleProtocol]
        )

    def test_function_NSEdgeInsetsMake(self):
        """Python can invoke NSEdgeInsetsMake to create NSEdgeInsets."""

        insets = NSEdgeInsets(0.0, 1.1, 2.2, 3.3)
        other_insets = NSEdgeInsetsMake(0.0, 1.1, 2.2, 3.3)

        # structs are NOT equal
        self.assertNotEqual(insets, other_insets)

        # but their values are
        self.assertEqual(insets.top, other_insets.top)
        self.assertEqual(insets.left, other_insets.left)
        self.assertEqual(insets.bottom, other_insets.bottom)
        self.assertEqual(insets.right, other_insets.right)

    def test_objc_const(self):
        """objc_const works."""

        string_const = objc_const(rubiconharness, "SomeGlobalStringConstant")
        self.assertEqual(str(string_const), "Some global string constant")

    def test_interface_return_struct(self):
        """An ObjC protocol implementation that returns values by struct can be defined in Python."""

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
        self.assertEqual(outSize.width, 25)
        self.assertEqual(outSize.height, 90)
        self.assertTrue(results.get("size"))

        outRect = handler2.computeRect(NSMakeRect(10, 20, 30, 40))
        self.assertEqual(outRect.origin.x, 30)
        self.assertEqual(outRect.origin.y, 110)
        self.assertEqual(outRect.size.width, 50)
        self.assertEqual(outRect.size.height, 60)
        self.assertTrue(results.get("rect"))

        # Invoke a method through an interface.
        Example = ObjCClass("Example")
        obj = Example.alloc().init()

        # Test the base class directly
        thing1 = Thing.alloc().init()
        obj.thing = thing1
        outSize = obj.testThing(10)
        self.assertEqual(outSize.width, 0)
        self.assertEqual(outSize.height, 30)

        # Test the python handler
        obj.thing = handler1
        outSize = obj.testThing(15)
        self.assertEqual(outSize.width, 5)
        self.assertEqual(outSize.height, 45)

    def test_objcinstance_python_attribute(self):
        """Python attributes can be added to an ObjCInstance."""

        Thing = ObjCClass("Thing")
        thing = Thing.alloc().init()

        # Use objects that don't have an obvious Objective-C equivalent,
        # to ensure that the actual Python objects are being stored,
        # and not converted Objective-C versions.
        thing.python_object_1 = range(2, 8)
        thing.python_object_2 = type
        self.assertEqual(thing.python_object_1, range(2, 8))
        self.assertEqual(thing.python_object_2, type)

        # Test deleting Python attribute.

        del thing.python_object_1

        with self.assertRaises(AttributeError):
            thing.python_object_1

    def test_objcinstance_python_attribute_keep_alive(self):
        """Python attributes on an ObjCInstance are kept even if the object
        temporarily has no Python references."""

        Example = ObjCClass("Example")
        example = Example.alloc().init()
        Thing = ObjCClass("Thing")
        thing = Thing.alloc().init()

        # Use objects that don't have an obvious Objective-C equivalent,
        # to ensure that the actual Python objects are being stored,
        # and not converted Objective-C versions.
        python_object_1 = range(2, 8)
        python_object_2 = type

        # Remember the objects' IDs to allow checking that the objects retrieved later are identical
        # without keeping an actual reference to the objects.
        python_object_1_id = id(python_object_1)
        python_object_2_id = id(python_object_2)

        # Add our Python attributes to the Objective-C object.
        thing.python_object_1 = python_object_1
        thing.python_object_2 = python_object_2

        # Store the object in an Objective-C property.
        # This creates a reference in Objective-C, but not in Python.
        example.setThing(thing)

        # Delete all of our Python references to the ObjCInstance and the objects stored on it.
        del python_object_1
        del python_object_2
        del thing

        # Try to force Python to destroy any no longer referenced objects.
        gc.collect()

        # Get our object back from Objective-C.
        thing = example.thing

        # Check that our Python attributes are still there.
        self.assertEqual(thing.python_object_1, range(2, 8))
        self.assertEqual(thing.python_object_2, type)

        # Check that these are exactly the same objects that we stored before.
        self.assertEqual(id(thing.python_object_1), python_object_1_id)
        self.assertEqual(id(thing.python_object_2), python_object_2_id)

    def test_objcinstance_python_attribute_freed(self):
        """Python attributes on an ObjCInstance are freed after the instance is
        released."""

        with autoreleasepool():
            obj = NSObject.alloc().init()

            # Use a custom object as attribute value so that we can keep a weak reference.

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
            self.assertIs(obj.python_object, wr_python_object())

            # Make sure that all Python objects are freed.
            del obj
            gc.collect()

        self.assertIsNone(wr_python_object())

    def test_objcinstance_returned_lifecycle(self):
        """An object is retained when creating an ObjCInstance for it without implicit
        ownership. It is autoreleased when the ObjCInstance is garbage collected.
        """

        def create_object():
            with autoreleasepool():
                return NSString.stringWithString(str(uuid.uuid4()))

        assert_lifecycle(self, create_object)

    def test_objcinstance_alloc_lifecycle(self):
        """We properly retain and release objects that are allocated but never
        initialized."""

        def create_object():
            with autoreleasepool():
                return NSObject.alloc()

        assert_lifecycle(self, create_object)

    def test_objcinstance_alloc_init_lifecycle(self):
        """An object is not additionally retained when we create and initialize it
        through an alloc().init() chain. It is autoreleased when the ObjCInstance is
        garbage collected.
        """

        def create_object():
            return NSObject.alloc().init()

        assert_lifecycle(self, create_object)

    def test_objcinstance_new_lifecycle(self):
        """An object is not additionally retained when we create and initialize it with
        a new call. It is autoreleased when the ObjCInstance is garbage collected.
        """

        def create_object():
            return NSObject.new()

        assert_lifecycle(self, create_object)

    def test_objcinstance_copy_lifecycle(self):
        """An object is not additionally retained when we create and initialize it with
        a copy call. It is autoreleased when the ObjCInstance is garbage collected.
        """

        def create_object():
            obj = NSMutableArray.alloc().init()
            copy = obj.copy()

            # Check that the copy is a new object.
            self.assertIsNot(obj, copy)
            self.assertNotEqual(obj.ptr.value, copy.ptr.value)

            return copy

        assert_lifecycle(self, create_object)

    def test_objcinstance_mutable_copy_lifecycle(self):
        """An object is not additionally retained when we create and initialize it with
        a mutableCopy call. It is autoreleased when the ObjCInstance is garbage collected.
        """

        def create_object():
            obj = NSMutableArray.alloc().init()
            copy = obj.mutableCopy()

            # Check that the copy is a new object.
            self.assertIsNot(obj, copy)
            self.assertNotEqual(obj.ptr.value, copy.ptr.value)

            return copy

        assert_lifecycle(self, create_object)

    def test_objcinstance_immutable_copy_lifecycle(self):
        """If the same object is returned from multiple creation methods, it is still
        freed on Python garbage collection."""

        def create_object():
            with autoreleasepool():
                obj = NSString.stringWithString(str(uuid.uuid4()))
                copy = obj.copy()

            # Check that the copy the same object as the original.
            self.assertIs(obj, copy)
            self.assertEqual(obj.ptr.value, copy.ptr.value)

            return obj

        assert_lifecycle(self, create_object)

    def test_objcinstance_init_change_lifecycle(self):
        """We do not leak memory if init returns a different object than it
        received in alloc."""

        def create_object():
            with autoreleasepool():
                obj_allocated = NSString.alloc()
                obj_initialized = obj_allocated.initWithString(str(uuid.uuid4()))

            # Check that the initialized object is a different one than the allocated.
            self.assertIsNot(obj_allocated, obj_initialized)
            self.assertNotEqual(obj_allocated.ptr.value, obj_initialized.ptr.value)

            return obj_initialized

        assert_lifecycle(self, create_object)

    def test_objcinstance_init_none(self):
        """We do not segfault if init returns nil."""
        with autoreleasepool():
            image = NSImage.alloc().initWithContentsOfFile("/no/file/here")

        self.assertIsNone(image)

    def test_objcinstance_dealloc(self):

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

        self.assertEqual(attr0.retainCount(), 2)
        self.assertEqual(attr1.retainCount(), 1)

        # Delete the Python wrapper and ensure that the Objective-C object is
        # deallocated after ``autorelease`` on garbage collection. This will also
        # trigger a decrement in the retain count of attr0.
        with autoreleasepool():
            del obj
            gc.collect()

        self.assertTrue(DeallocTester.did_dealloc, "custom dealloc did not run")
        self.assertEqual(
            attr0.retainCount(), 1, "strong property value was not released"
        )
        self.assertEqual(attr1.retainCount(), 1, "weak property value was released")

    def test_partial_with_override(self):
        """If one method in a partial is overridden, that doesn't impact lookup of other partial targets"""
        SpecificExample = ObjCClass("SpecificExample")

        obj = SpecificExample.alloc().init()

        # The subclass implementation is invoked, not the base
        obj.method(2, withArg=3)
        self.assertEqual(obj.baseIntField, 5)

        # The base class implementation can still be found an invoked.
        obj.method(2)
        self.assertEqual(obj.baseIntField, 2)

    def test_compatible_class_name_change(self):
        """If the class name changes in a compatible way, the wrapper isn't recreated (#257)"""
        Example = ObjCClass("Example")

        pre_init = Example.alloc()

        # Call initWithClassChange(), which does an internal class name change.
        # This mirrors what happens with NSWindow, where `init()` changes the
        # class name to NSKVONotifying_NSWindow.
        post_init = pre_init.initWithClassChange()

        # Memory address hasn't changed
        assert pre_init.ptr.value == post_init.ptr.value
        # The class name hasn't changed either
        assert pre_init.objc_class.name == post_init.objc_class.name == "Example"
        # The wrapper is the same object
        assert id(pre_init) == id(post_init)

    def test_threaded_wrapper_creation(self):
        """If 2 threads try to create a wrapper for the same object, only 1 wrapper is created (#251)"""
        # Create an ObjC instance, and keep a track of the memory address
        Example = ObjCClass("Example")
        obj = Example.alloc().init()
        ptr = obj.ptr

        # The underlying problem is a race condition, so we need to try a
        # bunch of times to make it happen.
        for _ in range(0, 1000):
            # Flush the ObjC instance cache
            ObjCInstance._cached_objects = {}

            # Keep a log of the Example instances that have been created,
            # keyed by thread_id
            instances = {}

            # A worker method that will create a wrapper object from a (known
            # good) memory address, and track the wrapper object created.
            def work():
                instances[threading.get_ident()] = Example(ptr)

            # Run the work method in the main thread, and in a secondary thread;
            # wait for both to complete.
            thread = threading.Thread(target=work)
            thread.start()
            work()
            thread.join()

            # There should be 2 instances
            wrappers = list(instances.values())
            self.assertEqual(len(wrappers), 2)

            # They should be pointing at the same memory address
            self.assertEqual(wrappers[0].ptr, wrappers[1].ptr)

            # They should be the same object (i.e., one came from the cache)
            self.assertEqual(id(wrappers[0]), id(wrappers[1]))

    def test_threaded_method_cache(self):
        """If 2 threads try to access a method on the same object,
        there's no race condition populating the cache (#252)"""
        # Wrap a class with lots of methods, and create the instance
        Example = ObjCClass("Example")
        obj = Example.alloc().init()

        for _ in range(0, 1000):
            # Manually clear the method/property cache on Example.
            # This returns the attributes set in ObjCClass.__new__
            # to their initial values.
            Example.methods_ptr = None
            Example.instance_method_ptrs = {}
            Example.instance_methods = {}
            Example.instance_properties = {}
            Example.forced_properties = set()
            Example.partial_methods = {}

            # A worker method that invokes a method.
            # This will also populate the method cache.
            def work():
                try:
                    obj.mutateIntFieldWithValue(42)
                except AttributeError:
                    self.fail("method should exist; method cache is corrupt")

            # Run the work method in the main thread, and in a secondary thread;
            # wait for both to complete.
            thread = threading.Thread(target=work)
            thread.start()
            work()
            thread.join()

    def test_threaded_accessor_cache(self):
        """If 2 threads try to access an accessor on the same object,
        there's no race condition populating the cache (#252)"""
        # Wrap a class with lots of methods, and create the instance
        Example = ObjCClass("Example")
        obj = Example.alloc().init()

        for _ in range(0, 1000):
            # Manually clear the method/property cache on Example.
            # This returns the attributes set in ObjCClass.__new__
            # to their initial values.
            Example.methods_ptr = None
            Example.instance_method_ptrs = {}
            Example.instance_methods = {}
            Example.instance_properties = {}
            Example.forced_properties = set()
            Example.partial_methods = {}

            # A worker method that accesses a property
            # This will also populate the property cache.
            def work():
                try:
                    obj.intField
                except AttributeError:
                    self.fail("accessor should exist; property cache is corrupt")

            # Run the work method in the main thread, and in a secondary thread;
            # wait for both to complete.
            thread = threading.Thread(target=work)
            thread.start()
            work()
            thread.join()

    def test_threaded_mutator_cache(self):
        """If 2 threads try to access a mutator on the same object,
        there's no race condition populating the cache (#252)"""
        # Wrap a class with lots of methods, and create the instance
        Example = ObjCClass("Example")
        obj = Example.alloc().init()

        for _ in range(0, 1000):
            # Manually clear the method/property cache on Example.
            # This returns the attributes set in ObjCClass.__new__
            # to their initial values.
            Example.methods_ptr = None
            Example.instance_method_ptrs = {}
            Example.instance_methods = {}
            Example.instance_properties = {}
            Example.forced_properties = set()
            Example.partial_methods = {}

            # A worker method that mutates a property
            # This will also populate the property cache.
            def work():
                try:
                    obj.intField = 42
                except AttributeError:
                    self.fail("mutator should exist; property cache is corrupt")

            # Run the work method in the main thread, and in a secondary thread;
            # wait for both to complete.
            thread = threading.Thread(target=work)
            thread.start()
            work()
            thread.join()

    def test_get_method_family(self):
        self.assertEqual(get_method_family("mutableCopy"), "mutableCopy")
        self.assertEqual(get_method_family("mutableCopy:"), "mutableCopy")
        self.assertEqual(get_method_family("_mutableCopy:"), "mutableCopy")
        self.assertEqual(get_method_family("_mutableCopy:with:"), "mutableCopy")
        self.assertEqual(get_method_family("_mutableCopyWith:"), "mutableCopy")
        self.assertEqual(get_method_family("_mutableCopy_with:"), "mutableCopy")
        self.assertEqual(get_method_family("_mutableCopying:"), "")
