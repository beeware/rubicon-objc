__version__ = '0.2.10'

# Import commonly used submodules right away.
# The first two imports are only included for clarity. They are not strictly necessary, because the from-imports below
# also import the types and runtime modules and implicitly add them to the rubicon.objc namespace.
from . import types  # noqa: F401
from . import runtime  # noqa: F401
# The import of collections is important, however. The classes from collections are not meant to be used directly,
# instead they are registered with the runtime module (using the for_objcclass decorator) so they are used in place of
# ObjCInstance when representing Foundation collections in Python. If this module is not imported, the registration
# will not take place, and Foundation collections will not support the expected methods/operators in Python!
from . import collections  # noqa: F401

from .runtime import (  # noqa: F401
    IMP, SEL, Block, Class, Ivar, Method, NSArray, NSDictionary, NSMutableArray, NSMutableDictionary, NSObject,
    NSObjectProtocol, ObjCBlock, ObjCClass, ObjCInstance, ObjCMetaClass, ObjCProtocol, at, ns_from_py,
    objc_classmethod, objc_const, objc_id, objc_ivar, objc_method, objc_property, objc_property_t, objc_rawmethod,
    py_from_ns, send_message, send_super,
)
from .types import (  # noqa: F401
    CFIndex, CFRange, CGFloat, CGGlyph, CGPoint, CGPointMake, CGRect,
    CGRectMake, CGSize, CGSizeMake, NSEdgeInsets, NSEdgeInsetsMake, NSInteger,
    NSMakePoint, NSMakeRect, NSMakeSize, NSPoint, NSRange, NSRect, NSSize,
    NSTimeInterval, NSUInteger, NSZeroPoint, UIEdgeInsets, UIEdgeInsetsMake,
    UIEdgeInsetsZero, UniChar, unichar,
)
