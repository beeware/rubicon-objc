# `rubicon.objc.types` - Non-Objective-C types and utilities

This module contains definitions for common C constants and types, and
utilities for working with C types.

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
module level - document in source
These are commonly used C constants from various frameworks.

<:> UIEdgeInsetsZero
<!-- TODO: data -->
<!-- TODO: Doc notes -->
The constant
[UIEdgeInsetsZero](https://developer.apple.com/documentation/uikit/uiedgeinsetszero?language=objc):
a `UIEdgeInsets`{.interpreted-text role="class"} instance with all
insets set to zero.

<:> NSZeroPoint
<!-- TODO: data -->
<!-- TODO: Doc notes -->
The constant
[NSZeroPoint](https://developer.apple.com/documentation/foundation/nszeropoint?language=objc):
a [`NSPoint`][rubicon.objc.types.NSPoint] instance with the X and Y
coordinates set to zero.


<:> NSIntegerMax
<!-- TODO: data -->
<!-- TODO: Doc notes -->
The macro constant
[NSIntegerMax](https://developer.apple.com/documentation/objectivec/nsintegermax?language=objc)
from `<objc/NSObjCRuntime.h>`: the maximum value that a
`NSInteger`{.interpreted-text role="class"} can hold.


<:> NSNotFound
<!-- TODO: data -->
<!-- TODO: Doc notes -->
The constant
[NSNotFound](https://developer.apple.com/documentation/foundation/nsnotfound?language=objc)
from `<Foundation/NSObjCRuntime.h>`: a `NSInteger`{.interpreted-text
role="class"} sentinel value indicating that an item was not found
(usually when searching in a collection).


### Architecture detection constants

The following constants provide information about the architecture of
the current environment. All of them are equivalent to the C compiler
macros of the same names.

<:> LP64
<!-- TODO: data -->
<!-- TODO: Doc notes -->
Indicates whether the current environment is 64-bit. If true, C `long`s
and pointers are 64 bits in size, otherwise 32 bits.


<:> i386   x86_64   arm   arm64
<!-- TODO: data -->
<!-- TODO: Doc notes -->
Each of these constants is true if the current environment uses the
named architecture. At most one of these constants is true at once in a
single Python runtime. (If the current architecture cannot be
determined, all of these constants are false.)


## Objective-C type encoding conversion

These functions are used to convert Objective-C type encoding strings to
and from [`ctypes`][] types, and to manage
custom conversions in both directions.

All Objective-C encoding strings are represented as
[`bytes`][] rather than
[`str`][].

<:> ctype_for_encoding
<!-- TODO: function -->

<:> encoding_for_ctype
<!-- TODO: function -->

<:> register_preferred_encoding
<!-- TODO: function -->

<:> with_preferred_encoding
<!-- TODO: function -->

<:> register_encoding
<!-- TODO: function -->

<:> with_encoding
<!-- TODO: function -->

<:> unregister_encoding
<!-- TODO: function -->

<:> unregister_encoding_all
<!-- TODO: function -->

<:> unregister_ctype
<!-- TODO: function -->

<:> unregister_ctype_all
<!-- TODO: function -->

<:> get_ctype_for_encoding_map
<!-- TODO: function -->

<:> get_encoding_for_ctype_map
<!-- TODO: function -->

<:> split_method_encoding
<!-- TODO: function -->

<:> ctypes_for_method_encoding
<!-- TODO: function -->

### Default registered type encodings

The following table lists Objective-C's standard type encodings for
primitive types, and the corresponding registered ctypes. These mappings
can be considered stable, but nonetheless users should not hard code
these encodings unless necessary. Instead, the
`encoding_for_ctype`{.interpreted-text role="func"} function should be
used to encode types, because it is less error-prone and more readable
than typing encodings out by hand.

| `Ctype` | Type encoding | Notes |
|----|----|----|
| `None` (`void`) | `v` |  |
| `~ctypes.c_bool`{.interpreted-text role="class"} | `B` | This refers to the `bool` type from C99 and C++. It is not necessarily the same as the <span class="title-ref">BOOL</span> type, which may be either `~ctypes.c_byte`{.interpreted-text role="class"} or `~ctypes.c_bool`{.interpreted-text role="class"} depending on the system and architecture. |
| `~ctypes.c_byte`{.interpreted-text role="class"} | `c` |  |
| `~ctypes.c_ubyte`{.interpreted-text role="class"} | `C` |  |
| `~ctypes.c_short`{.interpreted-text role="class"} | `s` |  |
| [`c_c_ushort`][ctypes.c_c_ushort] | `S` |  |
| [`c_long`][ctypes.c_long] | `l` |  |
| [`c_ulong`][ctypes.c_ulong] | `L` |  |
| [`c_int`][ctypes.c_int] | `i` | On 32-bit systems, [`c_int`][ctypes.c_int] is an alias for [`c_long`][ctypes.c_long], and will be encoded as such. |
| [`c_uint`][ctypes.c_uint] | `I` | On 32-bit systems, [`c_uint`][ctypes.c_uint] is an alias for [`c_ulong`][ctypes.c_ulong], and will be encoded as such. |
| [`c_longlong`][ctypes.c_longlong] | `q` | On 64-bit systems, [`c_longlong`][ctypes.c_longlong] is an alias for [`c_long`][ctypes.c_long], and will be encoded as such. |
| `~ctypes.c_ulonglong`{.interpreted-text role="class"} | `Q` | On 64-bit systems, `~ctypes.c_ulonglong`{.interpreted-text role="class"} is an alias for [`c_ulong`][ctypes.c_ulong], and will be encoded as such. |
| [`c_float`][ctypes.c_float] | `f` |  |
| [`c_double`][ctypes.c_double] | `d` |  |
| `~ctypes.c_longdouble`{.interpreted-text role="class"} | `D` | On ARM, `~ctypes.c_longdouble`{.interpreted-text role="class"} is an alias for [`c_double`][ctypes.c_double], and will be encoded as such. |
| `~ctypes.c_char`{.interpreted-text role="class"} | `c` | Only when encoding. Decoding `c` produces `~ctypes.c_byte`{.interpreted-text role="class"}, to allow using `signed char` as a Boolean value. |
| `~ctypes.c_char_p`{.interpreted-text role="class"} | `*` |  |
| `POINTER(c_char)` | `*` | Only when encoding. Decoding `*` produces `~ctypes.c_char_p`{.interpreted-text role="class"} for easier use of C strings. |
| `POINTER(c_byte)` | `*` | Only when encoding. Decoding `*` produces `~ctypes.c_char_p`{.interpreted-text role="class"} for easier use of C strings. |
| `POINTER(c_ubyte)` | `*` | Only when encoding. Decoding `*` produces `~ctypes.c_char_p`{.interpreted-text role="class"} for easier use of C strings. |
| `~ctypes.c_wchar`{.interpreted-text role="class"} | `i` | Only when encoding. Decoding `i` produces [`c_int`][ctypes.c_int]. |
| `~ctypes.c_wchar_p`{.interpreted-text role="class"} | `^i` | Only when encoding. Decoding `^i` produces `POINTER(c_int)`. |
| `~ctypes.c_void_p`{.interpreted-text role="class"} | `^v` |  |
| `UnknownPointer`{.interpreted-text role="class"} | `^?` | This encoding stands for a pointer to a type that cannot be encoded, which in practice means a function pointer. |
| `UnknownPointer`{.interpreted-text role="class"} | `^{?}`, `^(?)` | Only when decoding. These encodings stand for pointers to a structure or union with unknown name and fields. |
| [`objc_id`][rubicon.objc.runtime.objc_id] | `@` | Class name suffixes in the encoding (e. g. `@"NSString"`) are ignored. |
| [`objc_block`][rubicon.objc.runtime.objc_block] | `@?` | Block signature suffixes in the encoding (e. g. `@?<v@?>`) are ignored. |
| `~rubicon.objc.runtime.SEL`{.interpreted-text role="class"} | `:` |  |
| `~rubicon.objc.runtime.Class`{.interpreted-text role="class"} | `#` |  |

<:> UnknownPointer
<!-- TODO: class -->

In addition, the following types defined by Rubicon are registered, but
their encodings may vary depending on the system and architecture:

<!-- TODO: style into list -->

- `ctypes.py_object`{.interpreted-text role="class"}
- `NSInteger`{.interpreted-text role="class"}
- [`NSUInteger`][rubicon.objc.types.NSUInteger]
- [`CGFloat`][rubicon.objc.types.CGFloat]
- [`NSPoint`][rubicon.objc.types.NSPoint]
- [`CGPoint`][rubicon.objc.types.CGPoint]
- [`NSSize`][rubicon.objc.types.NSSize]
- [`CGSize`][rubicon.objc.types.CGSize]
- `NSRect`{.interpreted-text role="class"}
- `CGRect`{.interpreted-text role="class"}
- `UIEdgeInsets`{.interpreted-text role="class"}
- `NSEdgeInsets`{.interpreted-text role="class"}
- `NSTimeInterval`{.interpreted-text role="class"}
- [`CFIndex`][rubicon.objc.types.CFIndex]
- `UniChar`{.interpreted-text role="class"}
- `unichar`{.interpreted-text role="class"}
- `CGGlyph`{.interpreted-text role="class"}
- `NSRange`{.interpreted-text role="class"}

## Conversion of Python sequences to C structures and arrays

This function is used to convert a Python sequence (such as a
`tuple`{.interpreted-text role="class"} or [`list`][]) to a specific C structure or array type. This function is
mainly used internally by Rubicon, to allow passing Python sequences as
method parameters where a C structure or array would normally be
required. Most users will not need to use this function directly.

<:> compound_value_for_sequence
<!-- TODO: function -->

## Python to [`ctypes`][] type mapping

These functions are used to map Python types to equivalent
[`ctypes`][] types, and to add or remove such
mappings. This mechanism is mainly used internally by Rubicon, to for
example allow `~rubicon.objc.api.ObjCInstance`{.interpreted-text
role="class"} to be used instead of
[`objc_id`][rubicon.objc.runtime.objc_id] in
method type annotations. Most users will not need to use these functions
directly.

::: rubicon.objc.types.ctype_for_type
<!-- TODO: function -->

<:> register_ctype_for_type
<!-- TODO: function -->

<:> unregister_ctype_for_type
<!-- TODO: function -->

<:> get_ctype_for_type_map
<!-- TODO: function -->

### Default registered mappings

The following mappings are registered by default by Rubicon.

| Python type | <span class="title-ref">Ctype</span> |
|----|----|
| `int`{.interpreted-text role="class"} | [`c_int`][ctypes.c_int] |
| `float`{.interpreted-text role="class"} | [`c_float`][ctypes.c_float] |
| `bool`{.interpreted-text role="class"} | `~ctypes.c_bool`{.interpreted-text role="class"} |
| [`bytes`][] | `~ctypes.c_char_p`{.interpreted-text role="class"} |
| `~rubicon.objc.api.ObjCInstance`{.interpreted-text role="class"} | [`objc_id`][rubicon.objc.runtime.objc_id] |
| `~rubicon.objc.api.ObjCClass`{.interpreted-text role="class"} | `~rubicon.objc.runtime.Class`{.interpreted-text role="class"} |
