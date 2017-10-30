from ctypes import (
    CFUNCTYPE, POINTER, byref, c_bool, c_buffer, c_byte, c_char_p, c_double,
    c_float, c_int, c_int8, c_int16, c_int32, c_int64, c_long, c_longlong,
    c_short, c_uint8, c_uint32, c_ulong, c_void_p, cast, cdll, util,
)
from decimal import Decimal
from enum import Enum

from .runtime import (
    SEL, Class, ObjCClass, ObjCInstance, get_class, libobjc, objc_id,
    send_message,
)
from .types import CFIndex, CFRange, CGFloat

__all__ = [
    'CFAbsoluteTime',
    'CFAllocatorRef',
    'CFArrayRef',
    'CFAttributedStringRef',
    'CFData',
    'CFDataRef',
    'CFDictionaryRef',
    'CFMutableArrayRef',
    'CFMutableDictionaryRef',
    'CFMutableSetRef',
    'CFNumberRef',
    'CFNumberType',
    'CFOptionFlags',
    'CFRunLoopRef',
    'CFSTR',
    'CFSetRef',
    'CFStringEncoding',
    'CFStringRef',
    'CFTimeInterval',
    'CFTypeID',
    'CFTypeRef',
    'NSDecimalNumber',
    'at',
    'from_value',
    'is_str',
    'kCFAllocatorDefault',
    'kCFNumberCFIndexType',
    'kCFNumberCGFloatType',
    'kCFNumberCharType',
    'kCFNumberDoubleType',
    'kCFNumberFloat32Type',
    'kCFNumberFloat64Type',
    'kCFNumberFloatType',
    'kCFNumberIntType',
    'kCFNumberLongLongType',
    'kCFNumberLongType',
    'kCFNumberMaxType',
    'kCFNumberNSIntegerType',
    'kCFNumberSInt16Type',
    'kCFNumberSInt32Type',
    'kCFNumberSInt64Type',
    'kCFNumberSInt8Type',
    'kCFNumberShortType',
    'kCFRunLoopDefaultMode',
    'kCFStringEncodingUTF8',
    'libcf',
    'to_bool',
    'to_list',
    'to_number',
    'to_set',
    'to_str',
    'to_value',
]


######################################################################

# CORE FOUNDATION

libcf = cdll.LoadLibrary(util.find_library('CoreFoundation'))

CFTypeID = c_ulong

# Core Foundation type refs. These are all treated as equivalent to objc_id.

CFTypeRef = objc_id

CFAllocatorRef = objc_id
kCFAllocatorDefault = None

CFArrayRef = objc_id
CFAttributedStringRef = objc_id
CFData = objc_id
CFDataRef = objc_id
CFDictionaryRef = objc_id
CFMutableArrayRef = objc_id
CFMutableDictionaryRef = objc_id
CFMutableSetRef = objc_id
CFNumberRef = objc_id
CFOptionFlags = c_ulong
CFRunLoopRef = objc_id
CFSetRef = objc_id
CFStringRef = objc_id

CFStringEncoding = c_uint32
kCFStringEncodingUTF8 = 0x08000100

CFTimeInterval = c_double
CFAbsoluteTime = CFTimeInterval

libcf.CFGetTypeID.restype = CFTypeID
libcf.CFGetTypeID.argtypes = [CFTypeRef]

libcf.CFRelease.restype = None
libcf.CFRelease.argtypes = [CFTypeRef]

libcf.CFStringCreateWithCString.restype = CFStringRef
libcf.CFStringCreateWithCString.argtypes = [CFAllocatorRef, c_char_p, CFStringEncoding]

libcf.CFStringGetLength.restype = CFIndex
libcf.CFStringGetLength.argtypes = [CFStringRef]

libcf.CFStringGetMaximumSizeForEncoding.restype = CFIndex
libcf.CFStringGetMaximumSizeForEncoding.argtypes = [CFIndex, CFStringEncoding]

libcf.CFStringGetCString.restype = c_bool
libcf.CFStringGetCString.argtypes = [CFStringRef, c_char_p, CFIndex, CFStringEncoding]

libcf.CFStringGetTypeID.restype = CFTypeID
libcf.CFStringGetTypeID.argtypes = []

libcf.CFAttributedStringCreate.restype = CFAttributedStringRef
libcf.CFAttributedStringCreate.argtypes = [CFAllocatorRef, CFStringRef, CFDictionaryRef]


# Core Foundation type to Python type conversion functions
def CFSTR(string):
    return ObjCInstance(libcf.CFStringCreateWithCString(
        None, string.encode('utf-8'), kCFStringEncodingUTF8,
    ))


# Other possible names for this method:
# ampersat, arobe, apenstaartje (little monkey tail), strudel,
# Klammeraffe (spider monkey), little_mouse, arroba, sobachka (doggie)
# malpa (monkey), snabel (trunk), papaki (small duck), afna (monkey),
# kukac (caterpillar).
def at(string):
    """Autoreleased version of CFSTR"""
    return ObjCInstance(send_message(CFSTR(string), 'autorelease'))


def to_str(cfstring):
    length = libcf.CFStringGetLength(cfstring)
    size = libcf.CFStringGetMaximumSizeForEncoding(length, kCFStringEncodingUTF8)
    buffer = c_buffer(size + 1)
    result = libcf.CFStringGetCString(cfstring, buffer, len(buffer), kCFStringEncodingUTF8)
    if result:
        return buffer.value.decode('utf-8')


def is_str(cfobject):
    return libcf.CFGetTypeID(cfobject) == libcf.CFStringGetTypeID()


libcf.CFDataCreate.restype = CFDataRef
libcf.CFDataCreate.argtypes = [CFAllocatorRef, POINTER(c_uint8), CFIndex]

libcf.CFDataGetBytes.restype = None
libcf.CFDataGetBytes.argtypes = [CFDataRef, CFRange, POINTER(c_uint8)]

libcf.CFDataGetLength.restype = CFIndex
libcf.CFDataGetLength.argtypes = [CFDataRef]

libcf.CFDictionaryGetValue.restype = c_void_p
libcf.CFDictionaryGetValue.argtypes = [CFDictionaryRef, c_void_p]

libcf.CFDictionaryCreateMutable.restype = c_void_p
libcf.CFDictionaryCreateMutable.argtypes = [CFAllocatorRef, CFIndex, c_void_p, c_void_p]

libcf.CFDictionaryAddValue.restype = None
libcf.CFDictionaryAddValue.argtypes = [CFMutableDictionaryRef, c_void_p, c_void_p]

# CFNumber.h
CFNumberType = c_uint32
kCFNumberSInt8Type = 1
kCFNumberSInt16Type = 2
kCFNumberSInt32Type = 3
kCFNumberSInt64Type = 4
kCFNumberFloat32Type = 5
kCFNumberFloat64Type = 6
kCFNumberCharType = 7
kCFNumberShortType = 8
kCFNumberIntType = 9
kCFNumberLongType = 10
kCFNumberLongLongType = 11
kCFNumberFloatType = 12
kCFNumberDoubleType = 13
kCFNumberCFIndexType = 14
kCFNumberNSIntegerType = 15
kCFNumberCGFloatType = 16
kCFNumberMaxType = 16

libcf.CFNumberCreate.restype = CFNumberRef
libcf.CFNumberCreate.argtypes = [CFAllocatorRef, CFNumberType, c_void_p]

libcf.CFNumberGetType.restype = CFNumberType
libcf.CFNumberGetType.argtypes = [CFNumberRef]

libcf.CFNumberGetValue.restype = c_bool
libcf.CFNumberGetValue.argtypes = [CFNumberRef, CFNumberType, c_void_p]

libcf.CFNumberGetTypeID.restype = CFTypeID
libcf.CFNumberGetTypeID.argtypes = []


def to_number(cfnumber):
    """Convert CFNumber to python int or float."""
    if type(cfnumber) == objc_id:
        cfnumber = ObjCInstance(cfnumber)

    numeric_type = libcf.CFNumberGetType(cfnumber)
    cfnum_to_ctype = {
        kCFNumberSInt8Type: c_int8,
        kCFNumberSInt16Type: c_int16,
        kCFNumberSInt32Type: c_int32,
        kCFNumberSInt64Type: c_int64,
        kCFNumberFloat32Type: c_float,
        kCFNumberFloat64Type: c_double,
        kCFNumberCharType: c_byte,
        kCFNumberShortType: c_short,
        kCFNumberIntType: c_int,
        kCFNumberLongType: c_long,
        kCFNumberLongLongType: c_longlong,
        kCFNumberFloatType: c_float,
        kCFNumberDoubleType: c_double,
        kCFNumberCFIndexType: CFIndex,
        kCFNumberCGFloatType: CGFloat
    }

    # NSDecimalNumber reports as a double. So does an NSNumber of type double.
    # In the case of NSDecimalNumber, convert to a Python decimal.
    if numeric_type == kCFNumberDoubleType and cfnumber.objc_class.name == 'NSDecimalNumber':
        return Decimal(cfnumber.stringValue)

    # Otherwise, just do the conversion.
    try:
        t = cfnum_to_ctype[numeric_type]
        result = t()
        if libcf.CFNumberGetValue(cfnumber, numeric_type, byref(result)):
            return result.value
    except KeyError:
        raise Exception('to_number: unhandled CFNumber type %d' % numeric_type)


def to_bool(cfbool):
    """Convert CFBoolean to python bool."""
    if type(cfbool) == objc_id:
        cfbool = ObjCInstance(cfbool)

    return bool(libcf.CFBooleanGetValue(cfbool))


# We need to be able to create raw NSDecimalNumber objects; if we use an
# normal ObjCClass() wrapper, the return values of constructors will be
# auto-converted back into Python Decimals. However, we want to cache
# class/selector/method lookups so that we don't have the overhead
# every time we use a decimal.
class NSDecimalNumber(object):
    objc_class = None

    @classmethod
    def from_decimal(cls, value):
        if cls.objc_class is None:
            cls.objc_class = get_class('NSDecimalNumber')
            cls.selector = SEL('decimalNumberWithString:')
            method = libobjc.class_getClassMethod(cls.objc_class, cls.selector)
            impl = libobjc.method_getImplementation(method)
            cls.constructor = cast(impl, CFUNCTYPE(objc_id, objc_id, SEL, objc_id))

        return ObjCInstance(cls.constructor(cast(cls.objc_class, objc_id), cls.selector, at(value.to_eng_string())))


NSArray = ObjCClass('NSArray')
NSMutableArray = ObjCClass('NSMutableArray')

NSDictionary = ObjCClass('NSDictionary')
NSMutableDictionary = ObjCClass('NSMutableDictionary')

NSNumber = ObjCClass('NSNumber')


def from_value(value):
    """Convert a Python type into an equivalent CFType type.
    """
    if isinstance(value, Enum):
        value = value.value

    if isinstance(value, str):
        return at(value)
    elif isinstance(value, bytes):
        return at(value.decode('utf-8'))
    elif isinstance(value, Decimal):
        return NSDecimalNumber.from_decimal(value)
    elif isinstance(value, dict):
        dikt = NSMutableDictionary.alloc().init()
        for k, v in value.items():
            dikt.setObject_forKey_(v, k)
        return dikt
    elif isinstance(value, list):
        array = NSMutableArray.alloc().init()
        for v in value:
            array.addObject(v)
        return array
    # Need to use raw message passing here to make sure Rubicon doesn't
    # convert the NSNumber back into Python objects.
    elif isinstance(value, bool):
        return cast(send_message(NSNumber, 'numberWithBool:', value), objc_id)
    elif isinstance(value, int):
        return cast(send_message(NSNumber, 'numberWithLong:', value), objc_id)
    elif isinstance(value, float):
        return cast(send_message(NSNumber, 'numberWithDouble:', value), objc_id)
    else:
        return value


# Dictionary of cftypes matched to the method converting them to python values.
known_cftypes = {
    libcf.CFStringGetTypeID(): to_str,
    libcf.CFNumberGetTypeID(): to_number,
    libcf.CFBooleanGetTypeID(): to_bool,
}


def to_value(cftype):
    """Convert a CFType into an equivalent python type.
    The convertible CFTypes are taken from the known_cftypes
    dictionary, which may be added to if another library implements
    its own conversion methods."""
    # Don't use simple boolean testing here since that can trigger a len()
    # check which will cause NS{,Mutable}{Array,Dict} to explode.
    if cftype is None:
        return None
    if isinstance(cftype, ObjCInstance):
        cftype = cftype._as_parameter_
    typeID = libcf.CFGetTypeID(cftype)
    try:
        convert_function = known_cftypes[typeID]
        ret = convert_function(cftype)
    except KeyError:
        ret = cftype

    if type(ret) == objc_id:
        return ObjCInstance(ret)
    elif type(ret) == Class:
        return ObjCClass(ret)
    else:
        return ret


libcf.CFSetGetCount.restype = CFIndex
libcf.CFSetGetCount.argtypes = [CFSetRef]

libcf.CFSetGetValues.restype = None
libcf.CFSetGetValues.argtypes = [CFSetRef, POINTER(c_void_p)]


def to_set(cfset):
    """Convert CFSet to python set."""
    count = libcf.CFSetGetCount(cfset)
    buffer = (c_void_p * count)()
    libcf.CFSetGetValues(cfset, buffer)
    return {to_value(cast(buffer[i], objc_id)) for i in range(count)}


libcf.CFArrayGetCount.restype = CFIndex
libcf.CFArrayGetCount.argtypes = [CFArrayRef]

libcf.CFArrayGetValueAtIndex.restype = c_void_p
libcf.CFArrayGetValueAtIndex.argtypes = [CFArrayRef, CFIndex]


def to_list(cfarray):
    """Convert CFArray to python list."""
    count = libcf.CFArrayGetCount(cfarray)
    return [
        to_value(cast(libcf.CFArrayGetValueAtIndex(cfarray, i), objc_id))
        for i in range(count)
    ]


kCFRunLoopDefaultMode = CFStringRef.in_dll(libcf, 'kCFRunLoopDefaultMode')

libcf.CFRunLoopGetCurrent.restype = CFRunLoopRef
libcf.CFRunLoopGetCurrent.argtypes = []

libcf.CFRunLoopGetMain.restype = CFRunLoopRef
libcf.CFRunLoopGetMain.argtypes = []
