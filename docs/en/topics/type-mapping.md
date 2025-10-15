# You're just not my type: Using Objective-C types in Python

Objective-C is a strongly and statically-typed language. Every variable
has a specific type, and that type cannot change over time. Function
parameters also have fixed types, and a function will only accept
arguments of the correct types.

Python, on the other hand, is a strongly, but *dynamically*-typed
language. Every object has a specific type, but all variables can hold
objects of any type. When a function accepts an argument, Python will
allow you to pass *any* object, of *any* type.

So, if you want to bridge between Objective-C and Python, you need to be
able to provide static typing information so that Rubicon can work out
how to convert a Python object of arbitrary type into a specific type
matching Objective-C's expectations.

## Type annotations

If you're calling an Objective-C method defined in a library, its types
are already known to the Objective-C runtime and Rubicon. However, if
you're defining a new method (or a method override) in Python, you need
to manually provide its types. This is done using Python 3's type
annotation syntax.

Passing and returning Objective-C objects doesn't require any extra work
---if you don't annotate a parameter or the return type, Rubicon assumes
that it is an Objective-C object. (To define a method that doesn't
return anything, you need to add an explicit `-> None` annotation.)

All other parameter and return types (primitives, pointers, structs)
need to be annotated to tell Rubicon and Objective-C which type to
expect. These annotations can use any of the types defined by Rubicon,
such as `~rubicon.objc.types.NSInteger`{.interpreted-text role="class"}
or `~rubicon.objc.types.NSRange`{.interpreted-text role="class"}, as
well as standard C types from the `ctypes`{.interpreted-text role="mod"}
module, such as `~ctypes.c_byte`{.interpreted-text role="class"} or
`~ctypes.c_double`{.interpreted-text role="class"}.

For example, a method that takes a C `double` and returns a
`~rubicon.objc.types.NSInteger`{.interpreted-text role="class"} would be
defined and annotated like this:

```python
@objc_method
def roundToZero_(self, value: c_double) -> NSInteger:
    return int(value)
```

Rubicon also allows certain Python types to be used in method
signatures, and converts them to matching primitive
`ctypes`{.interpreted-text role="mod"} types. For example, Python
`int`{.interpreted-text role="class"} is treated as
`~ctypes.c_int`{.interpreted-text role="class"}, and
`float`{.interpreted-text role="class"} is treated as
`~ctypes.c_double`{.interpreted-text role="class"}.

/// note | See also

The `rubicon.objc.types`{.interpreted-text role="mod"} reference
documentation lists all C type definitions provided by Rubicon, and
provides additional information about how Rubicon converts types.

///

## Type conversions

When you call existing Objective-C methods, Rubicon already knows which
type each argument needs to have and what it returns. Based on this type
information, Rubicon will automatically convert the passed arguments to
the proper Objective-C types, and the return value to an appropriate
Python type. This makes explicit type conversions between Python and
Objective-C types unnecessary in many cases.

### Argument conversion { #argument_conversion }

If an Objective-C method expects a C primitive argument, you can pass an
equivalent Python value instead. For example, a Python
`int`{.interpreted-text role="class"} value can be passed into any
integer argument (`int`, `NSInteger`, `uint8_t`, ...), and a Python
`float`{.interpreted-text role="class"} value can be passed into any
floating-point argument (`double`, `CGFloat`, ...).

To pass a C structure as an argument, you would normally need to
construct a structure instance by name. This can get somewhat lengthy,
especially with nested structures (e. g.
`NSRect(NSPoint(1.2, 3.4), NSSize(5.6, 7.8))`). As a shorthand, Rubicon
allows passing tuples instead of structure objects (e. g.
`((1.2, 3.4), (5.6, 7.8))`) and automatically converts them to the
required structure type.

If a parameter expects an Objective-C object, you can also pass certain
Python objects, which are automatically converted to their Objective-C
counterparts. For example, a Python `str`{.interpreted-text
role="class"} is converted to an `NSString`, `bytes`{.interpreted-text
role="class"} to `NSData`, etc. Collections are also supported:
`list`{.interpreted-text role="class"} and `dict`{.interpreted-text
role="class"} are converted to `NSArray` and `NSDictionary`, and their
elements are converted recursively.

/// note | Note

All of these conversions can also be performed manually - see
`manual_conversions`{.interpreted-text role="ref"} for details.

///

### Return value conversion and wrapping

Primitive values returned from methods are converted using the usual
`ctypes`{.interpreted-text role="mod"} conversions, e. g. C integers are
converted to Python `int`{.interpreted-text role="class"} and
floating-point values to Python `float`{.interpreted-text role="class"}.

Objective-C objects are automatically returned as
`~rubicon.objc.api.ObjCInstance`{.interpreted-text role="class"}
objects, so you can call methods on them and access their properties. In
some cases, Rubicon also provides additional Python methods on
Objective-C objects -see `python_style_apis_for_objc`{.interpreted-text
role="ref"} for details.

## Invoking Objective-C methods

Once an Objective-C class has been wrapped, the selectors on that class
(or instances of that class) can be invoked as if they were methods on
the Python class. Each Objective-C selector is converted into a Python
method name by replacing the colons in the selector with underscores.

For example, the Objective-C class `NSURL` has defines a instance
selector of `-initWithString:relativeToURL:`; this will be converted
into the Python method `initWithString_relativeToURL_()`. Arguments to
this method are all positional, and passed in the order they are defined
in the selector. Selectors without arguments (such as `+alloc` or
`-init`) are defined as methods with no arguments, and no underscores in
the name:

```python
# Wrap the NSURL class
NSURL = ObjCClass("NSURL")
# Invoke the +alloc selector
my_url = NSURL.alloc()
# Invoke -initWithString:relativeToURL:
my_url.initWithString_relativeToURL_("something/", "https://example.com/")
```

This can result in very long method names; so Rubicon also provides an
alternate mapping for methods, using Python keyword arguments. In this
approach, the first argument is handled as a positional argument, and
all subsequent arguments are handled as keyword arguments, with the
underscore suffixes being omitted. The last method in the previous
example could also be invoked as:

```python
# Invoke -initWithString:relativeToURL:
my_url.initWithString("something/", relativeToURL="https://example.com/")
```

Keyword arguments *must* be passed in the order they are defined in the
selector. For example, if you were invoking
`-initFileURLWithPath:isDirectory:relativeToURL`, it *must* be invoked
as:

```python
# Invoke -initFileURLWithPath:isDirectory:relativeToURL
my_url.initFileURLWithPath(
    "something/",
    isDirectory=True,
    relativeToURL="file:///Users/brutus/"
)
```

Even though from a strict *Python* perspective, passing `relativeToURL`
before `isDirectory` would be syntactically equivalent, this *will not*
match the corresponding Objective-C selector.

This "interleaved" keyword syntax works for *most* Objective-C selectors
without any problem. However, Objective-C allows arguments in a selector
to be repeated. For example, `NSLayoutConstraint` defines a
`+constraintWithItem:attribute:relatedBy:toItem:attribute:multiplier:constant:`
selector, duplicating the `attribute` keyword. Python will not allow a
keyword argument to be duplicated, so to reach selectors of this type,
Rubicon allows any keyword argument to be appended with a `__` suffix to
generate a name that is unique in the Python code:

```python
# Invoke +constraintWithItem:attribute:relatedBy:toItem:attribute:multiplier:constant:
NSLayoutConstraint.constraintWithItem(
    first_item,
    attribute__1=first_attribute,
    relatedBy=relation,
    toItem=second_item,
    attribute__2=second_attribute,
    multiplier=2.0,
    constant=1.0
)
```

The name used after the `__` has no significance - it is only used to
ensure that the Python keyword is unique, and is immediately stripped
and ignored. By convention, we recommend using integers as we've done in
this example; but you *can* use any unique text you want. For example,
`attribute__from` and `attribute__to` would also work in this situation,
as would `attribute` and `atribute__to` (as the names are unique in the
Python namespace).

## Python-style APIs and methods for Objective-C objects { #python_style_apis_for_objc }

For some standard Foundation classes, such as lists and dictionaries,
Rubicon provides additional Python methods to make them behave more like
their Python counterparts. This allows using Foundation objects in place
of regular Python objects, so that you do not need to convert them
manually.

### Strings

`~rubicon.objc.api.NSString`{.interpreted-text role="class"} objects
behave almost exactly like Python `str`{.interpreted-text role="class"}
objects - they can be sliced, concatenated, compared, etc. with other
Objective-C and Python strings.

```pycon
# Call an Objective-C method that returns a string.
# We're using NSBundle to give us a string version of a path
>>> NSBundle.mainBundle.bundlePath
<ObjCStrInstance: __NSCFString at 0x114a94d68: /Users/brutus/path/to/somewhere>

# Slice the Objective-C string
>>> NSBundle.mainBundle.bundlePath[:14]
<ObjCStrInstance: __NSCFString at 0x114aa80f0: /Users/brutus/>
```

/// note | Note

`~rubicon.objc.api.ObjCInstance`{.interpreted-text role="class"} objects
wrapping a `~rubicon.objc.api.NSString`{.interpreted-text role="class"}
internally have the class `ObjCStrInstance`, and you will see this name
in the `repr`{.interpreted-text role="func"} of
`~rubicon.objc.api.NSString`{.interpreted-text role="class"} objects.
This is an implementation detail - you should not refer to the
`ObjCStrInstance` class explicitly in your code.

///

If you have an `~rubicon.objc.api.NSString`{.interpreted-text
role="class"}, and you need to pass it to a method that does a specific
type check for `str`{.interpreted-text role="class"}, you can use
`str(nsstring)` to convert the
`~rubicon.objc.api.NSString`{.interpreted-text role="class"} to
`str`{.interpreted-text role="class"}:

```pycon
# Convert the Objective-C string to a Python string.
>>> str(NSBundle.mainBundle.bundlePath)
'/Users/rkm/projects/beeware/venv3.6/bin'
```

Conversely, if you have a `str`{.interpreted-text role="class"}, and you
specifically require a `~rubicon.objc.api.NSString`{.interpreted-text
role="class"}, you can use the `~rubicon.objc.api.at`{.interpreted-text
role="func"} function to convert the Python instance to an
`~rubicon.objc.api.NSString`{.interpreted-text role="class"}.

```pycon
>>> from rubicon.objc import at
# Create a Python string
>>> py_str = 'hello world'
# Convert to an Objective-C string
>>> at(py_str)
<ObjCStrInstance: __NSCFString at 0x114a94e48: hello world>
```

`~rubicon.objc.api.NSString`{.interpreted-text role="class"} also
supports all the utility methods that are available on
`str`{.interpreted-text role="class"}, such as `replace` and `split`.
When these methods return a string, the implementation may return Python
`str`{.interpreted-text role="class"} or Objective-C
`~rubicon.objc.api.NSString`{.interpreted-text role="class"} instances.
If you need to use the return value from these methods, you should
always use `str`{.interpreted-text role="class"} or
`~rubicon.objc.api.at`{.interpreted-text role="func"} to ensure that you
have the right kind of string for your needs.

```pycon
# Is the path comprised of all lowercase letters? (Hint: it isn't)
>>> NSBundle.mainBundle.bundlePath.islower()
False

# Convert string to lower case; use str() to ensure we get a Python string.
>>> str(NSBundle.mainBundle.bundlePath.lower())
'/users/rkm/projects/beeware/venv3.6/bin'
```

/// note | Note

`~rubicon.objc.api.NSString`{.interpreted-text role="class"} objects
behave slightly differently than Python `str`{.interpreted-text
role="class"} objects in some cases. For technical reasons,
`~rubicon.objc.api.NSString`{.interpreted-text role="class"}s are not
hashable in Python, which means they cannot be used as
`dict`{.interpreted-text role="class"} keys (but they *can* be used as
`~rubicon.objc.api.NSDictionary`{.interpreted-text role="class"} keys).
`~rubicon.objc.api.NSString`{.interpreted-text role="class"} also
handles Unicode code points above `U+FFFF` differently than Python
`str`{.interpreted-text role="class"}, because the former is based on
UTF-16.

///

### Lists

`~rubicon.objc.api.NSArray`{.interpreted-text role="class"} objects
behave like any other Python sequence - they can be indexed, sliced,
etc. and standard operations like `len`{.interpreted-text role="func"}
and `in` are supported:

```pycon
>>> from rubicon.objc import NSArray
>>> array = NSArray.arrayWithArray(list(range(4)))
>>> array[0]
0
>>> array[1:3]
<ObjCListInstance: _NSArrayI at 0x10b855208: <__NSArrayI 0x7f86f8e61950>(
1,
2
)
>
>>> len(array)
4
>>> 2 in array
True
>>> 5 in array
False
```

/// note | Note

`~rubicon.objc.api.ObjCInstance`{.interpreted-text role="class"} objects
wrapping a `~rubicon.objc.api.NSArray`{.interpreted-text role="class"}
internally have the class `ObjCListInstance` or
`ObjCMutableListInstance`, and you will see these names in the
`repr`{.interpreted-text role="func"} of
`~rubicon.objc.api.NSArray`{.interpreted-text role="class"} objects.
This is an implementation detail - you should not refer to the
`ObjCListInstance` and `ObjCMutableListInstance` classes explicitly in
your code.

///

`~rubicon.objc.api.NSMutableArray`{.interpreted-text role="class"}
objects additionally support mutating operations, like item and slice
assignment:

```pycon
>>> from rubicon.objc import NSMutableArray
>>> mutarray = NSMutableArray.arrayWithArray(list(range(4)))
>>> mutarray[0] = 42
>>> mutarray
<ObjCMutableListInstance: __NSArrayM at 0x10b8558d0: <__NSArrayM 0x7f86fb04d9f0>(
42,
1,
2,
3
)
>
>>> mutarray[1:3] = [9, 8, 7]
>>> mutarray
<ObjCMutableListInstance: __NSArrayM at 0x10b8558d0: <__NSArrayM 0x7f86fb04d9f0>(
42,
9,
8,
7,
3
)
>
```

Sequence methods like `index` and `pop` are also supported:

```pycon
>>> mutarray.index(7)
3
>>> mutarray.pop(3)
7
```

/// note | Note

Python objects stored in an
`~rubicon.objc.api.NSArray`{.interpreted-text role="class"} are
converted to Objective-C objects using the rules described in
`argument_conversion`{.interpreted-text role="ref"}.

///

### Dictionaries

`~rubicon.objc.api.NSDictionary`{.interpreted-text role="class"} objects
behave like any other Python mapping - their items can be accessed and
standard operations like `len`{.interpreted-text role="func"} and `in`
are supported:

```pycon
>>> from rubicon.objc import NSDictionary
>>> d = objc.NSDictionary.dictionaryWithDictionary({"one": 1, "two": 2})
>>> d["one"]
1
>>> len(d)
>>> 2
>>> "two" in d
True
>>> "five" in d
False
```

/// note | Note

`~rubicon.objc.api.ObjCInstance`{.interpreted-text role="class"} objects
wrapping a `~rubicon.objc.api.NSDictionary`{.interpreted-text
role="class"} internally have the class `ObjCDictInstance` or
`ObjCMutableDictInstance`, and you will see these names in the
`repr`{.interpreted-text role="func"} of
`~rubicon.objc.api.NSDictionary`{.interpreted-text role="class"}
objects. This is an implementation detail - you should not refer to the
`ObjCDictInstance` and `ObjCMutableDictInstance` classes explicitly in
your code.

///

`~rubicon.objc.api.NSMutableDictionary`{.interpreted-text role="class"}
objects additionally support mutating operations, like item assignment:

```pycon
>>> md = objc.NSMutableDictionary.dictionaryWithDictionary({"one": 1, "two": 2})
>>> md["three"] = 3
>>> md
<ObjCMutableDictInstance: __NSDictionaryM at 0x10b8a7860: {
    one = 1;
    three = 3;
    two = 2;
}>
```

Mapping methods like `keys` and `values` are also supported:

```pycon
>>> d.keys()
<ObjCListInstance: __NSArrayI at 0x10b898a90: <__NSArrayI 0x7f86f8db6b70>(
one,
two
)
>
>>> d.values()
<ObjCListInstance: __NSArrayI at 0x10b8a7b38: <__NSArrayI 0x7f86f8c00370>(
1,
2
)
>
```

/// note | Note

Python objects stored in an
`~rubicon.objc.api.NSDictionary`{.interpreted-text role="class"} are
converted to Objective-C objects using the rules described in
`argument_conversion`{.interpreted-text role="ref"}.

///

## Manual conversions { #manual_conversions }

If necessary, you can also manually call Rubicon's type conversion
functions, to convert objects between Python and Objective-C when
Rubicon doesn't do so automatically.

### Converting from Python to Objective-C

The function `~rubicon.objc.api.ns_from_py`{.interpreted-text
role="func"} (also available as `~rubicon.objc.api.at`{.interpreted-text
role="func"} for short) can convert most standard Python objects to
Foundation equivalents. For a full list of possible conversions, see the
reference documentation for
`~rubicon.objc.api.ns_from_py`{.interpreted-text role="func"}.

These conversions are performed automatically when a Python object is
passed into an Objective-C method parameter that expects an object - in
that case you do not need to call
`~rubicon.objc.api.ns_from_py`{.interpreted-text role="func"} manually
(see `argument_conversion`{.interpreted-text role="ref"}).

### Converting from Objective-C to Python

The function `~rubicon.objc.api.py_from_ns`{.interpreted-text
role="func"} can convert many common Foundation objects to Python
equivalents. For a full list of possible conversions, see the reference
documentation for `~rubicon.objc.api.py_from_ns`{.interpreted-text
role="func"}.

These conversions are not performed automatically by Rubicon. For
example, if an Objective-C method returns an `NSString`, Rubicon will
return it as an `~rubicon.objc.api.ObjCInstance`{.interpreted-text
role="class"} (with some additional Python methods -see
`python_style_apis_for_objc`{.interpreted-text role="ref"}). Using
`~rubicon.objc.api.py_from_ns`{.interpreted-text role="func"}, you can
convert the `NSString` to a real Python `str`{.interpreted-text
role="class"}.

When converting collections, such as `NSArray` or `NSDictionary`,
`~rubicon.objc.api.py_from_ns`{.interpreted-text role="func"} will
convert them recursively to a pure Python object. For example, if
`nsarray` is an `NSArray` containing `NSString`s, `py_from_ns(nsarray)`
will return a `list`{.interpreted-text role="class"} of
`str`{.interpreted-text role="class"}s. In most cases, that is the
desired behavior, but you can also avoid this recursive conversion by
passing the Foundation collection into a Python collection constructor:
for example `list(nsarray)` will return a `list`{.interpreted-text
role="class"} of `NSString`s.
