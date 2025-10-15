# `rubicon.objc.types`{.interpreted-text role="mod"} --- Non-Objective-C types and utilities { #rubicon.objc.types-----non-objective-c-types-and-utilities }

rubicon.objc.types

This module contains definitions for common C constants and types, and
utilities for working with C types.

## Common C type definitions

These are commonly used C types from various frameworks.

::: c_ptrdiff_t([value])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The [ptrdiff_t](https://en.cppreference.com/w/c/types/ptrdiff_t) type
from `<stddef.h>`. Equivalent to `~ctypes.c_long`{.interpreted-text
role="class"} on 64-bit systems and `~ctypes.c_int`{.interpreted-text
role="class"} on 32-bit systems.

::: NSInteger([value])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSInteger](https://developer.apple.com/documentation/objectivec/nsinteger?language=objc)
type from `<objc/NSObjCRuntime.h>`. Equivalent to
`~ctypes.c_long`{.interpreted-text role="class"} on 64-bit systems and
`~ctypes.c_int`{.interpreted-text role="class"} on 32-bit systems.

::: NSUInteger([value])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSUInteger](https://developer.apple.com/documentation/objectivec/nsuinteger?language=objc)
type from `<objc/NSObjCRuntime.h>`. Equivalent to
`~ctypes.c_ulong`{.interpreted-text role="class"} on 64-bit systems and
`~ctypes.c_uint`{.interpreted-text role="class"} on 32-bit systems.

::: CGFloat([value])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[CGFloat](https://developer.apple.com/documentation/corefoundation/cgfloat?language=objc)
type from `<CoreGraphics/CGBase.h>`. Equivalent to
`~ctypes.c_double`{.interpreted-text role="class"} on 64-bit systems and
`~ctypes.c_float`{.interpreted-text role="class"} on 32-bit systems.

::: NSPoint([x, .y])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSPoint](https://developer.apple.com/documentation/foundation/nspoint?language=objc)
structure from `<Foundation/NSGeometry.h>`.

/// note | Note

On 64-bit systems this is an alias for `CGPoint`{.interpreted-text
role="class"}.

///

::: x y <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The X and Y coordinates as `CGFloat`{.interpreted-text role="class"}s.



::: CGPoint([x, .y])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[CGPoint](https://developer.apple.com/documentation/corefoundation/cgpoint?language=objc)
structure from `<CoreGraphics/CGGeometry.h>`.

::: x y <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The X and Y coordinates as `CGFloat`{.interpreted-text role="class"}s.



::: NSSize([width, .height])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSSize](https://developer.apple.com/documentation/foundation/nssize?language=objc)
structure from `<Foundation/NSGeometry.h>`.

/// note | Note

On 64-bit systems this is an alias for `CGSize`{.interpreted-text
role="class"}.

///

::: width height <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The width and height as `CGFloat`{.interpreted-text role="class"}s.



::: CGSize([width, .height])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[CGSize](https://developer.apple.com/documentation/corefoundation/cgsize?language=objc)
structure from `<CoreGraphics/CGGeometry.h>`.

::: width height <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The width and height as `CGFloat`{.interpreted-text role="class"}s.



::: NSRect([origin, .size])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSRect](https://developer.apple.com/documentation/foundation/nsrect?language=objc)
structure from `<Foundation/NSGeometry.h>`.

/// note | Note

On 64-bit systems this is an alias for `CGRect`{.interpreted-text
role="class"}.

///

::: origin <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The origin as a `NSPoint`{.interpreted-text role="class"}.


::: size <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The size as a `NSSize`{.interpreted-text role="class"}.



::: CGRect([origin, .size])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[CGRect](https://developer.apple.com/documentation/corefoundation/cgrect?language=objc)
structure from `<CoreGraphics/CGGeometry.h>`.

::: origin <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The origin as a `CGPoint`{.interpreted-text role="class"}.


::: size <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The size as a `CGSize`{.interpreted-text role="class"}.



::: UIEdgeInsets([top, .left, .bottom, .right])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[UIEdgeInsets](https://developer.apple.com/documentation/uikit/uiedgeinsets?language=objc)
structure from `<UIKit/UIGeometry.h>`.

::: top left bottom right <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The insets as `CGFloat`{.interpreted-text role="class"}s.



::: NSEdgeInsets([top, .left, .bottom, .right])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSEdgeInsets](https://developer.apple.com/documentation/foundation/nsedgeinsets?language=objc)
structure from `<Foundation/NSGeometry.h>`.

::: top left bottom right <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The insets as `CGFloat`{.interpreted-text role="class"}s.



::: NSTimeInterval([value])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSTimeInterval](https://developer.apple.com/documentation/foundation/nstimeinterval?language=objc)
type from `<Foundation/NSDate.h>`. Equivalent to
`~ctypes.c_double`{.interpreted-text role="class"}.

::: CFIndex([value])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[CFIndex](https://developer.apple.com/documentation/corefoundation/cfindex?language=objc)
type from `<CoreFoundation/CFBase.h>`. Equivalent to
`~ctypes.c_longlong`{.interpreted-text role="class"} on 64-bit systems
and `~ctypes.c_long`{.interpreted-text role="class"} on 32-bit systems.

::: UniChar([value])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The `UniChar` type from `<MacTypes.h>`. Equivalent to
`~ctypes.c_ushort`{.interpreted-text role="class"}.

::: unichar([value])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[unichar](https://developer.apple.com/documentation/foundation/unichar?language=objc)
type from `<Foundation/NSString.h>`. Equivalent to
`~ctypes.c_ushort`{.interpreted-text role="class"}.

::: CGGlyph([value])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[CGGlyph](https://developer.apple.com/documentation/coregraphics/cgglyph?language=objc)
type from `<CoreGraphics/CGFont.h>`. Equivalent to
`~ctypes.c_ushort`{.interpreted-text role="class"}.

::: CFRange([location, .length])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[CFRange](https://developer.apple.com/documentation/corefoundation/cfrange?language=objc)
type from `<CoreFoundation/CFBase.h>`.

::: location length <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The location and length as `CFIndex`{.interpreted-text role="class"}es.



::: NSRange([location, .length])  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSRange](https://developer.apple.com/documentation/foundation/nsrange?language=objc)
type from `<Foundation/NSRange.h>`.

::: location length <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The location and length as `NSUInteger`{.interpreted-text
role="class"}s.

## Common C constants

These are commonly used C constants from various frameworks.

::: UIEdgeInsetsZero <!-- TODO: data -->
<!-- TODO: Doc notes -->
The constant
[UIEdgeInsetsZero](https://developer.apple.com/documentation/uikit/uiedgeinsetszero?language=objc):
a `UIEdgeInsets`{.interpreted-text role="class"} instance with all
insets set to zero.

::: NSZeroPoint <!-- TODO: data -->
<!-- TODO: Doc notes -->
The constant
[NSZeroPoint](https://developer.apple.com/documentation/foundation/nszeropoint?language=objc):
a `NSPoint`{.interpreted-text role="class"} instance with the X and Y
coordinates set to zero.


::: NSIntegerMax <!-- TODO: data -->
<!-- TODO: Doc notes -->
The macro constant
[NSIntegerMax](https://developer.apple.com/documentation/objectivec/nsintegermax?language=objc)
from `<objc/NSObjCRuntime.h>`: the maximum value that a
`NSInteger`{.interpreted-text role="class"} can hold.


::: NSNotFound <!-- TODO: data -->
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

::: LP64 <!-- TODO: data -->
<!-- TODO: Doc notes -->
Indicates whether the current environment is 64-bit. If true, C `long`s
and pointers are 64 bits in size, otherwise 32 bits.


::: i386   x86_64   arm   arm64 <!-- TODO: data -->
<!-- TODO: Doc notes -->
Each of these constants is true if the current environment uses the
named architecture. At most one of these constants is true at once in a
single Python runtime. (If the current architecture cannot be
determined, all of these constants are false.)


## Objective-C type encoding conversion

These functions are used to convert Objective-C type encoding strings to
and from `ctypes`{.interpreted-text role="mod"} types, and to manage
custom conversions in both directions.

All Objective-C encoding strings are represented as
`bytes`{.interpreted-text role="class"} rather than
`str`{.interpreted-text role="class"}.

::: ctype_for_encoding <!-- TODO: function -->

::: encoding_for_ctype <!-- TODO: function -->

::: register_preferred_encoding <!-- TODO: function -->

::: with_preferred_encoding <!-- TODO: function -->

::: register_encoding <!-- TODO: function -->

::: with_encoding <!-- TODO: function -->

::: unregister_encoding <!-- TODO: function -->

::: unregister_encoding_all <!-- TODO: function -->

::: unregister_ctype <!-- TODO: function -->

::: unregister_ctype_all <!-- TODO: function -->

::: get_ctype_for_encoding_map <!-- TODO: function -->

::: get_encoding_for_ctype_map <!-- TODO: function -->

::: split_method_encoding <!-- TODO: function -->

::: ctypes_for_method_encoding <!-- TODO: function -->

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
| `~ctypes.c_ushort`{.interpreted-text role="class"} | `S` |  |
| `~ctypes.c_long`{.interpreted-text role="class"} | `l` |  |
| `~ctypes.c_ulong`{.interpreted-text role="class"} | `L` |  |
| `~ctypes.c_int`{.interpreted-text role="class"} | `i` | On 32-bit systems, `~ctypes.c_int`{.interpreted-text role="class"} is an alias for `~ctypes.c_long`{.interpreted-text role="class"}, and will be encoded as such. |
| `~ctypes.c_uint`{.interpreted-text role="class"} | `I` | On 32-bit systems, `~ctypes.c_uint`{.interpreted-text role="class"} is an alias for `~ctypes.c_ulong`{.interpreted-text role="class"}, and will be encoded as such. |
| `~ctypes.c_longlong`{.interpreted-text role="class"} | `q` | On 64-bit systems, `~ctypes.c_longlong`{.interpreted-text role="class"} is an alias for `~ctypes.c_long`{.interpreted-text role="class"}, and will be encoded as such. |
| `~ctypes.c_ulonglong`{.interpreted-text role="class"} | `Q` | On 64-bit systems, `~ctypes.c_ulonglong`{.interpreted-text role="class"} is an alias for `~ctypes.c_ulong`{.interpreted-text role="class"}, and will be encoded as such. |
| `~ctypes.c_float`{.interpreted-text role="class"} | `f` |  |
| `~ctypes.c_double`{.interpreted-text role="class"} | `d` |  |
| `~ctypes.c_longdouble`{.interpreted-text role="class"} | `D` | On ARM, `~ctypes.c_longdouble`{.interpreted-text role="class"} is an alias for `~ctypes.c_double`{.interpreted-text role="class"}, and will be encoded as such. |
| `~ctypes.c_char`{.interpreted-text role="class"} | `c` | Only when encoding. Decoding `c` produces `~ctypes.c_byte`{.interpreted-text role="class"}, to allow using `signed char` as a Boolean value. |
| `~ctypes.c_char_p`{.interpreted-text role="class"} | `*` |  |
| `POINTER(c_char)` | `*` | Only when encoding. Decoding `*` produces `~ctypes.c_char_p`{.interpreted-text role="class"} for easier use of C strings. |
| `POINTER(c_byte)` | `*` | Only when encoding. Decoding `*` produces `~ctypes.c_char_p`{.interpreted-text role="class"} for easier use of C strings. |
| `POINTER(c_ubyte)` | `*` | Only when encoding. Decoding `*` produces `~ctypes.c_char_p`{.interpreted-text role="class"} for easier use of C strings. |
| `~ctypes.c_wchar`{.interpreted-text role="class"} | `i` | Only when encoding. Decoding `i` produces `~ctypes.c_int`{.interpreted-text role="class"}. |
| `~ctypes.c_wchar_p`{.interpreted-text role="class"} | `^i` | Only when encoding. Decoding `^i` produces `POINTER(c_int)`. |
| `~ctypes.c_void_p`{.interpreted-text role="class"} | `^v` |  |
| `UnknownPointer`{.interpreted-text role="class"} | `^?` | This encoding stands for a pointer to a type that cannot be encoded, which in practice means a function pointer. |
| `UnknownPointer`{.interpreted-text role="class"} | `^{?}`, `^(?)` | Only when decoding. These encodings stand for pointers to a structure or union with unknown name and fields. |
| `~rubicon.objc.runtime.objc_id`{.interpreted-text role="class"} | `@` | Class name suffixes in the encoding (e. g. `@"NSString"`) are ignored. |
| `~rubicon.objc.runtime.objc_block`{.interpreted-text role="class"} | `@?` | Block signature suffixes in the encoding (e. g. `@?<v@?>`) are ignored. |
| `~rubicon.objc.runtime.SEL`{.interpreted-text role="class"} | `:` |  |
| `~rubicon.objc.runtime.Class`{.interpreted-text role="class"} | `#` |  |

::: UnknownPointer <!-- TODO: class -->

In addition, the following types defined by Rubicon are registered, but
their encodings may vary depending on the system and architecture:

<!-- TODO: style into list -->

- `ctypes.py_object`{.interpreted-text role="class"}
- `NSInteger`{.interpreted-text role="class"}
- `NSUInteger`{.interpreted-text role="class"}
- `CGFloat`{.interpreted-text role="class"}
- `NSPoint`{.interpreted-text role="class"}
- `CGPoint`{.interpreted-text role="class"}
- `NSSize`{.interpreted-text role="class"}
- `CGSize`{.interpreted-text role="class"}
- `NSRect`{.interpreted-text role="class"}
- `CGRect`{.interpreted-text role="class"}
- `UIEdgeInsets`{.interpreted-text role="class"}
- `NSEdgeInsets`{.interpreted-text role="class"}
- `NSTimeInterval`{.interpreted-text role="class"}
- `CFIndex`{.interpreted-text role="class"}
- `UniChar`{.interpreted-text role="class"}
- `unichar`{.interpreted-text role="class"}
- `CGGlyph`{.interpreted-text role="class"}
- `NSRange`{.interpreted-text role="class"}

## Conversion of Python sequences to C structures and arrays

This function is used to convert a Python sequence (such as a
`tuple`{.interpreted-text role="class"} or `list`{.interpreted-text
role="class"}) to a specific C structure or array type. This function is
mainly used internally by Rubicon, to allow passing Python sequences as
method parameters where a C structure or array would normally be
required. Most users will not need to use this function directly.

::: compound_value_for_sequence <!-- TODO: function -->

## Python to `ctypes`{.interpreted-text role="mod"} type mapping

These functions are used to map Python types to equivalent
`ctypes`{.interpreted-text role="mod"} types, and to add or remove such
mappings. This mechanism is mainly used internally by Rubicon, to for
example allow `~rubicon.objc.api.ObjCInstance`{.interpreted-text
role="class"} to be used instead of
`~rubicon.objc.runtime.objc_id`{.interpreted-text role="class"} in
method type annotations. Most users will not need to use these functions
directly.

::: ctype_for_type <!-- TODO: function -->

::: register_ctype_for_type <!-- TODO: function -->

::: unregister_ctype_for_type <!-- TODO: function -->

::: get_ctype_for_type_map <!-- TODO: function -->

### Default registered mappings

The following mappings are registered by default by Rubicon.

| Python type | <span class="title-ref">Ctype</span> |
|----|----|
| `int`{.interpreted-text role="class"} | `~ctypes.c_int`{.interpreted-text role="class"} |
| `float`{.interpreted-text role="class"} | `~ctypes.c_float`{.interpreted-text role="class"} |
| `bool`{.interpreted-text role="class"} | `~ctypes.c_bool`{.interpreted-text role="class"} |
| `bytes`{.interpreted-text role="class"} | `~ctypes.c_char_p`{.interpreted-text role="class"} |
| `~rubicon.objc.api.ObjCInstance`{.interpreted-text role="class"} | `~rubicon.objc.runtime.objc_id`{.interpreted-text role="class"} |
| `~rubicon.objc.api.ObjCClass`{.interpreted-text role="class"} | `~rubicon.objc.runtime.Class`{.interpreted-text role="class"} |
