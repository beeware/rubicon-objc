class c_ptrdiff_t:
    """
    The [ptrdiff_t](https://en.cppreference.com/w/c/types/ptrdiff_t) type
    from `<stddef.h>`. Equivalent to [`c_long`][ctypes.c_long] on 64-bit systems
    and [`c_int`][ctypes.c_int] on 32-bit systems.
    """

    ...

class NSInteger:
    """
    The
    [NSInteger](https://developer.apple.com/documentation/objectivec/nsinteger?language=objc)
    type from `<objc/NSObjCRuntime.h>`. Equivalent to
    [`c_long`][ctypes.c_long] on 64-bit systems and
    [`c_int`][ctypes.c_int] on 32-bit systems.
    """

    ...

class NSUInteger:
    """
    The
    [NSUInteger](https://developer.apple.com/documentation/objectivec/nsuinteger?language=objc)
    type from `<objc/NSObjCRuntime.h>`. Equivalent to
    [`c_ulong`][ctypes.c_ulong] on 64-bit systems and
    [`c_uint`][ctypes.c_uint] on 32-bit systems.
    """

    ...

class CGFloat:
    """
    The
    [CGFloat](https://developer.apple.com/documentation/corefoundation/cgfloat?language=objc)
    type from `<CoreGraphics/CGBase.h>`. Equivalent to
    [`c_double`][ctypes.c_double] on 64-bit systems and
    [`c_float`][ctypes.c_float] on 32-bit systems.
    """

    ...

class NSPoint:
    """
    The
    [NSPoint](https://developer.apple.com/documentation/foundation/nspoint?language=objc)
    structure from `<Foundation/NSGeometry.h>`.

    /// note | Note

    On 64-bit systems this is an alias for [`CGPoint`][rubicon.objc.types.CGPoint].

    ///
    """
    @property
    def x(self):
        """
        The X coordinate as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...
    @property
    def y(self):
        """
        The Y coordinate as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...

class CGPoint:
    """
    The
    [CGPoint](https://developer.apple.com/documentation/corefoundation/cgpoint?language=objc)
    structure from `<CoreGraphics/CGGeometry.h>`.
    """
    @property
    def x(self):
        """
        The X coordinate as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...
    @property
    def y(self):
        """
        The Y coordinate as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...

class NSSize:
    """
    The
    [NSSize](https://developer.apple.com/documentation/foundation/nssize?language=objc)
    structure from `<Foundation/NSGeometry.h>`.

    /// note | Note

    On 64-bit systems this is an alias for `CGSize`{.interpreted-text
    role="class"}.

    ///
    """
    @property
    def width(self):
        """
        The width as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...
    @property
    def height(self):
        """
        The height as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...

class CGSize:
    """
    The
    [CGSize](https://developer.apple.com/documentation/corefoundation/cgsize?language=objc)
    structure from `<CoreGraphics/CGGeometry.h>`.
    """
    @property
    def width(self):
        """
        The width as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...
    @property
    def height(self):
        """
        The height as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...

class NSRect:
    """
    The
    [NSRect](https://developer.apple.com/documentation/foundation/nsrect?language=objc)
    structure from `<Foundation/NSGeometry.h>`.

    /// note | Note

    On 64-bit systems this is an alias for `CGRect`{.interpreted-text
    role="class"}.

    ///
    """
    @property
    def origin(self):
        """
        The origin as a [`NSPoint`][rubicon.objc.types.NSPoint].
        """
        ...
    @property
    def size(self):
        """
        The size as a [`NSSize`][rubicon.objc.types.NSSize].
        """
        ...

class CGRect:
    """
    The
    [CGRect](https://developer.apple.com/documentation/corefoundation/cgrect?language=objc)
    structure from `<CoreGraphics/CGGeometry.h>`.
    """
    @property
    def origin(self):
        """
        The origin as a [`CGPoint`][rubicon.objc.types.CGPoint].
        """
        ...
    @property
    def size(self):
        """
        The size as a [`CGSize`][rubicon.objc.types.CGSize].
        """
        ...

class UIEdgeInsets:
    """
    The
    [UIEdgeInsets](https://developer.apple.com/documentation/uikit/uiedgeinsets?language=objc)
    structure from `<UIKit/UIGeometry.h>`.
    """
    @property
    def top(self):
        """
        The top inset as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...
    @property
    def left(self):
        """
        The left inset as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...
    @property
    def bottom(self):
        """
        The bottom inset as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...
    @property
    def right(self):
        """
        The right inset as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """

class NSEdgeInsets:
    """
    The
    [NSEdgeInsets](https://developer.apple.com/documentation/foundation/nsedgeinsets?language=objc)
    structure from `<Foundation/NSGeometry.h>`.
    """
    @property
    def top(self):
        """
        The top inset as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...
    @property
    def left(self):
        """
        The left inset as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...
    @property
    def bottom(self):
        """
        The bottom inset as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...
    @property
    def right(self):
        """
        The right inset as a [`CGFloat`][rubicon.objc.types.CGFloat].
        """
        ...

class NSTimeInterval:
    """
    The
    [NSTimeInterval](https://developer.apple.com/documentation/foundation/nstimeinterval?language=objc)
    type from `<Foundation/NSDate.h>`. Equivalent to [`c_double`][ctypes.c_double].
    """

    ...

class CFIndex:
    """
    The
    [CFIndex](https://developer.apple.com/documentation/corefoundation/cfindex?language=objc)
    type from `<CoreFoundation/CFBase.h>`. Equivalent to
    [`c_longlong`][ctypes.c_longlong] on 64-bit systems
    and [`c_long`][ctypes.c_long] on 32-bit systems.
    """

    ...

class UniChar:
    """
    The `UniChar` type from `<MacTypes.h>`. Equivalent to
    [`c_ushort`][ctypes.c_ushort].
    """

    ...

class unichar:
    """
    The
    [unichar](https://developer.apple.com/documentation/foundation/unichar?language=objc)
    type from `<Foundation/NSString.h>`. Equivalent to
    [`c_ushort`][ctypes.c_ushort].
    """

    ...

class CGGlyph:
    """
    The
    [CGGlyph](https://developer.apple.com/documentation/coregraphics/cgglyph?language=objc)
    type from `<CoreGraphics/CGFont.h>`. Equivalent to
    [`c_ushort`][ctypes.c_ushort].
    """

    ...

class CFRange:
    """
    The
    [CFRange](https://developer.apple.com/documentation/corefoundation/cfrange?language=objc)
    type from `<CoreFoundation/CFBase.h>`.
    """
    @property
    def location(self):
        """
        The location as a [`CFIndex`][rubicon.objc.types.CFIndex].
        """
        ...
    @property
    def length(self):
        """
        The length as a [`CFIndex`][rubicon.objc.types.CFIndex].
        """
        ...

class NSRange:
    """
    The
    [NSRange](https://developer.apple.com/documentation/foundation/nsrange?language=objc)
    type from `<Foundation/NSRange.h>`.
    """
    def location(self):
        """
        The location as a [`NSUInteger`][rubicon.objc.types.NSUInteger].
        """
        ...
    def length(self):
        """
        The length as a [`NSUInteger`][rubicon.objc.types.NSUInteger].
        """
        ...
