import faulthandler
import os

from rubicon.objc.runtime import load_library

try:
    import platform
    OSX_VERSION = tuple(int(v) for v in platform.mac_ver()[0].split('.')[:2])
except Exception:
    OSX_VERSION = None

try:
    rubiconharness = load_library('rubiconharness')
except ValueError:
    try:
        DYLD_LIBRARY_PATH = os.environ['DYLD_LIBRARY_PATH']
        raise ValueError(
            "Couldn't load Rubicon test harness library (DYLD_LIBRARY_PATH={DYLD_LIBRARY_PATH!r})".format(
                DYLD_LIBRARY_PATH=DYLD_LIBRARY_PATH
            )
        )
    except KeyError:
        raise ValueError(
            "Couldn't load Rubicon test harness library. Have you set DYLD_LIBRARY_PATH?)"
        )

faulthandler.enable()
