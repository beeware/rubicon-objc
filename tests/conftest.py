from __future__ import annotations

import faulthandler
import os
import platform
from ctypes import (
    Structure,
    c_char,
)

from rubicon.objc import (
    NSObject,
    ObjCClass,
    objc_property,
)
from rubicon.objc.runtime import load_library

appkit = load_library("AppKit")

NSArray = ObjCClass("NSArray")
NSImage = ObjCClass("NSImage")
NSString = ObjCClass("NSString")


try:
    OSX_VERSION = tuple(int(v) for v in platform.mac_ver()[0].split(".")[:2])
except Exception:
    OSX_VERSION = None

try:
    rubiconharness = load_library(
        os.path.abspath("tests/objc/build/librubiconharness.dylib")
    )
except ValueError as exc:
    raise ValueError(
        "Couldn't load Rubicon test harness library. Did you remember to run make?"
    ) from exc

faulthandler.enable()


class ObjcWeakref(NSObject):
    weak_property = objc_property(weak=True)


class struct_int_sized(Structure):
    _fields_ = [("x", c_char * 4)]


class struct_oddly_sized(Structure):
    _fields_ = [("x", c_char * 5)]


class struct_large(Structure):
    _fields_ = [("x", c_char * 17)]
