from __future__ import annotations

import ctypes

import pytest

from rubicon.objc import ctypes_patch


def test_patch_structure():
    """A custom structure can be patched successfully."""

    class TestStruct(ctypes.Structure):
        _fields_ = [
            ("spam", ctypes.c_int),
            ("ham", ctypes.c_double),
        ]

    functype = ctypes.CFUNCTYPE(TestStruct)

    # Before patching, the structure cannot be returned from a callback.
    with pytest.raises(TypeError):

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
    assert struct.spam == 123
    assert struct.ham == 123


def test_patch_pointer():
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
    with pytest.raises(TypeError):

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
    assert ctypes.addressof(struct_pointer.contents) == ctypes.addressof(
        original_struct
    )
    assert struct_pointer.contents.spam == 123
    assert struct_pointer.contents.ham == 123


@pytest.mark.parametrize(
    "tp", [ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_void_p]
)
def test_no_patch_primitives(tp):
    """Primitive types cannot be patched."""

    with pytest.raises(ValueError):
        ctypes_patch.make_callback_returnable(tp)


def test_patch_idempotent():
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
        assert struct.spam == 123
        assert struct.ham == 123


def test_patched_type_returned_often():
    """Returning a patched type very often works properly without crashing anything.

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
        assert struct.spam == 123
        assert struct.ham == 123
