from ctypes import *

import platform
import struct

__LP64__ = (8*struct.calcsize("P") == 64)
__i386__ = (platform.machine() == 'i386')
__x86_64__ = (platform.machine() == 'x86_64')

# On iOS, platform.machine() is a device identifier like "iPhone9,4",
# but the platform.version() string contains the architecture. 
__arm__ = ('ARM32' in platform.version())
__arm64__ = ('ARM64' in platform.version())

PyObjectEncoding = b'{PyObject=@}'


def encoding_for_ctype(vartype):
    typecodes = {
        c_char: b'c', c_int: b'i', c_short: b's', c_long: b'l', c_longlong: b'q',
        c_ubyte: b'C', c_uint: b'I', c_ushort: b'S', c_ulong: b'L', c_ulonglong: b'Q',
        c_float: b'f', c_double: b'd', c_bool: b'B', c_char_p: b'*', c_void_p: b'@',
        py_object: PyObjectEncoding
    }
    return typecodes.get(vartype, b'?')

try:
    text = unicode
except NameError:
    text = str


# Note CGBase.h located at
# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/CoreGraphics.framework/Headers/CGBase.h
# defines CGFloat as double if __LP64__, otherwise it's a float.
if __LP64__:
    NSInteger = c_long
    NSUInteger = c_ulong
    CGFloat = c_double
    NSPointEncoding = b'{CGPoint=dd}'
    NSSizeEncoding = b'{CGSize=dd}'
    NSRectEncoding = b'{CGRect={CGPoint=dd}{CGSize=dd}}'
    NSRangeEncoding = b'{_NSRange=QQ}'
    UIEdgeInsetsEncoding = b'{UIEdgeInsets=dddd}'
    NSEdgeInsetsEncoding = b'{NSEdgeInsets=dddd}'
else:
    NSInteger = c_int
    NSUInteger = c_uint
    CGFloat = c_float
    NSPointEncoding = b'{CGPoint=ff}'
    NSSizeEncoding = b'{CGSize=ff}'
    NSRectEncoding = b'{CGRect={CGPoint=ff}{CGSize=ff}}'
    NSRangeEncoding = b'{NSRange=II}'
    UIEdgeInsetsEncoding = b'{UIEdgeInsets=ffff}'
    NSEdgeInsetsEncoding = b'{NSEdgeInsets=ffff}'

NSIntegerEncoding = encoding_for_ctype(NSInteger)
NSUIntegerEncoding = encoding_for_ctype(NSUInteger)
CGFloatEncoding = encoding_for_ctype(CGFloat)

# Special case so that NSImage.initWithCGImage_size_() will work.
CGImageEncoding = b'{CGImage=}'

NSZoneEncoding = b'{_NSZone=}'


# from /System/Library/Frameworks/Foundation.framework/Headers/NSGeometry.h
class NSPoint(Structure):
    _fields_ = [
        ("x", CGFloat),
        ("y", CGFloat)
    ]
CGPoint = NSPoint


class NSSize(Structure):
    _fields_ = [
        ("width", CGFloat),
        ("height", CGFloat)
    ]
CGSize = NSSize


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
class UIEdgeInsets(Structure):
    _fields_ = [('top', CGFloat),
                ('left', CGFloat),
                ('bottom', CGFloat),
                ('right', CGFloat)]

def UIEdgeInsetsMake(top, left, bottom, right):
    return UIEdgeInsets(top, left, bottom, right)

UIEdgeInsetsZero = UIEdgeInsets(0, 0, 0, 0)


# macOS: /System/Library/Frameworks/AppKit.framework/Headers/NSLayoutConstraint.h
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
unichar = c_wchar  # (actually defined as c_ushort in NSString.h, but need ctypes to convert properly)
CGGlyph = c_ushort


# CFRange struct defined in CFBase.h
# This replaces the CFRangeMake(LOC, LEN) macro.
class CFRange(Structure):
    _fields_ = [
        ("location", CFIndex),
        ("length", CFIndex)
    ]


# NSRange.h  (Note, not defined the same as CFRange)
class NSRange(Structure):
    _fields_ = [
        ("location", NSUInteger),
        ("length", NSUInteger)
    ]


NSZeroPoint = NSPoint(0, 0)

CFTypeID = c_ulong
CFNumberType = c_uint32
