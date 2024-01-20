try:
    # Read version from SCM metadata
    # This will only exist in a development environment
    from setuptools_scm import get_version

    # Excluded from coverage because a pure test environment (such as the one
    # used by tox in CI) won't have setuptools_scm
    __version__ = get_version("../../..", relative_to=__file__)  # pragma: no cover
except (ModuleNotFoundError, LookupError):
    # If setuptools_scm isn't in the environment, the call to import will fail.
    # If it *is* in the environment, but the code isn't a git checkout (e.g.,
    # it's been pip installed non-editable) the call to get_version() will fail.
    # If either of these occurs, read version from the installer metadata.

    # importlib.metadata.version was added in Python 3.8
    try:
        from importlib.metadata import version
    except ModuleNotFoundError:
        from importlib_metadata import version

    __version__ = version("rubicon-objc")

# `api`, `runtime` and `types` are only included for clarity. They are not
# strictly necessary, because the from-imports below also import the types and
# runtime modules and implicitly add them to the rubicon.objc namespace.
#
# The import of collections is important, however. The classes from collections
# are not meant to be used directly, instead they are registered with the
# runtime module (using the for_objcclass decorator) so they are used in place
# of ObjCInstance when representing Foundation collections in Python. If this
# module is not imported, the registration will not take place, and Foundation
# collections will not support the expected methods/operators in Python!
from . import api, collections, runtime, types
from .api import (
    Block,
    NSArray,
    NSDictionary,
    NSMutableArray,
    NSMutableDictionary,
    NSObject,
    NSObjectProtocol,
    ObjCBlock,
    ObjCClass,
    ObjCInstance,
    ObjCMetaClass,
    ObjCProtocol,
    at,
    ns_from_py,
    objc_classmethod,
    objc_const,
    objc_ivar,
    objc_method,
    objc_property,
    objc_rawmethod,
    py_from_ns,
)
from .runtime import SEL, objc_block, objc_id, send_message, send_super
from .types import (
    CFIndex,
    CFRange,
    CGFloat,
    CGGlyph,
    CGPoint,
    CGPointMake,
    CGRect,
    CGRectMake,
    CGSize,
    CGSizeMake,
    NSEdgeInsets,
    NSEdgeInsetsMake,
    NSInteger,
    NSMakePoint,
    NSMakeRect,
    NSMakeSize,
    NSPoint,
    NSRange,
    NSRect,
    NSSize,
    NSTimeInterval,
    NSUInteger,
    NSZeroPoint,
    UIEdgeInsets,
    UIEdgeInsetsMake,
    UIEdgeInsetsZero,
    UniChar,
    unichar,
)

__all__ = [
    "__version__",
    "CFIndex",
    "CFRange",
    "CGFloat",
    "CGGlyph",
    "CGPoint",
    "CGPointMake",
    "CGRect",
    "CGRectMake",
    "CGSize",
    "CGSizeMake",
    "NSEdgeInsets",
    "NSEdgeInsetsMake",
    "NSInteger",
    "NSMakePoint",
    "NSMakeRect",
    "NSMakeSize",
    "NSPoint",
    "NSRange",
    "NSRect",
    "NSSize",
    "NSTimeInterval",
    "NSUInteger",
    "NSZeroPoint",
    "UIEdgeInsets",
    "UIEdgeInsetsMake",
    "UIEdgeInsetsZero",
    "UniChar",
    "unichar",
    "SEL",
    "send_message",
    "send_super",
    "Block",
    "NSArray",
    "NSDictionary",
    "NSMutableArray",
    "NSMutableDictionary",
    "NSObject",
    "NSObjectProtocol",
    "ObjCBlock",
    "ObjCClass",
    "ObjCInstance",
    "ObjCMetaClass",
    "ObjCProtocol",
    "at",
    "ns_from_py",
    "objc_block",
    "objc_classmethod",
    "objc_const",
    "objc_id",
    "objc_ivar",
    "objc_method",
    "objc_property",
    "objc_rawmethod",
    "py_from_ns",
    "api",
    "collections",
    "runtime",
    "types",
]
