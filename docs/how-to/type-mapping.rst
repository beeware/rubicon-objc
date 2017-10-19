==========================================================
You're just not my type: Using Objective-C types in Python
==========================================================

Objective-C is a strong, static typed language. Every variable has a specific type, and that type cannot change over time. If a function declares that it accepts an integer, then it must receive a variable that is declared as an integer, or an expression that results in an integer.

Python, on the other hand, is strong, but *dynamically* typed language. Every variable has a specific type, but that type can be modified or interpreted in other ways. When a function accepts an argument, Python will allow you to pass *any* variable, of *any* type.

So, if you want to bridge between Objective-C and Python, you need to be able to provide static typing information so that Python can work out how to convert a variable of arbitrary type into a specific type matching Objective-C's expectations.

If you're calling an Objective C method defined in a library, this conversion is done automatically - the Objective-C runtime contains enough information for Rubicon to infer the required types. However, if you're defining a new method (or a method override) in Python, we need to provide that typing information. To do this, we use Python 3's type annotation. Here's how.

Primitives
----------

If a Python value needs to be passed in as a primitive, Rubicon will wrap the primitive:

===== =============================================================
Value C primitive
===== ============================================================
bool  8 bit integer (although it can only hold 2 values - 0 and 1)
int   32 bit integer
float double precision floating point
===== ============================================================

If a Python value needs to be passed in as an object, Rubicon will wrap the primitive in an object:

===== =================
Value Objective C type
===== =================
bool  NSNumber (bool)
int   NSNumber (long)
float NSNumber (double)
===== =================

If you're declaring a method and need to annotate the type of an argument, the Python type name can be used as the annotation type. You can also use any of the `ctypes` primitive types. Rubicon also provides type
definitions for common Objective-C typedefs, like `NSInteger`, `CGFloat`, and so on.

Lists
-----

If a method calls for an `NSArray` or `NSMutableArray` argument, you can provide a Python `list` for that argument. Rubicon will construct an `NSMutableArray` instance from the data in the `list` provided, and pass that value for the argument.

If a method returns an `NSArray` or `NSMutableArray`, the return value will be a wrapped `ObjCListInstance` type. This type implements a `list`-like interface, wrapped around the underlying `NSArray` data. This means you can treat the return value as if it were a list - iterating over values, retrieving objects by index, and so on.

Dictionaries
------------

If a method calls for an `NSDictionary` or `NSMutableDictionary` argument, you can provide a Python `dict`. Rubicon will construct an `NSMutableDictionary` instance from the data in the `list` provided, and pass that value for the argument.

If a method returns an `NSDictionary` or `NSMutableDictionary`, the return value will be a wrapped `ObjCDictInstance` type. This type implements a `dict`-like interface, wrapped around the underlying `NSDictionary` data. This means you can treat the return value as if it were a dict - iterating over keys, values or items, retrieving objects by key, and so on.

`NSPoint`, `NSSize`, and `NSRect`
---------------------------------

