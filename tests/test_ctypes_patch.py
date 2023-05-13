from __future__ import annotations

import ctypes
import unittest

from rubicon.objc import ctypes_patch


class CtypesPatchTest(unittest.TestCase):
    def test_patch_structure(self):
        """A custom structure can be patched successfully."""

        class TestStruct(ctypes.Structure):
            _fields_ = [
                ("spam", ctypes.c_int),
                ("ham", ctypes.c_double),
            ]

        functype = ctypes.CFUNCTYPE(TestStruct)

        # Before patching, the structure cannot be returned from a callback.
        with self.assertRaises(TypeError):

            @functype
            def get_struct_fail():
                return TestStruct(123, 123)

        ctypes_patch.make_callback_returnable(TestStruct)

        # After patching, the structure can be returned from a callback.
        @functype
        def get_struct():
            return TestStruct(123, 123)

        # After being returned from the callback, the structure's data is intact.
        struct = get_struct()
        self.assertEqual(struct.spam, 123)
        self.assertEqual(struct.ham, 123)

    def test_patch_pointer(self):
        """A custom pointer type can be patched successfully."""

        class TestStruct(ctypes.Structure):
            _fields_ = [
                ("spam", ctypes.c_int),
                ("ham", ctypes.c_double),
            ]

        pointertype = ctypes.POINTER(TestStruct)
        functype = ctypes.CFUNCTYPE(pointertype)

        original_struct = TestStruct(123, 123)

        # Before patching, the pointer cannot be returned from a callback.
        with self.assertRaises(TypeError):

            @functype
            def get_struct_fail():
                return pointertype(original_struct)

        ctypes_patch.make_callback_returnable(pointertype)

        # After patching, the structure can be returned from a callback.
        @functype
        def get_struct():
            return pointertype(original_struct)

        # After being returned from the callback, the pointer's data is intact.
        struct_pointer = get_struct()
        self.assertEqual(
            ctypes.addressof(struct_pointer.contents), ctypes.addressof(original_struct)
        )
        self.assertEqual(struct_pointer.contents.spam, 123)
        self.assertEqual(struct_pointer.contents.ham, 123)

    def test_no_patch_primitives(self):
        """Primitive types cannot be patched."""

        for tp in (ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_void_p):
            with self.subTest(tp):
                with self.assertRaises(ValueError):
                    ctypes_patch.make_callback_returnable(tp)

    def test_patch_idempotent(self):
        """Patching a type multiple times is equivalent to patching once."""

        class TestStruct(ctypes.Structure):
            _fields_ = [
                ("spam", ctypes.c_int),
                ("ham", ctypes.c_double),
            ]

        functype = ctypes.CFUNCTYPE(TestStruct)

        for _ in range(5):
            ctypes_patch.make_callback_returnable(TestStruct)

            # After patching, the structure can be returned from a callback.
            @functype
            def get_struct():
                return TestStruct(123, 123)

            # After being returned from the callback, the structure's data is intact.
            struct = get_struct()
            self.assertEqual(struct.spam, 123)
            self.assertEqual(struct.ham, 123)

    def test_patched_type_returned_often(self):
        """Returning a patched type very often works properly without crashing
        anything.

        This checks that bpo-36880 is either fixed or worked around.
        """

        class TestStruct(ctypes.Structure):
            _fields_ = [
                ("spam", ctypes.c_int),
                ("ham", ctypes.c_double),
            ]

        functype = ctypes.CFUNCTYPE(TestStruct)

        ctypes_patch.make_callback_returnable(TestStruct)

        # After patching, the structure can be returned from a callback.
        @functype
        def get_struct():
            return TestStruct(123, 123)

        for _ in range(10000):
            # After being returned from the callback, the structure's data is intact.
            struct = get_struct()
            self.assertEqual(struct.spam, 123)
            self.assertEqual(struct.ham, 123)
