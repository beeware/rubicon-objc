from __future__ import annotations

import unittest

from rubicon.objc import (
    NSDictionary,
    NSMutableDictionary,
    NSObject,
    ObjCClass,
    objc_method,
    objc_property,
)
from rubicon.objc.collections import ObjCDictInstance


class NSDictionaryMixinTest(unittest.TestCase):
    py_dict = {
        "one": "ONE",
        "two": "TWO",
        "three": "THREE",
    }

    def make_dictionary(self, contents=None):
        d = NSMutableDictionary.alloc().init()
        if contents is not None:
            for key, value in contents.items():
                d.setObject_forKey_(value, key)

        return NSDictionary.dictionaryWithDictionary(d)

    def test_getitem(self):
        d = self.make_dictionary(self.py_dict)

        for key, value in self.py_dict.items():
            self.assertEqual(d[key], value)

        with self.assertRaises(KeyError):
            d["NO SUCH KEY"]

    def test_iter(self):
        d = self.make_dictionary(self.py_dict)

        keys = set(self.py_dict)
        for k in d:
            keys.remove(str(k))

        self.assertTrue(len(keys) == 0)

    def test_len(self):
        d = self.make_dictionary(self.py_dict)
        self.assertEqual(len(d), len(self.py_dict))

    def test_get(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d.get("one"), "ONE")
        self.assertEqual(d.get("two", None), "TWO")
        self.assertEqual(d.get("four", None), None)
        self.assertEqual(d.get("five", 5), 5)
        self.assertEqual(d.get("six", None), None)

    def test_contains(self):
        d = self.make_dictionary(self.py_dict)
        for key in self.py_dict:
            self.assertTrue(key in d)

    def test_copy(self):
        d = self.make_dictionary(self.py_dict)
        e = d.copy()
        self.assertEqual(e, d)
        self.assertEqual(e, self.py_dict)

    def test_equivalence(self):
        d1 = self.make_dictionary(self.py_dict)
        d2 = self.make_dictionary(self.py_dict)
        smaller_py_dict = self.py_dict.copy()
        del smaller_py_dict["three"]
        bigger_py_dict = {"four": "FOUR"}
        bigger_py_dict.update(self.py_dict)

        self.assertEqual(d1, self.py_dict)
        self.assertEqual(d2, self.py_dict)
        self.assertEqual(d1, d2)
        self.assertEqual(self.py_dict, d1)
        self.assertEqual(self.py_dict, d2)
        self.assertEqual(d2, d1)

        self.assertNotEqual(d1, object())
        self.assertNotEqual(d1, {})
        self.assertNotEqual(d1, smaller_py_dict)
        self.assertNotEqual(d1, bigger_py_dict)

    def test_keys(self):
        a = self.make_dictionary(self.py_dict)
        for k1, k2 in zip(sorted(a.keys()), sorted(self.py_dict.keys())):
            self.assertEqual(k1, k2)

    def test_values(self):
        a = self.make_dictionary(self.py_dict)
        for v1, v2 in zip(sorted(a.values()), sorted(self.py_dict.values())):
            self.assertEqual(v1, v2)

    def test_items(self):
        d = self.make_dictionary(self.py_dict)
        for i1, i2 in zip(sorted(d.items()), sorted(self.py_dict.items())):
            self.assertEqual(i1[0], i2[0])
            self.assertEqual(i1[1], i2[1])

    def test_argument(self):
        Example = ObjCClass("Example")
        example = Example.alloc().init()

        d = self.make_dictionary(self.py_dict)
        # Call a method with an NSDictionary instance
        self.assertIsNone(example.processDictionary(d))
        # Call the same method with the raw Python dictionary
        self.assertIsNone(example.processDictionary(self.py_dict))

        raw = {"data": "stuff", "other": "gadgets"}
        d = self.make_dictionary(raw)
        # Call a method with an NSDictionary instance
        self.assertEqual(example.processDictionary(d), "stuff")
        # Call the same method with the raw Python dictionary
        self.assertEqual(example.processDictionary(raw), "stuff")

    def test_property(self):
        Example = ObjCClass("Example")
        example = Example.alloc().init()

        d = self.make_dictionary(self.py_dict)
        example.dict = d

        self.assertEqual(example.dict, self.py_dict)
        self.assertIsInstance(example.dict, ObjCDictInstance)
        self.assertEqual(example.dict["one"], "ONE")


class NSMutableDictionaryMixinTest(NSDictionaryMixinTest):
    def make_dictionary(self, contents=None):
        d = NSMutableDictionary.alloc().init()
        if contents is not None:
            for key, value in contents.items():
                d.setObject_forKey_(value, key)

        return d

    def test_setitem(self):
        d = self.make_dictionary()
        for key, value in self.py_dict.items():
            d[key] = value

        for key, value in self.py_dict.items():
            self.assertEqual(d[key], value)

    def test_del(self):
        d = self.make_dictionary(self.py_dict)
        del d["one"]
        self.assertEqual(len(d), 2)
        with self.assertRaises(KeyError):
            d["one"]

    def test_clear(self):
        d = self.make_dictionary(self.py_dict)
        d.clear()
        self.assertEqual(len(d), 0)

    def test_copy(self):
        d = self.make_dictionary(self.py_dict)
        e = d.copy()
        self.assertEqual(e, d)
        self.assertEqual(e, self.py_dict)

        e["four"] = "FOUR"

    def test_pop1(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d.pop("one"), "ONE")
        self.assertEqual(len(d), 2)
        with self.assertRaises(KeyError):
            d["one"]

    def test_pop2(self):
        d = self.make_dictionary(self.py_dict)

        with self.assertRaises(KeyError):
            d.pop("four")

    def test_pop3(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d.pop("four", 4), 4)

    def test_popitem(self):
        d = self.make_dictionary(self.py_dict)

        keys = set(self.py_dict)

        while len(d) > 0:
            key, value = d.popitem()
            self.assertTrue(str(key) in keys)
            self.assertEqual(value, self.py_dict[str(key)])
            self.assertTrue(key not in d)

        with self.assertRaises(KeyError):
            d.popitem()

    def test_setdefault1(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d.setdefault("one", "default"), "ONE")
        self.assertEqual(len(d), len(self.py_dict))

    def test_setdefault2(self):
        d = self.make_dictionary(self.py_dict)

        self.assertTrue("four" not in d)
        self.assertEqual(d.setdefault("four", "FOUR"), "FOUR")
        self.assertEqual(len(d), len(self.py_dict) + 1)
        self.assertEqual(d["four"], "FOUR")

    def test_setdefault3(self):
        d = self.make_dictionary(self.py_dict)

        self.assertTrue("four" not in d)
        self.assertEqual(d.setdefault("four"), None)
        self.assertEqual(len(d), len(self.py_dict))
        with self.assertRaises(KeyError):
            d["four"]

    def test_update1(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d, self.py_dict)
        d.update({"one": "two", "three": "four", "four": "FIVE"})
        self.assertNotEqual(d, self.py_dict)
        self.assertEqual(d["one"], "two")
        self.assertEqual(d["two"], "TWO")
        self.assertEqual(d["three"], "four")
        self.assertEqual(d["four"], "FIVE")
        self.assertEqual(len(d), len(self.py_dict) + 1)

    def test_update2(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d, self.py_dict)
        d.update([("one", "two"), ("three", "four"), ("four", "FIVE")])
        self.assertNotEqual(d, self.py_dict)
        self.assertEqual(d["one"], "two")
        self.assertEqual(d["two"], "TWO")
        self.assertEqual(d["three"], "four")
        self.assertEqual(len(d), len(self.py_dict) + 1)

    def test_update3(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d, self.py_dict)
        d.update(one="two", three="four", four="FIVE")
        self.assertNotEqual(d, self.py_dict)
        self.assertEqual(d["one"], "two")
        self.assertEqual(d["two"], "TWO")
        self.assertEqual(d["three"], "four")
        self.assertEqual(d["four"], "FIVE")
        self.assertEqual(len(d), len(self.py_dict) + 1)

    def test_update4(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d, self.py_dict)
        d.update({"one": "two"}, three="four", four="FIVE")
        self.assertNotEqual(d, self.py_dict)
        self.assertEqual(d["one"], "two")
        self.assertEqual(d["two"], "TWO")
        self.assertEqual(d["three"], "four")
        self.assertEqual(d["four"], "FIVE")
        self.assertEqual(len(d), len(self.py_dict) + 1)


class PythonObjectTest(unittest.TestCase):
    def test_primitive_dict_attribute(self):
        class PrimitiveDictAttrContainer(NSObject):
            @objc_method
            def init(self):
                self.data = {1: 2, 2: 4, 3: 6}
                return self

            @objc_method
            def initWithDict_(self, data):
                self.data = data
                return self

        obj1 = PrimitiveDictAttrContainer.alloc().init()
        self.assertEqual(obj1.data, {1: 2, 2: 4, 3: 6})
        self.assertIsInstance(obj1.data, dict)

        # If it's set through a method call, it becomes an objc instance
        obj2 = PrimitiveDictAttrContainer.alloc().initWithDict_({4: 8, 5: 10, 6: 12})
        self.assertEqual(obj2.data, {4: 8, 5: 10, 6: 12})
        self.assertIsInstance(obj2.data, ObjCDictInstance)

        # If it's set by direct attribute access, it becomes a Python object.
        obj2.data = {7: 14, 8: 16, 9: 18}
        self.assertEqual(obj2.data, {7: 14, 8: 16, 9: 18})
        self.assertIsInstance(obj2.data, dict)

    def test_primitive_dict_property(self):
        class PrimitiveDictContainer(NSObject):
            data = objc_property()

            @objc_method
            def init(self):
                self.data = {1: 2, 2: 4, 3: 6}
                return self

            @objc_method
            def initWithDict_(self, data):
                self.data = data
                return self

        obj1 = PrimitiveDictContainer.alloc().init()
        self.assertEqual(obj1.data, {1: 2, 2: 4, 3: 6})
        self.assertIsInstance(obj1.data, ObjCDictInstance)

        obj2 = PrimitiveDictContainer.alloc().initWithDict_({4: 8, 5: 10, 6: 12})
        self.assertEqual(obj2.data, {4: 8, 5: 10, 6: 12})
        self.assertIsInstance(obj2.data, ObjCDictInstance)

        obj2.data = {7: 14, 8: 16, 9: 18}
        self.assertEqual(obj2.data, {7: 14, 8: 16, 9: 18})
        self.assertIsInstance(obj2.data, ObjCDictInstance)

    def test_object_dict_attribute(self):
        class ObjectDictAttrContainer(NSObject):
            @objc_method
            def init(self):
                self.data = {"x": "x1", "y": "y2", "z": "z3"}
                return self

            @objc_method
            def initWithDict_(self, data):
                self.data = data
                return self

        obj1 = ObjectDictAttrContainer.alloc().init()
        self.assertEqual(obj1.data, {"x": "x1", "y": "y2", "z": "z3"})
        self.assertIsInstance(obj1.data, dict)

        # If it's set through a method call, it becomes an objc instance
        obj2 = ObjectDictAttrContainer.alloc().initWithDict_(
            {"a": "a4", "b": "b5", "c": "c6"}
        )
        self.assertEqual(obj2.data, {"a": "a4", "b": "b5", "c": "c6"})
        self.assertIsInstance(obj2.data, ObjCDictInstance)

        # If it's set by direct attribute access, it becomes a Python object.
        obj2.data = {"i": "i7", "j": "j8", "k": "k9"}
        self.assertEqual(obj2.data, {"i": "i7", "j": "j8", "k": "k9"})
        self.assertIsInstance(obj2.data, dict)

    def test_object_dict_property(self):
        class ObjectDictContainer(NSObject):
            data = objc_property()

            @objc_method
            def init(self):
                self.data = {"x": "x1", "y": "y2", "z": "z3"}
                return self

            @objc_method
            def initWithDict_(self, data):
                self.data = data
                return self

        obj1 = ObjectDictContainer.alloc().init()
        self.assertEqual(obj1.data, {"x": "x1", "y": "y2", "z": "z3"})
        self.assertIsInstance(obj1.data, ObjCDictInstance)

        obj2 = ObjectDictContainer.alloc().initWithDict_(
            {"a": "a4", "b": "b5", "c": "c6"}
        )
        self.assertEqual(obj2.data, {"a": "a4", "b": "b5", "c": "c6"})
        self.assertIsInstance(obj2.data, ObjCDictInstance)

        obj2.data = {"i": "i7", "j": "j8", "k": "k9"}
        self.assertEqual(obj2.data, {"i": "i7", "j": "j8", "k": "k9"})
        self.assertIsInstance(obj2.data, ObjCDictInstance)

    def test_multitype_dict_property(self):
        class MultitypeDictContainer(NSObject):
            data = objc_property()

        # All types can be stored in a dict.
        obj = MultitypeDictContainer.alloc().init()
        obj.data = {4: 16, True: False, "Hello": "Goodbye"}
        self.assertEqual(obj.data, {4: 16, True: False, "Hello": "Goodbye"})
        self.assertIsInstance(obj.data, ObjCDictInstance)
