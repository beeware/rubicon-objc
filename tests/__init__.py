import faulthandler
import os

from rubicon.objc.runtime import load_library

try:
    import platform

    OSX_VERSION = tuple(int(v) for v in platform.mac_ver()[0].split(".")[:2])
except Exception:
    OSX_VERSION = None

try:
    rubiconharness = load_library(
        os.path.abspath("tests/objc/build/librubiconharness.dylib")
    )
except ValueError:
    raise ValueError(
        "Couldn't load Rubicon test harness library. Did you remember to run make?"
    )

faulthandler.enable()
