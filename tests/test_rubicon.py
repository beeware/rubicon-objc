from ctypes import *
from ctypes import util
from decimal import Decimal
from enum import Enum
import math
import unittest

try:
    import platform
    OSX_VERSION = tuple(int(v) for v in platform.mac_ver()[0].split('.')[:2])
except:
    OSX_VERSION = None

from rubicon.objc import ObjCClass, objc_method, objc_classmethod, objc_property, NSEdgeInsets, NSEdgeInsetsMake


# Load the test harness library
harnesslib = util.find_library('rubiconharness')
if harnesslib is None:
    raise RuntimeError("Couldn't load Rubicon test harness library. Have you set DYLD_LIBRARY_PATH?")
cdll.LoadLibrary(harnesslib)


class RubiconTest(unittest.TestCase):
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

    def test_non_existent_class(self):
        "A Name Error is raised if a class doesn't exist."

        # If a class doesn't exist, raise NameError
        with self.assertRaises(NameError):
            ObjCClass('DoesNotExist')

        # If you try to create a class directly from a pointer, and
        # the pointer isn't valid, raise an error.
        with self.assertRaises(RuntimeError):
            ObjCClass(0)

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
        "A method with a float arguments can be handled."
        Example = ObjCClass('Example')
        example = Example.alloc().init()
        self.assertEqual(example.areaOfSquare_(1.5), 2.25)

    def test_double_method(self):
        "A method with a double arguments can be handled."
        Example = ObjCClass('Example')
        example = Example.alloc().init()
        self.assertAlmostEqual(example.areaOfCircle_(1.5), 1.5 * math.pi, 5)

    @unittest.skipIf(OSX_VERSION and OSX_VERSION < (10, 10),
                     "Property handling doesn't work on OS X 10.9 (Mavericks) and earlier")
    def test_decimal_method(self):
        "A method with a NSDecimalNumber arguments can be handled."
        Example = ObjCClass('Example')
        example = Example.alloc().init()

        result = example.areaOfTriangleWithWidth_andHeight_(Decimal('3.0'), Decimal('4.0'))
        self.assertEqual(result, Decimal('6.0'))
        self.assertTrue(isinstance(result, Decimal), 'Result should be a Decimal')

    def test_object_return(self):
        "If a method or field returns an object, you get an instance of that type returned"
        Example = ObjCClass('Example')
        example = Example.alloc().init()

        Thing = ObjCClass('Thing')
        thing = Thing.alloc().initWithName_value_('This is thing', 2)

        example.thing = thing

        the_thing = example.thing
        self.assertEqual(the_thing.toString(), "This is thing 2")

    def test_duplicate_class_registration(self):
        "If you define a class name twice in the same runtime, you get an error."

        NSObject = ObjCClass('NSObject')

        # First definition should work.
        class MyClass(NSObject):
            pass

        # Second definition will raise an error.
        # Without protection, this is a segfault.
        with self.assertRaises(RuntimeError):
            class MyClass(NSObject):
                pass

    def test_interface(self):
        "An ObjC protocol implementation can be defined in Python."

        results = {}

        NSObject = ObjCClass('NSObject')

        class Handler(NSObject):
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

    def test_class_properties(self):
        "A Python class can have ObjC properties with synthezied getters and setters."

        NSObject = ObjCClass('NSObject')
        NSURL = ObjCClass('NSURL')

        class URLBox(NSObject):

            # takes no type: All properties are pointers
            url = objc_property()

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

    def test_NSArray_iterable(self):
        "Pythonic interface for NSArray (and its subclasses) as iterable."

        NSMutableArray = ObjCClass('NSMutableArray')

        ns_array = NSMutableArray.array()
        test_list = ['item1', 'item2', 'item3', 'item4', 'item5']
        for item in test_list:
            ns_array.addObject_(item)

        # Todo: implement len
        self.assertEqual(ns_array.count, 5)

        # NSArray itself can be compared to other NSArrays
        # NSArray can be copied via copy-slice [:]
        self.assertEqual(ns_array[:], ns_array)

        # Needed because an NSArray does NOT equal a Python list. Their elements can, however, be equal.
        def compare(some_NSArray, python_list):
            self.assertEqual([item for item in some_NSArray], python_list)

        # Object retrieval via index
        self.assertEqual(ns_array[3], test_list[3])

        # positive indices
        compare(ns_array[1:], test_list[1:])
        compare(ns_array[2:3], test_list[2:3])
        compare(ns_array[4:2], test_list[4:2])
        compare(ns_array[:4], test_list[:4])

        # negative indices
        compare(ns_array[-1:], test_list[-1:])
        compare(ns_array[-2:-3], test_list[-2:-3])
        compare(ns_array[-4:-2], test_list[-4:-2])
        compare(ns_array[:-4], test_list[:-4])

        # positive indices with step 2
        compare(ns_array[1::2], test_list[1::2])
        compare(ns_array[2:3:2], test_list[2:3:2])
        compare(ns_array[4:2:2], test_list[4:2:2])
        compare(ns_array[:4:2], test_list[:4:2])

        # negative indices with step 2
        compare(ns_array[-1::2], test_list[-1::2])
        compare(ns_array[-2:-3:2], test_list[-2:-3:2])
        compare(ns_array[-4:-2:2], test_list[-4:-2:2])
        compare(ns_array[:-4:2], test_list[:-4:2])

        # positive indices with step -3
        compare(ns_array[1::-3], test_list[1::-3])
        compare(ns_array[2:3:-3], test_list[2:3:-3])
        compare(ns_array[4:2:-3], test_list[4:2:-3])
        compare(ns_array[:4:-3], test_list[:4:-3])

        # negative indices with step -3
        compare(ns_array[-1::-3], test_list[-1::-3])
        compare(ns_array[-2:-3:-3], test_list[-2:-3:-3])
        compare(ns_array[-4:-2:-3], test_list[-4:-2:-3])
        compare(ns_array[:-4:-3], test_list[:-4:-3])

        # test string representation
        self.assertEqual(repr(ns_array), 'NSArray ' + repr(test_list))

