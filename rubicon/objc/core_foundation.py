from ctypes import c_double, c_ulong, cdll
from ctypes.util import find_library

from .runtime import objc_id

__all__ = [
    'CFAbsoluteTime',
    'CFAllocatorRef',
    'CFDataRef',
    'CFOptionFlags',
    'CFRunLoopRef',
    'CFStringRef',
    'CFTimeInterval',
    'kCFAllocatorDefault',
    'libcf',
]

libcf = cdll.LoadLibrary(find_library('CoreFoundation'))

CFAllocatorRef = objc_id
kCFAllocatorDefault = None

CFDataRef = objc_id
CFOptionFlags = c_ulong
CFRunLoopRef = objc_id
CFStringRef = objc_id

CFTimeInterval = c_double
CFAbsoluteTime = CFTimeInterval

libcf.CFRunLoopGetMain.restype = CFRunLoopRef
libcf.CFRunLoopGetMain.argtypes = []
