from __future__ import annotations

import unittest
from ctypes import Structure, c_float, c_int, c_void_p

from rubicon.objc import NSObject, ObjCBlock, ObjCClass, objc_method
from rubicon.objc.api import Block
from rubicon.objc.runtime import objc_block


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

    def test_block_delegate_manual_struct(self):
        class BlockStruct(Structure):
            _fields_ = [
                ("a", c_int),
                ("b", c_int),
            ]

        class DelegateManualStruct(NSObject):
            @objc_method
            def structBlockMethod_(self, block: objc_block) -> int:
                return ObjCBlock(block, int, BlockStruct)(BlockStruct(42, 43))

        BlockObjectExample = ObjCClass("BlockObjectExample")
        delegate = DelegateManualStruct.alloc().init()
        instance = BlockObjectExample.alloc().initWithDelegate_(delegate)
        result = instance.structBlockExample()
        self.assertEqual(result, 85)

    def test_block_delegate_auto_struct(self):
        class BlockStruct(Structure):
            _fields_ = [
                ("a", c_int),
                ("b", c_int),
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

    def test_block_delegate_auto_struct_mismatch(self):
        class BadBlockStruct(Structure):
            _fields_ = [
                ("a", c_float),
                ("b", c_int),
            ]

        class BadDelegateAutoStruct(NSObject):
            @objc_method
            def structBlockMethod_(self, block: objc_block) -> int:
                try:
                    # block accepts an anonymous structure with 2 int arguments
                    # Passing in BadBlockStruct should raise a type error because
                    # the structure's shape doesn't match.
                    return block(BadBlockStruct(2.71828, 43))
                except TypeError:
                    # Ideally, this would be raised as an ObjC error;
                    # however, at least for now, that doesn't happen.
                    return -99

        BlockObjectExample = ObjCClass("BlockObjectExample")
        delegate = BadDelegateAutoStruct.alloc().init()
        instance = BlockObjectExample.alloc().initWithDelegate_(delegate)
        result = instance.structBlockExample()
        self.assertEqual(result, -99)

    def test_block_receiver(self):
        BlockReceiverExample = ObjCClass("BlockReceiverExample")
        instance = BlockReceiverExample.alloc().init()

        values = []

        def block(a: int, b: int) -> int:
            values.append(a + b)
            return 42

        result = instance.receiverMethod_(block)

        self.assertEqual(values, [27])
        self.assertEqual(result, 42)

    def test_block_receiver_no_return_annotation(self):
        BlockReceiverExample = ObjCClass("BlockReceiverExample")
        instance = BlockReceiverExample.alloc().init()

        def block(a: int, b: int):
            return a + b

        with self.assertRaises(ValueError):
            instance.receiverMethod_(block)

    def test_block_receiver_missing_arg_annotation(self):
        BlockReceiverExample = ObjCClass("BlockReceiverExample")
        instance = BlockReceiverExample.alloc().init()

        def block(a: int, b) -> int:
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

    def test_block_round_trip_no_arguments(self):
        """A block that takes no arguments can be created with both ways of
        specifying types."""

        BlockRoundTrip = ObjCClass("BlockRoundTrip")
        instance = BlockRoundTrip.alloc().init()

        @Block
        def block_1() -> c_int:
            return 42

        returned_block_1 = instance.roundTripNoArgs(block_1)
        self.assertEqual(returned_block_1(), 42)

        block_2 = Block(lambda: 42, c_int)
        returned_block_2 = instance.roundTripNoArgs(block_2)
        self.assertEqual(returned_block_2(), 42)

    def test_block_bound_method(self):
        """A bound method with type annotations can be wrapped in a block."""

        class Handler:
            def no_args(self) -> c_int:
                return 42

            def two_args(self, x: c_int, y: c_int) -> c_int:
                return x + y

        handler = Handler()
        no_args_block = Block(handler.no_args)
        two_args_block = Block(handler.two_args)

        BlockRoundTrip = ObjCClass("BlockRoundTrip")
        instance = BlockRoundTrip.alloc().init()

        returned_no_args_block = instance.roundTripNoArgs(no_args_block)
        self.assertEqual(returned_no_args_block(), 42)

        returned_two_args_block = instance.roundTrip(two_args_block)
        self.assertEqual(returned_two_args_block(12, 34), 46)
