# `rubicon.objc.api` - The high-level Rubicon API

{.module}
rubicon.objc.api

This module contains Rubicon's main high-level APIs, which allow easy
interaction with Objective-C classes and objects using Pythonic syntax.

Nearly all attributes of this module are also available on the main
`rubicon.objc`{.interpreted-text role="mod"} module, and if possible
that module should be used instead of importing
`rubicon.objc.api`{.interpreted-text role="mod"} directly.

## Objective-C objects

::: rubicon.objc.api.ObjCInstance
<!-- TODO: class, add `ptr` to args? -->

<:> ptr <span id="as_parameter">as_parameter</span>  <!-- TODO: attribute, stub candidate -->
<!-- TODO: stub notes -->


The wrapped object pointer as an
`~rubicon.objc.runtime.objc_id`{.interpreted-text role="class"}. This
attribute is also available as `_as_parameter_` to allow
`ObjCInstance`{.interpreted-text role="class"}s to be passed into
`ctypes`{.interpreted-text role="mod"} functions.

::: rubicon.objc.api.objc_const
<!-- TODO: function -->

<:> objc_class <!-- TODO: attribute -->

<:> str <!-- TODO: method -->

<:> repr <!-- TODO: method -->

<:> getattr <!-- TODO: method -->

<:> setattr <!-- TODO: method -->


## Objective-C classes

::: rubicon.objc.api.ObjCClass

(name_or_ptr, [bases, attrs, [protocols=(),auto_rename=None]]) <!-- TODO: add to args? -->

::: rubicon.objc.api.ObjCMetaClass
(name_or_ptr) <!-- TODO: add to args? -->

<:> name <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
The name of this class, as a `str`{.interpreted-text role="class"}.


<:> superclass <!-- TODO: attribute -->

<:> protocols <!-- TODO: attribute -->

<:> auto_rename <!-- TODO: attribute -->

<:> declare_property <!-- TODO: method -->

<:> declare_class_property <!-- TODO: method -->

<:> instancecheck <!-- TODO: method -->

<:> subclasscheck <!-- TODO: method -->

### Standard Objective-C and Foundation classes

The following classes from the [Objective-C
runtime](https://developer.apple.com/documentation/objectivec?language=objc)
and the
[Foundation](https://developer.apple.com/documentation/foundation?language=objc)
framework are provided as `ObjCClass`{.interpreted-text role="class"}es
for convenience. (Other classes not listed here can be looked up by
passing a class name to the `ObjCClass`{.interpreted-text role="class"}
constructor.)

/// note | Note

None of the following classes have a usable Python-style constructor -
for example, you *cannot* call `NSString("hello")` to create an
Objective-C string from a Python string. To create instances of these
classes, you should use `ns_from_py`{.interpreted-text role="func"}
(also called `at`{.interpreted-text role="func"}): `ns_from_py("hello")`
returns a `NSString`{.interpreted-text role="class"} instance with the
value `hello`.

///

::: NSObject
    options:
        find_stubs_package: true

<!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSObject](https://developer.apple.com/documentation/objectivec/nsobject?language=objc)
class from `<objc/NSObject.h>`.

/// note | Note

See the `ObjCInstance`{.interpreted-text role="class"} documentation for
a list of operations that Rubicon supports on all objects.

///

<:> debugDescription description <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
These Objective-C properties have been declared using
`ObjCClass.declare_property`{.interpreted-text role="meth"} and can
always be accessed using attribute syntax.



<:> Protocol  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[Protocol](https://developer.apple.com/documentation/objectivec/protocol?language=objc)
class from `<objc/Protocol.h>`.

/// note | Note

This class has no (non-deprecated) Objective-C methods; protocol objects
can only be manipulated using Objective-C runtime functions. Rubicon
automatically wraps all `Protocol`{.interpreted-text role="class"}
objects using `ObjCProtocol`{.interpreted-text role="class"}, which
provides an easier interface for working with protocols.

///


<:> NSNumber  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSNumber](https://developer.apple.com/documentation/foundation/nsnumber?language=objc)
class from `<Foundation/NSValue.h>`.

/// note | Note

This class can be converted to and from standard Python primitives
(`bool`, `int`, `float`) using `py_from_ns`{.interpreted-text
role="func"} and `ns_from_py`{.interpreted-text role="func"}.

///


<:> NSDecimalNumber  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSDecimalNumber](https://developer.apple.com/documentation/foundation/nsdecimalnumber?language=objc)
class from `<Foundation/NSDecimalNumber.h>`.

/// note | Note

This class can be converted to and from Python `decimal.Decimal` using
`py_from_ns`{.interpreted-text role="func"} and
`ns_from_py`{.interpreted-text role="func"}.

///


<:> NSString  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSString](https://developer.apple.com/documentation/foundation/nsstring?language=objc)
class from `<Foundation/NSString.h>`.

This class also supports all methods that `str`{.interpreted-text
role="class"} does.

/// note | Note

This class can be converted to and from Python `str`{.interpreted-text
role="class"} using `py_from_ns`{.interpreted-text role="func"} and
`ns_from_py`{.interpreted-text role="func"}. You can also call
`str(nsstring)` to convert a `NSString` to `str`{.interpreted-text
role="class"}.

`NSString`{.interpreted-text role="class"} objects consist of UTF-16
code units, unlike `str`{.interpreted-text role="class"}, which consists
of Unicode code points. All `NSString`{.interpreted-text role="class"}
indices and iteration are based on UTF-16, even when using the
Python-style operations/methods. If indexing or iteration based on code
points is required, convert the `NSString`{.interpreted-text
role="class"} to `str`{.interpreted-text role="class"} first.

///

<:> str () <!-- TODO: method -->
<!-- TODO: Doc notes -->
Return the value of this `NSString`{.interpreted-text role="class"} as a
`str`{.interpreted-text role="class"}.


<:> UTF8String <!-- TODO: attribute -->
<!-- TODO: Doc notes -->
This Objective-C property has been declared using
`ObjCClass.declare_property`{.interpreted-text role="meth"} and can
always be accessed using attribute syntax.



<:> NSData  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSData](https://developer.apple.com/documentation/foundation/nsdata?language=objc)
class from `<Foundation/NSData.h>`.

/// note | Note

This class can be converted to and from Python `bytes`{.interpreted-text
role="class"} using `py_from_ns`{.interpreted-text role="func"} and
`ns_from_py`{.interpreted-text role="func"}.

///


<:> NSArray  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSArray](https://developer.apple.com/documentation/foundation/nsarray?language=objc)
class from `<Foundation/NSArray.h>`.

/// note | Note

This class can be converted to and from Python `list`{.interpreted-text
role="class"} using `py_from_ns`{.interpreted-text role="func"} and
`ns_from_py`{.interpreted-text role="func"}.

`py_from_ns(nsarray)` will recursively convert `nsarray`'s elements to
Python objects, where possible. To avoid this recursive conversion, use
`list(nsarray)` instead.

`ns_from_py(pylist)` will recursively convert `pylist`'s elements to
Objective-C. As there is no way to store Python object references as
Objective-C objects yet, this recursive conversion cannot be avoided. If
any of `pylist`'s elements cannot be converted to Objective-C, an error
is raised.

///

<:> getitem (index)  len ()  iter ()
 contains (value)  eq (other)  ne (other) index(value)
count(value) copy() <!-- TODO: method -->
<!-- TODO: Doc notes -->
Python-style sequence interface.



<:> NSMutableArray  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSMutableArray](https://developer.apple.com/documentation/foundation/nsmutablearray?language=objc)
class from `<Foundation/NSArray.h>`.

/// note | Note

This class can be converted to and from Python exactly like its
superclass `NSArray`.

///

<:> setitem (index, value)  delitem (index) append(value)
clear() extend(values) insert(index, value) pop([index=-1])
remove(value) reverse() <!-- TODO: method -->
<!-- TODO: Doc notes -->
Python-style mutable sequence interface.



<:> NSDictionary  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSDictionary](https://developer.apple.com/documentation/foundation/nsdictionary?language=objc)
class from `<Foundation/NSDictionary.h>`.

/// note | Note

This class can be converted to and from Python `dict`{.interpreted-text
role="class"} using `py_from_ns`{.interpreted-text role="func"} and
`ns_from_py`{.interpreted-text role="func"}.

`py_from_ns(nsdict)` will recursively convert `nsdict`'s keys and values
to Python objects, where possible. To avoid the recursive conversion of
the values, use `{py_from_ns(k): v for k, v in nsdict.items()}`. The
conversion of the keys cannot be avoided, because Python
`dict`{.interpreted-text role="class"} keys need to be hashable, which
`ObjCInstance`{.interpreted-text role="class"} is not. If any of the
keys convert to a Python object that is not hashable, an error is raised
(regardless of which conversion method you use).

`ns_from_py(pydict)` will recursively convert `pydict`'s keys and values
to Objective-C. As there is no way to store Python object references as
Objective-C objects yet, this recursive conversion cannot be avoided. If
any of `pydict`'s keys or values cannot be converted to Objective-C, an
error is raised.

///

<!-- TODO: methods -->
getitem (key)  len ()  iter ()  contains (key)
 eq (other)  ne (other) copy() get(key, [default=None])
keys() items() values()

Python-style mapping interface.

/// note | Note

Unlike most Python mappings, `NSDictionary`{.interpreted-text
role="class"}'s `keys`{.interpreted-text role="attr"},
`values`{.interpreted-text role="attr"}, and `items`{.interpreted-text
role="attr"} methods don't return dynamic views of the dictionary's
keys, values, and items.

`keys`{.interpreted-text role="attr"} and `values`{.interpreted-text
role="attr"} return lists that are created each time the methods are
called, which can have an effect on performance and memory usage for
large dictionaries. To avoid this, you can cache the return values of
`keys`{.interpreted-text role="attr"} and `values`{.interpreted-text
role="attr"}, or convert the `NSDictionary`{.interpreted-text
role="class"} to a Python `dict`{.interpreted-text role="class"}
beforehand.

`items`{.interpreted-text role="attr"} is currently implemented as a
generator, meaning that it returns a single-use iterator. If you need to
iterate over `items`{.interpreted-text role="attr"} more than once or
perform other operations on it, you should convert it to a Python
`set`{.interpreted-text role="class"} or `list`{.interpreted-text
role="class"} first.

///



<:> NSMutableDictionary  <!-- TODO: stub candidate -->
<!-- TODO: stub notes -->
The
[NSMutableDictionary](https://developer.apple.com/documentation/foundation/nsmutabledictionary?language=objc)
class from `<Foundation/NSDictionary.h>`.

/// note | Note

This class can be converted to and from Python exactly like its
superclass `NSDictionary`.

///

<:> setitem (key, value)  delitem (key) clear() pop(item,
[default]) popitem() setdefault(key, [default=None])
update([other], **kwargs) <!-- TODO: method -->
<!-- TODO: Doc notes -->
Python-style mutable mapping interface.



## Objective-C protocols

<:> ObjCProtocol(name_or_ptr, [bases, attrs, [auto_rename=None]]) <!-- TODO: class -->

<:> name <!-- TODO: attribute -->

<:> protocols <!-- TODO: attribute -->

<:> auto_rename <!-- TODO: attribute -->

<:> instancecheck <!-- TODO: method -->

<:> subclasscheck <!-- TODO: method -->

### Standard Objective-C and Foundation protocols

The following protocols from the [Objective-C
runtime](https://developer.apple.com/documentation/objectivec?language=objc)
and the
[Foundation](https://developer.apple.com/documentation/foundation?language=objc)
framework are provided as `ObjCProtocol`{.interpreted-text
role="class"}s for convenience. (Other protocols not listed here can be
looked up by passing a protocol name to the
`ObjCProtocol`{.interpreted-text role="class"} constructor.)

<:> NSObjectProtocol <!-- TODO: data -->
<!-- TODO: Doc notes -->
The
[NSObject](https://developer.apple.com/documentation/objectivec/1418956-nsobject?language=objc)
protocol from `<objc/NSObject.h>`. The protocol is exported as
`NSObjectProtocol`{.interpreted-text role="class"} in Python because it
would otherwise clash with the `NSObject`{.interpreted-text
role="class"} class.


## Converting objects between Objective-C and Python

<:> py_from_ns(nsobj) <!-- TODO: function -->

<:> ns_from_py <!-- TODO: function -->

<:> at(pyobj) <!-- TODO: function -->
<!-- TODO: Doc notes -->
Alias for `ns_from_py`{.interpreted-text role="func"}.


## Creating custom Objective-C classes and protocols { #custom-classes-and-protocols }

Custom Objective-C classes are defined using Python `class` syntax, by
subclassing an existing `ObjCClass`{.interpreted-text role="class"}
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
`NSObject`{.interpreted-text role="class"} as the superclass.

Although Objective-C technically allows defining classes without a base
class (so-called *root classes*), this is almost never the desired
behavior (attempting to do so [causes a compiler error by
default](https://developer.apple.com/documentation/objectivec/objc_root_class)).
In practice, this feature is only used in the definitions of core
Objective-C classes like `NSObject`{.interpreted-text role="class"}.
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
`ObjCProtocol`{.interpreted-text role="class"}. Normally Python detects
the metaclass automatically by examining the base classes, but in this
case there are none, so we need to specify the metaclass manually.

```python
class MyProtocol(metaclass=ObjCProtocol):
    # method, property, etc. definitions go here
```

### Defining methods

<:> objc_method <!-- TODO: function -->

<:> objc_classmethod <!-- TODO: function -->

#### Method naming

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

#### Parameter and return types

The argument and return types of a Python-created Objective-C method are
determined based on the Python method's type annotations. The
annotations may contain any `ctypes`{.interpreted-text role="mod"} type,
as well as any of the Python types accepted by
`~rubicon.objc.types.ctype_for_type`{.interpreted-text role="func"}. If
a parameter or the return type is not specified, it defaults to
`ObjCInstance`{.interpreted-text role="class"}. The `self` parameter is
special-cased --- its type is always `ObjCInstance`{.interpreted-text
role="class"}, even if annotated otherwise. To annotate a method as
returning `void`, set its return type to `None`{.interpreted-text
role="class"}.

Before being passed to the Python method, any object parameters
(`~rubicon.objc.runtime.objc_id`{.interpreted-text role="class"}) are
automatically converted to `ObjCInstance`{.interpreted-text
role="class"}. If the method returns an Objective-C object, it is
converted using `ns_from_py`{.interpreted-text role="func"} before being
returned to Objective-C. These automatic conversions can be disabled by
using `objc_rawmethod`{.interpreted-text role="func"} instead of
`objc_method`{.interpreted-text role="func"}.

The implicit `_cmd` parameter is not passed to the Python method, as it
is normally redundant and not needed. If needed, the `_cmd` parameter
can be accessed by using `objc_rawmethod`{.interpreted-text role="func"}
instead of `objc_method`{.interpreted-text role="func"}.

<:> objc_rawmethod <!-- TODO: function -->

### Defining properties and `ivars`

<:> objc_property <!-- TODO: function -->

<:> objc_ivar <!-- TODO: function -->

<:> get_ivar <!-- TODO: function -->

<:> set_ivar <!-- TODO: function -->

## Objective-C blocks { #objc_blocks }

Blocks are the Objective-C equivalent of function objects, so Rubicon
provides ways to call Objective-C blocks from Python and to pass Python
callables to Objective-C as blocks.

### Automatic conversion

If an Objective-C method returns a block (according to its type
encoding), Rubicon will convert the return value to a special
`ObjCInstance`{.interpreted-text role="class"} that can be called in
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

<:> ObjCBlock(pointer, [return_type, *arg_types]) <!-- TODO: class -->

<:> call <!-- TODO: method -->


<:> Block(func, [restype, *argtypes]) <!-- TODO: class -->

## Defining custom subclasses of `ObjCInstance`{.interpreted-text role="class"}

The following functions can be used to register custom subclasses of
`ObjCInstance`{.interpreted-text role="class"} to be used when wrapping
instances of a certain Objective-C class. This mechanism is for example
used by Rubicon to provide Python-style operators and methods on
standard Foundation classes, such as `NSString`{.interpreted-text
role="class"} and `NSDictionary`{.interpreted-text role="class"}.

<:> register_type_for_objcclass <!-- TODO: function -->

<:> for_objcclass <!-- TODO: function -->

<:> type_for_objcclass <!-- TODO: function -->

<:> unregister_type_for_objcclass <!-- TODO: function -->

<:> get_type_for_objcclass_map <!-- TODO: function -->
