from __future__ import annotations

import unittest

from rubicon.objc import (
    NSArray,
    NSMutableArray,
    NSObject,
    ObjCClass,
    objc_method,
    objc_property,
    py_from_ns,
)
from rubicon.objc.collections import ObjCListInstance


class NSArrayMixinTest(unittest.TestCase):
    py_list = ["one", "two", "three"]

    def make_array(self, contents=None):
        a = NSMutableArray.alloc().init()
        if contents is not None:
            for value in contents:
                a.addObject(value)

        return NSArray.arrayWithArray(a)

    def test_getitem(self):
        a = self.make_array(self.py_list)

        for pos, value in enumerate(self.py_list):
            self.assertEqual(a[pos], value)

        with self.assertRaises(IndexError):
            a[len(self.py_list) + 10]

        with self.assertRaises(IndexError):
            a[-len(self.py_list) - 1]

    def test_len(self):
        a = self.make_array(self.py_list)

        self.assertEqual(len(a), len(self.py_list))

    def test_iter(self):
        a = self.make_array(self.py_list)

        keys = list(self.py_list)
        for k in a:
            self.assertTrue(k in keys)
            keys.remove(k)

        self.assertTrue(len(keys) == 0)

    def test_contains(self):
        a = self.make_array(self.py_list)
        for value in self.py_list:
            self.assertTrue(value in a)

    def test_index(self):
        a = self.make_array(self.py_list)
        self.assertEqual(a.index("two"), 1)
        with self.assertRaises(ValueError):
            a.index("umpteen")

    def test_count(self):
        a = self.make_array(self.py_list)
        self.assertEqual(a.count("one"), 1)

    def test_copy(self):
        a = self.make_array(self.py_list)
        b = a.copy()
        self.assertEqual(b, a)
        self.assertEqual(b, self.py_list)

        with self.assertRaises(AttributeError):
            b.append("four")

    def test_equivalence(self):
        a = self.make_array(self.py_list)
        b = self.make_array(self.py_list)

        self.assertEqual(a, self.py_list)
        self.assertEqual(b, self.py_list)
        self.assertEqual(a, b)
        self.assertEqual(self.py_list, a)
        self.assertEqual(self.py_list, b)
        self.assertEqual(b, a)

        self.assertNotEqual(a, object())
        self.assertNotEqual(a, [])
        self.assertNotEqual(a, self.py_list[:2])
        self.assertNotEqual(a, self.py_list + ["spam", "ham"])

    def test_slice_access(self):
        a = self.make_array(self.py_list * 2)
        self.assertEqual(a[1:4], ["two", "three", "one"])
        self.assertEqual(a[:-2], ["one", "two", "three", "one"])
        self.assertEqual(a[4:], ["two", "three"])
        self.assertEqual(a[1:5:2], ["two", "one"])

    def test_argument(self):
        Example = ObjCClass("Example")
        example = Example.alloc().init()

        a = self.make_array(self.py_list)
        # Call a method with an NSArray instance
        self.assertEqual(example.processArray(a), "two")
        # Call the same method with the Python list
        self.assertEqual(example.processArray(self.py_list), "two")

    def test_property(self):
        Example = ObjCClass("Example")
        example = Example.alloc().init()

        a = self.make_array(self.py_list)
        example.array = a

        self.assertEqual(example.array, self.py_list)
        self.assertIsInstance(example.array, ObjCListInstance)
        self.assertEqual(example.array[1], "two")


class NSMutableArrayMixinTest(NSArrayMixinTest):
    def make_array(self, contents=None):
        a = NSMutableArray.alloc().init()
        if contents is not None:
            for value in contents:
                a.addObject(value)

        return a

    def test_setitem(self):
        a = self.make_array(self.py_list)

        a[2] = "four"
        self.assertEqual(a[2], "four")

        with self.assertRaises(IndexError):
            a[len(a)] = "invalid"

        with self.assertRaises(IndexError):
            a[-len(a) - 1] = "invalid"

    def test_del(self):
        a = self.make_array(self.py_list)
        del a[0]
        self.assertEqual(len(a), 2)
        self.assertEqual(a[0], "two")

        with self.assertRaises(IndexError):
            del a[len(a)]

        with self.assertRaises(IndexError):
            del a[-len(a) - 1]

    def test_append(self):
        a = self.make_array()
        a.append("an item")
        self.assertTrue("an item" in a)

    def test_extend(self):
        a = self.make_array()
        a.extend(["an item", "another item"])
        self.assertTrue("an item" in a)
        self.assertTrue("another item" in a)

    def test_clear(self):
        a = self.make_array(self.py_list)
        a.clear()
        self.assertEqual(len(a), 0)

    def test_count(self):
        a = self.make_array(self.py_list)
        self.assertEqual(a.count("one"), 1)

        a.append("one")
        self.assertEqual(a.count("one"), 2)

    def test_copy(self):
        a = self.make_array(self.py_list)
        b = a.copy()
        self.assertEqual(b, a)
        self.assertEqual(b, self.py_list)

        b.append("four")

    def test_insert(self):
        a = self.make_array(self.py_list)
        a.insert(1, "four")
        self.assertEqual(a[0], "one")
        self.assertEqual(a[1], "four")
        self.assertEqual(a[2], "two")

    def test_pop(self):
        a = self.make_array(self.py_list)
        self.assertEqual(a.pop(), "three")
        self.assertEqual(a.pop(0), "one")
        self.assertEqual(len(a), 1)
        self.assertEqual(a[0], "two")

    def test_remove(self):
        a = self.make_array(self.py_list)
        a.remove("three")
        self.assertEqual(len(a), 2)
        self.assertEqual(a[-1], "two")
        with self.assertRaises(ValueError):
            a.remove("umpteen")

    def test_slice_assignment1(self):
        a = self.make_array(self.py_list * 2)
        a[2:4] = ["four", "five"]
        self.assertEqual(a, ["one", "two", "four", "five", "two", "three"])

    def test_slice_assignment2(self):
        a = self.make_array(self.py_list * 2)
        a[::2] = ["four", "five", "six"]
        self.assertEqual(a, ["four", "two", "five", "one", "six", "three"])

    def test_slice_assignment3(self):
        a = self.make_array(self.py_list * 2)
        a[2:4] = ["four"]
        self.assertEqual(a, ["one", "two", "four", "two", "three"])

    def test_bad_slice_assignment1(self):
        a = self.make_array(self.py_list * 2)

        with self.assertRaises(TypeError):
            a[2:4] = 4

    def test_bad_slice_assignment2(self):
        a = self.make_array(self.py_list * 2)

        with self.assertRaises(ValueError):
            a[::2] = [4]

    def test_del_slice1(self):
        a = self.make_array(self.py_list * 2)
        del a[-2:]
        self.assertEqual(len(a), 4)
        self.assertEqual(a[0], "one")
        self.assertEqual(a[-1], "one")

    def test_del_slice2(self):
        a = self.make_array(self.py_list * 2)
        del a[::2]
        self.assertEqual(len(a), 3)
        self.assertEqual(a[0], "two")
        self.assertEqual(a[1], "one")
        self.assertEqual(a[2], "three")

    def test_del_slice3(self):
        a = self.make_array(self.py_list * 2)
        del a[::-2]
        self.assertEqual(len(a), 3)
        self.assertEqual(a[0], "one")
        self.assertEqual(a[1], "three")
        self.assertEqual(a[2], "two")

    def test_reverse(self):
        a = self.make_array(self.py_list)
        a.reverse()

        for pos, value in enumerate(reversed(self.py_list)):
            self.assertEqual(a[pos], value)


class PythonObjectTest(unittest.TestCase):
    def test_primitive_list_attribute(self):
        class PrimitiveListAttrContainer(NSObject):
            @objc_method
            def init(self):
                self.data = [1, 2, 3]
                return self

            @objc_method
            def initWithList_(self, data):
                self.data = data
                return self

        obj1 = PrimitiveListAttrContainer.alloc().init()
        self.assertEqual(obj1.data, [1, 2, 3])
        self.assertIsInstance(obj1.data, list)

        # If it's set through a method call, it becomes an objc instance
        obj2 = PrimitiveListAttrContainer.alloc().initWithList_([4, 5, 6])
        self.assertIsInstance(obj2.data, ObjCListInstance)
        self.assertEqual(py_from_ns(obj2.data), [4, 5, 6])

        # If it's set by direct attribute access, it becomes a Python object.
        obj2.data = [7, 8, 9]
        self.assertIsInstance(obj2.data, list)
        self.assertEqual(obj2.data, [7, 8, 9])

    def test_primitive_list_property(self):
        class PrimitiveListContainer(NSObject):
            data = objc_property()

            @objc_method
            def init(self):
                self.data = [1, 2, 3]
                return self

            @objc_method
            def initWithList_(self, data):
                self.data = data
                return self

        obj1 = PrimitiveListContainer.alloc().init()
        self.assertIsInstance(obj1.data, ObjCListInstance)
        self.assertEqual(py_from_ns(obj1.data), [1, 2, 3])

        obj2 = PrimitiveListContainer.alloc().initWithList_([4, 5, 6])
        self.assertIsInstance(obj2.data, ObjCListInstance)
        self.assertEqual(py_from_ns(obj2.data), [4, 5, 6])

        obj2.data = [7, 8, 9]
        self.assertIsInstance(obj2.data, ObjCListInstance)
        self.assertEqual(py_from_ns(obj2.data), [7, 8, 9])

    def test_object_list_attribute(self):
        class ObjectListAttrContainer(NSObject):
            @objc_method
            def init(self):
                self.data = ["x1", "y2", "z3"]
                return self

            @objc_method
            def initWithList_(self, data):
                self.data = data
                return self

        obj1 = ObjectListAttrContainer.alloc().init()
        self.assertEqual(obj1.data, ["x1", "y2", "z3"])
        self.assertIsInstance(obj1.data, list)

        # If it's set through a method call, it becomes an objc instance
        obj2 = ObjectListAttrContainer.alloc().initWithList_(["a4", "b5", "c6"])
        self.assertEqual(obj2.data, ["a4", "b5", "c6"])
        self.assertIsInstance(obj2.data, ObjCListInstance)

        # If it's set by direct attribute access, it becomes a Python object.
        obj2.data = ["i7", "j8", "k9"]
        self.assertEqual(obj2.data, ["i7", "j8", "k9"])
        self.assertIsInstance(obj2.data, list)

    def test_object_list_property(self):
        class ObjectListContainer(NSObject):
            data = objc_property()

            @objc_method
            def init(self):
                self.data = ["x1", "y2", "z3"]
                return self

            @objc_method
            def initWithList_(self, data):
                self.data = data
                return self

        obj1 = ObjectListContainer.alloc().init()
        self.assertEqual(obj1.data, ["x1", "y2", "z3"])
        self.assertIsInstance(obj1.data, ObjCListInstance)

        obj2 = ObjectListContainer.alloc().initWithList_(["a4", "b5", "c6"])
        self.assertEqual(obj2.data, ["a4", "b5", "c6"])
        self.assertIsInstance(obj2.data, ObjCListInstance)

        obj2.data = ["i7", "j8", "k9"]
        self.assertEqual(obj2.data, ["i7", "j8", "k9"])
        self.assertIsInstance(obj2.data, ObjCListInstance)

    def test_multitype_list_property(self):
        class MultitypeListContainer(NSObject):
            data = objc_property()

        Example = ObjCClass("Example")
        example = Example.alloc().init()

        # All types can be stored in a list.
        obj = MultitypeListContainer.alloc().init()

        obj.data = [4, True, "Hello", example]
        self.assertIsInstance(obj.data, ObjCListInstance)
        self.assertEqual(py_from_ns(obj.data), [4, True, "Hello", example])
