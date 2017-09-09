import faulthandler
import unittest
from ctypes import CDLL, util

from rubicon.objc import NSDictionary, NSMutableDictionary, ObjCClass
from rubicon.objc.runtime import ObjCDictInstance

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


class NSDictionaryMixinTest(unittest.TestCase):
    py_dict = {
        'one': 'ONE',
        'two': 'TWO',
        'three': 'THREE',
    }
    name = 'NSDictionary'

    def make_dictionary(self, contents=None):
        d = NSMutableDictionary.alloc().init()
        if contents is not None:
            for key, value in contents.items():
                d.setObject_forKey_(value, key)

        return NSDictionary.dictionaryWithDictionary(d)

    def test_repr(self):
        a = self.make_dictionary({'one': 'ONE', 'two': 'TWO'})
        self.assertTrue(repr(a) in [
                "%s{'one': 'ONE', 'two': 'TWO'}" % self.name,
                "%s{'two': 'TWO', 'one': 'ONE'}" % self.name,
            ])

    def test_str(self):
        a = self.make_dictionary({'one': 'ONE', 'two': 'TWO'})
        self.assertTrue(str(a) in [
                "{'one': 'ONE', 'two': 'TWO'}",
                "{'two': 'TWO', 'one': 'ONE'}",
            ])

    def test_getitem(self):
        d = self.make_dictionary(self.py_dict)

        for key, value in self.py_dict.items():
            self.assertEqual(d[key], value)

        with self.assertRaises(KeyError):
            d['NO SUCH KEY']

    def test_iter(self):
        d = self.make_dictionary(self.py_dict)

        keys = set(self.py_dict)
        for k in d:
            self.assertTrue(k in keys)
            keys.remove(k)

        self.assertTrue(len(keys) == 0)

    def test_len(self):
        d = self.make_dictionary(self.py_dict)
        self.assertEqual(len(d), len(self.py_dict))

    def test_get(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d.get('one'), 'ONE')
        self.assertEqual(d.get('two', None), 'TWO')
        self.assertEqual(d.get('four', None), None)
        self.assertEqual(d.get('five', 5), 5)
        self.assertEqual(d.get('six', None), None)

    def test_contains(self):
        d = self.make_dictionary(self.py_dict)
        for key in self.py_dict:
            self.assertTrue(key in d)

    def test_copy(self):
        d = self.make_dictionary(self.py_dict)
        e = d.copy()
        self.assertEqual(e, d)
        self.assertEqual(e, self.py_dict)

        with self.assertRaises(TypeError):
            e['four'] = 'FOUR'

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

        raw = {'data': 'stuff', 'other': 'gadgets'}
        d = self.make_dictionary(raw)
        # Call a method with an NSDictionary instance
        self.assertEqual(example.processDictionary(d), 'stuff')
        # Call the same method with the raw Python dictionary
        self.assertEqual(example.processDictionary(raw), 'stuff')

    def test_property(self):
        Example = ObjCClass("Example")
        example = Example.alloc().init()

        d = self.make_dictionary(self.py_dict)
        example.dict = d

        self.assertEqual(example.dict, self.py_dict)
        self.assertTrue(isinstance(example.dict, ObjCDictInstance))
        self.assertEqual(example.dict['one'], 'ONE')


class NSMutableDictionaryMixinTest(NSDictionaryMixinTest):
    name = 'NSMutableDictionary'

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
        del d['one']
        self.assertEqual(len(d), 2)
        with self.assertRaises(KeyError):
            d['one']

    def test_clear(self):
        d = self.make_dictionary(self.py_dict)
        d.clear()
        self.assertEqual(len(d), 0)

    def test_copy(self):
        d = self.make_dictionary(self.py_dict)
        e = d.copy()
        self.assertEqual(e, d)
        self.assertEqual(e, self.py_dict)

        e['four'] = 'FOUR'

    def test_pop1(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d.pop('one'), 'ONE')
        self.assertEqual(len(d), 2)
        with self.assertRaises(KeyError):
            d['one']

    def test_pop2(self):
        d = self.make_dictionary(self.py_dict)

        with self.assertRaises(KeyError):
            d.pop('four')

    def test_pop3(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d.pop('four', 4), 4)

    def test_popitem(self):
        d = self.make_dictionary(self.py_dict)

        keys = set(self.py_dict)

        while len(d) > 0:
            key, value = d.popitem()
            self.assertTrue(key in keys)
            self.assertEqual(value, self.py_dict[key])
            self.assertTrue(key not in d)

    def test_setdefault1(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d.setdefault('one', 'default'), 'ONE')
        self.assertEqual(len(d), len(self.py_dict))

    def test_setdefault2(self):
        d = self.make_dictionary(self.py_dict)

        self.assertTrue('four' not in d)
        self.assertEqual(d.setdefault('four', 'FOUR'), 'FOUR')
        self.assertEqual(len(d), len(self.py_dict) + 1)
        self.assertEqual(d['four'], 'FOUR')

    def test_setdefault3(self):
        d = self.make_dictionary(self.py_dict)

        self.assertTrue('four' not in d)
        self.assertEqual(d.setdefault('four'), None)
        self.assertEqual(len(d), len(self.py_dict))
        with self.assertRaises(KeyError):
            d['four']

    def test_update1(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d, self.py_dict)
        d.update({'one': 'two', 'three': 'four', 'four': 'FIVE'})
        self.assertNotEqual(d, self.py_dict)
        self.assertEqual(d['one'], 'two')
        self.assertEqual(d['two'], 'TWO')
        self.assertEqual(d['three'], 'four')
        self.assertEqual(d['four'], 'FIVE')
        self.assertEqual(len(d), len(self.py_dict) + 1)

    def test_update2(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d, self.py_dict)
        d.update([('one', 'two'), ('three', 'four'), ('four', 'FIVE')])
        self.assertNotEqual(d, self.py_dict)
        self.assertEqual(d['one'], 'two')
        self.assertEqual(d['two'], 'TWO')
        self.assertEqual(d['three'], 'four')
        self.assertEqual(len(d), len(self.py_dict) + 1)

    def test_update3(self):
        d = self.make_dictionary(self.py_dict)

        self.assertEqual(d, self.py_dict)
        d.update(one='two', three='four', four='FIVE')
        self.assertNotEqual(d, self.py_dict)
        self.assertEqual(d['one'], 'two')
        self.assertEqual(d['two'], 'TWO')
        self.assertEqual(d['three'], 'four')
        self.assertEqual(d['four'], 'FIVE')
        self.assertEqual(len(d), len(self.py_dict) + 1)

    def test_argument(self):
        Example = ObjCClass("Example")
        example = Example.alloc().init()

        d = self.make_dictionary(self.py_dict)
        # Call a method with an NSDictionary instance
        self.assertIsNone(example.processDictionary(d))
        # Call the same method with the raw Python dictionary
        self.assertIsNone(example.processDictionary(self.py_dict))

        raw = {'data': 'stuff', 'other': 'gadgets'}
        d = self.make_dictionary(raw)
        # Call a method with an NSDictionary instance
        self.assertEqual(example.processDictionary(d), 'stuff')
        # Call the same method with the raw Python dictionary
        self.assertEqual(example.processDictionary(raw), 'stuff')

    def test_property(self):
        Example = ObjCClass("Example")
        example = Example.alloc().init()

        d = self.make_dictionary(self.py_dict)
        example.dict = d

        self.assertEqual(example.dict, self.py_dict)
        self.assertTrue(isinstance(example.dict, ObjCDictInstance))
        self.assertEqual(example.dict['one'], 'ONE')
