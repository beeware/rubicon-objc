import faulthandler
import functools
import math
import unittest
from ctypes import (
    CDLL, Structure, byref, c_char, c_double, c_float, c_int, c_void_p, cast,
    create_string_buffer, util,
)
from decimal import Decimal
from enum import Enum

from rubicon.objc import (
    SEL, NSEdgeInsets, NSEdgeInsetsMake, NSMakeRect, NSObject,
    NSObjectProtocol, NSRange, NSRect, NSSize, NSUInteger, ObjCClass,
    ObjCInstance, ObjCMetaClass, ObjCProtocol, core_foundation,
    objc_classmethod, objc_const, objc_method, objc_property, send_message,
    send_super, types,
)
from rubicon.objc.runtime import ObjCBoundMethod, libobjc

try:
    import platform
    OSX_VERSION = tuple(int(v) for v in platform.mac_ver()[0].split('.')[:2])
except Exception:
    OSX_VERSION = None


# Load the test harness library
rubiconharness_name = util.find_library('rubiconharness')
if rubiconharness_name is None:
    raise RuntimeError("Couldn't load Rubicon test harness library. Have you set DYLD_LIBRARY_PATH?")
rubiconharness = CDLL(rubiconharness_name)

faulthandler.enable()


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
            ObjCClass('DoesNotExist')

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
            ObjCMetaClass('DoesNotExist')

    def test_metametaclass(self):
        """The class of a metaclass can be looked up."""

        ExampleMeta = ObjCMetaClass("Example")
        ExampleMetaMeta = ExampleMeta.objc_class

        self.assertIsInstance(ExampleMetaMeta, ObjCMetaClass)
        self.assertEqual(ExampleMetaMeta, NSObject.objc_class)

    def test_protocol_by_name(self):
        """An Objective-C protocol can be looked up by name."""

        ExampleProtocol = ObjCProtocol('ExampleProtocol')
        self.assertEqual(ExampleProtocol.name, 'ExampleProtocol')

    def test_protocol_caching(self):
        """ObjCProtocol instances are cached."""

        ExampleProtocol1 = ObjCProtocol('ExampleProtocol')
        ExampleProtocol2 = ObjCProtocol('ExampleProtocol')

        self.assertIs(ExampleProtocol1, ExampleProtocol2)

    def test_protocol_by_pointer(self):
        """An Objective-C protocol can be created from a pointer."""

        example_protocol_ptr = libobjc.objc_getProtocol(b'ExampleProtocol')
        ExampleProtocol = ObjCProtocol(example_protocol_ptr)
        self.assertEqual(ExampleProtocol, ObjCProtocol('ExampleProtocol'))

    def test_nonexistant_protocol(self):
        """A NameError is raised if a protocol doesn't exist."""

        with self.assertRaises(NameError):
            ObjCProtocol('DoesNotExist')

    def test_objcinstance_can_produce_objcclass(self):
        """Creating an ObjCInstance for a class pointer gives an ObjCClass."""

        example_ptr = libobjc.objc_getClass(b"Example")
        Example = ObjCInstance(example_ptr)
        self.assertEqual(Example, ObjCClass("Example"))
        self.assertIsInstance(Example, ObjCClass)

    def test_objcinstance_can_produce_objcmetaclass(self):
        """Creating an ObjCInstance for a metaclass pointer gives an ObjCMetaClass."""

        examplemeta_ptr = libobjc.objc_getMetaClass(b"Example")
        ExampleMeta = ObjCInstance(examplemeta_ptr)
        self.assertEqual(ExampleMeta, ObjCMetaClass("Example"))
        self.assertIsInstance(ExampleMeta, ObjCMetaClass)

    def test_objcclass_can_produce_objcmetaclass(self):
        """Creating an ObjCClass for a metaclass pointer gives an ObjCMetaclass."""

        examplemeta_ptr = libobjc.objc_getMetaClass(b"Example")
        ExampleMeta = ObjCClass(examplemeta_ptr)
        self.assertEqual(ExampleMeta, ObjCMetaClass("Example"))
        self.assertIsInstance(ExampleMeta, ObjCMetaClass)

    def test_objcinstance_can_produce_objcprotocol(self):
        """Creating an ObjCInstance for a protocol pointer gives an ObjCProtocol."""

        example_protocol_ptr = libobjc.objc_getProtocol(b'ExampleProtocol')
        ExampleProtocol = ObjCInstance(example_protocol_ptr)
        self.assertEqual(ExampleProtocol, ObjCProtocol('ExampleProtocol'))
        self.assertIsInstance(ExampleProtocol, ObjCProtocol)

    def test_objcclass_requires_class(self):
        """ObjCClass only accepts class pointers."""

        random_obj = NSObject.alloc().init()
        with self.assertRaises(ValueError):
            ObjCClass(random_obj.ptr)
        random_obj.release()

    def test_objcmetaclass_requires_metaclass(self):
        """ObjCMetaClass only accepts metaclass pointers."""

        random_obj = NSObject.alloc().init()
        with self.assertRaises(ValueError):
            ObjCMetaClass(random_obj.ptr)
        random_obj.release()

        with self.assertRaises(ValueError):
            ObjCMetaClass(NSObject.ptr)

    def test_objcprotocol_requires_protocol(self):
        """ObjCProtocol only accepts protocol pointers."""

        random_obj = NSObject.alloc().init()
        with self.assertRaises(ValueError):
            ObjCProtocol(random_obj.ptr)
        random_obj.release()

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

        BaseExample = ObjCClass('BaseExample')
        ExampleProtocol = ObjCProtocol('ExampleProtocol')
        DerivedProtocol = ObjCProtocol('DerivedProtocol')

        self.assertEqual(BaseExample.protocols, (ExampleProtocol, DerivedProtocol))

    def test_objcprotocol_protocols(self):
        """An ObjCProtocol's protocols can be looked up."""

        DerivedProtocol = ObjCProtocol('DerivedProtocol')
        BaseProtocolOne = ObjCProtocol('BaseProtocolOne')
        BaseProtocolTwo = ObjCProtocol('BaseProtocolTwo')

        self.assertEqual(DerivedProtocol.protocols, (BaseProtocolOne, BaseProtocolTwo))

    def test_objcclass_instancecheck(self):
        """isinstance works with an ObjCClass as the second argument."""

        NSArray = ObjCClass('NSArray')
        NSString = ObjCClass('NSString')

        self.assertIsInstance(NSObject.new(), NSObject)
        self.assertIsInstance(core_foundation.at(''), NSString)
        self.assertIsInstance(core_foundation.at(''), NSObject)
        self.assertIsInstance(NSObject, NSObject)
        self.assertIsInstance(NSObject, NSObject.objc_class)

        self.assertNotIsInstance(object(), NSObject)
        self.assertNotIsInstance(NSObject.new(), NSString)
        self.assertNotIsInstance(NSArray.array, NSString)

    def test_objcclass_subclasscheck(self):
        """issubclass works with an ObjCClass as the second argument."""

        NSArray = ObjCClass('NSArray')
        NSString = ObjCClass('NSString')

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

        NSCoding = ObjCProtocol('NSCoding')
        NSSecureCoding = ObjCProtocol('NSSecureCoding')

        self.assertIsInstance(core_foundation.at(''), NSSecureCoding)
        self.assertIsInstance(core_foundation.at(''), NSCoding)

        self.assertNotIsInstance(object(), NSSecureCoding)
        self.assertNotIsInstance(NSObject.new(), NSSecureCoding)

    def test_objcprotocol_subclasscheck(self):
        """issubclass works with an ObjCProtocol as the second argument."""

        NSString = ObjCClass('NSString')
        NSCopying = ObjCProtocol('NSCopying')
        NSCoding = ObjCProtocol('NSCoding')
        NSSecureCoding = ObjCProtocol('NSSecureCoding')

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
        "A field on an instance can be accessed and mutated"

        Example = ObjCClass('Example')

        obj = Example.alloc().init()

        self.assertEqual(obj.baseIntField, 22)
        self.assertEqual(obj.intField, 33)

        obj.baseIntField = 8888
        obj.intField = 9999

        self.assertEqual(obj.baseIntField, 8888)
        self.assertEqual(obj.intField, 9999)

    def test_method(self):
        "An instance method can be invoked."
        Example = ObjCClass('Example')

        obj = Example.alloc().init()

        self.assertEqual(obj.accessBaseIntField(), 22)
        self.assertEqual(obj.accessIntField(), 33)

        obj.mutateBaseIntFieldWithValue_(8888)
        obj.mutateIntFieldWithValue_(9999)

        self.assertEqual(obj.accessBaseIntField(), 8888)
        self.assertEqual(obj.accessIntField(), 9999)

    def test_method_send(self):
        "An instance method can be invoked with send_message."
        Example = ObjCClass('Example')

        obj = Example.alloc().init()

        self.assertEqual(send_message(obj, "accessBaseIntField", restype=c_int), 22)
        self.assertEqual(send_message(obj, "accessIntField", restype=c_int), 33)

        send_message(obj, "mutateBaseIntFieldWithValue:", 8888, restype=None, argtypes=[c_int])
        send_message(obj, "mutateIntFieldWithValue:", 9999, restype=None, argtypes=[c_int])

        self.assertEqual(send_message(obj, "accessBaseIntField", restype=c_int), 8888)
        self.assertEqual(send_message(obj, "accessIntField", restype=c_int), 9999)

    def test_static_field(self):
        "A static field on a class can be accessed and mutated"
        Example = ObjCClass('Example')

        Example.mutateStaticBaseIntFieldWithValue_(1)
        Example.mutateStaticIntFieldWithValue_(11)

        self.assertEqual(Example.staticBaseIntField, 1)
        self.assertEqual(Example.staticIntField, 11)

        Example.staticBaseIntField = 1188
        Example.staticIntField = 1199

        self.assertEqual(Example.staticBaseIntField, 1188)
        self.assertEqual(Example.staticIntField, 1199)

    def test_static_method(self):
        "A static method on a class can be invoked."
        Example = ObjCClass('Example')

        Example.mutateStaticBaseIntFieldWithValue_(2288)
        Example.mutateStaticIntFieldWithValue_(2299)

        self.assertEqual(Example.accessStaticBaseIntField(), 2288)
        self.assertEqual(Example.accessStaticIntField(), 2299)

    def test_mutator_like_method(self):
        "A method that looks like a mutator doesn't confuse issues."
        Example = ObjCClass('Example')

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
        "An instance or property method can be explicitly declared as a property."
        Example = ObjCClass('Example')
        Example.declare_class_property('classMethod')
        Example.declare_class_property('classAmbiguous')
        Example.declare_property('instanceMethod')
        Example.declare_property('instanceAmbiguous')

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
        NSBundle = ObjCClass('NSBundle')
        NSBundle.declare_class_property('mainBundle')
        self.assertFalse(type(NSBundle.mainBundle) == ObjCBoundMethod, 'NSBundle.mainBundle should not be a method')

    def test_non_existent_field(self):
        "An attribute error is raised if you invoke a non-existent field."
        Example = ObjCClass('Example')

        obj1 = Example.alloc().init()

        # Non-existent fields raise an error.
        with self.assertRaises(AttributeError):
            obj1.field_doesnt_exist

        # Cache warming doesn't affect anything.
        with self.assertRaises(AttributeError):
            obj1.field_doesnt_exist

    def test_non_existent_method(self):
        "An attribute error is raised if you invoke a non-existent method."
        Example = ObjCClass('Example')

        obj1 = Example.alloc().init()

        # Non-existent methods raise an error.
        with self.assertRaises(AttributeError):
            obj1.method_doesnt_exist()

        # Cache warming doesn't affect anything.
        with self.assertRaises(AttributeError):
            obj1.method_doesnt_exist()

    def test_non_existent_static_field(self):
        "An attribute error is raised if you invoke a non-existent static field."
        Example = ObjCClass('Example')

        # Non-existent fields raise an error.
        with self.assertRaises(AttributeError):
            Example.static_field_doesnt_exist

        # Cache warming doesn't affect anything.
        with self.assertRaises(AttributeError):
            Example.static_field_doesnt_exist

    def test_non_existent_static_method(self):
        "An attribute error is raised if you invoke a non-existent static method."
        Example = ObjCClass('Example')

        # Non-existent methods raise an error.
        with self.assertRaises(AttributeError):
            Example.static_method_doesnt_exist()

        # Cache warming doesn't affect anything.
        with self.assertRaises(AttributeError):
            Example.static_method_doesnt_exist()

    def test_polymorphic_constructor(self):
        "Check that the right constructor is activated based on arguments used"
        Example = ObjCClass('Example')

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
        "An instance field/method cannot be accessed from the static context"
        Example = ObjCClass('Example')

        obj = Example.alloc().init()

        with self.assertRaises(AttributeError):
            obj.staticIntField

        with self.assertRaises(AttributeError):
            obj.get_staticIntField()

    def test_non_static_access_static(self):
        "A static field/method cannot be accessed from an instance context"
        Example = ObjCClass('Example')

        with self.assertRaises(AttributeError):
            Example.intField

        with self.assertRaises(AttributeError):
            Example.accessIntField()

    def test_string_argument(self):
        "A method with a string argument can be passed."
        Example = ObjCClass('Example')
        example = Example.alloc().init()
        self.assertEqual(example.duplicateString_("Wagga"), "WaggaWagga")

    def test_enum_argument(self):
        "An enumerated type can be used as an argument."
        Example = ObjCClass('Example')

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
        "If a method or field returns a string, you get a Python string back"
        Example = ObjCClass('Example')
        example = Example.alloc().init()
        self.assertEqual(example.toString(), "This is an ObjC Example object")

    def test_constant_string_return(self):
        "If a method or field returns a *constant* string, you get a Python string back"
        Example = ObjCClass('Example')
        example = Example.alloc().init()
        self.assertEqual(example.smiley(), "%-)")

    def test_number_return(self):
        "If a method or field returns a NSNumber, it is converted back to native types"
        Example = ObjCClass('Example')
        example = Example.alloc().init()

        self.assertEqual(example.theAnswer(), 42)
        self.assertAlmostEqual(example.twopi(), 2.0 * math.pi, 5)

    def test_float_method(self):
        "A method with a float argument can be handled."
        Example = ObjCClass('Example')
        example = Example.alloc().init()
        self.assertEqual(example.areaOfSquare_(1.5), 2.25)

    def test_float_method_send(self):
        "A method with a float argument can be handled by send_message."
        Example = ObjCClass('Example')
        example = Example.alloc().init()
        self.assertEqual(send_message(example, "areaOfSquare:", 1.5, restype=c_float, argtypes=[c_float]), 2.25)

    def test_double_method(self):
        "A method with a double argument can be handled."
        Example = ObjCClass('Example')
        example = Example.alloc().init()
        self.assertAlmostEqual(example.areaOfCircle_(1.5), 1.5 * math.pi, 5)

    def test_double_method_send(self):
        "A method with a double argument can be handled by send_message."
        Example = ObjCClass('Example')
        example = Example.alloc().init()
        self.assertAlmostEqual(
            send_message(
                example, "areaOfCircle:", 1.5,
                restype=c_double,
                argtypes=[c_double]
            ),
            1.5 * math.pi, 5
        )

    @unittest.skipIf(OSX_VERSION and OSX_VERSION < (10, 10),
                     "Property handling doesn't work on OS X 10.9 (Mavericks) and earlier")
    def test_decimal_method(self):
        "A method with a NSDecimalNumber arguments can be handled."
        Example = ObjCClass('Example')
        example = Example.alloc().init()

        result = example.areaOfTriangleWithWidth_andHeight_(Decimal('3.0'), Decimal('4.0'))
        self.assertEqual(result, Decimal('6.0'))
        self.assertIsInstance(result, Decimal, 'Result should be a Decimal')

    def test_auto_struct_creation(self):
        "Structs from method signatures are created automatically."
        Example = ObjCClass('Example')

        types.unregister_encoding_all(b'{simple=ii}')
        types.unregister_encoding_all(b'{simple}')
        types.unregister_encoding_all(b'{complex=[4s]^?{simple=ii}^{complex}b8b16b8}')
        types.unregister_encoding_all(b'{complex}')

        # Look up the method, so the return/argument types are decoded and the structs are registered.
        Example.doStuffWithStruct_

        struct_simple = types.ctype_for_encoding(b'{simple=ii}')
        self.assertEqual(struct_simple, types.ctype_for_encoding(b'{simple}'))

        simple = struct_simple(123, 456)
        ret = Example.doStuffWithStruct_(simple)
        struct_complex = types.ctype_for_encoding(b'{complex=[4s]^?{simple=ii}^{complex}b8b16b8}')
        self.assertIsInstance(ret, struct_complex)
        self.assertEqual(struct_complex, types.ctype_for_encoding(b'{complex}'))
        self.assertEqual(list(ret.field_0), [1, 2, 3, 4])
        self.assertEqual(ret.field_1.value, None)
        self.assertEqual(ret.field_2.field_0, 123)
        self.assertEqual(ret.field_2.field_1, 456)
        self.assertEqual(cast(ret.field_3, c_void_p).value, None)
        self.assertEqual(ret.field_4, 0)
        self.assertEqual(ret.field_5, 1)
        self.assertEqual(ret.field_6, 2)

    def test_sequence_arg_to_struct(self):
        "Sequence arguments are converted to structures."
        Example = ObjCClass('Example')

        ret = Example.extractSimpleStruct(([9, 8, 7, 6], None, (987, 654), None, 0, 0, 0))
        struct_simple = types.ctype_for_encoding(b'{simple=ii}')
        self.assertIsInstance(ret, struct_simple)
        self.assertEqual(ret.field_0, 987)
        self.assertEqual(ret.field_1, 654)

    def test_struct_return(self):
        "Methods returning structs of different sizes by value can be handled."
        Example = ObjCClass('Example')
        example = Example.alloc().init()

        class struct_int_sized(Structure):
            _fields_ = [("x", c_char * 4)]
        types.register_encoding(b'{int_sized=[4c]}', struct_int_sized)

        self.assertEqual(example.intSizedStruct().x, b"abc")

        class struct_oddly_sized(Structure):
            _fields_ = [("x", c_char * 5)]

        types.register_encoding(b'{oddly_sized=[5c]}', struct_oddly_sized)
        self.assertEqual(example.oddlySizedStruct().x, b"abcd")

        class struct_large(Structure):
            _fields_ = [("x", c_char * 17)]

        types.register_encoding(b'{large=[17c]}', struct_large)
        self.assertEqual(example.largeStruct().x, b"abcdefghijklmnop")

    def test_struct_return_send(self):
        "Methods returning structs of different sizes by value can be handled when using send_message."
        Example = ObjCClass('Example')
        example = Example.alloc().init()

        class struct_int_sized(Structure):
            _fields_ = [("x", c_char * 4)]

        self.assertEqual(send_message(example, "intSizedStruct", restype=struct_int_sized).x, b"abc")

        class struct_oddly_sized(Structure):
            _fields_ = [("x", c_char * 5)]

        self.assertEqual(send_message(example, "oddlySizedStruct", restype=struct_oddly_sized).x, b"abcd")

        class struct_large(Structure):
            _fields_ = [("x", c_char * 17)]

        self.assertEqual(send_message(example, "largeStruct", restype=struct_large).x, b"abcdefghijklmnop")

    def test_object_return(self):
        "If a method or field returns an object, you get an instance of that type returned"
        Example = ObjCClass('Example')
        example = Example.alloc().init()

        Thing = ObjCClass('Thing')
        thing = Thing.alloc().initWithName_value_('This is thing', 2)

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
        self.assertEqual(Example.overloaded(12, extraArg=34), 12+34)

    def test_partial_method_lots_of_args(self):
        pystring = "Uñîçö∂€"
        pybytestring = pystring.encode("utf-8")
        nsstring = core_foundation.at(pystring)
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

    def test_duplicate_class_registration(self):
        "If you define a class name twice in the same runtime, you get an error."

        # First definition should work.
        class MyClass(NSObject):
            pass

        # Second definition will raise an error.
        # Without protection, this is a segfault.
        with self.assertRaises(RuntimeError):
            class MyClass(NSObject):  # noqa: F811
                pass

    def test_interface(self):
        "An ObjC protocol implementation can be defined in Python."

        Callback = ObjCProtocol('Callback')
        results = {}

        class Handler(NSObject, protocols=[Callback]):
            @objc_method
            def initWithValue_(self, value: int):
                self.value = value
                return self

            @objc_method
            def peek_withValue_(self, example, value: int) -> None:
                results['string'] = example.toString() + " peeked"
                results['int'] = value + self.value

            @objc_method
            def poke_withValue_(self, example, value: int) -> None:
                results['string'] = example.toString() + " poked"
                results['int'] = value + self.value

            @objc_method
            def reverse_(self, input):
                return ''.join(reversed(input))

            @objc_method
            def message(self):
                return "Alea iacta est."

            @objc_classmethod
            def fiddle_(cls, value: int) -> None:
                results['string'] = "Fiddled with it"
                results['int'] = value

        # Check that the protocol is adopted.
        self.assertSequenceEqual(Handler.protocols, (Callback,))

        # Create two handler instances so we can check the right one
        # is being invoked.
        handler1 = Handler.alloc().initWithValue_(5)
        handler2 = Handler.alloc().initWithValue_(10)

        # Create an Example object, and register a handler with it.
        Example = ObjCClass('Example')
        example = Example.alloc().init()
        example.callback = handler2

        # Check some Python-side attributes
        self.assertEqual(handler1.value, 5)
        self.assertEqual(handler2.value, 10)

        # Invoke the callback; check that the results have been peeked as expected
        example.testPeek_(42)

        self.assertEqual(results['string'], 'This is an ObjC Example object peeked')
        self.assertEqual(results['int'], 52)

        example.testPoke_(37)

        self.assertEqual(results['string'], 'This is an ObjC Example object poked')
        self.assertEqual(results['int'], 47)

        self.assertEqual(example.getMessage(), 'Alea iacta est.')

        self.assertEqual(example.reverseIt_('Alea iacta est.'), '.tse atcai aelA')

        Handler.fiddle_(99)

        self.assertEqual(results['string'], 'Fiddled with it')
        self.assertEqual(results['int'], 99)

    def test_no_duplicate_protocols(self):
        """An Objective-C class cannot adopt a protocol more than once."""

        with self.assertRaises(ValueError):
            class DuplicateProtocol(NSObject, protocols=[NSObjectProtocol, NSObjectProtocol]):
                pass

    def test_class_properties(self):
        "A Python class can have ObjC properties with synthesized getters and setters."

        NSURL = ObjCClass('NSURL')

        class URLBox(NSObject):

            # takes no type: All properties are pointers
            url = objc_property()
            data = objc_property()

            @objc_method
            def getSchemeIfPresent(self):
                if self.url is not None:
                    return self.url.scheme
                return None

        box = URLBox.alloc().init()

        # Default property value is None
        self.assertIsNone(box.url)

        # Assign an object via synthesized property setter and call method that uses synthesized property getter
        url = NSURL.alloc().initWithString_('https://www.google.com')
        box.url = url
        self.assertEqual(box.getSchemeIfPresent(), 'https')

        # Assign None to dealloc property and see if method returns expected None
        box.url = None
        self.assertIsNone(box.getSchemeIfPresent())

        # Try composing URLs using constructors
        base = NSURL.URLWithString('https://pybee.org')
        full = NSURL.URLWithString('contributing/', relativeToURL=base)

        self.assertEqual(
            "Visit %s for details" % full.absoluteURL,
            "Visit https://pybee.org/contributing/ for details"
        )

        # ObjC type conversions are performed on property assignment.
        box.data = "Jabberwock"
        self.assertEqual(box.data, "Jabberwock")

        Example = ObjCClass('Example')
        example = Example.alloc().init()
        box.data = example
        self.assertEqual(box.data, example)

        box.data = None
        self.assertIsNone(box.data)

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

        ExampleProtocol = ObjCProtocol('ExampleProtocol')

        class ProtocolExtendsProtocols(NSObjectProtocol, ExampleProtocol):
            pass

        self.assertSequenceEqual(ProtocolExtendsProtocols.protocols, [NSObjectProtocol, ExampleProtocol])

    def test_function_NSEdgeInsetsMake(self):
        "Python can invoke NSEdgeInsetsMake to create NSEdgeInsets."

        insets = NSEdgeInsets(0.0, 1.1, 2.2, 3.3)
        other_insets = NSEdgeInsetsMake(0.0, 1.1, 2.2, 3.3)

        # structs are NOT equal
        self.assertNotEqual(insets, other_insets)

        # but their values are
        self.assertEqual(insets.top, other_insets.top)
        self.assertEqual(insets.left, other_insets.left)
        self.assertEqual(insets.bottom, other_insets.bottom)
        self.assertEqual(insets.right, other_insets.right)

    def test_cfstring_to_str(self):
        "CFString/NSString instances can be converted to Python str."

        self.assertEqual(str(core_foundation.at("abcdef")), "abcdef")

    def test_objc_const(self):
        "objc_const works."

        string_const = objc_const(rubiconharness, "SomeGlobalStringConstant")
        self.assertEqual(str(string_const), "Some global string constant")

    def test_interface_return_struct(self):
        "An ObjC protocol implementation that returns values by struct can be defined in Python."

        results = {}
        Thing = ObjCClass("Thing")

        class StructReturnHandler(Thing):
            @objc_method
            def initWithValue_(self, value):
                self.value = value
                return self

            @objc_method
            def computeSize_(self, input: NSSize) -> NSSize:
                results['size'] = True
                sup = send_super(self, 'computeSize:', input, restype=NSSize, argtypes=[NSSize])
                return NSSize(input.width + self.value, sup.height)

            @objc_method
            def computeRect_(self, input: NSRect) -> NSRect:
                results['rect'] = True
                sup = send_super(self, 'computeRect:', input, restype=NSRect, argtypes=[NSRect])
                return NSMakeRect(
                    input.origin.y + self.value, sup.origin.x,
                    input.size.height + self.value, sup.size.width
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
        self.assertTrue(results.get('size'))

        outRect = handler2.computeRect(NSMakeRect(10, 20, 30, 40))
        self.assertEqual(outRect.origin.x, 30)
        self.assertEqual(outRect.origin.y, 110)
        self.assertEqual(outRect.size.width, 50)
        self.assertEqual(outRect.size.height, 60)
        self.assertTrue(results.get('rect'))

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
