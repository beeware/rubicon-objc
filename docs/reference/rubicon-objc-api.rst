======================================================
:mod:`rubicon.objc.api` --- The high-level Rubicon API
======================================================

.. module:: rubicon.objc.api

This module contains Rubicon's main high-level APIs, which allow easy
interaction with Objective-C classes and objects using Pythonic syntax.

Nearly all attributes of this module are also available on the main
:mod:`rubicon.objc` module, and if possible that module should be used instead
of importing :mod:`rubicon.objc.api` directly.

Objective-C objects
-------------------

.. autoclass:: ObjCInstance(ptr)

    .. attribute::
        ptr
        _as_parameter_

        The wrapped object pointer as an :class:`~rubicon.objc.runtime.objc_id`.
        This attribute is also available as ``_as_parameter_`` to allow
        :class:`ObjCInstance`\s to be passed into :mod:`ctypes` functions.

    .. autoattribute:: objc_class
    .. automethod:: __str__
    .. automethod:: __repr__
    .. automethod:: __getattr__
    .. automethod:: __setattr__

.. autofunction:: objc_const

Objective-C classes
-------------------

.. autoclass:: ObjCClass(name_or_ptr, [bases, attrs, [protocols=(), auto_rename=None]])

    .. attribute:: name

        The name of this class, as a :class:`str`.

    .. autoattribute:: superclass
    .. autoattribute:: protocols
    .. autoattribute:: auto_rename
    .. automethod:: declare_property
    .. automethod:: declare_class_property
    .. automethod:: __instancecheck__
    .. automethod:: __subclasscheck__

.. autoclass:: ObjCMetaClass(name_or_ptr)

Standard Objective-C and Foundation classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following classes from the `Objective-C runtime
<https://developer.apple.com/documentation/objectivec?language=objc>`__ and the
`Foundation <https://developer.apple.com/documentation/foundation?language=objc>`__
framework are provided as :class:`ObjCClass`\es for convenience. (Other classes
not listed here can be looked up by passing a class name to the
:class:`ObjCClass` constructor.)

.. note::

    None of the following classes have a usable Python-style constructor - for
    example, you *cannot* call ``NSString("hello")`` to create an Objective-C
    string from a Python string. To create instances of these classes, you
    should use :func:`ns_from_py` (also called :func:`at`):
    ``ns_from_py("hello")`` returns a :class:`NSString` instance with the value
    ``hello``.

.. class::
    NSObject

    The `NSObject
    <https://developer.apple.com/documentation/objectivec/nsobject?language=objc>`__
    class from ``<objc/NSObject.h>``.

    .. note::

        See the :class:`ObjCInstance` documentation for a list of operations
        that Rubicon supports on all objects.

    .. attribute::
        debugDescription
        description

        These Objective-C properties have been declared using
        :meth:`ObjCClass.declare_property` and can always be accessed using
        attribute syntax.

.. class::
    Protocol

    The `Protocol
    <https://developer.apple.com/documentation/objectivec/protocol?language=objc>`__
    class from ``<objc/Protocol.h>``.

    .. note::

        This class has no (non-deprecated) Objective-C methods; protocol
        objects can only be manipulated using Objective-C runtime functions.
        Rubicon automatically wraps all :class:`Protocol` objects using
        :class:`ObjCProtocol`, which provides an easier interface for working
        with protocols.

.. class::
    NSNumber

    The `NSNumber
    <https://developer.apple.com/documentation/foundation/nsnumber?language=objc>`__
    class from ``<Foundation/NSValue.h>``.

    .. note::

        This class can be converted to and from standard Python primitives
        (``bool``, ``int``, ``float``) using :func:`py_from_ns` and
        :func:`ns_from_py`.

.. class::
    NSDecimalNumber

    The `NSDecimalNumber
    <https://developer.apple.com/documentation/foundation/nsdecimalnumber?language=objc>`__
    class from ``<Foundation/NSDecimalNumber.h>``.

    .. note::

        This class can be converted to and from Python ``decimal.Decimal``
        using :func:`py_from_ns` and :func:`ns_from_py`.

.. class::
    NSString

    The `NSString
    <https://developer.apple.com/documentation/foundation/nsstring?language=objc>`__
    class from ``<Foundation/NSString.h>``.

    This class also supports all methods that :class:`str` does.

    .. note::

        This class can be converted to and from Python :class:`str` using
        :func:`py_from_ns` and :func:`ns_from_py`. You can also call
        ``str(nsstring)`` to convert a ``NSString`` to :class:`str`.

        :class:`NSString` objects consist of UTF-16 code units, unlike
        :class:`str`, which consists of Unicode code points. All
        :class:`NSString` indices and iteration are based on UTF-16, even when
        using the Python-style operations/methods. If indexing or iteration
        based on code points is required, convert the :class:`NSString` to
        :class:`str` first.

    .. method:: __str__()

        Return the value of this :class:`NSString` as a :class:`str`.

    .. attribute::
        UTF8String

        This Objective-C property has been declared using
        :meth:`ObjCClass.declare_property` and can always be accessed using
        attribute syntax.

.. class::
    NSData

    The `NSData
    <https://developer.apple.com/documentation/foundation/nsdata?language=objc>`__
    class from ``<Foundation/NSData.h>``.

    .. note::

        This class can be converted to and from Python :class:`bytes` using
        :func:`py_from_ns` and :func:`ns_from_py`.

.. class::
    NSArray

    The `NSArray
    <https://developer.apple.com/documentation/foundation/nsarray?language=objc>`__
    class from ``<Foundation/NSArray.h>``.

    .. note::

        This class can be converted to and from Python :class:`list` using
        :func:`py_from_ns` and :func:`ns_from_py`.

        ``py_from_ns(nsarray)`` will recursively convert ``nsarray``'s elements
        to Python objects, where possible. To avoid this recursive conversion,
        use ``list(nsarray)`` instead.

        ``ns_from_py(pylist)`` will recursively convert ``pylist``'s elements
        to Objective-C. As there is no way to store Python object references
        as Objective-C objects yet, this recursive conversion cannot be
        avoided. If any of ``pylist``'s elements cannot be converted to
        Objective-C, an error is raised.

    .. method::
        __getitem__(index)
        __len__()
        __iter__()
        __contains__(value)
        __eq__(other)
        __ne__(other)
        index(value)
        count(value)
        copy()

        Python-style sequence interface.

.. class::
    NSMutableArray

    The `NSMutableArray
    <https://developer.apple.com/documentation/foundation/nsmutablearray?language=objc>`__
    class from ``<Foundation/NSArray.h>``.

    .. note::

        This class can be converted to and from Python exactly like its
        superclass ``NSArray``.

    .. method::
        __setitem__(index, value)
        __delitem__(index)
        append(value)
        clear()
        extend(values)
        insert(index, value)
        pop([index=-1])
        remove(value)
        reverse()

        Python-style mutable sequence interface.

.. class::
    NSDictionary

    The `NSDictionary
    <https://developer.apple.com/documentation/foundation/nsdictionary?language=objc>`__
    class from ``<Foundation/NSDictionary.h>``.

    .. note::

        This class can be converted to and from Python :class:`dict` using
        :func:`py_from_ns` and :func:`ns_from_py`.

        ``py_from_ns(nsdict)`` will recursively convert ``nsdict``'s keys and
        values to Python objects, where possible. To avoid the recursive
        conversion of the values, use ``{py_from_ns(k): v for k, v in
        nsdict.items()}``. The conversion of the keys cannot be avoided,
        because Python :class:`dict` keys need to be hashable, which
        :class:`ObjCInstance` is not. If any of the keys convert to a Python
        object that is not hashable, an error is raised (regardless of which
        conversion method you use).

        ``ns_from_py(pydict)`` will recursively convert ``pydict``'s keys and
        values to Objective-C. As there is no way to store Python object
        references as Objective-C objects yet, this recursive conversion cannot
        be avoided. If any of ``pydict``'s keys or values cannot be converted
        to Objective-C, an error is raised.

    .. method::
        __getitem__(key)
        __len__()
        __iter__()
        __contains__(key)
        __eq__(other)
        __ne__(other)
        copy()
        get(key, [default=None])
        keys()
        items()
        values()

        Python-style mapping interface.

        .. note::

            Unlike most Python mappings, :class:`NSDictionary`'s :attr:`keys`,
            :attr:`values`, and :attr:`items` methods don't return dynamic
            views of the dictionary's keys, values, and items.

            :attr:`keys` and :attr:`values` return lists that are created each
            time the methods are called, which can have an effect on
            performance and memory usage for large dictionaries. To avoid this,
            you can cache the return values of :attr:`keys` and :attr:`values`,
            or convert the :class:`NSDictionary` to a Python :class:`dict`
            beforehand.

            :attr:`items` is currently implemented as a generator, meaning that
            it returns a single-use iterator. If you need to iterate over
            :attr:`items` more than once or perform other operations on it, you
            should convert it to a Python :class:`set` or :class:`list` first.

.. class::
    NSMutableDictionary

    The `NSMutableDictionary
    <https://developer.apple.com/documentation/foundation/nsmutabledictionary?language=objc>`__
    class from ``<Foundation/NSDictionary.h>``.

    .. note::

        This class can be converted to and from Python exactly like its
        superclass ``NSDictionary``.

    .. method::
        __setitem__(key, value)
        __delitem__(key)
        clear()
        pop(item, [default])
        popitem()
        setdefault(key, [default=None])
        update([other], **kwargs)

        Python-style mutable mapping interface.

Objective-C protocols
---------------------

.. autoclass:: ObjCProtocol(name_or_ptr, [bases, attrs, [auto_rename=None]])

    .. autoattribute:: name
    .. autoattribute:: protocols
    .. autoattribute:: auto_rename
    .. automethod:: __instancecheck__
    .. automethod:: __subclasscheck__

Standard Objective-C and Foundation protocols
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following protocols from the `Objective-C runtime
<https://developer.apple.com/documentation/objectivec?language=objc>`__ and the
`Foundation <https://developer.apple.com/documentation/foundation?language=objc>`__
framework are provided as :class:`ObjCProtocol`\s for convenience. (Other
protocols not listed here can be looked up by passing a protocol name to the
:class:`ObjCProtocol` constructor.)

.. data:: NSObjectProtocol

    The `NSObject
    <https://developer.apple.com/documentation/objectivec/1418956-nsobject?language=objc>`__
    protocol from ``<objc/NSObject.h>``. The protocol is exported as
    :class:`NSObjectProtocol` in Python because it would otherwise clash with
    the :class:`NSObject` class.

Converting objects between Objective-C and Python
-------------------------------------------------

.. py_from_ns has an explicit parameter list to hide the private _auto kwarg.
.. autofunction:: py_from_ns(nsobj)
.. autofunction:: ns_from_py
.. function:: at(pyobj)

    Alias for :func:`ns_from_py`.

.. _custom-classes-and-protocols:

Creating custom Objective-C classes and protocols
-------------------------------------------------

Custom Objective-C classes are defined using Python ``class`` syntax, by
subclassing an existing :class:`ObjCClass` object:

.. code-block:: python

    class MySubclass(NSObject):
        # method, property, etc. definitions go here

A custom Objective-C class can only have a single superclass, since Objective-C
does not support multiple inheritance. However, the class can conform to any
number of protocols, which are specified by adding the ``protocols`` keyword
argument to the base class list:

.. code-block:: python

    class MySubclass(NSObject, protocols=[NSCopying, NSMutableCopying]):
        # method, property, etc. definitions go here

.. note::

    Rubicon requires specifying a superclass when defining a custom Objective-C
    class. If you don't need to extend any specific class, use
    :class:`NSObject` as the superclass.

    Although Objective-C technically allows defining classes without a base
    class (so-called *root classes*), this is almost never the desired behavior
    (attempting to do so `causes a compiler error by default
    <https://developer.apple.com/documentation/objectivec/objc_root_class>`_).
    In practice, this feature is only used in the definitions of core
    Objective-C classes like :class:`NSObject`. Because of this, Rubicon does
    not support defining Objective-C root classes.

Similar syntax is used to define custom Objective-C protocols. Unlike classes,
protocols can extend multiple other protocols:

.. code-block:: python

    class MyProtocol(NSCopying, NSMutableCopying):
        # method, property, etc. definitions go here

A custom protocol might not need to extend any other protocol at all. In this
case, we need to explicitly tell Python to define an :class:`ObjCProtocol`.
Normally Python detects the metaclass automatically by examining the base
classes, but in this case there are none, so we need to specify the metaclass
manually.

.. code-block:: python

    class MyProtocol(metaclass=ObjCProtocol):
        # method, property, etc. definitions go here

Defining methods
^^^^^^^^^^^^^^^^

.. autofunction:: objc_method
.. autofunction:: objc_classmethod

Method naming
"""""""""""""

The name of a Python-defined Objective-C method is same as the Python method's
name, but with all underscores (``_``) replaced with colons (``:``) --- for
example, ``initWithWidth_height_`` becomes ``initWithWidth:height:``.

.. warning::

    The Objective-C *language* imposes certain requirements on the usage of
    colons in method names: a method's name must contain exactly as many colons
    as the method has arguments (excluding the implicit ``self`` and ``_cmd``
    parameters), and the name of a method with arguments must end with a colon.
    For example, a method called ``init`` takes no arguments, ``initWithSize:``
    takes a single argument, ``initWithWidth:height:`` takes two, etc.
    ``initWithSize:spam`` is an invalid method name.

    These requirements are not enforced by the Objective-C *runtime*, but
    methods that do not follow them cannot easily be used from regular
    Objective-C code.

    In addition, although the Objective-C language allows method names with
    multiple consecutive colons or a colon at the start of the name, such names
    are considered bad style and never used in practice. For example,
    ``spam::``, ``:ham:``, and ``:`` are unusual, but valid method names.

    Future versions of Rubicon may warn about or disallow such nonstandard
    method names.

Parameter and return types
""""""""""""""""""""""""""

The argument and return types of a Python-created Objective-C method are
determined based on the Python method's type annotations. The annotations may
contain any :mod:`ctypes` type, as well as any of the Python types accepted by
:func:`~rubicon.objc.types.ctype_for_type`. If a parameter or the return type
is not specified, it defaults to :class:`ObjCInstance`. The ``self`` parameter
is special-cased --- its type is always :class:`ObjCInstance`, even if
annotated otherwise. To annotate a method as returning ``void``, set its return
type to :class:`None`.

Before being passed to the Python method, any object parameters
(:class:`~rubicon.objc.runtime.objc_id`) are automatically converted to
:class:`ObjCInstance`. If the method returns an Objective-C object, it is
converted using :func:`ns_from_py` before being returned to Objective-C. These
automatic conversions can be disabled by using :func:`objc_rawmethod` instead
of :func:`objc_method`.

The implicit ``_cmd`` parameter is not passed to the Python method, as it is
normally redundant and not needed. If needed, the ``_cmd`` parameter can be
accessed by using :func:`objc_rawmethod` instead of :func:`objc_method`.

.. autofunction:: objc_rawmethod

Defining properties and ``ivars``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: objc_property
.. autofunction:: objc_ivar
.. autofunction:: get_ivar
.. autofunction:: set_ivar

.. _objc_blocks:

Objective-C blocks
------------------

Blocks are the Objective-C equivalent of function objects, so Rubicon provides
ways to call Objective-C blocks from Python and to pass Python callables to
Objective-C as blocks.

Automatic conversion
^^^^^^^^^^^^^^^^^^^^

If an Objective-C method returns a block (according to its type encoding),
Rubicon will convert the return value to a special :class:`ObjCInstance` that
can be called in Python:

.. code-block:: python

    block = an_objc_instance.methodReturningABlock()
    res = block(arg, ...)

Similarly, if an Objective-C method has a parameter that expects a block, you
can pass in a Python callable object, and it will be converted to an
Objective-C block. In this case, the callable object needs to have parameter
and return type annotations, so that Rubicon can expose this type information
to the Objective-C runtime:

.. code-block:: python

    def result_handler(res: objc_id) -> None:
        print(ObjCInstance(res))

    an_objc_instance.doSomethingWithResultHandler(result_handler)

If you are writing a custom Objective-C method (see
:ref:`custom-classes-and-protocols`), you can annotate parameter or return
types using :class:`~rubicon.objc.runtime.objc_block` so that Rubicon converts
them appropriately:

.. code-block:: python

    class AnObjCClass(NSObject):
        @objc_method
        def methodReturningABlock() -> objc_block:
            def the_block(arg: NSInteger) -> NSUInteger:
                return abs(arg)
            return the_block

        @objc_method
        def doSomethingWithResultHandler_(result_handler: objc_block) -> None:
            res = SomeClass.someMethod()
            result_handler(res)

.. note::

    These automatic conversions are mostly equivalent to the manual conversions
    described in the next section. There are internal technical differences
    between automatic and manual conversions, but they are not noticeable to
    most users.

    The internals of automatic conversion and
    :class:`~rubicon.objc.runtime.objc_block` handling may change in the
    future, so if you need more control over the block conversion process, you
    should use the manual conversions described in the next section.

Manual conversion
^^^^^^^^^^^^^^^^^

These classes are used to manually convert blocks to Python callables and vice
versa. You may need to use them to perform these conversions outside of
Objective-C method calls, or if you need more control over the block's type
signature.

.. autoclass:: ObjCBlock(pointer, [return_type, *arg_types])

    .. automethod:: __call__

.. autoclass:: Block(func, [restype, *argtypes])

Defining custom subclasses of :class:`ObjCInstance`
---------------------------------------------------

The following functions can be used to register custom subclasses of
:class:`ObjCInstance` to be used when wrapping instances of a certain
Objective-C class. This mechanism is for example used by Rubicon to provide
Python-style operators and methods on standard Foundation classes, such as
:class:`NSString` and :class:`NSDictionary`.

.. autofunction:: register_type_for_objcclass
.. autofunction:: for_objcclass
.. autofunction:: type_for_objcclass
.. autofunction:: unregister_type_for_objcclass
.. autofunction:: get_type_for_objcclass_map
