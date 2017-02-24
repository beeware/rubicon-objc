from enum import Enum

from ctypes import *
from ctypes import util
from decimal import Decimal

from .objc import ObjCClass, ObjCInstance, send_message, get_class, get_selector, objc, objc_id, SEL, Class
from .types import *

######################################################################

# CORE FOUNDATION

cf = cdll.LoadLibrary(util.find_library('CoreFoundation'))

CFTypeID = c_ulong

# Core Foundation type refs. These are all treated as equivalent to objc_id.

CFTypeRef = objc_id

CFAllocatorRef = objc_id
CFArrayRef = objc_id
CFAttributedStringRef = objc_id
CFDataRef = objc_id
CFDictionaryRef = objc_id
CFMutableArrayRef = objc_id
CFMutableDictionaryRef = objc_id
CFMutableSetRef = objc_id
CFNumberRef = objc_id
CFRunLoopRef = objc_id
CFSetRef = objc_id
CFStringRef = objc_id

CFStringEncoding = c_uint32
kCFStringEncodingUTF8 = 0x08000100

cf.CFGetTypeID.restype = CFTypeID
cf.CFGetTypeID.argtypes = [CFTypeRef]

cf.CFRelease.restype = None
cf.CFRelease.argtypes = [CFTypeRef]

cf.CFStringCreateWithCString.restype = CFStringRef
cf.CFStringCreateWithCString.argtypes = [CFAllocatorRef, c_char_p, CFStringEncoding]

cf.CFStringGetLength.restype = CFIndex
cf.CFStringGetLength.argtypes = [CFStringRef]

cf.CFStringGetMaximumSizeForEncoding.restype = CFIndex
cf.CFStringGetMaximumSizeForEncoding.argtypes = [CFIndex, CFStringEncoding]

cf.CFStringGetCString.restype = c_bool
cf.CFStringGetCString.argtypes = [CFStringRef, c_char_p, CFIndex, CFStringEncoding]

cf.CFStringGetTypeID.restype = CFTypeID
cf.CFStringGetTypeID.argtypes = []

cf.CFAttributedStringCreate.restype = CFAttributedStringRef
cf.CFAttributedStringCreate.argtypes = [CFAllocatorRef, CFStringRef, CFDictionaryRef]


# Core Foundation type to Python type conversion functions
def CFSTR(string):
    return ObjCInstance(cf.CFStringCreateWithCString(
            None, string.encode('utf-8'), kCFStringEncodingUTF8))


# Other possible names for this method:
# ampersat, arobe, apenstaartje (little monkey tail), strudel,
# Klammeraffe (spider monkey), little_mouse, arroba, sobachka (doggie)
# malpa (monkey), snabel (trunk), papaki (small duck), afna (monkey),
# kukac (caterpillar).
def at(string):
    """Autoreleased version of CFSTR"""
    return ObjCInstance(send_message(CFSTR(string), 'autorelease'))


def to_str(cfstring):
    length = cf.CFStringGetLength(cfstring)
    size = cf.CFStringGetMaximumSizeForEncoding(length, kCFStringEncodingUTF8)
    buffer = c_buffer(size + 1)
    result = cf.CFStringGetCString(cfstring, buffer, len(buffer), kCFStringEncodingUTF8)
    if result:
        return buffer.value.decode('utf-8')

def is_str(cfobject):
    return cf.CFGetTypeID(cfobject) == cf.CFStringGetTypeID()

cf.CFDataCreate.restype = CFDataRef
cf.CFDataCreate.argtypes = [CFAllocatorRef, POINTER(c_uint8), CFIndex]

cf.CFDataGetBytes.restype = None
cf.CFDataGetBytes.argtypes = [CFDataRef, CFRange, POINTER(c_uint8)]

cf.CFDataGetLength.restype = CFIndex
cf.CFDataGetLength.argtypes = [CFDataRef]

cf.CFDictionaryGetValue.restype = c_void_p
cf.CFDictionaryGetValue.argtypes = [CFDictionaryRef, c_void_p]

cf.CFDictionaryCreateMutable.restype = c_void_p
cf.CFDictionaryCreateMutable.argtypes = [CFAllocatorRef, CFIndex, c_void_p, c_void_p]

cf.CFDictionaryAddValue.restype = None
cf.CFDictionaryAddValue.argtypes = [CFMutableDictionaryRef, c_void_p, c_void_p]

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

cf.CFNumberCreate.restype = CFNumberRef
cf.CFNumberCreate.argtypes = [CFAllocatorRef, CFNumberType, c_void_p]

cf.CFNumberGetType.restype = CFNumberType
cf.CFNumberGetType.argtypes = [CFNumberRef]

cf.CFNumberGetValue.restype = c_bool
cf.CFNumberGetValue.argtypes = [CFNumberRef, CFNumberType, c_void_p]

cf.CFNumberGetTypeID.restype = CFTypeID
cf.CFNumberGetTypeID.argtypes = []


def to_number(cfnumber):
    """Convert CFNumber to python int or float."""
    if type(cfnumber) == objc_id:
        cfnumber = ObjCInstance(cfnumber)
    
    numeric_type = cf.CFNumberGetType(cfnumber)
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
        if cf.CFNumberGetValue(cfnumber, numeric_type, byref(result)):
            return result.value
    except KeyError:
        raise Exception('to_number: unhandled CFNumber type %d' % numeric_type)


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
            cls.selector = get_selector('decimalNumberWithString:')
            method = objc.class_getClassMethod(cls.objc_class, cls.selector)
            impl = objc.method_getImplementation(method)
            cls.constructor = cast(impl, CFUNCTYPE(objc_id, objc_id, SEL, objc_id))

        return ObjCInstance(cls.constructor(cast(cls.objc_class, objc_id), cls.selector, at(value.to_eng_string())))


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
    else:
        return value


# Dictionary of cftypes matched to the method converting them to python values.
known_cftypes = {
    cf.CFStringGetTypeID(): to_str,
    cf.CFNumberGetTypeID(): to_number
}


def to_value(cftype):
    """Convert a CFType into an equivalent python type.
    The convertible CFTypes are taken from the known_cftypes
    dictionary, which may be added to if another library implements
    its own conversion methods."""
    if not cftype:
        return None
    if isinstance(cftype, ObjCInstance):
        cftype = cftype._as_parameter_
    typeID = cf.CFGetTypeID(cftype)
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

cf.CFSetGetCount.restype = CFIndex
cf.CFSetGetCount.argtypes = [CFSetRef]

cf.CFSetGetValues.restype = None
cf.CFSetGetValues.argtypes = [CFSetRef, POINTER(c_void_p)]


def to_set(cfset):
    """Convert CFSet to python set."""
    count = cf.CFSetGetCount(cfset)
    buffer = (c_void_p * count)()
    cf.CFSetGetValues(cfset, buffer)
    return {to_value(cast(buffer[i], objc_id)) for i in range(count)}

cf.CFArrayGetCount.restype = CFIndex
cf.CFArrayGetCount.argtypes = [CFArrayRef]

cf.CFArrayGetValueAtIndex.restype = c_void_p
cf.CFArrayGetValueAtIndex.argtypes = [CFArrayRef, CFIndex]


def to_list(cfarray):
    """Convert CFArray to python list."""
    count = cf.CFArrayGetCount(cfarray)
    return [
        to_value(cast(cf.CFArrayGetValueAtIndex(cfarray, i), objc_id))
        for i in range(count)
    ]

kCFRunLoopDefaultMode = CFStringRef.in_dll(cf, 'kCFRunLoopDefaultMode')

cf.CFRunLoopGetCurrent.restype = CFRunLoopRef
cf.CFRunLoopGetCurrent.argtypes = []

cf.CFRunLoopGetMain.restype = CFRunLoopRef
cf.CFRunLoopGetMain.argtypes = []
