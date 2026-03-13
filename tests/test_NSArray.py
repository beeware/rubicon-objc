from __future__ import annotations

import pytest

from rubicon.objc import (
    NSArray,
    NSMutableArray,
    NSObject,
    ObjCClass,
    objc_method,
    objc_property,
    py_from_ns,
)
from rubicon.objc.collections import ObjCListInstance

PY_LIST = ["one", "two", "three"]


def make_ns_array(contents=None):
    a = NSMutableArray.alloc().init()
    if contents is not None:
        for value in contents:
            a.addObject(value)

    return NSArray.arrayWithArray(a)


def make_ns_mutable_array(contents=None):
    a = NSMutableArray.alloc().init()
    if contents is not None:
        for value in contents:
            a.addObject(value)

    return a


@pytest.mark.parametrize(
    "make_array",
    [make_ns_array, make_ns_mutable_array],
)
def test_getitem(make_array):
    a = make_array(PY_LIST)

    for pos, value in enumerate(PY_LIST):
        assert a[pos] == value

    with pytest.raises(IndexError):
        a[len(PY_LIST) + 10]

    with pytest.raises(IndexError):
        a[-len(PY_LIST) - 1]


@pytest.mark.parametrize(
    "make_array",
    [make_ns_array, make_ns_mutable_array],
)
def test_len(make_array):
    a = make_array(PY_LIST)

    assert len(a) == len(PY_LIST)


@pytest.mark.parametrize(
    "make_array",
    [make_ns_array, make_ns_mutable_array],
)
def test_iter(make_array):
    a = make_array(PY_LIST)

    keys = list(PY_LIST)
    for k in a:
        assert k in keys
        keys.remove(k)

    assert len(keys) == 0


@pytest.mark.parametrize(
    "make_array",
    [make_ns_array, make_ns_mutable_array],
)
def test_contains(make_array):
    a = make_array(PY_LIST)
    for value in PY_LIST:
        assert value in a


@pytest.mark.parametrize(
    "make_array",
    [make_ns_array, make_ns_mutable_array],
)
def test_index(make_array):
    a = make_array(PY_LIST)
    assert a.index("two") == 1
    with pytest.raises(ValueError):
        a.index("umpteen")


@pytest.mark.parametrize(
    "make_array",
    [make_ns_array, make_ns_mutable_array],
)
def test_count(make_array):
    a = make_array(PY_LIST)
    assert a.count("one") == 1


@pytest.mark.parametrize(
    "make_array",
    [make_ns_array, make_ns_mutable_array],
)
def test_equivalence(make_array):
    a = make_array(PY_LIST)
    b = make_array(PY_LIST)

    assert a == PY_LIST
    assert b == PY_LIST
    assert a == b
    assert PY_LIST == a
    assert PY_LIST == b
    assert b == a

    assert a != object()
    assert a != []
    assert a != PY_LIST[:2]
    assert a != PY_LIST + ["spam", "ham"]


@pytest.mark.parametrize(
    "make_array",
    [make_ns_array, make_ns_mutable_array],
)
def test_slice_access(make_array):
    a = make_array(PY_LIST * 2)
    assert a[1:4] == ["two", "three", "one"]
    assert a[:-2] == ["one", "two", "three", "one"]
    assert a[4:] == ["two", "three"]
    assert a[1:5:2] == ["two", "one"]


@pytest.mark.parametrize(
    "make_array",
    [make_ns_array, make_ns_mutable_array],
)
def test_argument(make_array):
    Example = ObjCClass("Example")
    example = Example.alloc().init()

    a = make_array(PY_LIST)
    # Call a method with an NSArray instance
    assert example.processArray(a) == "two"
    # Call the same method with the Python list
    assert example.processArray(PY_LIST) == "two"


@pytest.mark.parametrize(
    "make_array",
    [make_ns_array, make_ns_mutable_array],
)
def test_property(make_array):
    Example = ObjCClass("Example")
    example = Example.alloc().init()

    a = make_array(PY_LIST)
    example.array = a

    assert example.array == PY_LIST
    assert isinstance(example.array, ObjCListInstance)
    assert example.array[1] == "two"


def test_ns_array_copy():
    a = make_ns_array(PY_LIST)
    b = a.copy()
    assert b == a
    assert b == PY_LIST

    with pytest.raises(AttributeError):
        b.append("four")


def test_ns_mutable_array_copy():
    a = make_ns_mutable_array(PY_LIST)
    b = a.copy()
    assert b == a
    assert b == PY_LIST

    b.append("four")


def test_ns_mutable_array_setitem():
    a = make_ns_mutable_array(PY_LIST)

    a[2] = "four"
    assert a[2] == "four"

    with pytest.raises(IndexError):
        a[len(a)] = "invalid"

    with pytest.raises(IndexError):
        a[-len(a) - 1] = "invalid"


def test_ns_mutable_array_del():
    a = make_ns_mutable_array(PY_LIST)
    del a[0]
    assert len(a) == 2
    assert a[0] == "two"

    with pytest.raises(IndexError):
        del a[len(a)]

    with pytest.raises(IndexError):
        del a[-len(a) - 1]


def test_ns_mutable_array_append():
    a = make_ns_mutable_array()
    a.append("an item")
    assert "an item" in a


def test_ns_mutable_array_extend():
    a = make_ns_mutable_array()
    a.extend(["an item", "another item"])
    assert "an item" in a
    assert "another item" in a


def test_ns_mutable_array_clear():
    a = make_ns_mutable_array(PY_LIST)
    a.clear()
    assert len(a) == 0


def test_ns_mutable_array_count():
    a = make_ns_mutable_array(PY_LIST)
    assert a.count("one") == 1

    a.append("one")
    assert a.count("one") == 2


def test_ns_mutable_array_insert():
    a = make_ns_mutable_array(PY_LIST)
    a.insert(1, "four")
    assert a[0] == "one"
    assert a[1] == "four"
    assert a[2] == "two"


def test_ns_mutable_array_pop():
    a = make_ns_mutable_array(PY_LIST)
    assert a.pop() == "three"
    assert a.pop(0) == "one"
    assert len(a) == 1
    assert a[0] == "two"


def test_ns_mutable_array_remove():
    a = make_ns_mutable_array(PY_LIST)
    a.remove("three")
    assert len(a) == 2
    assert a[-1] == "two"
    with pytest.raises(ValueError):
        a.remove("umpteen")


def test_ns_mutable_array_slice_assignment1():
    a = make_ns_mutable_array(PY_LIST * 2)
    a[2:4] = ["four", "five"]
    assert a == ["one", "two", "four", "five", "two", "three"]


def test_ns_mutable_array_slice_assignment2():
    a = make_ns_mutable_array(PY_LIST * 2)
    a[::2] = ["four", "five", "six"]
    assert a == ["four", "two", "five", "one", "six", "three"]


def test_ns_mutable_array_slice_assignment3():
    a = make_ns_mutable_array(PY_LIST * 2)
    a[2:4] = ["four"]
    assert a == ["one", "two", "four", "two", "three"]


def test_ns_mutable_array_bad_slice_assignment1():
    a = make_ns_mutable_array(PY_LIST * 2)

    with pytest.raises(TypeError):
        a[2:4] = 4


def test_ns_mutable_array_bad_slice_assignment2():
    a = make_ns_mutable_array(PY_LIST * 2)

    with pytest.raises(ValueError):
        a[::2] = [4]


def test_ns_mutable_array_del_slice1():
    a = make_ns_mutable_array(PY_LIST * 2)
    del a[-2:]
    assert len(a) == 4
    assert a[0] == "one"
    assert a[-1] == "one"


def test_ns_mutable_array_del_slice2():
    a = make_ns_mutable_array(PY_LIST * 2)
    del a[::2]
    assert len(a) == 3
    assert a[0] == "two"
    assert a[1] == "one"
    assert a[2] == "three"


def test_ns_mutable_array_del_slice3():
    a = make_ns_mutable_array(PY_LIST * 2)
    del a[::-2]
    assert len(a) == 3
    assert a[0] == "one"
    assert a[1] == "three"
    assert a[2] == "two"


def test_ns_mutable_array_reverse():
    a = make_ns_mutable_array(PY_LIST)
    a.reverse()

    for pos, value in enumerate(reversed(PY_LIST)):
        assert a[pos] == value


def test_python_object_primitive_list_attribute():
    class PrimitiveListAttrContainer(NSObject):
        @objc_method
        def init(self):
            self.data = [1, 2, 3]
            return self

        @objc_method
        def initWithList_(self, data):
            self.data = data
            return self

    obj1 = PrimitiveListAttrContainer.alloc().init()
    assert obj1.data == [1, 2, 3]
    assert isinstance(obj1.data, list)

    # If it's set through a method call, it becomes an objc instance
    obj2 = PrimitiveListAttrContainer.alloc().initWithList_([4, 5, 6])
    assert isinstance(obj2.data, ObjCListInstance)
    assert py_from_ns(obj2.data) == [4, 5, 6]

    # If it's set by direct attribute access, it becomes a Python object.
    obj2.data = [7, 8, 9]
    assert isinstance(obj2.data, list)
    assert obj2.data == [7, 8, 9]


def test_python_object_primitive_list_property():
    class PrimitiveListContainer(NSObject):
        data = objc_property()

        @objc_method
        def init(self):
            self.data = [1, 2, 3]
            return self

        @objc_method
        def initWithList_(self, data):
            self.data = data
            return self

    obj1 = PrimitiveListContainer.alloc().init()
    assert isinstance(obj1.data, ObjCListInstance)
    assert py_from_ns(obj1.data) == [1, 2, 3]

    obj2 = PrimitiveListContainer.alloc().initWithList_([4, 5, 6])
    assert isinstance(obj2.data, ObjCListInstance)
    assert py_from_ns(obj2.data) == [4, 5, 6]

    obj2.data = [7, 8, 9]
    assert isinstance(obj2.data, ObjCListInstance)
    assert py_from_ns(obj2.data) == [7, 8, 9]


def test_python_object_object_list_attribute():
    class ObjectListAttrContainer(NSObject):
        @objc_method
        def init(self):
            self.data = ["x1", "y2", "z3"]
            return self

        @objc_method
        def initWithList_(self, data):
            self.data = data
            return self

    obj1 = ObjectListAttrContainer.alloc().init()
    assert obj1.data == ["x1", "y2", "z3"]
    assert isinstance(obj1.data, list)

    # If it's set through a method call, it becomes an objc instance
    obj2 = ObjectListAttrContainer.alloc().initWithList_(["a4", "b5", "c6"])
    assert obj2.data == ["a4", "b5", "c6"]
    assert isinstance(obj2.data, ObjCListInstance)

    # If it's set by direct attribute access, it becomes a Python object.
    obj2.data = ["i7", "j8", "k9"]
    assert obj2.data == ["i7", "j8", "k9"]
    assert isinstance(obj2.data, list)


def test_python_object_object_list_property():
    class ObjectListContainer(NSObject):
        data = objc_property()

        @objc_method
        def init(self):
            self.data = ["x1", "y2", "z3"]
            return self

        @objc_method
        def initWithList_(self, data):
            self.data = data
            return self

    obj1 = ObjectListContainer.alloc().init()
    assert obj1.data == ["x1", "y2", "z3"]
    assert isinstance(obj1.data, ObjCListInstance)

    obj2 = ObjectListContainer.alloc().initWithList_(["a4", "b5", "c6"])
    assert obj2.data == ["a4", "b5", "c6"]
    assert isinstance(obj2.data, ObjCListInstance)

    obj2.data = ["i7", "j8", "k9"]
    assert obj2.data == ["i7", "j8", "k9"]
    assert isinstance(obj2.data, ObjCListInstance)


def test_python_object_multitype_list_property():
    class MultitypeListContainer(NSObject):
        data = objc_property()

    Example = ObjCClass("Example")
    example = Example.alloc().init()

    # All types can be stored in a list.
    obj = MultitypeListContainer.alloc().init()

    obj.data = [4, True, "Hello", example]
    assert isinstance(obj.data, ObjCListInstance)
    assert py_from_ns(obj.data) == [4, True, "Hello", example]
