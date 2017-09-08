import faulthandler
import unittest
from ctypes import CDLL, Structure, c_int, c_void_p, util

from rubicon.objc import NSObject, ObjCBlock, ObjCClass, objc_method
from rubicon.objc.runtime import Block, objc_block

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


class BlockTests(unittest.TestCase):
    def test_block_property_ctypes(self):
        BlockPropertyExample = ObjCClass("BlockPropertyExample")
        instance = BlockPropertyExample.alloc().init()
        result = ObjCBlock(instance.blockProperty, c_int, c_int, c_int)(1, 2)
        self.assertEqual(result, 3)

    def test_block_property_pytypes(self):
        BlockPropertyExample = ObjCClass("BlockPropertyExample")
        instance = BlockPropertyExample.alloc().init()
        result = ObjCBlock(instance.blockProperty, int, int, int)(1, 2)
        self.assertEqual(result, 3)

    def test_block_delegate_method_manual_ctypes(self):
        class DelegateManualC(NSObject):
            @objc_method
            def exampleMethod_(self, block):
                ObjCBlock(block, c_void_p, c_int, c_int)(2, 3)
        BlockObjectExample = ObjCClass("BlockObjectExample")
        delegate = DelegateManualC.alloc().init()
        instance = BlockObjectExample.alloc().initWithDelegate_(delegate)
        result = instance.blockExample()
        self.assertEqual(result, 5)

    def test_block_delegate_method_manual_pytypes(self):
        class DelegateManualPY(NSObject):
            @objc_method
            def exampleMethod_(self, block):
                ObjCBlock(block, None, int, int)(2, 3)
        BlockObjectExample = ObjCClass("BlockObjectExample")
        delegate = DelegateManualPY.alloc().init()
        instance = BlockObjectExample.alloc().initWithDelegate_(delegate)
        result = instance.blockExample()
        self.assertEqual(result, 5)

    def test_block_delegate_auto(self):
        class DelegateAuto(NSObject):
            @objc_method
            def exampleMethod_(self, block: objc_block):
                block(4, 5)
        BlockObjectExample = ObjCClass("BlockObjectExample")
        delegate = DelegateAuto.alloc().init()
        instance = BlockObjectExample.alloc().initWithDelegate_(delegate)
        result = instance.blockExample()
        self.assertEqual(result, 9)

    def test_block_delegate_auto_struct(self):
        class BlockStruct(Structure):
            _fields_ = [
                ('a', c_int),
                ('b', c_int),
            ]

        class DelegateAutoStruct(NSObject):
            @objc_method
            def structBlockMethod_(self, block: objc_block) -> int:
                return block(BlockStruct(42, 43))
        BlockObjectExample = ObjCClass("BlockObjectExample")
        delegate = DelegateAutoStruct.alloc().init()
        instance = BlockObjectExample.alloc().initWithDelegate_(delegate)
        result = instance.structBlockExample()
        self.assertEqual(result, 85)

    def test_block_receiver(self):
        BlockReceiverExample = ObjCClass("BlockReceiverExample")
        instance = BlockReceiverExample.alloc().init()

        values = []

        def block(a: int, b: int) -> None:
            values.append(a + b)
        instance.receiverMethod_(block)

        self.assertEqual(values, [27])

    def test_block_receiver_unannotated(self):
        BlockReceiverExample = ObjCClass("BlockReceiverExample")
        instance = BlockReceiverExample.alloc().init()

        def block(a, b):
            return a + b
        with self.assertRaises(ValueError):
            instance.receiverMethod_(block)

    def test_block_receiver_lambda(self):
        BlockReceiverExample = ObjCClass("BlockReceiverExample")
        instance = BlockReceiverExample.alloc().init()
        with self.assertRaises(ValueError):
            instance.receiverMethod_(lambda a, b: a + b)

    def test_block_receiver_explicit(self):
        BlockReceiverExample = ObjCClass("BlockReceiverExample")
        instance = BlockReceiverExample.alloc().init()

        values = []

        block = Block(lambda a, b: values.append(a + b), None, int, int)
        instance.receiverMethod_(block)

        self.assertEqual(values, [27])

    def test_block_round_trip(self):
        BlockRoundTrip = ObjCClass("BlockRoundTrip")
        instance = BlockRoundTrip.alloc().init()

        def block(a: int, b: int) -> int:
            return a + b

        returned_block = instance.roundTrip_(block)
        self.assertEqual(returned_block(8, 9), 17)
