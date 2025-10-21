# `rubicon.objc.api` - The high-level Rubicon API { #rubicon-objc-api }

This module contains Rubicon's main high-level APIs, which allow easy
interaction with Objective-C classes and objects using Pythonic syntax.

Nearly all attributes of this module are also available on the main
[`rubicon.objc`][rubicon-objc-module] module, and if possible
that module should be used instead of importing
[`rubicon.objc.api`][rubicon-objc-api] directly.

## Objective-C objects

::: rubicon.objc.api.ObjCInstance
    options:
        heading_level: 3

::: rubicon.objc.api.objc_const
    options:
        heading_level: 3

## Objective-C classes

::: rubicon.objc.api.ObjCClass

::: rubicon.objc.api.ObjCMetaClass

## Standard Objective-C and Foundation classes

The following classes from the [Objective-C runtime](https://developer.apple.com/documentation/objectivec?language=objc) and the [Foundation](https://developer.apple.com/documentation/foundation?language=objc) framework are provided as [`ObjCClass`][rubicon.objc.api.ObjCClass]es for convenience. (Other classes not listed here can be looked up by passing a class name to the [`ObjCClass`][rubicon.objc.api.ObjCClass] constructor.)

/// note | Note

None of the following classes have a usable Python-style constructor -
for example, you *cannot* call `NSString("hello")` to create an
Objective-C string from a Python string. To create instances of these
classes, you should use [`ns_from_py`][rubicon.objc.ns_from_py]
(also called [`at`][rubicon.objc.at]): `ns_from_py("hello")`
returns a [`NSString`][rubicon.objc.api.NSString] instance with the
value `hello`.

///

::: rubicon.objc.api.NSObject
    options:
        heading_level: 3
        show_symbol_type_toc: false
        show_labels: false

::: rubicon.objc.api.Protocol
    options:
        heading_level: 3
        show_symbol_type_toc: false
        show_labels: false

::: rubicon.objc.api.NSNumber
    options:
        heading_level: 3
        show_symbol_type_toc: false
        show_labels: false

::: rubicon.objc.api.NSDecimalNumber
    options:
        heading_level: 3
        show_symbol_type_toc: false
        show_labels: false

::: rubicon.objc.api.NSString
    options:
        heading_level: 3
        show_symbol_type_toc: false
        show_labels: false

::: rubicon.objc.api.NSData
    options:
        heading_level: 3
        show_symbol_type_toc: false
        show_labels: false

::: rubicon.objc.api.NSArray
    options:
        heading_level: 3
        show_symbol_type_toc: false
        show_labels: false

::: rubicon.objc.api.NSMutableArray
    options:
        heading_level: 3
        show_symbol_type_toc: false
        show_labels: false

::: rubicon.objc.api.NSDictionary
    options:
        heading_level: 3
        show_symbol_type_toc: false
        show_labels: false

::: rubicon.objc.api.NSMutableDictionary
    options:
        heading_level: 3
        show_symbol_type_toc: false
        show_labels: false

## Objective-C protocols

::: rubicon.objc.api.ObjCProtocol

## Standard Objective-C and Foundation protocols

The following protocols from the [Objective-C runtime](https://developer.apple.com/documentation/objectivec?language=objc) and the [Foundation](https://developer.apple.com/documentation/foundation?language=objc) framework are provided as [`ObjCProtocol`][rubicon.objc.api.ObjCProtocol]s for convenience. (Other protocols not listed here can be looked up by passing a protocol name to the [`ObjCProtocol`][rubicon.objc.api.ObjCProtocol] constructor.)

::: rubicon.objc.NSObjectProtocol
    options:
        heading_level: 3
        show_symbol_type_toc: false

## Converting objects between Objective-C and Python

::: rubicon.objc.py_from_ns
    options:
        heading_level: 3

::: rubicon.objc.ns_from_py
    options:
        heading_level: 3

::: rubicon.objc.at
    options:
        heading_level: 3

## Creating custom Objective-C classes and protocols { #custom-classes-and-protocols }

Custom Objective-C classes are defined using Python `class` syntax, by
subclassing an existing [`ObjCClass`][rubicon.objc.api.ObjCClass]
object:

```python
class MySubclass(NSObject):
    # method, property, etc. definitions go here
```

A custom Objective-C class can only have a single superclass, since
Objective-C does not support multiple inheritance. However, the class
can conform to any number of protocols, which are specified by adding
the `protocols` keyword argument to the base class list:

```python
class MySubclass(NSObject, protocols=[NSCopying, NSMutableCopying]):
    # method, property, etc. definitions go here
```

/// note | Note

Rubicon requires specifying a superclass when defining a custom
Objective-C class. If you don't need to extend any specific class, use
[`NSObject`][rubicon.objc.NSObject] as the superclass.

Although Objective-C technically allows defining classes without a base
class (so-called *root classes*), this is almost never the desired
behavior (attempting to do so [causes a compiler error by
default](https://developer.apple.com/documentation/objectivec/objc_root_class)).
In practice, this feature is only used in the definitions of core
Objective-C classes like [`NSObject`][rubicon.objc.NSObject].
Because of this, Rubicon does not support defining Objective-C root
classes.

///

Similar syntax is used to define custom Objective-C protocols. Unlike
classes, protocols can extend multiple other protocols:

```python
class MyProtocol(NSCopying, NSMutableCopying):
    # method, property, etc. definitions go here
```

A custom protocol might not need to extend any other protocol at all. In
this case, we need to explicitly tell Python to define an
[`ObjCProtocol`][rubicon.objc.api.ObjCProtocol]. Normally Python detects
the metaclass automatically by examining the base classes, but in this
case there are none, so we need to specify the metaclass manually.

```python
class MyProtocol(metaclass=ObjCProtocol):
    # method, property, etc. definitions go here
```

### Defining methods

::: rubicon.objc.api.objc_method
    options:
        heading_level: 4

::: rubicon.objc.api.objc_classmethod
    options:
        heading_level: 4

### Method naming

The name of a Python-defined Objective-C method is same as the Python
method's name, but with all underscores (`_`) replaced with colons (`:`)
--- for example, `initWithWidth_height_` becomes
`initWithWidth:height:`.

/// warning | Warning

The Objective-C *language* imposes certain requirements on the usage of
colons in method names: a method's name must contain exactly as many
colons as the method has arguments (excluding the implicit `self` and
`_cmd` parameters), and the name of a method with arguments must end
with a colon. For example, a method called `init` takes no arguments,
`initWithSize:` takes a single argument, `initWithWidth:height:` takes
two, etc. `initWithSize:spam` is an invalid method name.

These requirements are not enforced by the Objective-C *runtime*, but
methods that do not follow them cannot easily be used from regular
Objective-C code.

In addition, although the Objective-C language allows method names with
multiple consecutive colons or a colon at the start of the name, such
names are considered bad style and never used in practice. For example,
`spam::`, `:ham:`, and `:` are unusual, but valid method names.

Future versions of Rubicon may warn about or disallow such nonstandard
method names.

///

### Parameter and return types

The argument and return types of a Python-created Objective-C method are
determined based on the Python method's type annotations. The
annotations may contain any [`ctypes`][] type,
as well as any of the Python types accepted by
`~rubicon.objc.types.ctype_for_type`{.interpreted-text role="func"}. If
a parameter or the return type is not specified, it defaults to
[`ObjCInstance`][rubicon.objc.api.ObjCInstance]. The `self` parameter is
special-cased --- its type is always `ObjCInstance`{.interpreted-text
role="class"}, even if annotated otherwise. To annotate a method as
returning `void`, set its return type to `None`{.interpreted-text
role="class"}.

Before being passed to the Python method, any object parameters
(`~rubicon.objc.runtime.objc_id`{.interpreted-text role="class"}) are
automatically converted to `ObjCInstance`{.interpreted-text
role="class"}. If the method returns an Objective-C object, it is
converted using [`ns_from_py`][rubicon.objc.ns_from_py] before being
returned to Objective-C. These automatic conversions can be disabled by
using `objc_rawmethod`{.interpreted-text role="func"} instead of
`objc_method`{.interpreted-text role="func"}.

The implicit `_cmd` parameter is not passed to the Python method, as it
is normally redundant and not needed. If needed, the `_cmd` parameter
can be accessed by using `objc_rawmethod`{.interpreted-text role="func"}
instead of `objc_method`{.interpreted-text role="func"}.

::: rubicon.objc.api.objc_rawmethod
    options:
        heading_level: 4

### Defining properties and `ivars`

::: rubicon.objc.api.objc_property
    options:
        heading_level: 4

::: rubicon.objc.api.objc_ivar
    options:
        heading_level: 4

::: rubicon.objc.api.get_ivar
    options:
        heading_level: 4

::: rubicon.objc.api.set_ivar
    options:
        heading_level: 4

## Objective-C blocks { #objc_blocks }

Blocks are the Objective-C equivalent of function objects, so Rubicon
provides ways to call Objective-C blocks from Python and to pass Python
callables to Objective-C as blocks.

### Automatic conversion

If an Objective-C method returns a block (according to its type
encoding), Rubicon will convert the return value to a special
[`ObjCInstance`][rubicon.objc.api.ObjCInstance] that can be called in
Python:

```python
block = an_objc_instance.methodReturningABlock()
res = block(arg, ...)
```

Similarly, if an Objective-C method has a parameter that expects a
block, you can pass in a Python callable object, and it will be
converted to an Objective-C block. In this case, the callable object
needs to have parameter and return type annotations, so that Rubicon can
expose this type information to the Objective-C runtime:

```python
def result_handler(res: objc_id) -> None:
    print(ObjCInstance(res))

an_objc_instance.doSomethingWithResultHandler(result_handler)
```

If you are writing a custom Objective-C method (see
`custom-classes-and-protocols`{.interpreted-text role="ref"}), you can
annotate parameter or return types using
`~rubicon.objc.runtime.objc_block`{.interpreted-text role="class"} so
that Rubicon converts them appropriately:

```python
class AnObjCClass(NSObject):
    @objc_method
    def methodReturningABlock() -> objc_block:
        def the_block(arg: NSInteger) -> NSUInteger:
            return abs(arg)
        return the_block

    @objc_method
    def doSomethingWithResultHandler_(result_handler: objc_block) -> None:
        res = SomeClass.someMethod()
        result_handler(res)
```

/// note | Note

These automatic conversions are mostly equivalent to the manual
conversions described in the next section. There are internal technical
differences between automatic and manual conversions, but they are not
noticeable to most users.

The internals of automatic conversion and
`~rubicon.objc.runtime.objc_block`{.interpreted-text role="class"}
handling may change in the future, so if you need more control over the
block conversion process, you should use the manual conversions
described in the next section.

///

### Manual conversion

These classes are used to manually convert blocks to Python callables
and vice versa. You may need to use them to perform these conversions
outside of Objective-C method calls, or if you need more control over
the block's type signature.

::: rubicon.objc.api.ObjCBlock
    options:
        heading_level: 4
        members:
            - __call__

::: rubicon.objc.api.Block
    options:
        heading_level: 4

## Defining custom subclasses of [`ObjCInstance`][rubicon.objc.api.ObjCInstance]

The following functions can be used to register custom subclasses of
[`ObjCInstance`][rubicon.objc.api.ObjCInstance] to be used when wrapping
instances of a certain Objective-C class. This mechanism is for example
used by Rubicon to provide Python-style operators and methods on
standard Foundation classes, such as [`NSString`][rubicon.objc.api.NSString] and `NSDictionary`{.interpreted-text role="class"}.

::: rubicon.objc.api.register_type_for_objcclass
    options:
        heading_level: 3

::: rubicon.objc.api.for_objcclass
    options:
        heading_level: 3

::: rubicon.objc.api.type_for_objcclass
    options:
        heading_level: 3

::: rubicon.objc.api.unregister_type_for_objcclass
    options:
        heading_level: 3

::: rubicon.objc.api.get_type_for_objcclass_map
    options:
        heading_level: 3
