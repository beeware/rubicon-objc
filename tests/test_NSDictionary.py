from __future__ import annotations

import pytest

from rubicon.objc import (
    NSDictionary,
    NSMutableDictionary,
    NSObject,
    ObjCClass,
    objc_method,
    objc_property,
)
from rubicon.objc.collections import ObjCDictInstance

PY_DICT = {
    "one": "ONE",
    "two": "TWO",
    "three": "THREE",
}


def make_ns_dictionary(contents=None):
    d = NSMutableDictionary.alloc().init()
    if contents is not None:
        for key, value in contents.items():
            d.setObject_forKey_(value, key)

    return NSDictionary.dictionaryWithDictionary(d)


def make_ns_mutable_dictionary(contents=None):
    d = NSMutableDictionary.alloc().init()
    if contents is not None:
        for key, value in contents.items():
            d.setObject_forKey_(value, key)

    return d


@pytest.mark.parametrize(
    "make_dictionary", [make_ns_dictionary, make_ns_mutable_dictionary]
)
def test_getitem(make_dictionary):
    d = make_dictionary(PY_DICT)

    for key, value in PY_DICT.items():
        assert d[key] == value

    with pytest.raises(KeyError):
        d["NO SUCH KEY"]


@pytest.mark.parametrize(
    "make_dictionary", [make_ns_dictionary, make_ns_mutable_dictionary]
)
def test_iter(make_dictionary):
    d = make_dictionary(PY_DICT)

    keys = set(PY_DICT)
    for k in d:
        keys.remove(str(k))

    assert len(keys) == 0


@pytest.mark.parametrize(
    "make_dictionary", [make_ns_dictionary, make_ns_mutable_dictionary]
)
def test_len(make_dictionary):
    d = make_dictionary(PY_DICT)
    assert len(d) == len(PY_DICT)


@pytest.mark.parametrize(
    "make_dictionary", [make_ns_dictionary, make_ns_mutable_dictionary]
)
def test_get(make_dictionary):
    d = make_dictionary(PY_DICT)

    assert d.get("one") == "ONE"
    assert d.get("two", None) == "TWO"
    assert d.get("four", None) is None
    assert d.get("five", 5) == 5
    assert d.get("six", None) is None


@pytest.mark.parametrize(
    "make_dictionary", [make_ns_dictionary, make_ns_mutable_dictionary]
)
def test_contains(make_dictionary):
    d = make_dictionary(PY_DICT)
    for key in PY_DICT:
        assert key in d


@pytest.mark.parametrize(
    "make_dictionary", [make_ns_dictionary, make_ns_mutable_dictionary]
)
def test_copy(make_dictionary):
    d = make_dictionary(PY_DICT)
    e = d.copy()
    assert e == d
    assert e == PY_DICT


@pytest.mark.parametrize(
    "make_dictionary", [make_ns_dictionary, make_ns_mutable_dictionary]
)
def test_equivalence(make_dictionary):
    d1 = make_dictionary(PY_DICT)
    d2 = make_dictionary(PY_DICT)
    smaller_py_dict = PY_DICT.copy()
    del smaller_py_dict["three"]
    bigger_py_dict = {"four": "FOUR"}
    bigger_py_dict.update(PY_DICT)

    assert d1 == PY_DICT
    assert d2 == PY_DICT
    assert d1 == d2
    assert PY_DICT == d1
    assert PY_DICT == d2
    assert d2 == d1

    assert d1 != object()
    assert d1 != {}
    assert d1 != smaller_py_dict
    assert d1 != bigger_py_dict


@pytest.mark.parametrize(
    "make_dictionary", [make_ns_dictionary, make_ns_mutable_dictionary]
)
def test_keys(make_dictionary):
    a = make_dictionary(PY_DICT)
    for k1, k2 in zip(
        sorted(a.keys()),
        sorted(PY_DICT.keys()),
        strict=True,
    ):
        assert k1 == k2


@pytest.mark.parametrize(
    "make_dictionary", [make_ns_dictionary, make_ns_mutable_dictionary]
)
def test_values(make_dictionary):
    a = make_dictionary(PY_DICT)
    for v1, v2 in zip(
        sorted(a.values()),
        sorted(PY_DICT.values()),
        strict=True,
    ):
        assert v1 == v2


@pytest.mark.parametrize(
    "make_dictionary", [make_ns_dictionary, make_ns_mutable_dictionary]
)
def test_items(make_dictionary):
    d = make_dictionary(PY_DICT)
    for i1, i2 in zip(
        sorted(d.items()),
        sorted(PY_DICT.items()),
        strict=True,
    ):
        assert i1[0] == i2[0]
        assert i1[1] == i2[1]


@pytest.mark.parametrize(
    "make_dictionary", [make_ns_dictionary, make_ns_mutable_dictionary]
)
def test_argument(make_dictionary):
    Example = ObjCClass("Example")
    example = Example.alloc().init()

    d = make_dictionary(PY_DICT)
    # Call a method with an NSDictionary instance
    assert example.processDictionary(d) is None
    # Call the same method with the raw Python dictionary
    assert example.processDictionary(PY_DICT) is None

    raw = {"data": "stuff", "other": "gadgets"}
    d = make_dictionary(raw)
    # Call a method with an NSDictionary instance
    assert example.processDictionary(d) == "stuff"
    # Call the same method with the raw Python dictionary
    assert example.processDictionary(raw) == "stuff"


@pytest.mark.parametrize(
    "make_dictionary", [make_ns_dictionary, make_ns_mutable_dictionary]
)
def test_property(make_dictionary):
    Example = ObjCClass("Example")
    example = Example.alloc().init()

    d = make_dictionary(PY_DICT)
    example.dict = d

    assert example.dict == PY_DICT
    assert isinstance(example.dict, ObjCDictInstance)
    assert example.dict["one"] == "ONE"


def test_ns_mutable_dictionary_setitem():
    d = make_ns_mutable_dictionary()
    for key, value in PY_DICT.items():
        d[key] = value

    for key, value in PY_DICT.items():
        assert d[key] == value


def test_ns_mutable_dictionary_del():
    d = make_ns_mutable_dictionary(PY_DICT)
    del d["one"]
    assert len(d) == 2
    with pytest.raises(KeyError):
        d["one"]


def test_ns_mutable_dictionary_clear():
    d = make_ns_mutable_dictionary(PY_DICT)
    d.clear()
    assert len(d) == 0


def test_ns_mutable_dictionary_copy():
    d = make_ns_mutable_dictionary(PY_DICT)
    e = d.copy()
    assert e == d
    assert e == PY_DICT

    e["four"] = "FOUR"


def test_ns_mutable_dictionary_pop1():
    d = make_ns_mutable_dictionary(PY_DICT)

    assert d.pop("one") == "ONE"
    assert len(d) == 2
    with pytest.raises(KeyError):
        d["one"]


def test_ns_mutable_dictionary_pop2():
    d = make_ns_mutable_dictionary(PY_DICT)

    with pytest.raises(KeyError):
        d.pop("four")


def test_ns_mutable_dictionary_pop3():
    d = make_ns_mutable_dictionary(PY_DICT)

    assert d.pop("four", 4) == 4


def test_ns_mutable_dictionary_popitem():
    d = make_ns_mutable_dictionary(PY_DICT)

    keys = set(PY_DICT)

    while len(d) > 0:
        key, value = d.popitem()
        assert str(key) in keys
        assert value == PY_DICT[str(key)]
        assert key not in d

    with pytest.raises(KeyError):
        d.popitem()


def test_ns_mutable_dictionary_setdefault1():
    d = make_ns_mutable_dictionary(PY_DICT)

    assert d.setdefault("one", "default") == "ONE"
    assert len(d) == len(PY_DICT)


def test_ns_mutable_dictionary_setdefault2():
    d = make_ns_mutable_dictionary(PY_DICT)

    assert "four" not in d
    assert d.setdefault("four", "FOUR") == "FOUR"
    assert len(d) == (len(PY_DICT) + 1)
    assert d["four"] == "FOUR"


def test_ns_mutable_dictionary_setdefault3():
    d = make_ns_mutable_dictionary(PY_DICT)

    assert "four" not in d
    assert d.setdefault("four") is None
    assert len(d) == len(PY_DICT)
    with pytest.raises(KeyError):
        d["four"]


def test_ns_mutable_dictionary_update1():
    d = make_ns_mutable_dictionary(PY_DICT)

    assert d == PY_DICT
    d.update({"one": "two", "three": "four", "four": "FIVE"})
    assert d != PY_DICT
    assert d["one"] == "two"
    assert d["two"] == "TWO"
    assert d["three"] == "four"
    assert d["four"] == "FIVE"
    assert len(d) == (len(PY_DICT) + 1)


def test_ns_mutable_dictionary_update2():
    d = make_ns_mutable_dictionary(PY_DICT)

    assert d == PY_DICT
    d.update([("one", "two"), ("three", "four"), ("four", "FIVE")])
    assert d != PY_DICT
    assert d["one"] == "two"
    assert d["two"] == "TWO"
    assert d["three"] == "four"
    assert len(d) == (len(PY_DICT) + 1)


def test_ns_mutable_dictionary_update3():
    d = make_ns_mutable_dictionary(PY_DICT)

    assert d == PY_DICT
    d.update(one="two", three="four", four="FIVE")
    assert d != PY_DICT
    assert d["one"] == "two"
    assert d["two"] == "TWO"
    assert d["three"] == "four"
    assert d["four"] == "FIVE"
    assert len(d) == (len(PY_DICT) + 1)


def test_ns_mutable_dictionary_update4():
    d = make_ns_mutable_dictionary(PY_DICT)

    assert d == PY_DICT
    d.update({"one": "two"}, three="four", four="FIVE")
    assert d != PY_DICT
    assert d["one"] == "two"
    assert d["two"] == "TWO"
    assert d["three"] == "four"
    assert d["four"] == "FIVE"
    assert len(d) == (len(PY_DICT) + 1)


def test_python_object_primitive_dict_attribute():
    class PrimitiveDictAttrContainer(NSObject):
        @objc_method
        def init(self):
            self.data = {1: 2, 2: 4, 3: 6}
            return self

        @objc_method
        def initWithDict_(self, data):
            self.data = data
            return self

    obj1 = PrimitiveDictAttrContainer.alloc().init()
    assert obj1.data == {1: 2, 2: 4, 3: 6}
    assert isinstance(obj1.data, dict)

    # If it's set through a method call, it becomes an objc instance
    obj2 = PrimitiveDictAttrContainer.alloc().initWithDict_({4: 8, 5: 10, 6: 12})
    assert obj2.data == {4: 8, 5: 10, 6: 12}
    assert isinstance(obj2.data, ObjCDictInstance)

    # If it's set by direct attribute access, it becomes a Python object.
    obj2.data = {7: 14, 8: 16, 9: 18}
    assert obj2.data == {7: 14, 8: 16, 9: 18}
    assert isinstance(obj2.data, dict)


def test_python_object_primitive_dict_property():
    class PrimitiveDictContainer(NSObject):
        data = objc_property()

        @objc_method
        def init(self):
            self.data = {1: 2, 2: 4, 3: 6}
            return self

        @objc_method
        def initWithDict_(self, data):
            self.data = data
            return self

    obj1 = PrimitiveDictContainer.alloc().init()
    assert obj1.data == {1: 2, 2: 4, 3: 6}
    assert isinstance(obj1.data, ObjCDictInstance)

    obj2 = PrimitiveDictContainer.alloc().initWithDict_({4: 8, 5: 10, 6: 12})
    assert obj2.data == {4: 8, 5: 10, 6: 12}
    assert isinstance(obj2.data, ObjCDictInstance)

    obj2.data = {7: 14, 8: 16, 9: 18}
    assert obj2.data == {7: 14, 8: 16, 9: 18}
    assert isinstance(obj2.data, ObjCDictInstance)


def test_python_object_object_dict_attribute():
    class ObjectDictAttrContainer(NSObject):
        @objc_method
        def init(self):
            self.data = {"x": "x1", "y": "y2", "z": "z3"}
            return self

        @objc_method
        def initWithDict_(self, data):
            self.data = data
            return self

    obj1 = ObjectDictAttrContainer.alloc().init()
    assert obj1.data == {"x": "x1", "y": "y2", "z": "z3"}
    assert isinstance(obj1.data, dict)

    # If it's set through a method call, it becomes an objc instance
    obj2 = ObjectDictAttrContainer.alloc().initWithDict_(
        {"a": "a4", "b": "b5", "c": "c6"}
    )
    assert obj2.data == {"a": "a4", "b": "b5", "c": "c6"}
    assert isinstance(obj2.data, ObjCDictInstance)

    # If it's set by direct attribute access, it becomes a Python object.
    obj2.data = {"i": "i7", "j": "j8", "k": "k9"}
    assert obj2.data == {"i": "i7", "j": "j8", "k": "k9"}
    assert isinstance(obj2.data, dict)


def test_python_object_object_dict_property():
    class ObjectDictContainer(NSObject):
        data = objc_property()

        @objc_method
        def init(self):
            self.data = {"x": "x1", "y": "y2", "z": "z3"}
            return self

        @objc_method
        def initWithDict_(self, data):
            self.data = data
            return self

    obj1 = ObjectDictContainer.alloc().init()
    assert obj1.data == {"x": "x1", "y": "y2", "z": "z3"}
    assert isinstance(obj1.data, ObjCDictInstance)

    obj2 = ObjectDictContainer.alloc().initWithDict_({"a": "a4", "b": "b5", "c": "c6"})
    assert obj2.data == {"a": "a4", "b": "b5", "c": "c6"}
    assert isinstance(obj2.data, ObjCDictInstance)

    obj2.data = {"i": "i7", "j": "j8", "k": "k9"}
    assert obj2.data == {"i": "i7", "j": "j8", "k": "k9"}
    assert isinstance(obj2.data, ObjCDictInstance)


def test_python_object_multitype_dict_property():
    class MultitypeDictContainer(NSObject):
        data = objc_property()

    # All types can be stored in a dict.
    obj = MultitypeDictContainer.alloc().init()
    obj.data = {4: 16, True: False, "Hello": "Goodbye"}
    assert obj.data == {4: 16, True: False, "Hello": "Goodbye"}
    assert isinstance(obj.data, ObjCDictInstance)
