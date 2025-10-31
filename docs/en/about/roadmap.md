# Road map

Rubicon Objective-C is feature complete for most practical purposes.

There are some larger features that would be nice to add, but have not proven to be essential requirements, including:

* Improve the integration between Python and Objective-C initialization methods ([#26](https://github.com/beeware/rubicon-objc/issues/26))
* Simplify the type hierarchy used by ObjCClass ([#70](https://github.com/beeware/rubicon-objc/issues/70))
* Improved exception handling ([#73](https://github.com/beeware/rubicon-objc/issues/73))
* Adding support for GNUStep. ([#176](https://github.com/beeware/rubicon-objc/issues/176))

For other potential enhancements, see the [GitHub issues page](https://github.com/beeware/rubicon-objc/issues?q=is%3Aissue%20state%3Aopen%20label%3Aenhancement)

## Support for Swift

At this point, Objective-C is mostly a language of historical significance. All new APIs that Apple are announcing for macOS and iOS are being released as Swift APIs, rather than Objective-C.

Supporting Swift will likely require the development of an entirely new "Rubicon Swift" project, as the features of the Swift language do not lend them to the type of introspection that Rubicon Objective-C uses. It is likely that something closer to the approach used by [PyBind11](https://pybind11.readthedocs.io) will be required, as the constraints of C++ are somewhat similar to those of Swift. Some initial discussion of this topic can be found on [Issue #563](https://github.com/beeware/rubicon-objc/issues/563).
