from __future__ import annotations

import functools
import gc
import weakref
from ctypes import c_int

import pytest

from rubicon.objc import (
    NSMakeRect,
    NSObject,
    NSObjectProtocol,
    NSRect,
    ObjCClass,
    ObjCInstance,
    ObjCMetaClass,
    ObjCProtocol,
    at,
    objc_classmethod,
    objc_ivar,
    objc_method,
    objc_property,
)
from rubicon.objc.runtime import (
    autoreleasepool,
    get_ivar,
    libobjc,
    objc_id,
    set_ivar,
)

NSArray = ObjCClass("NSArray")
NSString = ObjCClass("NSString")


def test_by_name():
    """An Objective-C class can be looked up by name."""

    Example = ObjCClass("Example")
    assert Example.name == "Example"


def test_caching():
    """ObjCClass instances are cached."""

    Example1 = ObjCClass("Example")
    Example2 = ObjCClass("Example")

    assert Example1 is Example2


def test_by_pointer():
    """An Objective-C class can be created from a pointer."""

    example_ptr = libobjc.objc_getClass(b"Example")
    Example = ObjCClass(example_ptr)
    assert Example is ObjCClass("Example")


def test_nonexistant():
    """A NameError is raised if a class doesn't exist."""

    with pytest.raises(NameError):
        ObjCClass("DoesNotExist")


def test_produce_objcmetaclass():
    """Creating an ObjCClass for a metaclass pointer gives an ObjCMetaclass."""

    examplemeta_ptr = libobjc.objc_getMetaClass(b"Example")
    ExampleMeta = ObjCClass(examplemeta_ptr)
    assert ExampleMeta == ObjCMetaClass("Example")
    assert isinstance(ExampleMeta, ObjCMetaClass)


def test_requires_class():
    """ObjCClass only accepts class pointers."""

    random_obj = NSObject.alloc().init()
    with pytest.raises(ValueError):
        ObjCClass(random_obj.ptr)


def test_superclass():
    """An ObjCClass's superclass can be looked up."""

    Example = ObjCClass("Example")
    BaseExample = ObjCClass("BaseExample")

    assert Example.superclass == BaseExample
    assert BaseExample.superclass == NSObject
    assert NSObject.superclass is None


def test_protocols():
    """An ObjCClass's protocols can be looked up."""

    BaseExample = ObjCClass("BaseExample")
    ExampleProtocol = ObjCProtocol("ExampleProtocol")
    DerivedProtocol = ObjCProtocol("DerivedProtocol")

    assert BaseExample.protocols == (ExampleProtocol, DerivedProtocol)


def test_instancecheck():
    """``isinstance()`` works with an ObjCClass as the second argument."""
    assert isinstance(NSObject.new(), NSObject)
    assert isinstance(at(""), NSString)
    assert isinstance(at(""), NSObject)
    assert isinstance(NSObject, NSObject)
    assert isinstance(NSObject, NSObject.objc_class)

    assert not isinstance(object(), NSObject)
    assert not isinstance(NSObject.new(), NSString)
    assert not isinstance(NSArray.array, NSString)


def test_subclasscheck():
    """``issubclass()`` works with an ObjCClass as the second argument."""
    assert issubclass(NSObject, NSObject)
    assert issubclass(NSString, NSObject)
    assert issubclass(NSObject.objc_class, NSObject)
    assert issubclass(NSObject.objc_class, NSObject.objc_class)

    assert not issubclass(NSObject, NSString)
    assert not issubclass(NSArray, NSString)

    with pytest.raises(TypeError):
        issubclass(object(), NSObject)
    with pytest.raises(TypeError):
        issubclass(object, NSObject)
    with pytest.raises(TypeError):
        issubclass(NSObject.new(), NSObject)
    with pytest.raises(TypeError):
        issubclass(NSObjectProtocol, NSObject)


def test_repr():
    """Test ObjCClass repr and str return correct value."""

    assert repr(NSObject) == "<ObjCClass: NSObject>"
    assert str(NSObject) == "ObjCClass('NSObject')"


def test_duplicate_registration():
    """If you define a class name twice in the same runtime, you get an error."""

    # First definition should work.
    class MyClass(NSObject):
        pass

    # Second definition will raise an error.
    # Without protection, this is a segfault.
    with pytest.raises(RuntimeError):

        class MyClass(NSObject):
            pass


def test_auto_rename_global():
    """Test the global automatic renaming option of ObjCClass."""

    try:
        ObjCClass.auto_rename = True

        class TestGlobalRenamedClass(NSObject):
            @objc_method
            def oldMethod(self):
                pass

        class1 = TestGlobalRenamedClass

        class TestGlobalRenamedClass_2(NSObject):
            pass

        class TestGlobalRenamedClass(NSObject):
            @objc_method
            def testMethod(self):
                return "TEST1"

        # Check that the class was renamed
        assert TestGlobalRenamedClass.name == "TestGlobalRenamedClass_3"
        assert class1 is not TestGlobalRenamedClass

        # Check that methods are updated
        obj = TestGlobalRenamedClass.new()
        with pytest.raises(AttributeError):
            obj.oldMethod()
        assert obj.testMethod() == "TEST1"

    finally:
        ObjCClass.auto_rename = False


def test_auto_rename_per_class():
    """Test the per-class automatic renaming option of ObjCClass."""

    class TestLocalRenamedClass(NSObject):
        @objc_method
        def oldMethod(self):
            pass

    class1 = TestLocalRenamedClass

    class TestLocalRenamedClass_2(NSObject):
        pass

    class TestLocalRenamedClass(NSObject, auto_rename=True):
        @objc_method
        def testMethod(self):
            return "TEST2"

    # Check that the class was renamed
    assert TestLocalRenamedClass.name == "TestLocalRenamedClass_3"
    assert class1 is not TestLocalRenamedClass

    # Check that methods are updated
    obj = TestLocalRenamedClass.new()
    with pytest.raises(AttributeError):
        obj.oldMethod()
    assert obj.testMethod() == "TEST2"


def test_ivars():
    """An Objective-C class can have instance variables."""

    class Ivars(NSObject):
        object = objc_ivar(objc_id)
        int = objc_ivar(c_int)
        rect = objc_ivar(NSRect)

    ivars = Ivars.alloc().init()

    set_ivar(ivars, "object", at("foo").ptr)
    set_ivar(ivars, "int", c_int(12345))
    set_ivar(ivars, "rect", NSMakeRect(12, 34, 56, 78))

    s = ObjCInstance(get_ivar(ivars, "object"))
    assert str(s) == "foo"

    i = get_ivar(ivars, "int")
    assert i.value == 12345

    r = get_ivar(ivars, "rect")
    assert r.origin.x == 12
    assert r.origin.y == 34
    assert r.size.width == 56
    assert r.size.height == 78


def test_properties():
    """A Python class can have ObjC properties with synthesized getters and setters of
    ObjCInstance type."""

    NSURL = ObjCClass("NSURL")

    class URLBox(NSObject):
        url = objc_property(ObjCInstance)
        data = objc_property(ObjCInstance)

        @objc_method
        def getSchemeIfPresent(self):
            if self.url is not None:
                return self.url.scheme
            return None

    box = URLBox.alloc().init()

    # Default property value is None
    assert box.url is None

    # Assign an object via synthesized property setter and call method
    # that uses synthesized property getter
    url = NSURL.alloc().initWithString_("https://www.google.com")
    box.url = url
    assert box.getSchemeIfPresent() == "https"

    # Assign None to dealloc property and see if method returns expected None
    box.url = None
    assert box.getSchemeIfPresent() is None

    # Try composing URLs using constructors
    base = NSURL.URLWithString("https://beeware.org")
    full = NSURL.URLWithString("contributing/", relativeToURL=base)

    assert (
        f"Visit {full.absoluteURL} for details"
        == "Visit https://beeware.org/contributing/ for details"
    )

    # ObjC type conversions are performed on property assignment.
    box.data = "Jabberwock"
    assert box.data == "Jabberwock"

    Example = ObjCClass("Example")
    example = Example.alloc().init()
    box.data = example
    assert box.data == example

    box.data = None
    assert box.data is None


def test_python_properties():
    """A Python class can have ObjC properties with synthesized getters and setters of
    Python type."""

    class PythonObjectProperties(NSObject):
        object = objc_property(object)

    class PythonObject:
        pass

    properties = PythonObjectProperties.alloc().init()

    o = PythonObject()
    wr = weakref.ref(o)

    properties.object = o

    # Test that Python object is properly stored.
    assert properties.object == o

    # Test that Python object is retained by the property.
    del o
    gc.collect()

    assert properties.object is wr()

    # Test that Python object is released by the property.
    properties.object = None
    gc.collect()
    assert wr() is None

    # Test that Python object is released by dealloc.

    o = PythonObject()
    wr = weakref.ref(o)

    properties.object = o
    assert properties.object is o

    with autoreleasepool():
        del o
        del properties
        gc.collect()

    assert wr() is None


def test_python_properties_weak():
    class WeakPythonObjectProperties(NSObject):
        object = objc_property(object, weak=True)

    class PythonObject:
        pass

    properties = WeakPythonObjectProperties.alloc().init()

    o = PythonObject()
    wr = weakref.ref(o)

    properties.object = o

    # Test that Python object is properly stored.
    assert properties.object is o

    # Test that Python object is not retained by the property.
    del o
    gc.collect()

    assert properties.object is None
    assert wr() is None


def test_nonobject_properties():
    """An Objective-C class can have properties of non-object types."""

    class NonObjectProperties(NSObject):
        object = objc_property(ObjCInstance)
        int = objc_property(c_int)
        rect = objc_property(NSRect)

    properties = NonObjectProperties.alloc().init()

    properties.object = at("foo")
    properties.int = 12345
    properties.rect = NSMakeRect(12, 34, 56, 78)

    assert properties.object == "foo"
    assert properties.int == 12345

    r = properties.rect
    assert r.origin.x == 12
    assert r.origin.y == 34
    assert r.size.width == 56
    assert r.size.height == 78


def test_nonobject_properties_weak():
    with pytest.raises(TypeError):

        class WeakNonObjectProperties(NSObject):
            int = objc_property(c_int, weak=True)


def test_properties_lifecycle_strong():
    class StrongObjectProperties(NSObject):
        object = objc_property(ObjCInstance)

    with autoreleasepool():
        properties = StrongObjectProperties.alloc().init()

        obj = NSObject.alloc().init()
        obj_pointer = obj.ptr.value  # store the object pointer for future use

        properties.object = obj

        del obj
        gc.collect()

    # assert that the object was retained by the property
    assert properties.object.ptr.value == obj_pointer


def test_properties_lifecycle_weak():
    class WeakObjectProperties(NSObject):
        object = objc_property(ObjCInstance, weak=True)

    with autoreleasepool():
        properties = WeakObjectProperties.alloc().init()

        obj = NSObject.alloc().init()
        properties.object = obj

        assert properties.object is obj

        del obj
        gc.collect()

    assert properties.object is None


def test_with_wrapped_methods():
    """An ObjCClass can have wrapped methods."""

    def deco(f):
        @functools.wraps(f)
        def _wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return _wrapper

    class SimpleMath(NSObject):
        @objc_method
        @deco
        def addOne_(self, num: c_int) -> c_int:
            return num + 1

        @objc_classmethod
        @deco
        def subtractOne_(cls, num: c_int) -> c_int:
            return num - 1

    simplemath = SimpleMath.alloc().init()
    assert simplemath.addOne_(254) == 255
    assert SimpleMath.subtractOne_(75) == 74


def test_compatible_name_change():
    """If the class name changes in a compatible way, the wrapper isn't recreated
    (#257)"""
    Example = ObjCClass("Example")

    pre_init = Example.alloc()

    # Call initWithClassChange(), which does an internal class name change.
    # This mirrors what happens with NSWindow, where `init()` changes the
    # class name to NSKVONotifying_NSWindow.
    post_init = pre_init.initWithClassChange()

    # Memory address hasn't changed
    assert pre_init.ptr.value == post_init.ptr.value
    # The class name hasn't changed either
    assert pre_init.objc_class.name == post_init.objc_class.name == "Example"

    # The wrapper is the same object
    assert id(pre_init) == id(post_init)


def test_property_forcing():
    """An instance or property method can be explicitly declared as a property."""
    Example = ObjCClass("Example")
    Example.declare_class_property("classMethod")
    Example.declare_class_property("classAmbiguous")
    Example.declare_property("instanceMethod")
    Example.declare_property("instanceAmbiguous")

    # A class method can be turned into a property
    assert Example.classMethod == 37

    # An actual class property can be accessed as a property
    assert Example.classAmbiguous == 37

    # An instance property can be accessed
    obj1 = Example.alloc().init()

    # An instance method can be turned into a property
    assert obj1.instanceMethod == 42

    # An actual property can be accessed as a property
    assert obj1.instanceAmbiguous == 42

    # Practical example: In Sierra, mainBundle was turned into a class property.
    # Previously, it was a method.
    NSBundle = ObjCClass("NSBundle")
    NSBundle.declare_class_property("mainBundle")
    assert not callable(NSBundle.mainBundle), (
        "NSBundle.mainBundle should not be a method"
    )
