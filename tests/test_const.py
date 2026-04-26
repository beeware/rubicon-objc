from __future__ import annotations

from rubicon.objc import objc_const

from .conftest import rubiconharness


def test_objc_const():
    """objc_const works."""
    string_const = objc_const(rubiconharness, "SomeGlobalStringConstant")
    assert str(string_const) == "Some global string constant"
