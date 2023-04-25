===============================================
:mod:`rubicon.objc` --- The main Rubicon module
===============================================

.. module:: rubicon.objc

This is the main namespace of Rubicon-ObjC. Rubicon is structured into multiple
submodules of :mod:`rubicon.objc`, and the most commonly used attributes from
these submodules are exported via the :mod:`rubicon.objc` module. This means
that most users only need to import and use the main :mod:`rubicon.objc`
module; the individual submodules only need to be used for attributes that are
not also available on :mod:`rubicon.objc`.

Exported Attributes
-------------------

This is a full list of all attributes exported on the :mod:`rubicon.objc`
module. For detailed documentation on these attributes, click the links below
to visit the relevant sections of the submodules' documentation.

From :mod:`rubicon.objc.api`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. hlist::

    * :class:`~rubicon.objc.api.Block`
    * :data:`~rubicon.objc.api.NSArray`
    * :data:`~rubicon.objc.api.NSDictionary`
    * :data:`~rubicon.objc.api.NSMutableArray`
    * :data:`~rubicon.objc.api.NSMutableDictionary`
    * :data:`~rubicon.objc.api.NSObject`
    * :data:`~rubicon.objc.api.NSObjectProtocol`
    * :class:`~rubicon.objc.api.ObjCBlock`
    * :class:`~rubicon.objc.api.ObjCClass`
    * :class:`~rubicon.objc.api.ObjCInstance`
    * :class:`~rubicon.objc.api.ObjCMetaClass`
    * :class:`~rubicon.objc.api.ObjCProtocol`
    * :func:`~rubicon.objc.api.at`
    * :func:`~rubicon.objc.api.ns_from_py`
    * :func:`~rubicon.objc.api.objc_classmethod`
    * :func:`~rubicon.objc.api.objc_const`
    * :func:`~rubicon.objc.api.objc_ivar`
    * :func:`~rubicon.objc.api.objc_method`
    * :func:`~rubicon.objc.api.objc_property`
    * :func:`~rubicon.objc.api.objc_rawmethod`
    * :func:`~rubicon.objc.api.py_from_ns`

From :mod:`rubicon.objc.runtime`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. hlist::

    * :class:`~rubicon.objc.runtime.SEL`
    * :func:`~rubicon.objc.runtime.send_message`
    * :func:`~rubicon.objc.runtime.send_super`

From :mod:`rubicon.objc.types`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. hlist::

    * :class:`~rubicon.objc.types.CFIndex`
    * :class:`~rubicon.objc.types.CFRange`
    * :class:`~rubicon.objc.types.CGFloat`
    * :class:`~rubicon.objc.types.CGGlyph`
    * :class:`~rubicon.objc.types.CGPoint`
    * :func:`~rubicon.objc.types.CGPointMake`
    * :class:`~rubicon.objc.types.CGRect`
    * :func:`~rubicon.objc.types.CGRectMake`
    * :class:`~rubicon.objc.types.CGSize`
    * :func:`~rubicon.objc.types.CGSizeMake`
    * :class:`~rubicon.objc.types.NSEdgeInsets`
    * :func:`~rubicon.objc.types.NSEdgeInsetsMake`
    * :class:`~rubicon.objc.types.NSInteger`
    * :func:`~rubicon.objc.types.NSMakePoint`
    * :func:`~rubicon.objc.types.NSMakeRect`
    * :func:`~rubicon.objc.types.NSMakeSize`
    * :class:`~rubicon.objc.types.NSPoint`
    * :class:`~rubicon.objc.types.NSRange`
    * :class:`~rubicon.objc.types.NSRect`
    * :class:`~rubicon.objc.types.NSSize`
    * :class:`~rubicon.objc.types.NSTimeInterval`
    * :class:`~rubicon.objc.types.NSUInteger`
    * :data:`~rubicon.objc.types.NSZeroPoint`
    * :class:`~rubicon.objc.types.UIEdgeInsets`
    * :func:`~rubicon.objc.types.UIEdgeInsetsMake`
    * :data:`~rubicon.objc.types.UIEdgeInsetsZero`
    * :class:`~rubicon.objc.types.UniChar`
    * :class:`~rubicon.objc.types.unichar`
