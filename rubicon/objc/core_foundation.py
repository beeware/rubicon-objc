from ctypes import c_double, c_ulong

from .runtime import load_library, objc_id

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

libcf = load_library('CoreFoundation')

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
