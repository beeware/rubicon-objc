====================================================================
:mod:`rubicon.objc.runtime` --- Low-level Objective-C runtime access
====================================================================

.. module:: rubicon.objc.runtime

This module contains types, functions, and C libraries used for low-level
access to the Objective-C runtime.

In most cases there is no need to use this module directly --- the
:mod:`rubicon.objc.api` module provides the same functionality through a
high-level interface.

.. _predefined-c-libraries:

C libraries
-----------

Some commonly used C libraries are provided as :class:`~ctypes.CDLL`\s. Other
libraries can be loaded using the :func:`load_library` function.

.. data:: libc
    :annotation: = load_library('c')

    The `C standard library <https://en.cppreference.com/w/c>`__.

    The following functions are accessible by default:

    .. hlist::
        * ``free``

.. data:: libobjc
    :annotation: = load_library('objc')

    The `Objective-C runtime library <https://developer.apple.com/documentation/objectivec>`__.

    The following functions are accessible by default:

    .. hlist::
        * ``class_addIvar``
        * ``class_addMethod``
        * ``class_addProperty``
        * ``class_addProtocol``
        * ``class_copyIvarList``
        * ``class_copyMethodList``
        * ``class_copyPropertyList``
        * ``class_copyProtocolList``
        * ``class_getClassMethod``
        * ``class_getClassVariable``
        * ``class_getInstanceMethod``
        * ``class_getInstanceSize``
        * ``class_getInstanceVariable``
        * ``class_getIvarLayout``
        * ``class_getMethodImplementation``
        * ``class_getName``
        * ``class_getProperty``
        * ``class_getSuperclass``
        * ``class_getVersion``
        * ``class_getWeakIvarLayout``
        * ``class_isMetaClass``
        * ``class_replaceMethod``
        * ``class_respondsToSelector``
        * ``class_setIvarLayout``
        * ``class_setVersion``
        * ``class_setWeakIvarLayout``
        * ``ivar_getName``
        * ``ivar_getOffset``
        * ``ivar_getTypeEncoding``
        * ``method_exchangeImplementations``
        * ``method_getImplementation``
        * ``method_getName``
        * ``method_getTypeEncoding``
        * ``method_setImplementation``
        * ``objc_allocateClassPair``
        * ``objc_copyProtocolList``
        * ``objc_getAssociatedObject``
        * ``objc_getClass``
        * ``objc_getMetaClass``
        * ``objc_getProtocol``
        * ``objc_registerClassPair``
        * ``objc_removeAssociatedObjects``
        * ``objc_setAssociatedObject``
        * ``object_getClass``
        * ``object_getClassName``
        * ``object_getIvar``
        * ``object_setIvar``
        * ``property_getAttributes``
        * ``property_getName``
        * ``property_copyAttributeList``
        * ``protocol_addMethodDescription``
        * ``protocol_addProtocol``
        * ``protocol_addProperty``
        * ``objc_allocateProtocol``
        * ``protocol_conformsToProtocol``
        * ``protocol_copyMethodDescriptionList``
        * ``protocol_copyPropertyList``
        * ``protocol_copyProtocolList``
        * ``protocol_getMethodDescription``
        * ``protocol_getName``
        * ``objc_registerProtocol``
        * ``sel_getName``
        * ``sel_isEqual``
        * ``sel_registerName``

.. data:: Foundation
    :annotation: = load_library('Foundation')

    The `Foundation <https://developer.apple.com/documentation/foundation>`__
    framework.

.. autofunction:: load_library

Objective-C runtime types
-------------------------

These are various types used by the Objective-C runtime functions.

.. autoclass:: objc_id([value])
.. autoclass:: objc_block([value])

.. autoclass:: SEL([value])

    .. autoattribute:: name

.. autoclass:: Class([value])
.. autoclass:: IMP([value])
.. autoclass:: Method([value])
.. autoclass:: Ivar([value])
.. autoclass:: objc_property_t([value])

.. autoclass:: objc_property_attribute_t([name, value])

    .. attribute::
        name
        value

        The attribute name and value as C strings (:class:`bytes`).

.. autoclass:: objc_method_description([name, value])

    .. attribute:: name

        The method name as a :class:`SEL`.

    .. attribute:: types

        The method's signature encoding as a C string (:class:`bytes`).

.. autoclass:: objc_super([receiver, super_class])

    .. attribute:: receiver

        The receiver of the call, as an :class:`objc_id`.

    .. attribute:: super_class

        The class in which to start searching for method implementations, as a
        :class:`Class`.

Objective-C runtime utility functions
-------------------------------------

These utility functions provide easier access from Python to certain parts of
the Objective-C runtime.

.. function:: object_isClass(obj)

    Return whether the given Objective-C object is a class (or a metaclass).

    This is equivalent to the :data:`libobjc` function `object_isClass
    <https://developer.apple.com/documentation/objectivec/1418659-object_isclass?language=objc>`__
    from ``<objc/runtime.h>``, which is only available since OS X 10.10 and iOS
    8. This module-level function is provided to support older systems --- it
    uses the :data:`libobjc` function if available, and otherwise emulates it.

.. autofunction:: get_class
.. autofunction:: should_use_stret
.. autofunction:: should_use_fpret
.. autofunction:: send_message
.. autofunction:: send_super
.. autofunction:: add_method
.. autofunction:: add_ivar
.. autofunction:: get_ivar
.. autofunction:: set_ivar
