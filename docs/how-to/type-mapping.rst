==========================================================
You're just not my type: Using Objective-C types in Python
==========================================================

Objective-C is a strongly and statically-typed language. Every variable has a
specific type, and that type cannot change over time. Function parameters also
have fixed types, and a function will only accept arguments of the correct
types.

Python, on the other hand, is a strongly, but *dynamically*-typed language.
Every object has a specific type, but all variables can hold objects of any
type. When a function accepts an argument, Python will allow you to pass *any*
object, of *any* type.

So, if you want to bridge between Objective-C and Python, you need to be able
to provide static typing information so that Rubicon can work out how to
convert a Python object of arbitrary type into a specific type matching
Objective-C's expectations.

Type annotations
----------------

If you're calling an Objective-C method defined in a library, its types are
already known to the Objective-C runtime and Rubicon. However, if you're
defining a new method (or a method override) in Python, you need to manually
provide its types. This is done using Python 3's type annotation syntax.

Passing and returning Objective-C objects doesn't require any extra work ---
if you don't annotate a parameter or the return type, Rubicon assumes that it
is an Objective-C object. (To define a method that doesn't return anything, you
need to add an explicit ``-> None`` annotation.)

All other parameter and return types (primitives, pointers, structs) need to be
annotated to tell Rubicon and Objective-C which type to expect. These
annotations can use any of the types defined by Rubicon, such as
:class:`~rubicon.objc.types.NSInteger` or :class:`~rubicon.objc.types.NSRange`,
as well as standard C types from the :mod:`ctypes` module, such as
:class:`~ctypes.c_byte` or :class:`~ctypes.c_double`.

For example, a method that takes a C ``double`` and returns a
:class:`~rubicon.objc.types.NSInteger` would be defined and annotated like
this:

.. code-block:: python

    @objc_method
    def roundToZero_(self, value: c_double) -> NSInteger:
        return int(value)

Rubicon also allows certain Python types to be used in method signatures, and
converts them to matching primitive :mod:`ctypes` types. For example, Python
:class:`int` is treated as :class:`~ctypes.c_int`, and :class:`float` is
treated as :class:`~ctypes.c_double`.

.. seealso::

    The :mod:`rubicon.objc.types` reference documentation lists all C type
    definitions provided by Rubicon, and provides additional information about
    how Rubicon converts types.

Type conversions
----------------

When you call existing Objective-C methods, Rubicon already knows which type
each argument needs to have and what it returns. Based on this type
information, Rubicon will automatically convert the passed arguments to the
proper Objective-C types, and the return value to an appropriate Python type.
This makes explicit type conversions between Python and Objective-C types
unnecessary in many cases.

.. _argument_conversion:

Argument conversion
^^^^^^^^^^^^^^^^^^^

If an Objective-C method expects a C primitive argument, you can pass an
equivalent Python value instead. For example, a Python :class:`int` value can
be passed into any integer argument (``int``, ``NSInteger``, ``uint8_t``, ...),
and a Python :class:`float` value can be passed into any floating-point
argument (``double``, ``CGFloat``, ...).

To pass a C structure as an argument, you would normally need to construct a
structure instance by name. This can get somewhat lengthy, especially with
nested structures (e. g. ``NSRect(NSPoint(1.2, 3.4), NSSize(5.6, 7.8))``). As a
shorthand, Rubicon allows passing tuples instead of structure objects (e. g.
``((1.2, 3.4), (5.6, 7.8))``) and automatically converts them to the required
structure type.

If a parameter expects an Objective-C object, you can also pass certain Python
objects, which are automatically converted to their Objective-C counterparts.
For example, a Python :class:`str` is converted to an ``NSString``,
:class:`bytes` to ``NSData``, etc. Collections are also supported:
:class:`list` and :class:`dict` are converted to ``NSArray`` and
``NSDictionary``, and their elements are converted recursively.

.. note::

    All of these conversions can also be performed manually - see
    :ref:`manual_conversions` for details.

Return value conversion and wrapping
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Primitive values returned from methods are converted using the usual
:mod:`ctypes` conversions, e. g. C integers are converted to Python
:class:`int` and floating-point values to Python :class:`float`.

Objective-C objects are automatically returned as
:class:`~rubicon.objc.api.ObjCInstance` objects, so you can call methods on
them and access their properties. In some cases, Rubicon also provides
additional Python methods on Objective-C objects -
see :ref:`python_style_apis_for_objc` for details.

.. _python_style_apis_for_objc:

Python-style APIs and methods for Objective-C objects
-----------------------------------------------------

For some standard Foundation classes, such as lists and dictionaries,
Rubicon provides additional Python methods to make them behave more like their
Python counterparts. This allows using Foundation objects in place of regular
Python objects, so that you do not need to convert them manually.

Strings
^^^^^^^

:class:`~rubicon.objc.api.NSString` objects behave almost exactly like Python
:class:`str` objects - they can be sliced, concatenated, compared, etc. with
other Objective-C and Python strings.

.. code-block:: python

    # Call an Objective-C method that returns a string.
    # We're using NSBundle to give us a string version of a path
    >>> NSBundle.mainBundle.bundlePath
    <ObjCStrInstance: __NSCFString at 0x114a94d68: /Users/brutus/path/to/somewhere>

    # Slice the Objective-C string
    >>> NSBundle.mainBundle.bundlePath[:14]
    <ObjCStrInstance: __NSCFString at 0x114aa80f0: /Users/brutus/>

.. note::

    :class:`~rubicon.objc.api.ObjCInstance` objects wrapping a
    :class:`~rubicon.objc.api.NSString` internally have the class
    ``ObjCStrInstance``, and you will see this name in the :func:`repr` of
    :class:`~rubicon.objc.api.NSString` objects. This is an implementation
    detail - you should not refer to the ``ObjCStrInstance`` class explicitly
    in your code.

If you have an :class:`~rubicon.objc.api.NSString`, and you need to pass it to
a method that does a specific type check for :class:`str`, you can use
``str(nsstring)`` to convert the :class:`~rubicon.objc.api.NSString` to
:class:`str`:

.. code-block:: python

    # Convert the Objective-C string to a Python string.
    >>> str(NSBundle.mainBundle.bundlePath)
    '/Users/rkm/projects/beeware/venv3.6/bin'

Conversely, if you have a :class:`str`, and you specifically require a
:class:`~rubicon.objc.api.NSString`, you can use the
:func:`~rubicon.objc.api.at` function to convert the Python instance to an
:class:`~rubicon.objc.api.NSString`.

.. code-block:: python

    >>> from rubicon.objc import at
    # Create a Python string
    >>> py_str = 'hello world'
    # Convert to an Objective-C string
    >>> at(py_str)
    <ObjCStrInstance: __NSCFString at 0x114a94e48: hello world>

:class:`~rubicon.objc.api.NSString` also supports all the utility methods that
are available on :class:`str`, such as ``replace`` and ``split``. When these
methods return a string, the implementation may return Python :class:`str` or
Objective-C :class:`~rubicon.objc.api.NSString` instances. If you need to use
the return value from these methods, you should always use :class:`str` or
:func:`~rubicon.objc.api.at` to ensure that you have the right kind of string
for your needs.

.. code-block:: python

    # Is the path comprised of all lowercase letters? (Hint: it isn't)
    >>> NSBundle.mainBundle.bundlePath.islower()
    False

    # Convert string to lower case; use str() to ensure we get a Python string.
    >>> str(NSBundle.mainBundle.bundlePath.lower())
    '/users/rkm/projects/beeware/venv3.6/bin'

.. note::

    :class:`~rubicon.objc.api.NSString` objects behave slightly differently
    than Python :class:`str` objects in some cases. For technical reasons,
    :class:`~rubicon.objc.api.NSString`\s are not hashable in Python, which
    means they cannot be used as :class:`dict` keys (but they *can* be used as
    :class:`~rubicon.objc.api.NSDictionary` keys).
    :class:`~rubicon.objc.api.NSString` also handles Unicode code points above
    ``U+FFFF`` differently than Python :class:`str`, because the former is
    based on UTF-16.

Lists
^^^^^

:class:`~rubicon.objc.api.NSArray` objects behave like any other Python
sequence - they can be indexed, sliced, etc. and standard operations like
:func:`len` and ``in`` are supported:

.. code-block:: python

    >>> from rubicon.objc import NSArray
    >>> array = NSArray.arrayWithArray(list(range(4)))
    >>> array[0]
    0
    >>> array[1:3]
    <ObjCListInstance: _NSArrayI at 0x10b855208: <__NSArrayI 0x7f86f8e61950>(
    1,
    2
    )
    >
    >>> len(array)
    4
    >>> 2 in array
    True
    >>> 5 in array
    False

.. note::

    :class:`~rubicon.objc.api.ObjCInstance` objects wrapping a
    :class:`~rubicon.objc.api.NSArray` internally have the class
    ``ObjCListInstance`` or ``ObjCMutableListInstance``, and you will
    see these names in the :func:`repr` of :class:`~rubicon.objc.api.NSArray`
    objects. This is an implementation detail - you should not refer to the
    ``ObjCListInstance`` and ``ObjCMutableListInstance`` classes explicitly in
    your code.

:class:`~rubicon.objc.api.NSMutableArray` objects additionally support mutating
operations, like item and slice assignment:

.. code-block:: python

    >>> from rubicon.objc import NSMutableArray
    >>> mutarray = NSMutableArray.arrayWithArray(list(range(4)))
    >>> mutarray[0] = 42
    >>> mutarray
    <ObjCMutableListInstance: __NSArrayM at 0x10b8558d0: <__NSArrayM 0x7f86fb04d9f0>(
    42,
    1,
    2,
    3
    )
    >
    >>> mutarray[1:3] = [9, 8, 7]
    >>> mutarray
    <ObjCMutableListInstance: __NSArrayM at 0x10b8558d0: <__NSArrayM 0x7f86fb04d9f0>(
    42,
    9,
    8,
    7,
    3
    )
    >

Sequence methods like ``index`` and ``pop`` are also supported:

.. code-block:: python

    >>> mutarray.index(7)
    3
    >>> mutarray.pop(3)
    7

.. note::

    Python objects stored in an :class:`~rubicon.objc.api.NSArray` are
    converted to Objective-C objects using the rules described in
    :ref:`argument_conversion`.

Dictionaries
^^^^^^^^^^^^

:class:`~rubicon.objc.api.NSDictionary` objects behave like any other Python
mapping - their items can be accessed and standard operations like :func:`len`
and ``in`` are supported:

.. code-block:: python

    >>> from rubicon.objc import NSDictionary
    >>> d = objc.NSDictionary.dictionaryWithDictionary({"one": 1, "two": 2})
    >>> d["one"]
    1
    >>> len(d)
    >>> 2
    >>> "two" in d
    True
    >>> "five" in d
    False

.. note::

    :class:`~rubicon.objc.api.ObjCInstance` objects wrapping a
    :class:`~rubicon.objc.api.NSDictionary` internally have the class
    ``ObjCDictInstance`` or ``ObjCMutableDictInstance``, and you will see these
    names in the :func:`repr` of :class:`~rubicon.objc.api.NSDictionary`
    objects. This is an implementation detail - you should not refer to the
    ``ObjCDictInstance`` and ``ObjCMutableDictInstance`` classes explicitly in
    your code.

:class:`~rubicon.objc.api.NSMutableDictionary` objects additionally support
mutating operations, like item assignment:

.. code-block:: python

    >>> md = objc.NSMutableDictionary.dictionaryWithDictionary({"one": 1, "two": 2})
    >>> md["three"] = 3
    >>> md
    <ObjCMutableDictInstance: __NSDictionaryM at 0x10b8a7860: {
        one = 1;
        three = 3;
        two = 2;
    }>

Mapping methods like ``keys`` and ``values`` are also supported:

.. code-block:: python

    >>> d.keys()
    <ObjCListInstance: __NSArrayI at 0x10b898a90: <__NSArrayI 0x7f86f8db6b70>(
    one,
    two
    )
    >
    >>> d.values()
    <ObjCListInstance: __NSArrayI at 0x10b8a7b38: <__NSArrayI 0x7f86f8c00370>(
    1,
    2
    )
    >

.. note::

    Python objects stored in an :class:`~rubicon.objc.api.NSDictionary` are
    converted to Objective-C objects using the rules described in
    :ref:`argument_conversion`.

.. _manual_conversions:

Manual conversions
------------------

If necessary, you can also manually call Rubicon's type conversion functions,
to convert objects between Python and Objective-C when Rubicon doesn't do so
automatically.

Converting from Python to Objective-C
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The function :func:`~rubicon.objc.api.ns_from_py` (also available as
:func:`~rubicon.objc.api.at` for short) can convert most standard Python
objects to Foundation equivalents. For a full list of possible conversions, see
the reference documentation for :func:`~rubicon.objc.api.ns_from_py`.

These conversions are performed automatically when a Python object is passed
into an Objective-C method parameter that expects an object - in that case you
do not need to call :func:`~rubicon.objc.api.ns_from_py` manually (see
:ref:`argument_conversion`).

Converting from Objective-C to Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The function :func:`~rubicon.objc.api.py_from_ns` can convert many common
Foundation objects to Python equivalents. For a full list of possible
conversions, see the reference documentation for
:func:`~rubicon.objc.api.py_from_ns`.

These conversions are not performed automatically by Rubicon. For example, if
an Objective-C method returns an ``NSString``, Rubicon will return it as an
:class:`~rubicon.objc.api.ObjCInstance` (with some additional Python methods -
see :ref:`python_style_apis_for_objc`). Using
:func:`~rubicon.objc.api.py_from_ns`, you can convert the ``NSString`` to a
real Python :class:`str`.

When converting collections, such as ``NSArray`` or ``NSDictionary``,
:func:`~rubicon.objc.api.py_from_ns` will convert them recursively to a pure
Python object. For example, if ``nsarray`` is an ``NSArray`` containing
``NSString``\s, ``py_from_ns(nsarray)`` will return a :class:`list` of
:class:`str`\s. In most cases, that is the desired behavior, but you can also
avoid this recursive conversion by passing the Foundation collection into a
Python collection constructor: for example ``list(nsarray)`` will return a
:class:`list` of ``NSString``\s.
