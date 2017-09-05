from ctypes import util, CDLL
import faulthandler
import unittest

try:
    import platform
    OSX_VERSION = tuple(int(v) for v in platform.mac_ver()[0].split('.')[:2])
except Exception:
    OSX_VERSION = None


from rubicon.objc import ObjCClass

# Load the test harness library
rubiconharness_name = util.find_library('rubiconharness')
if rubiconharness_name is None:
    raise RuntimeError("Couldn't load Rubicon test harness library. Have you set DYLD_LIBRARY_PATH?")
rubiconharness = CDLL(rubiconharness_name)

faulthandler.enable()


class NSArrayMixinTest(unittest.TestCase):
    nsarray = ObjCClass('NSArray')
    nsmutablearray = ObjCClass('NSMutableArray')

    py_list = ['one', 'two', 'three']

    def make_array(self, contents=None):
        a = self.nsmutablearray.alloc().init()
        if contents is not None:
            for value in contents:
                a.addObject(value)

        return self.nsarray.arrayWithArray(a)

    def test_getitem(self):
        a = self.make_array(self.py_list)

        for pos, value in enumerate(self.py_list):
            self.assertEqual(a[pos], value)

        with self.assertRaises(IndexError):
            a[len(self.py_list) + 10]

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
        self.assertEqual(a.index('two'), 1)
        with self.assertRaises(ValueError):
            a.index('umpteen')

    def test_count(self):
        a = self.make_array(self.py_list)
        self.assertEqual(a.count('one'), 1)

    def test_copy(self):
        a = self.make_array(self.py_list)
        b = a.copy()
        self.assertEqual(b, a)
        self.assertEqual(b, self.py_list)

        with self.assertRaises(AttributeError):
            b.append('four')

    def test_equivalence(self):
        a = self.make_array(self.py_list)
        b = self.make_array(self.py_list)

        self.assertEqual(a, self.py_list)
        self.assertEqual(b, self.py_list)
        self.assertEqual(a, b)
        self.assertEqual(self.py_list, a)
        self.assertEqual(self.py_list, b)
        self.assertEqual(b, a)

    def test_slice_access(self):
        a = self.make_array(self.py_list * 2)
        self.assertEqual(a[1:4], ['two', 'three', 'one'])
        self.assertEqual(a[:-2], ['one', 'two', 'three', 'one'])
        self.assertEqual(a[4:], ['two', 'three'])
        self.assertEqual(a[1:5:2], ['two', 'one'])


class NSMutableArrayMixinTest(NSArrayMixinTest):
    def make_array(self, contents=None):
        a = self.nsmutablearray.alloc().init()
        if contents is not None:
            for value in contents:
                a.addObject(value)

        return a

    def test_setitem(self):
        a = self.make_array(self.py_list)

        a[2] = 'four'
        self.assertEqual(a[2], 'four')

    def test_del(self):
        a = self.make_array(self.py_list)
        del a[0]
        self.assertEqual(len(a), 2)
        self.assertEqual(a[0], 'two')

    def test_append(self):
        a = self.make_array()
        a.append('an item')
        self.assertTrue('an item' in a)

    def test_extend(self):
        a = self.make_array()
        a.extend(['an item', 'another item'])
        self.assertTrue('an item' in a)
        self.assertTrue('another item' in a)

    def test_clear(self):
        a = self.make_array(self.py_list)
        a.clear()
        self.assertEqual(len(a), 0)

    def test_count(self):
        a = self.make_array(self.py_list)
        self.assertEqual(a.count('one'), 1)

        a.append('one')
        self.assertEqual(a.count('one'), 2)

    def test_copy(self):
        a = self.make_array(self.py_list)
        b = a.copy()
        self.assertEqual(b, a)
        self.assertEqual(b, self.py_list)

        b.append('four')

    def test_insert(self):
        a = self.make_array(self.py_list)
        a.insert(1, 'four')
        self.assertEqual(a[0], 'one')
        self.assertEqual(a[1], 'four')
        self.assertEqual(a[2], 'two')

    def test_pop(self):
        a = self.make_array(self.py_list)
        self.assertEqual(a.pop(), 'three')
        self.assertEqual(a.pop(0), 'one')
        self.assertEqual(len(a), 1)
        self.assertEqual(a[0], 'two')

    def test_remove(self):
        a = self.make_array(self.py_list)
        a.remove('three')
        self.assertEqual(len(a), 2)
        self.assertEqual(a[-1], 'two')
        with self.assertRaises(ValueError):
            a.remove('umpteen')

    def test_slice_assignment1(self):
        a = self.make_array(self.py_list * 2)
        a[2:4] = ['four', 'five']
        self.assertEqual(a, ['one', 'two', 'four', 'five', 'two', 'three'])

    def test_slice_assignment2(self):
        a = self.make_array(self.py_list * 2)
        a[::2] = ['four', 'five', 'six']
        self.assertEqual(a, ['four', 'two', 'five', 'one', 'six', 'three'])

    def test_slice_assignment3(self):
        a = self.make_array(self.py_list * 2)
        a[2:4] = ['four']
        self.assertEqual(a, ['one', 'two', 'four', 'two', 'three'])

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
        self.assertEqual(a[0], 'one')
        self.assertEqual(a[-1], 'one')

    def test_del_slice2(self):
        a = self.make_array(self.py_list * 2)
        del a[::2]
        self.assertEqual(len(a), 3)
        self.assertEqual(a[0], 'two')
        self.assertEqual(a[1], 'one')
        self.assertEqual(a[2], 'three')

    def test_del_slice3(self):
        a = self.make_array(self.py_list * 2)
        del a[::-2]
        self.assertEqual(len(a), 3)
        self.assertEqual(a[0], 'one')
        self.assertEqual(a[1], 'three')
        self.assertEqual(a[2], 'two')

    def test_reverse(self):
        a = self.make_array(self.py_list)
        a.reverse()

        for pos, value in enumerate(reversed(self.py_list)):
            self.assertEqual(a[pos], value)
