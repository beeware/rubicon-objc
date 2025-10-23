# `rubicon.objc.runtime` - Low-level Objective-C runtime access

This module contains types, functions, and C libraries used for
low-level access to the Objective-C runtime.

In most cases there is no need to use this module directly --- the
[`rubicon.objc.api`][rubicon-objc-api] module provides the
same functionality through a high-level interface.

## C libraries { #predefined-c-libraries }

Some commonly used C libraries are provided as
[`CDLL`][ctypes.CDLL]s. Other libraries can be
loaded using the [`load_library`][rubicon.objc.runtime.load_library] function.

::: rubicon.objc.runtime.load_library

::: rubicon.objc.runtime.libc

::: rubicon.objc.runtime.libobjc

::: rubicon.objc.runtime.Foundation

## Objective-C runtime types

These are various types used by the Objective-C runtime functions.

::: rubicon.objc.runtime.objc_id

::: rubicon.objc.runtime.objc_block

::: rubicon.objc.runtime.SEL

::: rubicon.objc.runtime.Class

::: rubicon.objc.runtime.IMP

::: rubicon.objc.runtime.Method

::: rubicon.objc.runtime.Ivar

::: rubicon.objc.runtime.objc_property_t

::: rubicon.objc.runtime.objc_property_attribute_t

::: rubicon.objc.runtime.objc_method_description

::: rubicon.objc.runtime.objc_super

## Objective-C runtime utility functions

These utility functions provide easier access from Python to certain
parts of the Objective-C runtime.

::: rubicon.objc.runtime.object_isClass

::: rubicon.objc.runtime.get_class

::: rubicon.objc.runtime.should_use_stret

::: rubicon.objc.runtime.should_use_fpret

::: rubicon.objc.runtime.send_message

::: rubicon.objc.runtime.send_super

::: rubicon.objc.runtime.add_method

::: rubicon.objc.runtime.add_ivar

::: rubicon.objc.runtime.get_ivar

::: rubicon.objc.runtime.set_ivar
