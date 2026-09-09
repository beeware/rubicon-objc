from __future__ import annotations

from ctypes import (
    POINTER,
    Structure,
    Union,
    c_byte,
    c_char_p,
    c_double,
    c_int,
    c_uint,
    c_void_p,
    sizeof,
)

import pytest

import rubicon.objc.types
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
    _end_of_encoding,
    compound_value_for_sequence,
    ctype_for_encoding,
    ctype_for_type,
    ctypes_for_method_encoding,
    encoding_for_ctype,
    get_ctype_for_encoding_map,
    get_ctype_for_type_map,
    get_encoding_for_ctype_map,
    register_ctype_for_type,
    register_preferred_encoding,
    split_method_encoding,
    unregister_ctype,
    unregister_ctype_all,
    unregister_ctype_for_type,
    unregister_encoding,
    unregister_encoding_all,
)


@pytest.fixture
def clean_registries():
    """Restore the global type and encoding registries after the test."""
    registries = (
        rubicon.objc.types._ctype_for_type_map,
        rubicon.objc.types._ctype_for_encoding_map,
        rubicon.objc.types._encoding_for_ctype_map,
    )
    saved = [dict(registry) for registry in registries]

    yield

    for registry, contents in zip(registries, saved, strict=True):
        registry.clear()
        registry.update(contents)


class UnregisteredType:
    """A Python type that has no registered ctype."""


class UnregisteredStruct(Structure):
    """A ctypes structure that has no registered type encoding."""

    _fields_ = [("spam", c_int)]


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


@pytest.mark.parametrize(
    "make, args, expected",
    [
        pytest.param(NSMakeSize, (1.5, 2.5), NSSize(1.5, 2.5), id="NSMakeSize"),
        pytest.param(CGSizeMake, (1.5, 2.5), CGSize(1.5, 2.5), id="CGSizeMake"),
        pytest.param(NSMakePoint, (1.5, 2.5), NSPoint(1.5, 2.5), id="NSMakePoint"),
        pytest.param(CGPointMake, (1.5, 2.5), CGPoint(1.5, 2.5), id="CGPointMake"),
        pytest.param(
            NSMakeRect,
            (1.5, 2.5, 3.5, 4.5),
            NSRect(NSPoint(1.5, 2.5), NSSize(3.5, 4.5)),
            id="NSMakeRect",
        ),
        pytest.param(
            CGRectMake,
            (1.5, 2.5, 3.5, 4.5),
            CGRect(CGPoint(1.5, 2.5), CGSize(3.5, 4.5)),
            id="CGRectMake",
        ),
        pytest.param(
            UIEdgeInsetsMake,
            (0.0, 1.1, 2.2, 3.3),
            UIEdgeInsets(0.0, 1.1, 2.2, 3.3),
            id="UIEdgeInsetsMake",
        ),
    ],
)
def test_make_function(make, args, expected):
    """A Make function builds the same struct as the corresponding constructor.

    Structs are compared by their raw bytes, because ctypes structs of equal value don't
    compare equal to each other.
    """
    made = make(*args)

    assert type(made) is type(expected)
    assert bytes(made) == bytes(expected)


def test_ctype_for_type_unregistered():
    """An unregistered type is returned unchanged."""
    assert ctype_for_type(UnregisteredType) is UnregisteredType


def test_register_ctype_for_type(clean_registries):
    """A type-to-ctype conversion can be registered and unregistered."""
    register_ctype_for_type(UnregisteredType, c_int)

    assert ctype_for_type(UnregisteredType) is c_int
    assert get_ctype_for_type_map()[UnregisteredType] is c_int

    unregister_ctype_for_type(UnregisteredType)

    assert ctype_for_type(UnregisteredType) is UnregisteredType
    assert UnregisteredType not in get_ctype_for_type_map()


def test_get_ctype_for_type_map_is_a_copy(clean_registries):
    """Modifying the returned type map doesn't affect the registry."""
    type_map = get_ctype_for_type_map()
    type_map[UnregisteredType] = c_int

    assert ctype_for_type(UnregisteredType) is UnregisteredType


def test_get_encoding_maps_are_copies(clean_registries):
    """Modifying the returned encoding maps doesn't affect the registries."""
    ctype_map = get_ctype_for_encoding_map()
    encoding_map = get_encoding_for_ctype_map()

    assert ctype_map[b"i"] is c_int
    assert encoding_map[c_double] == b"d"

    ctype_map[b"i"] = c_double
    encoding_map[c_double] = b"i"

    assert ctype_for_encoding(b"i") is c_int
    assert encoding_for_ctype(c_double) == b"d"


def test_unregister_encoding(clean_registries):
    """Unregistering an encoding leaves the reverse conversion in place."""
    register_preferred_encoding(b"{Spam=i}", UnregisteredStruct)

    unregister_encoding(b"{Spam=i}")

    assert ctype_for_encoding(b"{Spam=i}") is not UnregisteredStruct
    assert encoding_for_ctype(UnregisteredStruct) == b"{Spam=i}"


def test_unregister_unknown_encoding(clean_registries):
    """Unregistering an unknown encoding does nothing."""
    unregister_encoding(b"{unknown=i}")


def test_unregister_unknown_encoding_all(clean_registries):
    """Unregistering an unknown encoding and all its ctypes does nothing."""
    unregister_encoding_all(b"{unknown=i}")


def test_unregister_ctype(clean_registries):
    """Unregistering a ctype currently fails.

    `unregister_ctype()` passes the default value to `dict.pop()` as a keyword argument,
    which `dict.pop()` doesn't accept.
    """
    register_preferred_encoding(b"{Spam=i}", UnregisteredStruct)

    with pytest.raises(TypeError, match="takes no keyword arguments"):
        unregister_ctype(UnregisteredStruct)


def test_unregister_ctype_all(clean_registries):
    """Unregistering a ctype and all its encodings fails the same way."""
    register_preferred_encoding(b"{Spam=i}", UnregisteredStruct)

    with pytest.raises(TypeError, match="takes no keyword arguments"):
        unregister_ctype_all(UnregisteredStruct)


def test_unregister_encoding_all(clean_registries):
    """Unregistering an encoding and all its ctypes fails the same way.

    It unregisters every ctype registered for the encoding with
    `unregister_ctype_all()`.
    """
    register_preferred_encoding(b"{Spam=i}", UnregisteredStruct)

    with pytest.raises(TypeError, match="takes no keyword arguments"):
        unregister_encoding_all(b"{Spam=i}")


@pytest.mark.parametrize(
    "encoding, expected",
    [
        pytest.param(b"Ni", c_int, id="inout-qualifier"),
        pytest.param(b"ri", c_int, id="const-qualifier"),
        pytest.param(b"^d", POINTER(c_double), id="pointer"),
        pytest.param(b"[4i]", c_int * 4, id="array"),
        pytest.param(b'@"NSString"', ctype_for_encoding(b"@"), id="class-name"),
        pytest.param(b"@?<v@?>", ctype_for_encoding(b"@?"), id="block-signature"),
    ],
)
def test_ctype_for_encoding(clean_registries, encoding, expected):
    """A compound encoding is converted to the expected ctype."""
    assert ctype_for_encoding(encoding) == expected


def test_ctype_for_encoding_structure(clean_registries):
    """A structure encoding is converted to a ctypes.Structure subclass."""
    struct = ctype_for_encoding(b"{unnamed_fields=ic}")

    assert issubclass(struct, Structure)
    assert struct.__name__ == "unnamed_fields"
    assert not struct.__anonymous__
    assert struct._fields_ == [("field_0", c_int), ("field_1", c_byte)]


def test_ctype_for_encoding_structure_named_fields(clean_registries):
    """Field names in a structure encoding are used for the ctypes fields."""
    struct = ctype_for_encoding(b'{named_fields="spam"i"ham"c}')

    assert struct._fields_ == [("spam", c_int), ("ham", c_byte)]


def test_ctype_for_encoding_structure_bit_fields(clean_registries):
    """Bit fields in a structure encoding are converted to ctypes bit fields."""
    struct = ctype_for_encoding(b"{bit_fields=b1b7}")

    assert struct._fields_ == [("field_0", c_uint, 1), ("field_1", c_uint, 7)]


def test_ctype_for_encoding_structure_anonymous(clean_registries):
    """A structure encoding without a name is converted to an anonymous type."""
    struct = ctype_for_encoding(b"{?=ic}")

    assert struct.__name__ == "_Anonymous"
    assert struct.__anonymous__


def test_ctype_for_encoding_structure_recursive(clean_registries):
    """A structure that contains a pointer to itself is converted correctly."""
    struct = ctype_for_encoding(b"{node=i^{node}}")

    assert struct._fields_[0] == ("field_0", c_int)
    assert struct._fields_[1][1] is POINTER(struct)


def test_ctype_for_encoding_structure_without_fields(clean_registries):
    """A structure whose fields are unknown is treated as a void."""
    assert ctype_for_encoding(b"{fieldless}") is None
    assert ctype_for_encoding(b"^{fieldless}") is c_void_p


def test_ctype_for_encoding_union(clean_registries):
    """A union encoding is converted to a ctypes.Union subclass."""
    union = ctype_for_encoding(b"(spam_union=ic)")

    assert issubclass(union, Union)
    assert union._fields_ == [("field_0", c_int), ("field_1", c_byte)]
    assert sizeof(union) == sizeof(c_int)


def test_ctype_for_encoding_is_registered(clean_registries):
    """A newly created ctype is registered for its encoding and for its name."""
    struct = ctype_for_encoding(b"{registered=ic}")

    assert ctype_for_encoding(b"{registered=ic}") is struct
    assert ctype_for_encoding(b"{registered}") is struct


@pytest.mark.parametrize(
    "encoding, message",
    [
        (b"b8", "A bit field encoding cannot appear outside a structure"),
        (b"?", "An unknown encoding cannot appear outside of a pointer"),
        (b"T", "128-bit integers are not supported by ctypes"),
        (b"t", "128-bit integers are not supported by ctypes"),
        (b"j", "Complex numbers are not supported by ctypes"),
        (b"A", "Atomic types are not supported by ctypes"),
        (b"X", "Unknown encoding"),
        (b"^X", "Unknown encoding"),
    ],
)
def test_ctype_for_unknown_encoding(clean_registries, encoding, message):
    """An encoding that cannot be converted raises a ValueError."""
    with pytest.raises(ValueError, match=message):
        ctype_for_encoding(encoding)


def test_encoding_for_ctype_pointer():
    """The encoding of an unregistered pointer type is derived from its target."""
    assert encoding_for_ctype(POINTER(POINTER(c_int))) == b"^^i"


def test_encoding_for_unknown_ctype():
    """A ctype that cannot be converted raises an error.

    The documented error is a `ValueError`, but a type without a known encoding is
    assumed to be a pointer type, so the missing `_type_` attribute surfaces as an
    `AttributeError` before the `ValueError` can be raised.
    """
    with pytest.raises(AttributeError, match="has no attribute '_type_'"):
        encoding_for_ctype(UnregisteredStruct)


@pytest.mark.parametrize(
    "encoding, expected",
    [
        pytest.param(b"v@:", [b"v", b"@", b":"], id="no-arguments"),
        pytest.param(b"v12@0:4i8", [b"v", b"@", b":", b"i"], id="legacy-stack-offsets"),
        pytest.param(
            b'@"NSString"@:@?<v@?>{spam=ic}',
            [b'@"NSString"', b"@", b":", b"@?<v@?>", b"{spam=ic}"],
            id="compound-encodings",
        ),
        pytest.param(b"v@:^i", [b"v", b"@", b":", b"^i"], id="pointer-argument"),
    ],
)
def test_split_method_encoding(encoding, expected):
    """A method signature encoding is split into its type encodings."""
    assert split_method_encoding(encoding) == expected


def test_ctypes_for_method_encoding(clean_registries):
    """A method signature encoding is converted to a sequence of ctypes."""
    assert ctypes_for_method_encoding(b"*8@0:4i") == [
        c_char_p,
        ctype_for_encoding(b"@"),
        ctype_for_encoding(b":"),
        c_int,
    ]


@pytest.mark.parametrize("start", [-1, 1, 100])
def test_end_of_encoding_start_out_of_range(start):
    """A start index outside of the encoding raises a ValueError."""
    with pytest.raises(ValueError, match="not in range"):
        _end_of_encoding(b"i", start)


@pytest.mark.parametrize(
    "encoding, expected",
    [
        pytest.param(b"b8i", 2, id="bit-field-before-next-encoding"),
        pytest.param(b"b8", 2, id="bit-field-at-end-of-string"),
        pytest.param(b"@i", 1, id="object-pointer"),
        pytest.param(b"@?i", 2, id="block"),
    ],
)
def test_end_of_encoding(encoding, expected):
    """The end of the encoding starting at index 0 is found correctly."""
    assert _end_of_encoding(encoding, 0) == expected


@pytest.mark.parametrize(
    "encoding, message",
    [
        (b"X", "Unknown encoding"),
        (b"{spam=i", "Incomplete encoding, missing 1 closing parentheses"),
        (b"^", "Incomplete encoding, reached end of string too early"),
    ],
)
def test_end_of_encoding_invalid(encoding, message):
    """An invalid encoding raises a ValueError."""
    with pytest.raises(ValueError, match=message):
        _end_of_encoding(encoding, 0)


def test_compound_value_for_sequence_struct():
    """A sequence can be converted to a structure."""
    rect = compound_value_for_sequence([(1, 2), (3, 4)], NSRect)

    assert bytes(rect) == bytes(NSRect(NSPoint(1, 2), NSSize(3, 4)))


def test_compound_value_for_sequence_struct_wrong_length():
    """Converting a sequence of the wrong length to a structure is an error."""
    with pytest.raises(ValueError, match="has 2 fields, but a sequence of length 3"):
        compound_value_for_sequence([(1, 2), (3, 4), (5, 6)], NSRect)


def test_compound_value_for_sequence_array():
    """A sequence can be converted to an array."""
    array = compound_value_for_sequence([1, 2, 3], c_int * 3)

    assert list(array) == [1, 2, 3]


def test_compound_value_for_sequence_array_of_structs():
    """The elements of an array of structures are converted recursively."""
    array = compound_value_for_sequence([(1, 2), NSPoint(3, 4)], NSPoint * 2)

    assert bytes(array) == bytes((NSPoint * 2)(NSPoint(1, 2), NSPoint(3, 4)))


def test_compound_value_for_sequence_array_wrong_length():
    """Converting a sequence of the wrong length to an array is an error."""
    with pytest.raises(ValueError, match="has 3 fields, but a sequence of length 2"):
        compound_value_for_sequence([1, 2], c_int * 3)


def test_compound_value_for_sequence_not_compound():
    """A sequence can only be converted to a structure or array."""
    with pytest.raises(TypeError, match="Don't know how to convert a sequence"):
        compound_value_for_sequence([1], c_int)
