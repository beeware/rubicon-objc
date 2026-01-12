# `rubicon.objc.types` - Non-Objective-C types and utilities { #rubicon-types }

This module contains definitions for common C constants and types, and utilities for working with C types.

## Common C type definitions

These are commonly used C types from various frameworks.

::: rubicon.objc.types.c_ptrdiff_t

::: rubicon.objc.types.NSInteger

::: rubicon.objc.types.NSUInteger

::: rubicon.objc.types.CGFloat

::: rubicon.objc.types.NSPoint

::: rubicon.objc.types.CGPoint

::: rubicon.objc.types.NSSize

::: rubicon.objc.types.CGSize

::: rubicon.objc.types.NSRect

::: rubicon.objc.types.CGRect

::: rubicon.objc.types.UIEdgeInsets

::: rubicon.objc.types.NSEdgeInsets

::: rubicon.objc.types.NSTimeInterval

::: rubicon.objc.types.CFIndex

::: rubicon.objc.types.UniChar

::: rubicon.objc.types.unichar

::: rubicon.objc.types.CGGlyph

::: rubicon.objc.types.CFRange

::: rubicon.objc.types.NSRange

## Common C constants
module level - document in source These are commonly used C constants from various frameworks.

::: rubicon.objc.types.UIEdgeInsetsZero

::: rubicon.objc.types.NSZeroPoint

::: rubicon.objc.types.NSIntegerMax
    options:
        show_attribute_values: false

::: rubicon.objc.types.NSNotFound
    options:
        show_attribute_values: false

### Architecture detection constants

The following constants provide information about the architecture of the current environment. All of them are equivalent to the C compiler macros of the same names.

::: rubicon.objc.types.__LP64__
    options:
        show_attribute_values: false
        heading_level: 4

Each of the following constants is true if the current environment uses the named architecture. At most one of these constants is true at once in a single Python runtime. (If the current architecture cannot be determined, all of these constants are false.)

::: rubicon.objc.types.__i386__
    options:
        show_attribute_values: false
        heading_level: 4

::: rubicon.objc.types.__x86_64__
    options:
        show_attribute_values: false
        heading_level: 4

::: rubicon.objc.types.__arm__
    options:
        show_attribute_values: false
        heading_level: 4

::: rubicon.objc.types.__arm64__
    options:
        show_attribute_values: false
        heading_level: 4

## Objective-C type encoding conversion

These functions are used to convert Objective-C type encoding strings to and from [`ctypes`][] types, and to manage custom conversions in both directions.

All Objective-C encoding strings are represented as [`bytes`][] rather than [`str`][].

::: rubicon.objc.types.ctype_for_encoding

::: rubicon.objc.types.encoding_for_ctype

::: rubicon.objc.types.register_preferred_encoding

::: rubicon.objc.types.with_preferred_encoding

::: rubicon.objc.types.register_preferred_encoding

::: rubicon.objc.types.with_encoding

::: rubicon.objc.types.unregister_encoding

::: rubicon.objc.types.unregister_encoding_all

::: rubicon.objc.types.unregister_ctype

::: rubicon.objc.types.unregister_ctype_all

::: rubicon.objc.types.get_ctype_for_encoding_map

::: rubicon.objc.types.get_encoding_for_ctype_map

::: rubicon.objc.types.split_method_encoding

::: rubicon.objc.types.ctypes_for_method_encoding

::: rubicon.objc.types.UnknownPointer

### Default registered type encodings

The following table lists Objective-C's standard type encodings for primitive types, and the corresponding registered ctypes. These mappings can be considered stable, but nonetheless users should not hard code these encodings unless necessary. Instead, the [`encoding_for_ctype`][rubicon.objc.types.encoding_for_ctype] function should be used to encode types, because it is less error-prone and more readable than typing encodings out by hand.

| `Ctype`                                               | Type encoding  | Notes                                                                                                                                                                                                                                                |
|-------------------------------------------------------|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `None` (`void`)                                       | `v`            |                                                                                                                                                                                                                                                      |
| [`c_bool`][ctypes.c_bool]                             | `B`            | This refers to the `bool` type from C99 and C++. It is not necessarily the same as the <span class="title-ref">BOOL</span> type, which may be either [`c_byte`][ctypes.c_byte]or [`c_bool`][ctypes.c_bool] depending on the system and architecture. |
| [`c_byte`][ctypes.c_byte]                             | `c`            |                                                                                                                                                                                                                                                      |
| [`c_ubyte`][ctypes.c_ubyte]                           | `C`            |                                                                                                                                                                                                                                                      |
| [`c_short`][ctypes.c_short]                           | `s`            |                                                                                                                                                                                                                                                      |
| [`c_ushort`][ctypes.c_ushort]                         | `S`            |                                                                                                                                                                                                                                                      |
| [`c_long`][ctypes.c_long]                             | `l`            |                                                                                                                                                                                                                                                      |
| [`c_ulong`][ctypes.c_ulong]                           | `L`            |                                                                                                                                                                                                                                                      |
| [`c_int`][ctypes.c_int]                               | `i`            | On 32-bit systems, [`c_int`][ctypes.c_int] is an alias for [`c_long`][ctypes.c_long], and will be encoded as such.                                                                                                                                   |
| [`c_uint`][ctypes.c_uint]                             | `I`            | On 32-bit systems, [`c_uint`][ctypes.c_uint] is an alias for [`c_ulong`][ctypes.c_ulong], and will be encoded as such.                                                                                                                               |
| [`c_longlong`][ctypes.c_longlong]                     | `q`            | On 64-bit systems, [`c_longlong`][ctypes.c_longlong] is an alias for [`c_long`][ctypes.c_long], and will be encoded as such.                                                                                                                         |
| [`c_ulonglong`][ctypes.c_ulonglong]                   | `Q`            | On 64-bit systems, [`c_ulonglong`][ctypes.c_ulonglong]is an alias for [`c_ulong`][ctypes.c_ulong], and will be encoded as such.                                                                                                                      |
| [`c_float`][ctypes.c_float]                           | `f`            |                                                                                                                                                                                                                                                      |
| [`c_double`][ctypes.c_double]                         | `d`            |                                                                                                                                                                                                                                                      |
| [`c_longdouble`][ctypes.c_longdouble]                 | `D`            | On ARM, [`c_longdouble`][ctypes.c_longdouble]is an alias for [`c_double`][ctypes.c_double], and will be encoded as such.                                                                                                                             |
| [`c_char`][ctypes.c_char]                             | `c`            | Only when encoding. Decoding `c` produces [`ctypes.c_byte`][], to allow using `signed char` as a Boolean value.                                                                                                         |
| [`c_char_p`][ctypes.c_char_p]                         | `*`            |                                                                                                                                                                                                                                                      |
| `POINTER(c_char)`                                     | `*`            | Only when encoding. Decoding `*` produces [`c_char_p`][ctypes.c_char_p] for easier use of C strings.                                                                                                                                                 |
| `POINTER(c_byte)`                                     | `*`            | Only when encoding. Decoding `*` produces [`c_char_p`][ctypes.c_char_p] for easier use of C strings.                                                                                                                                                 |
| `POINTER(c_ubyte)`                                    | `*`            | Only when encoding. Decoding `*` produces [`c_char_p`][ctypes.c_char_p] for easier use of C strings.                                                                                                                                                 |
| [`c_wchar`][ctypes.c_wchar]                           | `i`            | Only when encoding. Decoding `i` produces [`c_int`][ctypes.c_int].                                                                                                                                                                                   |
| [`c_wchar_p`][ctypes.c_wchar_p]                       | `^i`           | Only when encoding. Decoding `^i` produces `POINTER(c_int)`.                                                                                                                                                                                         |
| [`c_void_p`][ctypes.c_void_p]                         | `^v`           |                                                                                                                                                                                                                                                      |
| [`UnknownPointer`][rubicon.objc.types.UnknownPointer] | `^?`           | This encoding stands for a pointer to a type that cannot be encoded, which in practice means a function pointer.                                                                                                                                     |
| [`UnknownPointer`][rubicon.objc.types.UnknownPointer] | `^{?}`, `^(?)` | Only when decoding. These encodings stand for pointers to a structure or union with unknown name and fields.                                                                                                                                         |
| [`objc_id`][rubicon.objc.runtime.objc_id]             | `@`            | Class name suffixes in the encoding (e. g. `@"NSString"`) are ignored.                                                                                                                                                                               |
| [`objc_block`][rubicon.objc.runtime.objc_block]       | `@?`           | Block signature suffixes in the encoding (e. g. `@?<v@?>`) are ignored.                                                                                                                                                                              |
| [`SEL`][rubicon.objc.runtime.SEL]                     | `:`            |                                                                                                                                                                                                                                                      |
| [`Class`][rubicon.objc.runtime.Class]                 | `#`            |                                                                                                                                                                                                                                                      |

In addition, the following types defined by Rubicon are registered, but their encodings may vary depending on the system and architecture:

* [`ctypes.py_object`][]
* [`NSInteger`][rubicon.objc.types.NSInteger]
* [`NSUInteger`][rubicon.objc.types.NSUInteger]
* [`CGFloat`][rubicon.objc.types.CGFloat]
* [`NSPoint`][rubicon.objc.types.NSPoint]
* [`CGPoint`][rubicon.objc.types.CGPoint]
* [`NSSize`][rubicon.objc.types.NSSize]
* [`CGSize`][rubicon.objc.types.CGSize]
* [`NSRect`][rubicon.objc.types.NSRect]
* [`CGRect`][rubicon.objc.types.CGRect]
* [`UIEdgeInsets`][rubicon.objc.types.UIEdgeInsets]
* [`NSEdgeInsets`][rubicon.objc.types.NSEdgeInsets]
* [`NSTimeInterval`][rubicon.objc.types.NSTimeInterval]
* [`CFIndex`][rubicon.objc.types.CFIndex]
* [`UniChar`][rubicon.objc.types.UniChar]
* [`unichar`][rubicon.objc.types.unichar]
* [`CGGlyph`][rubicon.objc.types.CGGlyph]
* [`NSRange`][rubicon.objc.types.NSRange]

## Conversion of Python sequences to C structures and arrays

This function is used to convert a Python sequence (such as a [`tuple`][] or [`list`][]) to a specific C structure or array type. This function is mainly used internally by Rubicon, to allow passing Python sequences as method parameters where a C structure or array would normally be required. Most users will not need to use this function directly.

::: rubicon.objc.types.compound_value_for_sequence

## Python to [`ctypes`][] type mapping

These functions are used to map Python types to equivalent [`ctypes`][] types, and to add or remove such mappings. This mechanism is mainly used internally by Rubicon, to for example allow [`ObjCInstance`][rubicon.objc.api.ObjCInstance] to be used instead of [`objc_id`][rubicon.objc.runtime.objc_id] in method type annotations. Most users will not need to use these functions directly.

::: rubicon.objc.types.ctype_for_type

::: rubicon.objc.types.register_ctype_for_type

::: rubicon.objc.types.unregister_ctype_for_type

::: rubicon.objc.types.get_ctype_for_type_map

### Default registered mappings

The following mappings are registered by default by Rubicon.

| Python type                                     | <span class="title-ref">Ctype</span>      |
|-------------------------------------------------|-------------------------------------------|
| [`int`][]                                       | [`c_int`][ctypes.c_int]                   |
| [`float`][]                                     | [`c_float`][ctypes.c_float]               |
| [`bool`][]                                      | [`c_bool`][ctypes.c_bool]                 |
| [`bytes`][]                                     | [`c_char_p`][ctypes.c_char_p]             |
| [`ObjCInstance`][rubicon.objc.api.ObjCInstance] | [`objc_id`][rubicon.objc.runtime.objc_id] |
| [`ObjCClass`][rubicon.objc.api.ObjCClass]       | [`Class`][rubicon.objc.runtime.Class]     |

## Constructor methods

::: rubicon.objc.types.CGPointMake

::: rubicon.objc.types.CGRectMake

::: rubicon.objc.types.CGSizeMake

::: rubicon.objc.types.NSEdgeInsetsMake

Creates an NSEdgeInsets structure using top, left, bottom, and right values.

::: rubicon.objc.types.NSMakePoint

::: rubicon.objc.types.NSMakeRect

::: rubicon.objc.types.NSMakeSize

::: rubicon.objc.types.UIEdgeInsetsMake
