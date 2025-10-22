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
        [`ObjCClass.declare_property`][rubicon.objc.api.ObjCClass.declare_property]
        and can always be accessed using attribute syntax.
        """
        ...
