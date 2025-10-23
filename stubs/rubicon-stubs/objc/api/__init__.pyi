class NSObject:
    """
    The
    [NSObject](https://developer.apple.com/documentation/objectivec/nsobject?language
    =objc)
    class from `<objc/NSObject.h>`.

    See the [`ObjCInstance`][rubicon.objc.api.ObjCInstance]
    documentation for a list of operations that Rubicon supports on all objects.
    """
    def debugDescription(self) -> str:
        """
        Exposes the Objective-C
        [`debugDescription`](https://developer.apple.com/documentation/objectivec/nsobjectprotocol/debugdescription?language=objc)
        property.
        """
        ...
    def description(self):
        """Exposes the Objective-C
        [`description`](https://developer.apple.com/documentation/objectivec/nsobjectprotocol/description?language=objc)
        property.
        """
        ...

class NSNumber:
    """
    The
    [NSNumber](https://developer.apple.com/documentation/foundation/nsnumber?language=objc)
    class from `<Foundation/NSValue.h>`.

    This class can be converted to and from standard Python primitives
    (`bool`, `int`, `float`) using [`py_from_ns`][rubicon.objc.py_from_ns] and
    [`ns_from_py`][rubicon.objc.ns_from_py].
    """

    ...

class NSDecimalNumber:
    """
    The
    [NSDecimalNumber](https://developer.apple.com/documentation/foundation/nsdecimalnumber?language=objc)
    class from `<Foundation/NSDecimalNumber.h>`.

    This class can be converted to and from Python `decimal.Decimal` using
    [`py_from_ns`][rubicon.objc.py_from_ns] and
    [`ns_from_py`][rubicon.objc.ns_from_py].
    """

    ...

class NSString:
    """
    The
    [NSString](https://developer.apple.com/documentation/foundation/nsstring?language=objc)
    class from `<Foundation/NSString.h>`.

    This class also supports all methods that [`str`][] does.

    This class can be converted to and from Python [`str`][] using
    [`py_from_ns`][rubicon.objc.py_from_ns] and
    [`ns_from_py`][rubicon.objc.ns_from_py]. You can also call
    `str(nsstring)` to convert a `NSString` to [`str`][].

    [`NSString`][rubicon.objc.api.NSString] objects consist of UTF-16
    code units, unlike [`str`][], which consists
    of Unicode code points. All [`NSString`][rubicon.objc.api.NSString]
    indices and iteration are based on UTF-16, even when using the
    Python-style operations/methods. If indexing or iteration based on code
    points is required, convert the [`NSString`][rubicon.objc.api.NSString] to
    [`str`][] first.
    """
    def __str__(self):
        """
        Return the value of this [`NSString`][rubicon.objc.api.NSString] as a
        [`str`][].
        """
        ...
    def UTF8String(self):
        """
        This Objective-C property has been declared using
        [`ObjCClass.declare_property()`][rubicon.objc.api.ObjCClass.declare_property]
        and can always be accessed using attribute syntax.
        """
        ...

class NSData:
    """
    The
    [NSData](https://developer.apple.com/documentation/foundation/nsdata?language=objc)
    class from `<Foundation/NSData.h>`.

    This class can be converted to and from Python [`bytes`][] using
    [`py_from_ns`][rubicon.objc.py_from_ns] and
    [`ns_from_py`][rubicon.objc.ns_from_py].
    """

    ...

class NSArray:
    """
    The
    [NSArray](https://developer.apple.com/documentation/foundation/nsarray?language=objc)
    class from `<Foundation/NSArray.h>`.

    This class can be converted to and from Python [`list`][] using
    [`py_from_ns`][rubicon.objc.py_from_ns] and
    [`ns_from_py`][rubicon.objc.ns_from_py].

    `py_from_ns(nsarray)` will recursively convert `nsarray`'s elements to
    Python objects, where possible. To avoid this recursive conversion, use
    `list(nsarray)` instead.

    `ns_from_py(pylist)` will recursively convert `pylist`'s elements to
    Objective-C. As there is no way to store Python object references as
    Objective-C objects yet, this recursive conversion cannot be avoided. If
    any of `pylist`'s elements cannot be converted to Objective-C, an error
    is raised.

    Supports
    [Python-style sequence operations](https://docs.python.org/3/library/stdtypes.html#typesseq)
    including: `__getitem__()`, `__len__()`, `__iter__()`, `__contains__()`, `__eq__()`,
    `__ne__()`, `index()`, `count()`, and `copy()`.
    """

    ...

class NSMutableArray:
    """
    The
    [NSMutableArray](https://developer.apple.com/documentation/foundation/nsmutablearray?language=objc)
    class from `<Foundation/NSArray.h>`.

    This class can be converted to and from Python exactly like its
    superclass `NSArray`.

    Supports
    [Python-style mutable sequence operations](https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types)
    including: `__setitem__()`, `__delitem__()`, `append()`, `clear()`, `extend()`,
    `insert()`, `pop()`, `remove()`, and `reverse()`.
    """

    ...

class NSDictionary:
    """
    The
    [NSDictionary](https://developer.apple.com/documentation/foundation/nsdictionary?language=objc)
    class from `<Foundation/NSDictionary.h>`.

    This class can be converted to and from Python [`dict`][] using
    [`py_from_ns`][rubicon.objc.py_from_ns] and
    [`ns_from_py`][rubicon.objc.ns_from_py].

    `py_from_ns(nsdict)` will recursively convert `nsdict`'s keys and values
    to Python objects, where possible. To avoid the recursive conversion of
    the values, use `{py_from_ns(k): v for k, v in nsdict.items()}`. The
    conversion of the keys cannot be avoided, because Python
    [`dict`][] keys need to be hashable, which
    [`ObjCInstance`][rubicon.objc.api.ObjCInstance] is not. If any of the
    keys convert to a Python object that is not hashable, an error is raised
    (regardless of which conversion method you use).

    `ns_from_py(pydict)` will recursively convert `pydict`'s keys and values
    to Objective-C. As there is no way to store Python object references as
    Objective-C objects yet, this recursive conversion cannot be avoided. If
    any of `pydict`'s keys or values cannot be converted to Objective-C, an
    error is raised.

    Supports
    [Python-style mapping operations](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
    including `__getitem__()`, `__len__()`, `__iter__()`, `__contains__()`, `__eq__()`,
     `__ne__()`, `copy()`, `get()`, `keys()`, `items()`, and `values()`.

    Unlike most Python mappings, [`NSDictionary`][rubicon.objc.api.NSDictionary]'s
    [`keys`](https://docs.python.org/3/library/stdtypes.html#dict.keys),
    [`values`](https://docs.python.org/3/library/stdtypes.html#dict.values), and
    [`items`](https://docs.python.org/3/library/stdtypes.html#dict.items)
    methods don't return dynamic views of the dictionary's
    keys, values, and items.

    [`keys`](https://docs.python.org/3/library/stdtypes.html#dict.keys) and
    [`values`](https://docs.python.org/3/library/stdtypes.html#dict.values) return
    lists that are created each time the methods are
    called, which can have an effect on performance and memory usage for
    large dictionaries. To avoid this, you can cache the return values of
    [`keys`](https://docs.python.org/3/library/stdtypes.html#dict.keys) and
    [`values`](https://docs.python.org/3/library/stdtypes.html#dict.values), or convert
    the [`NSDictionary`][rubicon.objc.api.NSDictionary] to a Python [`dict`][]
    beforehand.

    [`items`](https://docs.python.org/3/library/stdtypes.html#dict.items) is currently
    implemented as a generator, meaning that it returns a single-use iterator. If you
    need to iterate over
    [`items`](https://docs.python.org/3/library/stdtypes.html#dict.items) more than
    once or perform other operations on it, you should convert it to a Python
    [`set`][] or [`list`][] first.
    """

    ...

class NSMutableDictionary:
    """
    The
    [NSMutableDictionary](https://developer.apple.com/documentation/foundation/nsmutabledictionary?language=objc)
    class from `<Foundation/NSDictionary.h>`.

    This class can be converted to and from Python exactly like its
    superclass `NSDictionary`.

    Supports
    [Python-style mutable mapping operations](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
    including `setitem()`, `delitem()`, `clear()`, `pop()`, `popitem()`, `setdefault()`,
    and `update()`.
    """

    ...

class Protocol:
    """
    The
    [Protocol](https://developer.apple.com/documentation/objectivec/protocol?language=objc)
    class from `<objc/Protocol.h>`.

    This class has no (non-deprecated) Objective-C methods; protocol objects
    can only be manipulated using Objective-C runtime functions. Rubicon
    automatically wraps all [`Protocol`][rubicon.objc.api.Protocol]
    objects using [`ObjCProtocol`][rubicon.objc.api.ObjCProtocol], which
    provides an easier interface for working with protocols.
    """

    ...

class NSObjectProtocol:
    """
    The
    [NSObject](https://developer.apple.com/documentation/objectivec/1418956-nsobject?language=objc)
    protocol from `<objc/NSObject.h>`. The protocol is exported as
    [`NSObjectProtocol`][rubicon.objc.NSObjectProtocol] in Python because it
    would otherwise clash with the [`NSObject`][rubicon.objc.NSObject] class.
    """

    ...

def at(pyobj):
    """Alias for [`ns_from_py`][rubicon.objc.ns_from_py]."""
