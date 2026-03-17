from __future__ import annotations

from rubicon.objc import (
    CFRange,
    CGPoint,
    CGRect,
    CGSize,
    NSEdgeInsets,
    NSEdgeInsetsMake,
    NSPoint,
    NSRange,
    NSRect,
    NSSize,
    UIEdgeInsets,
)
from rubicon.objc.types import __LP64__


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
