# `rubicon.objc` - The main Rubicon module { #rubicon-objc-module }


This is the main namespace of Rubicon-ObjC. Rubicon is structured into
multiple submodules of [`rubicon.objc`][rubicon-objc-module], and
the most commonly used attributes from these submodules are exported via
the [`rubicon.objc`][rubicon-objc-module] module. This means that
most users only need to import and use the main
[`rubicon.objc`][rubicon-objc-module] module; the individual
submodules only need to be used for attributes that are not also
available on [`rubicon.objc`][rubicon-objc-module].

## Exported Attributes

This is a full list of all attributes exported on the
[`rubicon.objc`][rubicon-objc-module] module. For detailed
documentation on these attributes, click the links below to visit the
relevant sections of the submodules' documentation.

### From `rubicon.objc.api`

* [`Block`][rubicon.objc.api.Block]
* [`NSArray`][rubicon.objc.api.NSArray]
* [`NSDictionary`][rubicon.objc.api.NSDictionary]
* [`NSMutableArray`][rubicon.objc.api.NSMutableArray]
* [`NSMutableDictionary`][rubicon.objc.api.NSMutableDictionary]
* [`NSObject`][rubicon.objc.api.NSObject]
* [`NSObjectProtocol`][rubicon.objc.api.NSObjectProtocol]
* [`ObjCBlock`][rubicon.objc.api.ObjCBlock]
* [`ObjCClass`][rubicon.objc.api.ObjCClass]
* [`ObjCInstance`][rubicon.objc.api.ObjCInstance]
* [`ObjCMetaClass`][rubicon.objc.api.ObjCMetaClass]
* [`ObjCProtocol`][rubicon.objc.api.ObjCProtocol]
* [`at`][rubicon.objc.api.at]
* [`ns_from_py`][rubicon.objc.api.ns_from_py]
* [`objc_classmethod`][rubicon.objc.api.objc_classmethod]
* [`objc_const`][rubicon.objc.api.objc_const]
* [`objc_ivar`][rubicon.objc.api.objc_ivar]
* [`objc_method`][rubicon.objc.api.objc_method]
* [`objc_property`][rubicon.objc.api.objc_property]
* [`objc_rawmethod`][rubicon.objc.api.objc_rawmethod]
* [`py_from_ns`][rubicon.objc.api.py_from_ns]


### From `rubicon.objc.runtime`

* [`SEL`][rubicon.objc.runtime.SEL]
* [`send_message`][rubicon.objc.runtime.send_message]
* [`send_super`][rubicon.objc.runtime.send_super]


### From `rubicon.objc.types`

* [`CFIndex`][rubicon.objc.types.CFIndex]
* [`CFRange`][rubicon.objc.types.CFRange]
* [`CGFloat`][rubicon.objc.types.CGFloat]
* [`CGGlyph`][rubicon.objc.types.CGGlyph]
* [`CGPoint`][rubicon.objc.types.CGPoint]
* [`CGPointMake`][rubicon.objc.types.CGPointMake]
* [`CGRect`][rubicon.objc.types.CGRect]
* [`CGRectMake`][rubicon.objc.types.CGRectMake]
* [`CGSize`][rubicon.objc.types.CGSize]
* [`CGSizeMake`][rubicon.objc.types.CGSizeMake]
* [`NSEdgeInsets`][rubicon.objc.types.NSEdgeInsets]
* [`NSEdgeInsetsMake`][rubicon.objc.types.NSEdgeInsetsMake]
* [`NSInteger`][rubicon.objc.types.NSInteger]
* [`NSMakePoint`][rubicon.objc.types.NSMakePoint]
* [`NSMakeRect`][rubicon.objc.types.NSMakeRect]
* [`NSMakeSize`][rubicon.objc.types.NSMakeSize]
* [`NSPoint`][rubicon.objc.types.NSPoint]
* [`NSRange`][rubicon.objc.types.NSRange]
* [`NSRect`][rubicon.objc.types.NSRect]
* [`NSSize`][rubicon.objc.types.NSSize]
* [`NSTimeInterval`][rubicon.objc.types.NSTimeInterval]
* [`NSUInteger`][rubicon.objc.types.NSUInteger]
* [`NSZeroPoint`][rubicon.objc.types.NSZeroPoint]
* [`UIEdgeInsets`][rubicon.objc.types.UIEdgeInsets]
* [`UIEdgeInsetsMake`][rubicon.objc.types.UIEdgeInsetsMake]
* [`UIEdgeInsetsZero`][rubicon.objc.types.UIEdgeInsetsZero]
* [`UniChar`][rubicon.objc.types.UniChar]
* [`unichar`][rubicon.objc.types.unichar]
