==========================================================
You're just not my type: Using Objective-C types in Python
==========================================================

Objective-C is a strong, static typed language. Every variable has a specific
type, and that type cannot change over time. If a function declares that it
accepts an integer, then it must receive a variable that is declared as an
integer, or an expression that results in an integer.

Python, on the other hand, is strong, but *dynamically* typed language. Every
variable has a specific type, but that type can be modified or interpreted in
other ways. When a function accepts an argument, Python will allow you to pass
*any* variable, of *any* type.

So, if you want to bridge between Objective-C and Python, you need to be able
to provide static typing information so that Python can work out how to convert
a variable of arbitrary type into a specific type matching Objective-C's
expectations.

If you're calling an Objective C method defined in a library, this conversion
is done automatically - the Objective-C runtime contains enough information for
Rubicon to infer the required types. However, if you're defining a new method
(or a method override) in Python, we need to provide that typing information.
To do this, we use Python 3's type annotation. Here's how.

Primitives
----------

If a Python value needs to be passed in as a primitive, Rubicon will wrap the
primitive:

============== ============================================================
Value          C primitive
============== ============================================================
:class:`bool`  8 bit integer (although it can only hold 2 values - 0 and 1)
:class:`int`   32 bit integer
:class:`float` double precision floating point
============== ============================================================

If a Python value needs to be passed in as an object, Rubicon will wrap the
primitive in an object:

============== ==========================
Value          Objective C type
============== ==========================
:class:`bool`  :class:`NSNumber` (bool)
:class:`int`   :class:`NSNumber` (long)
:class:`float` :class:`NSNumber` (double)
============== ==========================

If you're declaring a method and need to annotate the type of an argument, the
Python type name can be used as the annotation type. You can also use any of
the ``ctypes`` primitive types. Rubicon also provides type definitions for common
Objective-C typedefs, like :class:`NSInteger`, :class:`CGFloat`, and so on.

Strings
-------

If a method calls for an :class:`NSString` argument, you can provide a Python
:class:`str` for that argument. Rubicon will construct an :class:`NSString`
instance from the data in the :class:`str` provided, and pass that value for
the argument.

If a method returns an :class:`NSString`, the return value will be a wrapped
:class:`ObjCStrInstance` type. This type implements a :class:`str`-like
interface, wrapped around the underlying :class:`NSString` data. This means
you can treat the return value as if it were a string - slicing it,
concatenating it with other strings, comparing it, and so on::

    # Call an Objective C method that returns a string.
    # We're using NSBundle to give us a string version of a path
    >>> NSBundle.mainBundle.bundlePath
    <rubicon.objc.collections.ObjCStrInstance 0x114a94d68: __NSCFString at 0x7fec8ba7fbd0: /Users/brutus/path/to/somewhere>

    # Slice the Objective C string
    >>> NSBundle.mainBundle.bundlePath[:14]
    <rubicon.objc.collections.ObjCStrInstance 0x114aa80f0: __NSCFString at 0x7fec8ba7fbd0: /Users/brutus/>

Note that :class:`ObjCStrInstance` objects behave slightly differently than
Python :class:`str` objects in some cases. For technical reasons,
:class:`ObjCStrInstance` objects are not hashable, which means they cannot be
used as :class:`dict` keys (but they *can* be used as :class:`NSDictionary`
keys). :class:`ObjCStrInstance` also handles Unicode code points above
``U+FFFF`` differently than Python :class:`str`, because the underlying
:class:`NSString` is based on UTF-16.

If you have an :class:`ObjCStrInstance` instance, and you need to pass that
instance to a method that does a specific typecheck for :class:`str`, you can
use ``str(nsstring)`` to convert the :class:`ObjCStrInstance` instance to
:class:`str`::

    # Convert the Objective C string to a Python string.
    >>> str(NSBundle.mainBundle.bundlePath)
    '/Users/rkm/projects/beeware/venv3.6/bin'

Conversely, if you have a :class:`str`, and you specifically require a
:class:`ObjCStrInstance` instance, you can use the :meth:`at()` method to
convert the Python instance to an :class:`ObjCStrInstance`.

    >>> from rubicon.objc import at
    # Create a Python string
    >>> py_str = 'hello world'

    # Convert to an Objective C string
    >>> at(py_str)
    <rubicon.objc.collections.ObjCStrInstance 0x114a94e48: __NSCFString at 0x7fec8ba7fc10: hello world>

:class:`ObjCStrInstance` implements all the utility methods that are available
on :class:`str`, such as ``replace`` and ``split``. When these methods return
a string, the implementation may return Python :class:`str` or
:class:`ObjCStrInstance` instances. If you need to use the return value from
these methods, you should always use ``str()`` to ensure you have a Python
string::

    # Is the path comprised of all lowercase letters? (Hint: it isn't)
    >>> NSBundle.mainBundle.bundlePath.islower()
    False

    # Convert string to lower case; use str() to ensure we get a Python string.
    >>> str(NSBundle.mainBundle.bundlePath.lower())
    '/users/rkm/projects/beeware/venv3.6/bin'


Lists
-----

If a method calls for an :class:`NSArray` or :class:`NSMutableArray` argument,
you can provide a Python :class:`list` for that argument. Rubicon will
construct an :class:`NSMutableArray` instance from the data in the
:class:`list` provided, and pass that value for the argument.

If a method returns an :class:`NSArray` or :class:`NSMutableArray`, the return
value will be a wrapped :class:`ObjCListInstance` type. This type implements a
:class:`list`-like interface, wrapped around the underlying :class:`NSArray`
data. This means you can treat the return value as if it were a list -
iterating over values, retrieving objects by index, and so on.

Dictionaries
------------

If a method calls for an :class:`NSDictionary` or :class:`NSMutableDictionary`
argument, you can provide a Python :class:`dict`. Rubicon will construct an
:class:`NSMutableDictionary` instance from the data in the :class:`dict`
provided, and pass that value for the argument.

If a method returns an :class:`NSDictionary` or :class:`NSMutableDictionary`,
the return value will be a wrapped :class:`ObjCDictInstance` type. This type
implements a :class:`dict`-like interface, wrapped around the underlying
:class:`NSDictionary` data. This means you can treat the return value as if it
were a dict - iterating over keys, values or items, retrieving objects by key,
and so on.


:class:`NSPoint`, :class:`NSSize`, and :class:`NSRect`
------------------------------------------------------

On instances of an Objective C structure, each field is exposed as a Python
attribute. For example, if you create an instance of an :class:`NSSize` object
you can access its width and height by calling :meth:`NSSize.width`.

When you need to pass an Objective C structure to an Objective C method,
you can pass a tuple instead. For example, if you pass (10.0, 5.1) where a
:class:`NSSize` is expected, it will be converted automatically in the appropriate
width, height for the structure.
