=======================
You're just not my type
=======================

We've already seen some of examples of places where Objective-C requires you to provide extra information about the type of arguments. Lets look at this a bit more.

Primitives
----------


bool    8 bit integer
int     64 bit integer
float   double precision floating point

If a primitive needs to be passed in as an object, Rubicon will wrap the primitive in an object.

bool    NSNumber (bool)
int     NSNumber (long)
float   NSNumber (double)

Lists
-----

If a method calls for an `NSArray` or `NSMutableArray` argument, you can provide a Python `list` for that argument. Rubicon will construct an `NSMutableArray` instance from the data in the `list` provided, and pass that value for the argument.

If a method returns an `NSArray` or `NSMutableArray`, the return value will be a wrapped `ObjCListInstance` type. This type implements a `list`-like interface, wrapped around the underlying `NSDictionary` data. This means you can treat the return value as if it were a list - iterating over values, retrieving objects by index, and so on.

Dictionaries
------------

If a method calls for an `NSDictionary` or `NSMutableDictionary` argument, you can provide a Python `dict`. Rubicon will construct an `NSMutableDictionary` instance from the data in the `list` provided, and pass that value for the argument.

If a method returns an `NSDictionary` or `NSMutableDictionary`, the return value will be a wrapped `ObjCDictInstance` type. This type implements a `dict`-like interface, wrapped around the underlying `NSDictionary` data. This means you can treat the return value as if it were a dict - iterating over keys, values or items, retrieving objects by key, and so on.

`NSPoint`, `NSSize`, and `NSRect`
---------------------------------

