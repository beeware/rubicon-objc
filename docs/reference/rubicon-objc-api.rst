======================================================
:mod:`rubicon.objc.api` --- The high-level Rubicon API
======================================================

.. module:: rubicon.objc.api

This module contains Rubicon's main high-level APIs, which allow easy interaction with Objective-C classes and objects using Pythonic syntax.

Nearly all attributes of this module are also available on the main :mod:`rubicon.objc` module, and if possible that module should be used instead of importing :mod:`rubicon.objc.api` directly.

.. contents::

Objective-C objects
-------------------

.. autoclass:: ObjCInstance(ptr)

    .. attribute::
        ptr
        _as_parameter_

        The wrapped object pointer as an :class:`~rubicon.objc.runtime.objc_id`. This attribute is also available as ``_as_parameter_`` to allow :class:`ObjCInstance`\s to be passed into :mod:`ctypes` functions.

    .. autoattribute:: objc_class
    .. automethod:: __str__
    .. automethod:: __repr__
    .. automethod:: __getattr__
    .. automethod:: __setattr__

.. autofunction:: objc_const

Objective-C classes
-------------------

.. autoclass:: ObjCClass(name_or_ptr, [bases, attrs, [protocols=()]])

    .. attribute:: name

        The name of this class, as a :class:`str`.

    .. autoattribute:: superclass
    .. autoattribute:: protocols
    .. automethod:: declare_property
    .. automethod:: declare_class_property
    .. automethod:: __instancecheck__
    .. automethod:: __subclasscheck__

.. autoclass:: ObjCMetaClass(name_or_ptr)

.. autoclass:: ObjCMethod

    .. automethod:: __call__

    .. attribute:: selector

        The method's selector, as a :class:`~rubicon.objc.runtime.SEL`.

    .. attribute:: encoding

        The method's signature type encoding, as :class:`bytes`.

    .. attribute:: restype

        The method's return type, as a :mod:`ctypes` type, or ``None`` for ``void`` methods.

    .. attribute:: argtypes

        The method's argument types, as a sequence of :mod:`ctypes` types. The types of the implicit ``self`` and ``_cmd`` parameters, :class:`~rubicon.objc.runtime.objc_id` and :class:`~rubicon.objc.runtime.SEL`, are included here.

    .. attribute:: imp

        The method's implementation function pointer, as an :class:`~rubicon.objc.runtime.IMP`.

        .. note::

            This function pointer cannot be called directly, as it does not carry any type information. To call the method, call the :class:`ObjCMethod` object itself (see :meth:`__call__`), and not its :attr:`imp`. This way Rubicon determines the correct argument and return types automatically, checks the types of the passed arguments, and converts the arguments and return value as needed.

Standard Objective-C and Foundation classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following classes from the `Objective-C runtime <https://developer.apple.com/documentation/objectivec?language=objc>`__ and the `Foundation <https://developer.apple.com/documentation/foundation?language=objc>`__ framework are provided as :class:`ObjCClass`\es for convenience. (Other classes not listed here can be looked up by passing a class name to the :class:`ObjCClass` constructor.)

.. class::
    NSObject

    The `NSObject <https://developer.apple.com/documentation/objectivec/nsobject?language=objc>`__ class from ``<objc/NSObject.h>``.

    .. note::

        See the :class:`ObjCInstance` documentation for a list of operations that Rubicon supports on all objects.

    .. attribute::
        debugDescription
        description

        These Objective-C properties have been declared using :meth:`ObjCClass.declare_property` and can always be accessed using attribute syntax.

.. class::
    Protocol

    The `Protocol <https://developer.apple.com/documentation/objectivec/protocol?language=objc>`__ class from ``<objc/Protocol.h>``.

    .. note::

        This class has no (non-deprecated) Objective-C methods; protocol objects can only be manipulated using Objective-C runtime functions. Rubicon automatically wraps all :class:`Protocol` objects using :class:`ObjCProtocol`, which provides an easier interface for working with protocols. 

.. class::
    NSNumber
    NSDecimalNumber

    The `NSNumber <https://developer.apple.com/documentation/foundation/nsnumber?language=objc>`__ and `NSDecimalNumber <https://developer.apple.com/documentation/foundation/nsdecimalnumber?language=objc>`__ classes from ``<Foundation/NSValue.h>`` and ``<Foundation/NSDecimalNumber.h>``.

.. class::
    NSString

    The `NSString <https://developer.apple.com/documentation/foundation/nsstring?language=objc>`__ class from ``<Foundation/NSString.h>``.

    This class also supports all methods that :class:`str` does.

    .. note::

        :class:`NSString` objects consist of UTF-16 code units, unlike :class:`str`, which consists of Unicode code points. All :class:`NSString` indices and iteration are based on UTF-16, even when using the Python-style operations/methods. If indexing or iteration based on code points is required, convert the :class:`NSString` to :class:`str` first.

    .. method:: __str__()

        Return the value of this :class:`NSString` as a :class:`str`.

    .. attribute::
        UTF8String

        This Objective-C property has been declared using :meth:`ObjCClass.declare_property` and can always be accessed using attribute syntax.

.. class::
    NSData

    The `NSData <https://developer.apple.com/documentation/foundation/nsdata?language=objc>`__ class from ``<Foundation/NSData.h>``.

.. class::
    NSArray

    The `NSArray <https://developer.apple.com/documentation/foundation/nsarray?language=objc>`__ class from ``<Foundation/NSArray.h>``.

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

    The `NSMutableArray <https://developer.apple.com/documentation/foundation/nsmutablearray?language=objc>`__ class from ``<Foundation/NSArray.h>``.

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

    The `NSDictionary <https://developer.apple.com/documentation/foundation/nsdictionary?language=objc>`__ class from ``<Foundation/NSDictionary.h>``.

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

            Unlike most Python mappings, :class:`NSDictionary`'s :attr:`keys`, :attr:`values`, and :attr:`items` methods don't return dynamic views of the dictionary's keys, values, and items.

            :attr:`keys` and :attr:`values` return lists that are created each time the methods are called, which can have an effect on performance and memory usage for large dictionaries. To avoid this, you can cache the return values of :attr:`keys` and :attr:`values`, or convert the :class:`NSDictionary` to a Python :class:`dict` beforehand.

            :attr:`items` is currently implemented as a generator, meaning that it returns a single-use iterator. If you need to iterate over :attr:`items` more than once or perform other operations on it, you should convert it to a Python :class:`set` or :class:`list` first.

.. class::
    NSMutableDictionary

    The `NSMutableDictionary <https://developer.apple.com/documentation/foundation/nsmutabledictionary?language=objc>`__ class from ``<Foundation/NSDictionary.h>``.

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

.. autoclass:: ObjCProtocol(name_or_ptr, [bases, attrs])

    .. autoattribute:: name
    .. autoattribute:: protocols
    .. automethod:: __instancecheck__
    .. automethod:: __subclasscheck__

Standard Objective-C and Foundation protocols
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following protocols from the `Objective-C runtime <https://developer.apple.com/documentation/objectivec?language=objc>`__ and the `Foundation <https://developer.apple.com/documentation/foundation?language=objc>`__ framework are provided as :class:`ObjCProtocol`\s for convenience. (Other protocols not listed here can be looked up by passing a protocol name to the :class:`ObjCProtocol` constructor.)

.. data:: NSObjectProtocol

    The `NSObject <https://developer.apple.com/documentation/objectivec/1418956-nsobject?language=objc>`__ protocol from ``<objc/NSObject.h>``. The protocol is exported as :class:`NSObjectProtocol` in Python because it would otherwise clash with the :class:`NSObject` class.

Converting objects between Objective-C and Python
-------------------------------------------------

.. py_from_ns has an explicit parameter list to hide the private _auto kwarg.
.. autofunction:: py_from_ns(nsobj)
.. autofunction:: ns_from_py
.. function:: at(pyobj)

    Alias for :func:`ns_from_py`.

.. _auto-objc-python-conversion:

Automatic conversion of Objective-C objects to Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When Python code receives an Objective-C object, Rubicon will automatically convert certain kinds of objects to their Python counterparts, using a subset of the conversions performed by :func:`py_from_ns`:

* :class:`~rubicon.objc.runtime.objc_id` objects are converted to :class:`ObjCInstance` before further conversion
* :class:`NSDecimalNumber` objects are converted to :class:`decimal.Decimal`
* :class:`NSNumber` objects are converted to :class:`bool`, :class:`int`, or :class:`float` based on their contents

.. _custom-classes-and-protocols:

Creating custom Objective-C classes and protocols
-------------------------------------------------

Custom Objective-C classes are defined using Python ``class`` syntax, by subclassing an existing :class:`ObjCClass` object:

.. code-block:: python

    class MySubclass(NSObject):
        # method, property, etc. definitions go here

A custom Objective-C class can only have a single superclass, since Objective-C does not support multiple inheritance. However, the class can conform to any number of protocols, which are specified by adding the ``protocols`` keyword argument to the base class list:

.. code-block:: python

    class MySubclass(NSObject, protocols=[NSCopying, NSMutableCopying]):
        # method, property, etc. definitions go here

.. note::

    Rubicon requires specifying a superclass when defining a custom Objective-C class. If you don't need to extend any specific class, use :class:`NSObject` as the superclass.

    Although Objective-C technically allows defining classes without a base class (so-called *root classes*), this is almost never the desired behavior (attempting to do so `causes a compiler error by default <https://developer.apple.com/documentation/objectivec/objc_root_class>`_). In practice, this feature is only used in the definitions of core Objective-C classes like :class:`NSObject`. Because of this, Rubicon does not support defining Objective-C root classes.

Similar syntax is used to define custom Objective-C protocols. Unlike classes, protocols can extend multiple other protocols:

.. code-block:: python

    class MyProtocol(NSCopying, NSMutableCopying):
        # method, property, etc. definitions go here

A custom protocol might not need to extend any other protocol at all. In this case, we need to explicitly tell Python to define an :class:`ObjCProtocol`. Normally Python detects the metaclass automatically by examining the base classes, but in this case there are none, so we need to specify the metaclass manually.

.. code-block:: python

    class MyProtocol(metaclass=ObjCProtocol):
        # method, property, etc. definitions go here

Defining methods
^^^^^^^^^^^^^^^^

.. autofunction:: objc_method
.. autofunction:: objc_classmethod

Method naming
"""""""""""""

The name of a Python-defined Objective-C method is same as the Python method's name, but with all underscores (``_``) replaced with colons (``:``) --- for example, ``initWithWidth_height_`` becomes ``initWithWidth:height:``.

.. warning::

    The Objective-C *language* imposes certain requirements on the usage of colons in method names: a method's name must contain exactly as many colons as the method has arguments (excluding the implicit ``self`` and ``_cmd`` parameters), and the name of a method with arguments must end with a colon. For example, a method called ``init`` takes no arguments, ``initWithSize:`` takes a single argument, ``initWithWidth:height:`` takes two, etc. ``initWithSize:spam`` is an invalid method name.

    These requirements are not enforced by the Objective-C *runtime*, but methods that do not follow them cannot easily be used from regular Objective-C code.

    In addition, although the Objective-C language allows method names with multiple consecutive colons or a colon at the start of the name, such names are considered bad style and never used in practice. For example, ``spam::``, ``:ham:``, and ``:`` are unusual, but valid method names.

    Future versions of Rubicon may warn about or disallow such nonstandard method names.

Parameter and return types
""""""""""""""""""""""""""

The argument and return types of a Python-created Objective-C method are determined based on the Python method's type annotations. The annotations may contain any :mod:`ctypes` type, as well as any of the Python types accepted by :func:`~rubicon.objc.types.ctype_for_type`. If a parameter or the return type is not specified, it defaults to :class:`ObjCInstance`. The ``self`` parameter is special-cased --- its type is always :class:`ObjCInstance`, even if annotated otherwise. To annotate a method as returning ``void``, set its return type to ``None``.

Before being passed to the Python method, the arguments are :ref:`converted automatically <auto-objc-python-conversion>`. If the method returns an Objective-C object, it is converted using :func:`ns_from_py` before being returned to Objective-C. These automatic conversions can be disabled by using :func:`objc_rawmethod` instead of :func:`objc_method`.

The implicit ``_cmd`` parameter is not passed to the Python method, as it is normally redundant and not needed. If needed, the ``_cmd`` parameter can be accessed by using :func:`objc_rawmethod` instead of :func:`objc_method`.

.. autofunction:: objc_rawmethod

Defining properties and ivars
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: objc_property
.. autofunction:: objc_ivar
.. autofunction:: get_ivar
.. autofunction:: set_ivar

Objective-C blocks
------------------

.. autoclass:: ObjCBlock(pointer, [return_type, *arg_types])
.. autoclass:: Block(func, [restype, *argtypes])

Defining custom subclasses of :class:`ObjCInstance`
---------------------------------------------------

The following functions can be used to register custom subclasses of :class:`ObjCInstance` to be used when wrapping instances of a certain Objective-C class. This mechanism is for example used by Rubicon to provide Python-style operators and methods on standard Foundation classes, such as :class:`NSString` and :class:`NSDictionary`.

.. autofunction:: register_type_for_objcclass
.. autofunction:: for_objcclass
.. autofunction:: type_for_objcclass
.. autofunction:: unregister_type_for_objcclass
.. autofunction:: get_type_for_objcclass_map
