=================================================================
:mod:`rubicon.objc.types` --- Non-Objective-C types and utilities
=================================================================

.. module:: rubicon.objc.types

This module contains definitions for common C constants and types, and
utilities for working with C types.

Common C type definitions
-------------------------

These are commonly used C types from various frameworks.

.. class:: c_ptrdiff_t([value])

    The `ptrdiff_t <https://en.cppreference.com/w/c/types/ptrdiff_t>`__ type
    from ``<stddef.h>``. Equivalent to :class:`~ctypes.c_long` on 64-bit
    systems and :class:`~ctypes.c_int` on 32-bit systems.

.. class:: NSInteger([value])

    The `NSInteger
    <https://developer.apple.com/documentation/objectivec/nsinteger?language=objc>`__
    type from ``<objc/NSObjCRuntime.h>``. Equivalent to :class:`~ctypes.c_long`
    on 64-bit systems and :class:`~ctypes.c_int` on 32-bit systems.

.. class:: NSUInteger([value])

    The `NSUInteger
    <https://developer.apple.com/documentation/objectivec/nsuinteger?language=objc>`__
    type from ``<objc/NSObjCRuntime.h>``. Equivalent to
    :class:`~ctypes.c_ulong` on 64-bit systems and :class:`~ctypes.c_uint` on
    32-bit systems.

.. class:: CGFloat([value])

    The `CGFloat
    <https://developer.apple.com/documentation/corefoundation/cgfloat?language=objc>`__
    type from ``<CoreGraphics/CGBase.h>``. Equivalent to
    :class:`~ctypes.c_double` on 64-bit systems and :class:`~ctypes.c_float` on
    32-bit systems.

.. class:: NSPoint([x, y])

    The `NSPoint
    <https://developer.apple.com/documentation/foundation/nspoint?language=objc>`__
    structure from ``<Foundation/NSGeometry.h>``.

    .. note::

        On 64-bit systems this is an alias for :class:`CGPoint`.

    .. attribute::
        x
        y

        The X and Y coordinates as :class:`CGFloat`\s.

.. class:: CGPoint([x, y])

    The `CGPoint
    <https://developer.apple.com/documentation/corefoundation/cgpoint?language=objc>`__
    structure from ``<CoreGraphics/CGGeometry.h>``.

    .. attribute::
        x
        y

        The X and Y coordinates as :class:`CGFloat`\s.

.. class:: NSSize([width, height])

    The `NSSize
    <https://developer.apple.com/documentation/foundation/nssize?language=objc>`__
    structure from ``<Foundation/NSGeometry.h>``.

    .. note::

        On 64-bit systems this is an alias for :class:`CGSize`.

    .. attribute::
        width
        height

        The width and height as :class:`CGFloat`\s.

.. class:: CGSize([width, height])

    The `CGSize
    <https://developer.apple.com/documentation/corefoundation/cgsize?language=objc>`__
    structure from ``<CoreGraphics/CGGeometry.h>``.

    .. attribute::
        width
        height

        The width and height as :class:`CGFloat`\s.

.. class:: NSRect([origin, size])

    The `NSRect
    <https://developer.apple.com/documentation/foundation/nsrect?language=objc>`__
    structure from ``<Foundation/NSGeometry.h>``.

    .. note::

        On 64-bit systems this is an alias for :class:`CGRect`.

    .. attribute:: origin

        The origin as a :class:`NSPoint`.

    .. attribute:: size

        The size as a :class:`NSSize`.

.. class:: CGRect([origin, size])

    The `CGRect
    <https://developer.apple.com/documentation/corefoundation/cgrect?language=objc>`__
    structure from ``<CoreGraphics/CGGeometry.h>``.

    .. attribute:: origin

        The origin as a :class:`CGPoint`.

    .. attribute:: size

        The size as a :class:`CGSize`.

.. class:: UIEdgeInsets([top, left, bottom, right])

    The `UIEdgeInsets
    <https://developer.apple.com/documentation/uikit/uiedgeinsets?language=objc>`__
    structure from ``<UIKit/UIGeometry.h>``.

    .. attribute::
        top
        left
        bottom
        right

        The insets as :class:`CGFloat`\s.

.. class:: NSEdgeInsets([top, left, bottom, right])

    The `NSEdgeInsets
    <https://developer.apple.com/documentation/foundation/nsedgeinsets?language=objc>`__
    structure from ``<Foundation/NSGeometry.h>``.

    .. attribute::
        top
        left
        bottom
        right

        The insets as :class:`CGFloat`\s.

.. class:: NSTimeInterval([value])

    The `NSTimeInterval
    <https://developer.apple.com/documentation/foundation/nstimeinterval?language=objc>`__
    type from ``<Foundation/NSDate.h>``. Equivalent to :class:`~ctypes.c_double`.

.. class:: CFIndex([value])

    The `CFIndex
    <https://developer.apple.com/documentation/corefoundation/cfindex?language=objc>`__
    type from ``<CoreFoundation/CFBase.h>``. Equivalent to
    :class:`~ctypes.c_longlong` on 64-bit systems and
    :class:`~ctypes.c_long` on 32-bit systems.

.. class:: UniChar([value])

    The ``UniChar`` type from ``<MacTypes.h>``. Equivalent to
    :class:`~ctypes.c_ushort`.

.. class:: unichar([value])

    The `unichar
    <https://developer.apple.com/documentation/foundation/unichar?language=objc>`__
    type from ``<Foundation/NSString.h>``. Equivalent to
    :class:`~ctypes.c_ushort`.

.. class:: CGGlyph([value])

    The `CGGlyph
    <https://developer.apple.com/documentation/coregraphics/cgglyph?language=objc>`__
    type from ``<CoreGraphics/CGFont.h>``. Equivalent to
    :class:`~ctypes.c_ushort`.

.. class:: CFRange([location, length])

    The `CFRange
    <https://developer.apple.com/documentation/corefoundation/cfrange?language=objc>`__
    type from ``<CoreFoundation/CFBase.h>``.

    .. attribute::
        location
        length

        The location and length as :class:`CFIndex`\es.

.. class:: NSRange([location, length])

    The `NSRange
    <https://developer.apple.com/documentation/foundation/nsrange?language=objc>`__
    type from ``<Foundation/NSRange.h>``.

    .. attribute::
        location
        length

        The location and length as :class:`NSUInteger`\s.

Common C constants
------------------

These are commonly used C constants from various frameworks.

.. data:: UIEdgeInsetsZero

    The constant `UIEdgeInsetsZero
    <https://developer.apple.com/documentation/uikit/uiedgeinsetszero?language=objc>`__:
    a :class:`UIEdgeInsets` instance with all insets set to zero.

.. data:: NSZeroPoint

    The constant `NSZeroPoint
    <https://developer.apple.com/documentation/foundation/nszeropoint?language=objc>`__:
    a :class:`NSPoint` instance with the X and Y coordinates set to zero.

.. data:: NSIntegerMax

    The macro constant `NSIntegerMax
    <https://developer.apple.com/documentation/objectivec/nsintegermax?language=objc>`__
    from ``<objc/NSObjCRuntime.h>``: the maximum value that a
    :class:`NSInteger` can hold.

.. data:: NSNotFound

    The constant `NSNotFound
    <https://developer.apple.com/documentation/foundation/nsnotfound?language=objc>`__
    from ``<Foundation/NSObjCRuntime.h>``: a :class:`NSInteger` sentinel value
    indicating that an item was not found (usually when searching in a
    collection).

Architecture detection constants
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following constants provide information about the architecture of the
current environment. All of them are equivalent to the C compiler macros of the
same names.

.. data:: __LP64__

    Indicates whether the current environment is 64-bit. If true, C ``long``\s
    and pointers are 64 bits in size, otherwise 32 bits.

.. data::
    __i386__
    __x86_64__
    __arm__
    __arm64__

    Each of these constants is true if the current environment uses the named
    architecture. At most one of these constants is true at once in a single
    Python runtime. (If the current architecture cannot be determined, all of
    these constants are false.)

Objective-C type encoding conversion
------------------------------------

These functions are used to convert Objective-C type encoding strings to and
from :mod:`ctypes` types, and to manage custom conversions in both directions.

All Objective-C encoding strings are represented as :class:`bytes` rather than
:class:`str`.

.. autofunction:: ctype_for_encoding
.. autofunction:: encoding_for_ctype
.. autofunction:: register_preferred_encoding
.. autofunction:: with_preferred_encoding
.. autofunction:: register_encoding
.. autofunction:: with_encoding
.. autofunction:: unregister_encoding
.. autofunction:: unregister_encoding_all
.. autofunction:: unregister_ctype
.. autofunction:: unregister_ctype_all
.. autofunction:: get_ctype_for_encoding_map
.. autofunction:: get_encoding_for_ctype_map
.. autofunction:: split_method_encoding
.. autofunction:: ctypes_for_method_encoding

Default registered type encodings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following table lists Objective-C's standard type encodings for primitive
types, and the corresponding registered ctypes. These mappings can be
considered stable, but nonetheless users should not hard code these encodings
unless necessary. Instead, the :func:`encoding_for_ctype` function should be
used to encode types, because it is less error-prone and more readable than
typing encodings out by hand.

========================================= ========================== =====
``Ctype``                                 Type encoding              Notes
========================================= ========================== =====
``None`` (``void``)                       ``v``
:class:`~ctypes.c_bool`                   ``B``                      This refers to the ``bool`` type from C99 and C++. It is not necessarily the same as the `BOOL` type, which may be either :class:`~ctypes.c_byte` or :class:`~ctypes.c_bool` depending on the system and architecture.
:class:`~ctypes.c_byte`                   ``c``
:class:`~ctypes.c_ubyte`                  ``C``
:class:`~ctypes.c_short`                  ``s``
:class:`~ctypes.c_ushort`                 ``S``
:class:`~ctypes.c_long`                   ``l``
:class:`~ctypes.c_ulong`                  ``L``
:class:`~ctypes.c_int`                    ``i``                      On 32-bit systems, :class:`~ctypes.c_int` is an alias for :class:`~ctypes.c_long`, and will be encoded as such.
:class:`~ctypes.c_uint`                   ``I``                      On 32-bit systems, :class:`~ctypes.c_uint` is an alias for :class:`~ctypes.c_ulong`, and will be encoded as such.
:class:`~ctypes.c_longlong`               ``q``                      On 64-bit systems, :class:`~ctypes.c_longlong` is an alias for :class:`~ctypes.c_long`, and will be encoded as such.
:class:`~ctypes.c_ulonglong`              ``Q``                      On 64-bit systems, :class:`~ctypes.c_ulonglong` is an alias for :class:`~ctypes.c_ulong`, and will be encoded as such.
:class:`~ctypes.c_float`                  ``f``
:class:`~ctypes.c_double`                 ``d``
:class:`~ctypes.c_longdouble`             ``D``                      On ARM, :class:`~ctypes.c_longdouble` is an alias for :class:`~ctypes.c_double`, and will be encoded as such.
:class:`~ctypes.c_char`                   ``c``                      Only when encoding. Decoding ``c`` produces :class:`~ctypes.c_byte`, to allow using ``signed char`` as a Boolean value.
:class:`~ctypes.c_char_p`                 ``*``
``POINTER(c_char)``                       ``*``                      Only when encoding. Decoding ``*`` produces :class:`~ctypes.c_char_p` for easier use of C strings.
``POINTER(c_byte)``                       ``*``                      Only when encoding. Decoding ``*`` produces :class:`~ctypes.c_char_p` for easier use of C strings.
``POINTER(c_ubyte)``                      ``*``                      Only when encoding. Decoding ``*`` produces :class:`~ctypes.c_char_p` for easier use of C strings.
:class:`~ctypes.c_wchar`                  ``i``                      Only when encoding. Decoding ``i`` produces :class:`~ctypes.c_int`.
:class:`~ctypes.c_wchar_p`                ``^i``                     Only when encoding. Decoding ``^i`` produces ``POINTER(c_int)``.
:class:`~ctypes.c_void_p`                 ``^v``
:class:`UnknownPointer`                   ``^?``                     This encoding stands for a pointer to a type that cannot be encoded, which in practice means a function pointer.
:class:`UnknownPointer`                   ``^{?}``, ``^(?)``         Only when decoding. These encodings stand for pointers to a structure or union with unknown name and fields.
:class:`~rubicon.objc.runtime.objc_id`    ``@``                      Class name suffixes in the encoding (e. g. ``@"NSString"``) are ignored.
:class:`~rubicon.objc.runtime.objc_block` ``@?``                     Block signature suffixes in the encoding (e. g. ``@?<v@?>``) are ignored.
:class:`~rubicon.objc.runtime.SEL`        ``:``
:class:`~rubicon.objc.runtime.Class`      ``#``
========================================= ========================== =====

.. autoclass:: UnknownPointer

In addition, the following types defined by Rubicon are registered, but their encodings may vary depending on the system
and architecture:

.. hlist::

    * :class:`ctypes.py_object`
    * :class:`NSInteger`
    * :class:`NSUInteger`
    * :class:`CGFloat`
    * :class:`NSPoint`
    * :class:`CGPoint`
    * :class:`NSSize`
    * :class:`CGSize`
    * :class:`NSRect`
    * :class:`CGRect`
    * :class:`UIEdgeInsets`
    * :class:`NSEdgeInsets`
    * :class:`NSTimeInterval`
    * :class:`CFIndex`
    * :class:`UniChar`
    * :class:`unichar`
    * :class:`CGGlyph`
    * :class:`NSRange`

Conversion of Python sequences to C structures and arrays
---------------------------------------------------------

This function is used to convert a Python sequence (such as a :class:`tuple` or
:class:`list`) to a specific C structure or array type. This function is mainly
used internally by Rubicon, to allow passing Python sequences as method
parameters where a C structure or array would normally be required. Most users
will not need to use this function directly.

.. autofunction:: compound_value_for_sequence

Python to :mod:`ctypes` type mapping
------------------------------------

These functions are used to map Python types to equivalent :mod:`ctypes` types,
and to add or remove such mappings. This mechanism is mainly used internally by
Rubicon, to for example allow :class:`~rubicon.objc.api.ObjCInstance` to be
used instead of :class:`~rubicon.objc.runtime.objc_id` in method type
annotations. Most users will not need to use these functions directly.

.. autofunction:: ctype_for_type
.. autofunction:: register_ctype_for_type
.. autofunction:: unregister_ctype_for_type
.. autofunction:: get_ctype_for_type_map

Default registered mappings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following mappings are registered by default by Rubicon.

======================================= =======
Python type                             `Ctype`
======================================= =======
:class:`int`                            :class:`~ctypes.c_int`
:class:`float`                          :class:`~ctypes.c_float`
:class:`bool`                           :class:`~ctypes.c_bool`
:class:`bytes`                          :class:`~ctypes.c_char_p`
:class:`~rubicon.objc.api.ObjCInstance` :class:`~rubicon.objc.runtime.objc_id`
:class:`~rubicon.objc.api.ObjCClass`    :class:`~rubicon.objc.runtime.Class`
======================================= =======
