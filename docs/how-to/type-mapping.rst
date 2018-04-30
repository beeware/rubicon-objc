==========================================================
You're just not my type: Using Objective-C types in Python
==========================================================

Objective-C is a strong, static typed language. Every variable has a specific
type, and that type cannot change over time. If a function declares that it
accepts an integer, then it must receive a variable that is declared as an
integer, or an expression that results in an integer.

Python, on the other hand, is strong, but *dynamically* typed language. Every
variable has a specific type, but that type can be modified or interpreted in
other ways. When a function accepts an argument, Python will allow you to pass
*any* variable, of *any* type.

So, if you want to bridge between Objective-C and Python, you need to be able
to provide static typing information so that Python can work out how to convert
a variable of arbitrary type into a specific type matching Objective-C's
expectations.

If you're calling an Objective C method defined in a library, this conversion
is done automatically - the Objective-C runtime contains enough information for
Rubicon to infer the required types. However, if you're defining a new method
(or a method override) in Python, we need to provide that typing information.
To do this, we use Python 3's type annotation. Here's how.

Primitives
----------

If a Python value needs to be passed in as a primitive, Rubicon will wrap the
primitive:

===== =============================================================
Value C primitive
===== ============================================================
bool  8 bit integer (although it can only hold 2 values - 0 and 1)
int   32 bit integer
float double precision floating point
===== ============================================================

If a Python value needs to be passed in as an object, Rubicon will wrap the
primitive in an object:

===== =================
Value Objective C type
===== =================
bool  NSNumber (bool)
int   NSNumber (long)
float NSNumber (double)
===== =================

If you're declaring a method and need to annotate the type of an argument, the
Python type name can be used as the annotation type. You can also use any of
the `ctypes` primitive types. Rubicon also provides type definitions for common
Objective-C typedefs, like `NSInteger`, `CGFloat`, and so on.

Strings
-------

If a method calls for an `NSString` argument, you can provide a Python `str`
for that argument. Rubicon will construct an `NSString` instance from the data
in the `str` provided, and pass that value for the argument.

If a method returns an `NSString`, the return value will be a wrapped
`ObjCStrInstance` type. This type implements a `str`-like interface, wrapped
around the underlying `NSString` data. This means you can treat the return
value as if it were a string - slicing it, concatenating it with other strings,
comparing it, and so on.

Note that `ObjCStrInstance` objects behave slightly differently than Python
`str` objects in some cases. For technical reasons, `ObjCStrInstance` objects
are not hashable, which means they cannot be used as `dict` keys (but they
*can* be used as `NSDictionary` keys). `ObjCStrInstance` also handles Unicode
code points above U+FFFF differently than Python `str`, because the underlying
`NSString` is based on UTF-16.

At the moment `ObjCStrInstance` does not yet support many methods that are
available on `str`. More methods will be implemented in the future, such as
`replace` and `split`. However some methods will likely never be available on
`ObjCStrInstance` as they would be too complex to reimplement, such as `format`
and `encode`. If you need to use a method that `ObjCStrInstance` doesn't
support, you can use `str(nsstring)` to convert it to `str`.

Lists
-----

If a method calls for an `NSArray` or `NSMutableArray` argument, you can
provide a Python `list` for that argument. Rubicon will construct an
`NSMutableArray` instance from the data in the `list` provided, and pass that
value for the argument.

If a method returns an `NSArray` or `NSMutableArray`, the return value will be
a wrapped `ObjCListInstance` type. This type implements a `list`-like
interface, wrapped around the underlying `NSArray` data. This means you can
treat the return value as if it were a list - iterating over values, retrieving
objects by index, and so on.

Dictionaries
------------

If a method calls for an `NSDictionary` or `NSMutableDictionary` argument, you
can provide a Python `dict`. Rubicon will construct an `NSMutableDictionary`
instance from the data in the `dict` provided, and pass that value for the
argument.

If a method returns an `NSDictionary` or `NSMutableDictionary`, the return
value will be a wrapped `ObjCDictInstance` type. This type implements a
`dict`-like interface, wrapped around the underlying `NSDictionary` data. This
means you can treat the return value as if it were a dict - iterating over
keys, values or items, retrieving objects by key, and so on.


`NSPoint`, `NSSize`, and `NSRect`
---------------------------------

On instances of an Objective C structure, each field is exposed as a Python
attribute. For example, if you create an instance of an `NSSize` object you can
access its width and height by calling `NSSize.width`.

When you need to pass an Objective C structure to an Objective C method,
you can pass a tuple instead. For example, if you pass (10.0, 5.1) where a
`NSSize` is expected, it will be converted automatically in the appropriate
width, height for the structure.
