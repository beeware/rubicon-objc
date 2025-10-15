# `rubicon.objc.runtime`{.interpreted-text role="mod"} --- Low-level Objective-C runtime access { #rubicon.objc.runtime-----low-level-objective-c-runtime-access }

rubicon.objc.runtime

This module contains types, functions, and C libraries used for
low-level access to the Objective-C runtime.

In most cases there is no need to use this module directly --- the
`rubicon.objc.api`{.interpreted-text role="mod"} module provides the
same functionality through a high-level interface.

## C libraries { #predefined-c-libraries }

Some commonly used C libraries are provided as
`~ctypes.CDLL`{.interpreted-text role="class"}s. Other libraries can be
loaded using the `load_library`{.interpreted-text role="func"} function.

:::: {.data annotation="= load_library('c')"}
libc

The [C standard library](https://en.cppreference.com/w/c).

The following functions are accessible by default:

::: {.hlist}
* `free`
:::
::::

:::: {.data annotation="= load_library('objc')"}
libobjc

The [Objective-C runtime
library](https://developer.apple.com/documentation/objectivec).

The following functions are accessible by default:

::: {.hlist}
* `class_addIvar` * `class_addMethod` * `class_addProperty` *
`class_addProtocol` * `class_copyIvarList` * `class_copyMethodList` *
`class_copyPropertyList` * `class_copyProtocolList` *
`class_getClassMethod` * `class_getClassVariable` *
`class_getInstanceMethod` * `class_getInstanceSize` *
`class_getInstanceVariable` * `class_getIvarLayout` *
`class_getMethodImplementation` * `class_getName` *
`class_getProperty` * `class_getSuperclass` * `class_getVersion` *
`class_getWeakIvarLayout` * `class_isMetaClass` *
`class_replaceMethod` * `class_respondsToSelector` *
`class_setIvarLayout` * `class_setVersion` * `class_setWeakIvarLayout`
* `ivar_getName` * `ivar_getOffset` * `ivar_getTypeEncoding` *
`method_exchangeImplementations` * `method_getImplementation` *
`method_getName` * `method_getTypeEncoding` *
`method_setImplementation` * `objc_allocateClassPair` *
`objc_copyProtocolList` * `objc_getAssociatedObject` * `objc_getClass`
* `objc_getMetaClass` * `objc_getProtocol` * `objc_registerClassPair`
* `objc_removeAssociatedObjects` * `objc_setAssociatedObject` *
`object_getClass` * `object_getClassName` * `object_getIvar` *
`object_setIvar` * `property_getAttributes` * `property_getName` *
`property_copyAttributeList` * `protocol_addMethodDescription` *
`protocol_addProtocol` * `protocol_addProperty` *
`objc_allocateProtocol` * `protocol_conformsToProtocol` *
`protocol_copyMethodDescriptionList` * `protocol_copyPropertyList` *
`protocol_copyProtocolList` * `protocol_getMethodDescription` *
`protocol_getName` * `objc_registerProtocol` * `sel_getName` *
`sel_isEqual` * `sel_registerName`
:::
::::

::: {.data annotation="= load_library('Foundation')"}
Foundation

The [Foundation](https://developer.apple.com/documentation/foundation)
framework.
:::

::: load_library <!-- TODO: function -->

## Objective-C runtime types

These are various types used by the Objective-C runtime functions.

::: objc_id([value]) <!-- TODO: class -->

::: objc_block([value]) <!-- TODO: class -->

::: SEL([value]) <!-- TODO: class -->

::: name <!-- TODO: attribute -->
::::

::: Class([value]) <!-- TODO: class -->

::: IMP([value]) <!-- TODO: class -->

::: Method([value]) <!-- TODO: class -->

::: Ivar([value]) <!-- TODO: class -->

::: objc_property_t([value]) <!-- TODO: class -->

::: objc_property_attribute_t([name, value]) <!-- TODO: class -->

::: name value <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The attribute name and value as C strings (`bytes`{.interpreted-text
role="class"}).

::::

::: objc_method_description([name, value]) <!-- TODO: class -->

::: name <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The method name as a `SEL`{.interpreted-text role="class"}.


::: types <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The method's signature encoding as a C string (`bytes`{.interpreted-text
role="class"}).

:::::

::: objc_super([receiver, super_class]) <!-- TODO: class -->

::: receiver <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The receiver of the call, as an `objc_id`{.interpreted-text
role="class"}.


::: super_class <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The class in which to start searching for method implementations, as a
`Class`{.interpreted-text role="class"}.

:::::

## Objective-C runtime utility functions

These utility functions provide easier access from Python to certain
parts of the Objective-C runtime.

::: object_isClass(obj) <!-- TODO: function -->
<!-- TODO: Doc notes -->
Return whether the given Objective-C object is a class (or a metaclass).

This is equivalent to the `libobjc`{.interpreted-text role="data"}
function
[object_isClass](https://developer.apple.com/documentation/objectivec/1418659-object_isclass?language=objc)
from `<objc/runtime.h>`, which is only available since OS X 10.10 and
iOS 8. This module-level function is provided to support older systems
--- it uses the `libobjc`{.interpreted-text role="data"} function if
available, and otherwise emulates it.


::: get_class <!-- TODO: function -->

::: should_use_stret <!-- TODO: function -->

::: should_use_fpret <!-- TODO: function -->

::: send_message <!-- TODO: function -->

::: send_super <!-- TODO: function -->

::: add_method <!-- TODO: function -->

::: add_ivar <!-- TODO: function -->

::: get_ivar <!-- TODO: function -->

::: set_ivar <!-- TODO: function -->
