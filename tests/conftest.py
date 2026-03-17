from __future__ import annotations

import faulthandler
import os
import platform
from ctypes import Structure, c_char

from rubicon.objc import ObjCClass
from rubicon.objc.runtime import load_library

##########################################################################
# Determine the macOS version
##########################################################################
try:
    OSX_VERSION = tuple(int(v) for v in platform.mac_ver()[0].split(".")[:2])
except Exception:
    OSX_VERSION = None

##########################################################################
# Load AppKit and define some useful classes
##########################################################################
appkit = load_library("AppKit")

NSArray = ObjCClass("NSArray")
NSImage = ObjCClass("NSImage")
NSString = ObjCClass("NSString")

##########################################################################
# Load the Rubicon test harness library
##########################################################################
try:
    rubiconharness = load_library(
        os.path.abspath("tests/objc/build/librubiconharness.dylib")
    )
except ValueError as exc:
    raise ValueError(
        "Couldn't load Rubicon test harness library. Did you remember to run make?"
    ) from exc

##########################################################################
# Enable faulthandler for clean handling of crashes
##########################################################################

faulthandler.enable()

##########################################################################
# Utility structures
##########################################################################


class struct_int_sized(Structure):
    _fields_ = [("x", c_char * 4)]


class struct_oddly_sized(Structure):
    _fields_ = [("x", c_char * 5)]


class struct_large(Structure):
    _fields_ = [("x", c_char * 17)]
