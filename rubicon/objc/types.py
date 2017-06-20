from ctypes import *

import platform
import struct

__LP64__ = (8*struct.calcsize("P") == 64)

# platform.machine() indicates the machine's physical architecture,
# which means that on a 64-bit Intel machine it is always "x86_64",
# even if Python is built as 32-bit.
_any_x86 = (platform.machine() in ('i386', 'x86_64'))
__i386__ = (_any_x86 and not __LP64__)
__x86_64__ = (_any_x86 and __LP64__)

# On iOS, platform.machine() is a device identifier like "iPhone9,4",
# but the platform.version() string contains the architecture.
_any_arm = ('ARM' in platform.version())
__arm64__ = (_any_arm and __LP64__)
__arm__ = (_any_arm and not __LP64__)


_ctype_for_type_map = {
    int: c_int,
    float: c_double,
    bool: c_bool,
    bytes: c_char_p,
}

def ctype_for_type(tp):
    """Look up the ctypes type corresponding to the given type.
    This conversion is applied to types used in objc_method signatures, objc_ivar types, etc.
    This translates Python built-in types and rubicon.objc classes to their ctypes equivalents.
    Unregistered types (including things that are already ctypes types) are returned unchanged.
    """
    
    return _ctype_for_type_map.get(tp, tp)

def register_ctype_for_type(tp, ctype):
    """Register a conversion from a type to a ctypes type."""
    
    _ctype_for_type_map[tp] = ctype

def unregister_ctype_for_type(tp):
    """Unregister a conversion from a type to a ctypes type."""
    
    del _ctype_for_type_map[tp]

def get_ctype_for_type_map():
    """Get a copy of all currently registered type-to-ctype conversions as a mapping."""
    
    return dict(_ctype_for_type_map)

_ctype_for_encoding_map = {}
_encoding_for_ctype_map = {}

def ctype_for_encoding(encoding):
    """Return ctypes type for an encoded Objective-C type."""
    
    # Remove qualifiers, as documented in Table 6-2 here:
    # https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtTypeEncodings.html
    encoding = encoding.lstrip(b"NORVnor")
    
    try:
        # Look up simple type encodings directly
        return _ctype_for_encoding_map[encoding]
    except KeyError:
        if encoding[0:1] == b'^':
            try:
                # Try to resolve pointer types recursively
                target = ctype_for_encoding(encoding[1:])
            except ValueError:
                # For unknown pointer types, fall back to c_void_p (this is not ideal, but at least it works instead of erroring)
                return c_void_p
            else:
                return POINTER(target)
        else:
            raise ValueError('Unknown encoding: %s' % (encoding,))

def encoding_for_ctype(ctype):
    """Return the Objective-C type encoding for the given ctypes type."""
    
    try:
        return _encoding_for_ctype_map[ctype]
    except KeyError:
        raise ValueError('No type encoding known for ctype {}'.format(ctype))

def register_preferred_encoding(encoding, ctype):
    """Register a preferred conversion between an Objective-C type encoding and a ctypes type.
    This overwrites any existing conversions in each direction.
    """
    
    _ctype_for_encoding_map[encoding] = ctype
    _encoding_for_ctype_map[ctype] = encoding

def with_preferred_encoding(encoding):
    """Decorator for registering a preferred conversion between the given encoding and the decorated type.
    This is equivalent to calling register_preferred_encoding.
    """
    
    def _with_preferred_encoding_decorator(ctype):
        register_preferred_encoding(encoding, ctype)
        return ctype
    
    return _with_preferred_encoding_decorator

def register_encoding(encoding, ctype):
    """Register an additional conversion between an Objective-C type encoding and a ctypes type.
    If a conversion already exists in one or both directions, it is not overwritten.
    """
    
    _ctype_for_encoding_map.setdefault(encoding, ctype)
    _encoding_for_ctype_map.setdefault(ctype, encoding)

def with_encoding(encoding):
    """Decorator for registering a conversion between the given encoding and the decorated type.
    This is equivalent to calling register_encoding.
    """
    
    def _with_encoding_decorator(ctype):
        register_encoding(encoding, ctype)
        return ctype
    
    return _with_encoding_decorator

def unregister_encoding(encoding):
    """Unregister the conversion between an Objective-C type encoding and its corresponding ctypes type.
    
    Note that this does not remove any conversions in the other direction (from a ctype to this encoding). These conversions may be replaced with register_encoding, or unregistered with unregister_ctype. To remove all ctypes for an encoding, use unregister_encoding_all.
    If encoding was not registered previously, nothing happens.
    """
    
    _ctype_for_encoding_map.pop(encoding, default=None)
    

def unregister_encoding_all(encoding):
    """Unregister all conversions between an Objective-C type encoding and all corresponding ctypes types.
    All conversions from any ctype to this encoding are removed recursively using unregister_ctype_all.
    If encoding was not registered previously, nothing happens.
    """
    
    _ctype_for_encoding_map.pop(encoding, default=None)
    for ct, enc in list(_encoding_for_ctype_map.items()):
        if enc == encoding:
            unregister_ctype_all(ct)

def unregister_ctype(ctype):
    """Unregister the conversion from a ctypes type to an Objective-C type encoding.
    Note that this does not remove any conversions in the other direction (from an encoding to this ctype). These conversions may be replaced with register_encoding, or unregistered with unregister_encoding. To remove all encodings for a ctype, use unregister_ctype_all.
    If ctype was not registered previously, nothing happens.
    """
    
    _encoding_for_ctype_map.pop(ctype, default=None)

def unregister_ctype_all(ctype):
    """Unregister all conversions between a ctypes type and all corresponding Objective-C type encodings.
    All conversions from any type encoding to this ctype are removed recursively using unregister_encoding_all.
    If ctype was not registered previously, nothing happens.
    """
    
    _encoding_for_ctype_map.pop(ctype, default=None)
    for enc, ct in list(_ctype_for_encoding_map.items()):
        if ct == ctype:
            unregister_encoding_all(enc)

def get_ctype_for_encoding_map():
    """Get a copy of all currently registered encoding-to-ctype conversions as a map."""
    
    return dict(_ctype_for_encoding_map)

def get_encoding_for_ctype_map():
    """Get a copy of all currently registered ctype-to-encoding conversions as a map."""
    
    return dict(_encoding_for_ctype_map)

# Register all type encoding mappings.

register_preferred_encoding(b'v', None)
register_preferred_encoding(b'B', c_bool)

# Note, we prefer to map b'c' to c_byte rather than c_char, because otherwise
# ctypes converts the value into a one-character string which is generally
# not what we want at all, especially when the b'c' represents a BOOL var.
register_preferred_encoding(b'c', c_byte)
register_preferred_encoding(b'C', c_ubyte)
register_encoding(b'c', c_char)

register_preferred_encoding(b's', c_short)
register_preferred_encoding(b'S', c_ushort)
register_preferred_encoding(b'l', c_long)
register_preferred_encoding(b'L', c_ulong)

# Do not register c_int or c_longlong as preferred.
# If c_int or c_longlong is the same size as c_long, ctypes makes it an alias for c_long.
# If we would register c_int and c_longlong as preferred, this could cause c_long to be encoded as b'i' or b'q', instead of b'l'.
# The same applies to the unsigned versions.
register_encoding(b'i', c_int)
register_encoding(b'I', c_uint)
register_encoding(b'q', c_longlong)
register_encoding(b'Q', c_ulonglong)

register_preferred_encoding(b'f', c_float)
register_preferred_encoding(b'd', c_double)
# As above, c_longdouble may be c_double, so do not make it preferred.
register_encoding(b'D', c_longdouble)

# c_char encodes the same as c_byte.
# ctypes converts c_char values to a one-character bytestring, which is usually not the desired behavior, especially since BOOL is c_byte on 32-bit, and truth tests work differently for bytestrings than for numbers.
# So we do not make this mapping preferred.
register_encoding(b'c', c_char)

# Strictly speaking, c_char_p is only appropriate for actual C strings (null-terminated pointers to char without explicit signedness).
# However, all char pointers encode to b'*', regardless of signedness, and they might point to non-null-terminated data.
# Despite this, we prefer to map b'*' to c_char_p, because its most common use is for C strings.
register_preferred_encoding(b'*', c_char_p)
# Register the other char pointers, so they are all correctly mapped to b'*'.
# The compiler never generates encodings b'^c' or b'^C'.
register_encoding(b'*', POINTER(c_char))
register_encoding(b'*', POINTER(c_byte))
register_encoding(b'*', POINTER(c_ubyte))

# c_wchar encodes the same as c_int, and c_wchar_p the same as POINTER(c_int). wchar_t is rarely used in Objective-C, so we do not make c_wchar or c_wchar_p preferred.
register_encoding(b'i', c_wchar)
register_encoding(b'^i', c_wchar_p)
# Register POINTER(c_int) as preferred so it takes precedence over c_wchar_p.
# (Other pointer types are resolved automatically by ctype_for_encoding and encoding_for_ctype.)
register_preferred_encoding(b'^i', POINTER(c_int))

register_preferred_encoding(b'^v', c_void_p)


# Note CGBase.h located at
# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/CoreGraphics.framework/Headers/CGBase.h
# defines CGFloat as double if __LP64__, otherwise it's a float.
if __LP64__:
    NSInteger = c_long
    NSUInteger = c_ulong
    CGFloat = c_double
    _NSPointEncoding = b'{CGPoint=dd}'
    _NSSizeEncoding = b'{CGSize=dd}'
    _NSRectEncoding = b'{CGRect={CGPoint=dd}{CGSize=dd}}'
    _NSRangeEncoding = b'{_NSRange=QQ}'
    _UIEdgeInsetsEncoding = b'{UIEdgeInsets=dddd}'
    _NSEdgeInsetsEncoding = b'{NSEdgeInsets=dddd}'
    _PyObjectEncoding = b'^{_object=q^{_typeobject}}'
else:
    NSInteger = c_int
    NSUInteger = c_uint
    CGFloat = c_float
    _NSPointEncoding = b'{CGPoint=ff}'
    _NSSizeEncoding = b'{CGSize=ff}'
    _NSRectEncoding = b'{CGRect={CGPoint=ff}{CGSize=ff}}'
    _NSRangeEncoding = b'{_NSRange=II}'
    _UIEdgeInsetsEncoding = b'{UIEdgeInsets=ffff}'
    _NSEdgeInsetsEncoding = b'{NSEdgeInsets=ffff}'
    _PyObjectEncoding = b'^{_object=i^{_typeobject}}'

register_preferred_encoding(_PyObjectEncoding, py_object)


@with_preferred_encoding(b'^?')
class UnknownPointer(c_void_p):
    """Placeholder for the b'^?' "unknown pointer" type. Not to be confused with a b'^v' void pointer.
    Usually a b'^?' is a function pointer, but because the encoding doesn't contain the function signature, you need to manually create a CFUNCTYPE with the proper types, and cast this pointer to it.
    """

# from /System/Library/Frameworks/Foundation.framework/Headers/NSGeometry.h
@with_preferred_encoding(_NSPointEncoding)
class NSPoint(Structure):
    _fields_ = [
        ("x", CGFloat),
        ("y", CGFloat)
    ]
CGPoint = NSPoint


@with_preferred_encoding(_NSSizeEncoding)
class NSSize(Structure):
    _fields_ = [
        ("width", CGFloat),
        ("height", CGFloat)
    ]
CGSize = NSSize


@with_preferred_encoding(_NSRectEncoding)
class NSRect(Structure):
    _fields_ = [
        ("origin", NSPoint),
        ("size", NSSize)
    ]
CGRect = NSRect


def NSMakeSize(w, h):
    return NSSize(w, h)

CGSizeMake = NSMakeSize


def NSMakeRect(x, y, w, h):
    return NSRect(NSPoint(x, y), NSSize(w, h))

CGRectMake = NSMakeRect


def NSMakePoint(x, y):
    return NSPoint(x, y)

CGPointMake = NSMakePoint


# iOS: /System/Library/Frameworks/UIKit.framework/Headers/UIGeometry.h
@with_preferred_encoding(_UIEdgeInsetsEncoding)
class UIEdgeInsets(Structure):
    _fields_ = [('top', CGFloat),
                ('left', CGFloat),
                ('bottom', CGFloat),
                ('right', CGFloat)]

def UIEdgeInsetsMake(top, left, bottom, right):
    return UIEdgeInsets(top, left, bottom, right)

UIEdgeInsetsZero = UIEdgeInsets(0, 0, 0, 0)


# macOS: /System/Library/Frameworks/AppKit.framework/Headers/NSLayoutConstraint.h
@with_preferred_encoding(_NSEdgeInsetsEncoding)
class NSEdgeInsets(Structure):
    _fields_ = [('top', CGFloat),
                ('left', CGFloat),
                ('bottom', CGFloat),
                ('right', CGFloat)]

def NSEdgeInsetsMake(top, left, bottom, right):
    return NSEdgeInsets(top, left, bottom, right)

# strangely, there is no NSEdgeInsetsZero, neither in public nor in private API.


# NSDate.h
NSTimeInterval = c_double

CFIndex = c_long
UniChar = c_ushort
unichar = c_ushort
CGGlyph = c_ushort


# CFRange struct defined in CFBase.h
# This replaces the CFRangeMake(LOC, LEN) macro.
class CFRange(Structure):
    _fields_ = [
        ("location", CFIndex),
        ("length", CFIndex)
    ]


# NSRange.h  (Note, not defined the same as CFRange)
@with_preferred_encoding(_NSRangeEncoding)
class NSRange(Structure):
    _fields_ = [
        ("location", NSUInteger),
        ("length", NSUInteger)
    ]

NSZeroPoint = NSPoint(0, 0)
if sizeof(c_void_p) == 4:
    NSIntegerMax = 0x7fffffff
elif sizeof(c_void_p) == 8:
    NSIntegerMax = 0x7fffffffffffffff
NSNotFound = NSIntegerMax