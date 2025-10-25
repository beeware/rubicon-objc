class objc_property_attribute_t:
    """
    The [objc_property_attribute_t](https://developer.apple.com/documentation/objectivec/objc_property_attribute_t?language=objc)
    structure from `<objc/runtime.h>`.
    """
    @property
    def name(self) -> bytes:
        """
        The attribute name as a C string ([`bytes`][]).
        """
        ...
    @property
    def value(self) -> bytes:
        """
        The attribute value as a C string ([`bytes`][]).
        """
        ...

class objc_method_description:
    """
    The [objc_method_description](https://developer.apple.com/documentation/objectivec/objc_method_description?language=objc)
    structure from `<objc/runtime.h>`.
    """
    @property
    def name(self) -> SEL:
        """
        The method name as a [`SEL`][rubicon.objc.runtime.SEL].
        """
        ...
    @property
    def types(self) -> bytes:
        """
        The method's signature encoding as a C string ([`bytes`][]).
        """

class objc_super:
    """The [objc_super](https://developer.apple.com/documentation/objectivec/objc_super?language=objc)
    structure from `<objc/message.h>`.
    pyi content
    """
    @property
    def receiver(self) -> objc_id:
        """
        The receiver of the call, as an [`objc_id`][rubicon.objc.runtime.objc_id].
        """
        ...
    @property
    def super_class(self) -> Class:
        """
        The class in which to start searching for method implementations, as a
        [`Class`][rubicon.objc.runtime.Class].
        """
        ...
