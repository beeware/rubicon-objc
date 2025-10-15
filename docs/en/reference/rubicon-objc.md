# `rubicon.objc`{.interpreted-text role="mod"} --- The main Rubicon module { #rubicon.objc-----the-main-rubicon-module }

{.module}
rubicon.objc

This is the main namespace of Rubicon-ObjC. Rubicon is structured into
multiple submodules of `rubicon.objc`{.interpreted-text role="mod"}, and
the most commonly used attributes from these submodules are exported via
the `rubicon.objc`{.interpreted-text role="mod"} module. This means that
most users only need to import and use the main
`rubicon.objc`{.interpreted-text role="mod"} module; the individual
submodules only need to be used for attributes that are not also
available on `rubicon.objc`{.interpreted-text role="mod"}.

## Exported Attributes

This is a full list of all attributes exported on the
`rubicon.objc`{.interpreted-text role="mod"} module. For detailed
documentation on these attributes, click the links below to visit the
relevant sections of the submodules' documentation.

### From `rubicon.objc.api`{.interpreted-text role="mod"} { #from-rubicon.objc.api }

<!-- TODO: style into list -->

- `~rubicon.objc.api.Block`{.interpreted-text role="class"}
- `~rubicon.objc.api.NSArray`{.interpreted-text role="data"}
- `~rubicon.objc.api.NSDictionary`{.interpreted-text role="data"}
- `~rubicon.objc.api.NSMutableArray`{.interpreted-text role="data"}
- `~rubicon.objc.api.NSMutableDictionary`{.interpreted-text role="data"}
- `~rubicon.objc.api.NSObject`{.interpreted-text role="data"}
- `~rubicon.objc.api.NSObjectProtocol`{.interpreted-text role="data"}
- `~rubicon.objc.api.ObjCBlock`{.interpreted-text role="class"}
- `~rubicon.objc.api.ObjCClass`{.interpreted-text role="class"}
- `~rubicon.objc.api.ObjCInstance`{.interpreted-text role="class"}
- `~rubicon.objc.api.ObjCMetaClass`{.interpreted-text role="class"}
- `~rubicon.objc.api.ObjCProtocol`{.interpreted-text role="class"}
- `~rubicon.objc.api.at`{.interpreted-text role="func"}
- `~rubicon.objc.api.ns_from_py`{.interpreted-text role="func"}
- `~rubicon.objc.api.objc_classmethod`{.interpreted-text role="func"}
- `~rubicon.objc.api.objc_const`{.interpreted-text role="func"}
- `~rubicon.objc.api.objc_ivar`{.interpreted-text role="func"}
- `~rubicon.objc.api.objc_method`{.interpreted-text role="func"}
- `~rubicon.objc.api.objc_property`{.interpreted-text role="func"}
- `~rubicon.objc.api.objc_rawmethod`{.interpreted-text role="func"}
- `~rubicon.objc.api.py_from_ns`{.interpreted-text role="func"}


### From `rubicon.objc.runtime`{.interpreted-text role="mod"} { #from-rubicon.objc.runtime }

<!-- TODO: style into list -->

- `~rubicon.objc.runtime.SEL`{.interpreted-text role="class"}
- `~rubicon.objc.runtime.send_message`{.interpreted-text role="func"}
- `~rubicon.objc.runtime.send_super`{.interpreted-text role="func"}


### From `rubicon.objc.types`{.interpreted-text role="mod"} { #from-rubicon.objc.types }

<!-- TODO: style into list -->

- `~rubicon.objc.types.CFIndex`{.interpreted-text role="class"}
- `~rubicon.objc.types.CFRange`{.interpreted-text role="class"}
- `~rubicon.objc.types.CGFloat`{.interpreted-text role="class"}
- `~rubicon.objc.types.CGGlyph`{.interpreted-text role="class"}
- `~rubicon.objc.types.CGPoint`{.interpreted-text role="class"}
- `~rubicon.objc.types.CGPointMake`{.interpreted-text role="func"}
- `~rubicon.objc.types.CGRect`{.interpreted-text role="class"}
- `~rubicon.objc.types.CGRectMake`{.interpreted-text role="func"}
- `~rubicon.objc.types.CGSize`{.interpreted-text role="class"}
- `~rubicon.objc.types.CGSizeMake`{.interpreted-text role="func"}
- `~rubicon.objc.types.NSEdgeInsets`{.interpreted-text role="class"}
- `~rubicon.objc.types.NSEdgeInsetsMake`{.interpreted-text role="func"}
- `~rubicon.objc.types.NSInteger`{.interpreted-text role="class"}
- `~rubicon.objc.types.NSMakePoint`{.interpreted-text role="func"}
- `~rubicon.objc.types.NSMakeRect`{.interpreted-text role="func"}
- `~rubicon.objc.types.NSMakeSize`{.interpreted-text role="func"}
- `~rubicon.objc.types.NSPoint`{.interpreted-text role="class"}
- `~rubicon.objc.types.NSRange`{.interpreted-text role="class"}
- `~rubicon.objc.types.NSRect`{.interpreted-text role="class"}
- `~rubicon.objc.types.NSSize`{.interpreted-text role="class"}
- `~rubicon.objc.types.NSTimeInterval`{.interpreted-text role="class"}
- `~rubicon.objc.types.NSUInteger`{.interpreted-text role="class"}
- `~rubicon.objc.types.NSZeroPoint`{.interpreted-text role="data"}
- `~rubicon.objc.types.UIEdgeInsets`{.interpreted-text role="class"}
- `~rubicon.objc.types.UIEdgeInsetsMake`{.interpreted-text role="func"}
- `~rubicon.objc.types.UIEdgeInsetsZero`{.interpreted-text role="data"}
- `~rubicon.objc.types.UniChar`{.interpreted-text role="class"}
- `~rubicon.objc.types.unichar`{.interpreted-text role="class"}
