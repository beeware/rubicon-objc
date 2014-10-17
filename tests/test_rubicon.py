# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from ctypes import *
from ctypes import util

import math
# Python 2.6 compatibility shim
import unittest
if not hasattr(unittest.TestCase, 'assertIsNotNone'):
    import unittest2 as unittest

from rubicon.objc import ObjCClass, ObjCSubclass


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

        # ... but retrieving like a property is an error:
        with self.assertRaises(AttributeError):
            obj1.specialValue

        # ... and mutating like a property is an error:
        with self.assertRaises(AttributeError):
            obj1.specialValue = 37

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

    def test_string_return(self):
        "If a method or field returns a string, you get a Python string back"
        Example = ObjCClass('Example')
        example = Example.alloc().init()
        self.assertEqual(example.toString(), "This is an ObjC Example object")

    def test_float_method(self):
        "A method with a float arguments can be handled."
        Example = ObjCClass('Example')
        example = Example.alloc().init()
        self.assertEqual(example.areaOfSquare_(1.5), 2.25)

    def test_double_method(self):
        "A method with a double arguments can be handled."
        Example = ObjCClass('Example')
        example = Example.alloc().init()
        self.assertEqual(example.areaOfCircle_(1.5), 1.5 * math.pi)

    def test_object_return(self):
        "If a method or field returns an object, you get an instance of that type returned"
        Example = ObjCClass('Example')
        example = Example.alloc().init()

        Thing = ObjCClass('Thing')
        thing = Thing.alloc().initWithName_value_('This is thing', 2)

        example.thing = thing

        the_thing = example.thing
        self.assertEqual(the_thing.toString(), "This is thing 2")

    def test_interface(self):
        "An ObjC protocol implementation can be defined in Python."

        results = {}

        class Handler_impl(object):
            Handler = ObjCSubclass('NSObject', 'Handler')

            @Handler.method('@i')
            def initWithValue_(self, value):
                self.__dict__['value'] = value
                return self

            @Handler.method('v@i')
            def peek_withValue_(self, example, value):
                results['string'] = example.toString() + " peeked"
                results['int'] = value + self.__dict__['value']

            @Handler.method('v@i')
            def poke_withValue_(self, example, value):
                results['string'] = example.toString() + " poked"
                results['int'] = value + self.__dict__['value']

        Handler = ObjCClass('Handler')

        # Create two handler instances so we can check the right one
        # is being invoked.
        handler1 = Handler.alloc().initWithValue_(5)
        handler2 = Handler.alloc().initWithValue_(10)

        # Create an Example object, and register a handler with it.
        Example = ObjCClass('Example')
        example = Example.alloc().init()
        example.callback = handler2

        # Invoke the callback; check that the results have been peeked as expected
        example.testPeek_(42)

        self.assertEqual(results['string'], 'This is an ObjC Example object peeked')
        self.assertEqual(results['int'], 52)

        example.testPoke_(37)

        self.assertEqual(results['string'], 'This is an ObjC Example object poked')
        self.assertEqual(results['int'], 47)
