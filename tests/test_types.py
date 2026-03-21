from __future__ import annotations

from ctypes import Structure, Union, c_int

import pytest

from rubicon.objc import (
    CFRange,
    CGPoint,
    CGPointMake,
    CGRect,
    CGRectMake,
    CGSize,
    CGSizeMake,
    NSEdgeInsets,
    NSEdgeInsetsMake,
    NSMakePoint,
    NSMakeRect,
    NSMakeSize,
    NSPoint,
    NSRange,
    NSRect,
    NSSize,
    UIEdgeInsets,
    UIEdgeInsetsMake,
)
from rubicon.objc.types import (
    __LP64__,
    _create_structish_type_for_encoding,
    _end_of_encoding,
    compound_value_for_sequence,
    ctype_for_encoding,
    encoding_for_ctype,
    get_ctype_for_encoding_map,
    get_ctype_for_type_map,
    get_encoding_for_ctype_map,
    register_ctype_for_type,
    unregister_ctype_for_type,
    unregister_encoding,
    unregister_encoding_all,
)


def test_nspoint_repr():
    """Test NSPoint repr and str returns correct value."""

    my_point = NSPoint(10, 20)
    assert repr(my_point) == "<NSPoint(10.0, 20.0)>"
    assert str(my_point) == "(10.0, 20.0)"


def test_cgpoint_repr():
    """Test CGPoint repr and str returns correct value."""

    my_point = CGPoint(10, 20)
    if __LP64__:
        assert repr(my_point) == "<NSPoint(10.0, 20.0)>"
    else:
        assert repr(my_point) == "<CGPoint(10.0, 20.0)>"
    assert str(my_point) == "(10.0, 20.0)"


def test_nsrect_repr():
    """Test NSRect repr and str returns correct value."""

    my_rect = NSRect(NSPoint(10, 20), NSSize(5, 15))
    assert repr(my_rect) == "<NSRect(NSPoint(10.0, 20.0), NSSize(5.0, 15.0))>"
    assert str(my_rect) == "5.0 x 15.0 @ (10.0, 20.0)"


def test_cgrect_repr():
    """Test CGRect repr and str returns correct value."""

    my_rect = CGRect(CGPoint(10, 20), CGSize(5, 15))
    if __LP64__:
        assert repr(my_rect) == "<NSRect(NSPoint(10.0, 20.0), NSSize(5.0, 15.0))>"
    else:
        assert repr(my_rect) == "<CGRect(CGPoint(10.0, 20.0), CGSize(5.0, 15.0))>"

    assert str(my_rect) == "5.0 x 15.0 @ (10.0, 20.0)"


def test_nssize_repr():
    """Test NSSize repr and str returns correct value."""

    my_size = NSSize(5, 15)
    assert repr(my_size) == "<NSSize(5.0, 15.0)>"
    assert str(my_size) == "5.0 x 15.0"


def test_cgsize_repr():
    """Test NSSize repr and str returns correct value."""

    my_size = CGSize(5, 15)
    if __LP64__:
        assert repr(my_size) == "<NSSize(5.0, 15.0)>"
    else:
        assert repr(my_size) == "<CGSize(5.0, 15.0)>"
    assert str(my_size) == "5.0 x 15.0"


def test_nsrange_repr():
    """Test NSRange repr and str returns correct value."""

    my_range = NSRange(5, 6)
    assert repr(my_range) == "<NSRange(5, 6)>"
    assert str(my_range) == "location=5, length=6"


def test_cfrange_repr():
    """Test NSRange repr and str returns correct value."""

    my_range = CFRange(5, 6)
    assert repr(my_range) == "<CFRange(5, 6)>"
    assert str(my_range) == "location=5, length=6"


def test_nsedgeinsets_repr():
    """Test NSRange repr and str returns correct value."""

    my_edge_insets = NSEdgeInsets(4, 5, 6, 7)
    assert repr(my_edge_insets) == "<NSEdgeInsets(4.0, 5.0, 6.0, 7.0)>"
    assert str(my_edge_insets) == "top=4.0, left=5.0, bottom=6.0, right=7.0"


def test_uiedgeinsets_repr():
    """Test NSRange repr and str returns correct value."""

    my_edge_insets = UIEdgeInsets(4, 5, 6, 7)
    assert repr(my_edge_insets) == "<UIEdgeInsets(4.0, 5.0, 6.0, 7.0)>"
    assert str(my_edge_insets) == "top=4.0, left=5.0, bottom=6.0, right=7.0"


def test_function_NSEdgeInsetsMake():
    """Python can invoke NSEdgeInsetsMake to create NSEdgeInsets."""

    insets = NSEdgeInsets(0.0, 1.1, 2.2, 3.3)
    other_insets = NSEdgeInsetsMake(0.0, 1.1, 2.2, 3.3)

    # structs are NOT equal
    assert insets != other_insets

    # but their values are
    assert insets.top == other_insets.top
    assert insets.left == other_insets.left
    assert insets.bottom == other_insets.bottom
    assert insets.right == other_insets.right


def test_type_map_management():
    """Test unregister_ctype_for_type and get_ctype_for_type_map (lines 161, 168)"""

    class MyType:
        pass

    register_ctype_for_type(MyType, c_int)
    assert get_ctype_for_type_map()[MyType] == c_int

    unregister_ctype_for_type(MyType)
    assert MyType not in get_ctype_for_type_map()


def test_end_of_encoding_errors():
    """Test _end_of_encoding error cases (lines 183, 235, 238, 244)"""
    with pytest.raises(ValueError, match="Start index 10 not in range"):
        _end_of_encoding(b"i", 10)

    with pytest.raises(ValueError, match="Unknown encoding"):
        _end_of_encoding(b"Z", 0)

    with pytest.raises(
        ValueError, match="Incomplete encoding, missing 1 closing parentheses"
    ):
        _end_of_encoding(b"{abc=i", 0)

    # Incomplete encoding, reached end of string too early
    with pytest.raises(ValueError, match="Unknown encoding"):
        _end_of_encoding(b"!", 0)


def test_create_structish_no_fields():
    """Test _create_structish_type_for_encoding with no fields (line 266)"""
    # Encoding without '=' means no fields
    assert _create_structish_type_for_encoding(b"{MyStruct}", base=Structure) is None


def test_ctype_for_encoding_unknown():
    """Test ctype_for_encoding unknown cases (lines 336-360)"""
    # Union
    u = ctype_for_encoding(b"(MyUnion=ic)")
    assert issubclass(u, Union)

    # Block signature
    assert ctype_for_encoding(b"@?<v@?>") == ctype_for_encoding(b"@?")

    # Object pointer class name
    assert ctype_for_encoding(b'@"NSString"') == ctype_for_encoding(b"@")

    # Errors
    with pytest.raises(
        ValueError, match="bit field encoding cannot appear outside a structure"
    ):
        ctype_for_encoding(b"b8")

    with pytest.raises(
        ValueError, match="unknown encoding cannot appear outside of a pointer"
    ):
        ctype_for_encoding(b"?")


def test_encoding_for_ctype_error():
    """Test encoding_for_ctype error case (line 415)"""

    class UnregisteredType:
        pass

    with pytest.raises(ValueError, match="No type encoding known for ctype"):
        encoding_for_ctype(UnregisteredType)


def test_encoding_registration_management():
    """Test unregister functions and map getters (lines 492, 508, 525, 539-542, 549,
    556)"""

    # dummy registration
    class DummyType(Structure):
        _fields_ = [("x", c_int)]

    encoding = b"{Dummy=i}"
    # Use unregister_encoding_all to clean up first if exists
    unregister_encoding_all(encoding)

    from rubicon.objc.types import register_encoding

    register_encoding(encoding, DummyType)

    assert encoding in get_ctype_for_encoding_map()
    assert DummyType in get_encoding_for_ctype_map()

    unregister_encoding(encoding)
    assert encoding not in get_ctype_for_encoding_map()

    # Re-register and test all-unregister
    register_encoding(encoding, DummyType)
    unregister_encoding_all(encoding)
    assert encoding not in get_ctype_for_encoding_map()
    assert DummyType not in get_encoding_for_ctype_map()


def test_compound_value_errors():
    """Test compound_value_for_sequence errors (lines 598, 620, 660)"""

    class MyStruct(Structure):
        _fields_ = [("x", c_int), ("y", c_int)]

    with pytest.raises(
        ValueError, match="has 2 fields, but a sequence of length 1 was given"
    ):
        compound_value_for_sequence([1], MyStruct)

    MyArray = c_int * 3
    with pytest.raises(
        ValueError, match="has 3 fields, but a sequence of length 2 was given"
    ):
        compound_value_for_sequence([1, 2], MyArray)

    with pytest.raises(TypeError, match="Don't know how to convert a sequence"):
        compound_value_for_sequence([1], c_int)


def test_maker_functions():
    """Test maker functions (lines 888, 893, 903, 908, 913, 938)"""
    assert isinstance(NSMakeSize(1, 2), NSSize)
    assert isinstance(CGSizeMake(1, 2), CGSize)
    assert isinstance(NSMakeRect(1, 2, 3, 4), NSRect)
    assert isinstance(CGRectMake(1, 2, 3, 4), CGRect)
    assert isinstance(NSMakePoint(1, 2), NSPoint)
    assert isinstance(CGPointMake(1, 2), CGPoint)
    assert isinstance(UIEdgeInsetsMake(1, 2, 3, 4), UIEdgeInsets)
