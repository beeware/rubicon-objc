import faulthandler

from rubicon.objc.runtime import load_library

try:
    import platform
    OSX_VERSION = tuple(int(v) for v in platform.mac_ver()[0].split('.')[:2])
except Exception:
    OSX_VERSION = None

try:
    rubiconharness = load_library('rubiconharness')
except ValueError:
    raise ValueError("Couldn't load Rubicon test harness library. Have you set DYLD_LIBRARY_PATH?")

faulthandler.enable()
