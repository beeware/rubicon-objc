from __future__ import annotations

import math
import re
import sys
from ctypes import (
    ArgumentError,
    c_void_p,
    cast,
)
from decimal import Decimal
from enum import Enum

import pytest

from rubicon.objc import (
    NSObject,
    ObjCClass,
    ObjCInstance,
    py_from_ns,
    types,
)
from rubicon.objc.api import get_method_family

from .conftest import (
    OSX_VERSION,
    struct_int_sized,
    struct_large,
    struct_oddly_sized,
)


def test_method():
    """An instance method can be invoked."""
    Example = ObjCClass("Example")

    obj = Example.alloc().init()

    assert obj.accessBaseIntField() == 22
    assert obj.accessIntField() == 33

    obj.mutateBaseIntFieldWithValue_(8888)
    obj.mutateIntFieldWithValue_(9999)

    assert obj.accessBaseIntField() == 8888
    assert obj.accessIntField() == 9999


def test_non_existent():
    """An attribute error is raised if you invoke a non-existent method."""
    Example = ObjCClass("Example")

    obj1 = Example.alloc().init()

    # Non-existent methods raise an error.
    with pytest.raises(AttributeError):
        obj1.method_doesnt_exist()

    # Cache warming doesn't affect anything.
    with pytest.raises(AttributeError):
        obj1.method_doesnt_exist()


def test_incorrect_argument_count():
    """Attempting to call a method with an incorrect number of arguments throws an
    exception."""

    Example = ObjCClass("Example")
    obj = Example.alloc().init()

    with pytest.raises(TypeError):
        obj.accessIntField("extra argument 1")

    with pytest.raises(TypeError):
        obj.mutateIntFieldWithValue_()

    with pytest.raises(TypeError):
        obj.mutateIntFieldWithValue_(123, "extra argument")


def test_incorrect_argument_type():
    """Attempting to call a method with the wrong type of argument throws an
    exception."""

    Example = ObjCClass("Example")
    obj = Example.alloc().init()

    with pytest.raises(
        ArgumentError,
        match=(
            r"mutateIntFieldWithValue: argument 3: "
            + (
                r"TypeError: 'float' object cannot be interpreted as an "
                r"integer; argtypes: c_int"
                if sys.version_info >= (3, 12)
                else (
                    r"TypeError: wrong type; argtypes: c_int"
                    if sys.version_info >= (3, 10)
                    else r"<class 'TypeError'>: wrong type; argtypes: c_int"
                )
            )
        ),
    ):
        obj.mutateIntFieldWithValue_(1.234)


def test_str_repr():
    """Test ObjCMethod, ObjCPartialMethod, and ObjCBoundMethod str and repr."""

    obj = NSObject.new()

    # ObjCMethod
    assert repr(obj.init.method) == "<ObjCMethod: init @16@0:8>"
    assert str(obj.init.method) == "<ObjCMethod: init @16@0:8>"

    # ObjCBoundMethod
    assert re.search(
        r"ObjCBoundMethod\(<ObjCMethod: init @16@0:8>, <NSObject: 0x[0-9a-f]+>\)",
        repr(obj.init),
    )
    assert re.search(
        r"ObjCBoundMethod\(<ObjCMethod: init @16@0:8>, <NSObject: 0x[0-9a-f]+>\)",
        str(obj.init),
    )

    # ObjCPartialMethod
    assert repr(obj.performSelector.method) == "ObjCPartialMethod('performSelector')"
    assert str(obj.performSelector.method) == "ObjCPartialMethod('performSelector')"


def test_float_method():
    """A method with a float argument can be handled."""
    Example = ObjCClass("Example")
    example = Example.alloc().init()
    assert example.areaOfSquare_(1.5) == 2.25


def test_double_method():
    """A method with a double argument can be handled."""
    Example = ObjCClass("Example")
    example = Example.alloc().init()
    assert example.areaOfCircle_(1.5) == pytest.approx(1.5 * math.pi)


@pytest.mark.skipif(
    OSX_VERSION and OSX_VERSION < (10, 10),
    reason="Property handling doesn't work on OS X 10.9 (Mavericks) and earlier",
)
def test_decimal_method():
    """A method with a NSDecimalNumber arguments can be handled."""
    Example = ObjCClass("Example")
    example = Example.alloc().init()

    result = example.areaOfTriangleWithWidth_andHeight_(Decimal("3.0"), Decimal("4.0"))
    assert isinstance(result, ObjCClass("NSDecimalNumber"))
    assert py_from_ns(result) == Decimal("6.0")


def test_static_method():
    """A static method on a class can be invoked."""
    Example = ObjCClass("Example")

    Example.mutateStaticBaseIntFieldWithValue_(2288)
    Example.mutateStaticIntFieldWithValue_(2299)

    assert Example.accessStaticBaseIntField() == 2288
    assert Example.accessStaticIntField() == 2299


def test_non_existent_static_method():
    """An attribute error is raised if you invoke a non-existent static method."""
    Example = ObjCClass("Example")

    # Non-existent methods raise an error.
    with pytest.raises(AttributeError):
        Example.static_method_doesnt_exist()

    # Cache warming doesn't affect anything.
    with pytest.raises(AttributeError):
        Example.static_method_doesnt_exist()


def test_mutator_like_method():
    """A method that looks like a mutator doesn't confuse issues."""
    Example = ObjCClass("Example")

    obj1 = Example.alloc().init()

    # setSpecialValue: looks like it might be a mutator
    # for a specialValue property, but this property doesn't exist.

    # We can invoke the method directly...
    obj1.setSpecialValue_(42)

    # ... but retrieving like a property is an error
    with pytest.raises(AttributeError):
        _ = obj1.specialValue

    # ...until you set it explicitly...
    obj1.specialValue = 37

    # ...at which point it's fair game to be retrieved.
    assert obj1.specialValue == 37


def test_string_argument():
    """A method with a string argument can be passed."""
    Example = ObjCClass("Example")
    example = Example.alloc().init()
    assert example.duplicateString_("Wagga") == "WaggaWagga"


def test_enum_argument():
    """An enumerated type can be used as an argument."""
    Example = ObjCClass("Example")

    obj = Example.alloc().init()

    assert obj.accessBaseIntField() == 22
    assert obj.accessIntField() == 33

    class MyEnum(Enum):
        value1 = 8888
        value2 = 9999
        value3 = 3333
        value4 = 4444

    obj.mutateBaseIntFieldWithValue_(MyEnum.value1)
    obj.mutateIntFieldWithValue_(MyEnum.value2)

    assert obj.accessBaseIntField() == MyEnum.value1.value
    assert obj.accessIntField() == MyEnum.value2.value

    obj.baseIntField = MyEnum.value3
    obj.intField = MyEnum.value4

    assert obj.accessBaseIntField() == MyEnum.value3.value
    assert obj.accessIntField() == MyEnum.value4.value


def test_string_return():
    """If a method or field returns a string, you get a Python string back."""
    Example = ObjCClass("Example")
    example = Example.alloc().init()
    assert example.toString() == "This is an ObjC Example object"


def test_constant_string_return():
    """If a method or field returns a *constant* string, you get a Python string
    back."""
    Example = ObjCClass("Example")
    example = Example.alloc().init()
    assert example.smiley() == "%-)"


def test_number_return():
    """If a method or field returns a NSNumber, it is not automatically converted to a
    Python number."""
    Example = ObjCClass("Example")
    example = Example.alloc().init()

    answer = example.theAnswer()
    assert isinstance(answer, ObjCInstance)
    assert py_from_ns(answer) == 42
    tau = example.twopi()
    assert isinstance(tau, ObjCInstance)
    assert py_from_ns(tau) == pytest.approx(2.0 * math.pi)


def test_auto_struct_creation():
    """Structs from method signatures are created automatically."""
    Example = ObjCClass("Example")

    types.unregister_encoding_all(b"{simple=ii}")
    types.unregister_encoding_all(b"{simple}")
    types.unregister_encoding_all(b"{complex=[4s]^?{simple=ii}^{complex}}")
    types.unregister_encoding_all(b"{complex}")

    # Look up the method, so the return/argument types are decoded
    # and the structs are registered.
    _ = Example.doStuffWithStruct_

    struct_simple = types.ctype_for_encoding(b"{simple=ii}")
    assert struct_simple == types.ctype_for_encoding(b"{simple}")

    simple = struct_simple(123, 456)
    ret = Example.doStuffWithStruct_(simple)
    struct_complex = types.ctype_for_encoding(b"{complex=[4s]^?{simple=ii}^{complex}}")
    assert isinstance(ret, struct_complex)
    assert struct_complex == types.ctype_for_encoding(b"{complex}")
    assert list(ret.field_0) == [1, 2, 3, 4]
    assert ret.field_1.value is None
    assert ret.field_2.field_0 == 123
    assert ret.field_2.field_1 == 456
    assert cast(ret.field_3, c_void_p).value is None


def test_sequence_arg_to_struct():
    """Sequence arguments are converted to structures."""
    Example = ObjCClass("Example")

    ret = Example.extractSimpleStruct(([9, 8, 7, 6], None, (987, 654), None))
    struct_simple = types.ctype_for_encoding(b"{simple=ii}")
    assert isinstance(ret, struct_simple)
    assert ret.field_0 == 987
    assert ret.field_1 == 654


def test_struct_return():
    """Methods returning structs of different sizes by value can be handled."""
    Example = ObjCClass("Example")
    example = Example.alloc().init()

    types.register_encoding(b"{int_sized=[4c]}", struct_int_sized)
    assert example.intSizedStruct().x == b"abc"

    types.register_encoding(b"{oddly_sized=[5c]}", struct_oddly_sized)
    assert example.oddlySizedStruct().x == b"abcd"

    types.register_encoding(b"{large=[17c]}", struct_large)
    assert example.largeStruct().x == b"abcdefghijklmnop"


def test_object_return():
    """If a method or field returns an object, you get an instance of that type
    returned."""
    Example = ObjCClass("Example")
    example = Example.alloc().init()

    Thing = ObjCClass("Thing")
    thing = Thing.alloc().initWithName_value_("This is thing", 2)

    example.thing = thing

    the_thing = example.thing
    assert the_thing.toString() == "This is thing 2"


def test_no_convert_return():
    Example = ObjCClass("Example")
    example = Example.alloc().init()

    res = example.toString(convert_result=False)
    assert not isinstance(res, ObjCInstance)
    assert str(ObjCInstance(res)) == "This is an ObjC Example object"


@pytest.mark.parametrize(
    ("method_name", "method_family"),
    [
        ("mutableCopy", "mutableCopy"),
        ("mutableCopy:", "mutableCopy"),
        ("_mutableCopy:", "mutableCopy"),
        ("_mutableCopy:with:", "mutableCopy"),
        ("_mutableCopyWith:", "mutableCopy"),
        ("_mutableCopy_with:", "mutableCopy"),
        ("_mutableCopying:", ""),
    ],
)
def test_get_method_family(method_name, method_family):
    assert get_method_family(method_name) == method_family
