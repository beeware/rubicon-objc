# Release History

## 0.5.2 (2025-08-07)

### Bugfixes

- The name of the deprecated `AbstractEventLoopPolicy` symbol has been
  corrected to reflect the restoration of the original name in
  3.14.0rc1. (#619)

### Documentation

- The structure of Rubicon's documentation now matches other BeeWare
  projects. (#604)
- The Rubicon docs now use the BeeWare theme. (#621)

### Misc

- #599, #600, #601, #602, #603, #605, #606, #607, #608, #611,
  #612, #613, #615, #616, #617, #618, #623, #624, #626, #627

## 0.5.1 (2025-06-03)

### Features

- `RubiconEventLoop()` is now exposed as an interface for creating a
  CoreFoundation compatible event loop. (#557)

### Bugfixes

- The interface with EventLoopPolicy was updated to account for the
  eventual deprecation of that API in Python. (#557)

### Backward Incompatible Changes

- Python 3.14 deprecated the use of custom event loop policies, in favor
  of directly instantiating event loops. Instead of calling
  `asyncio.new_event_loop()` after installing an instance of
  `rubicon.objc.eventloop.EventLoopPolicy`, you can call
  `RubiconEventLoop()` to instantiate an instance of an event loop and
  use that instance directly. This approach can be used on all versions
  of Python; on Python 3.13 and earlier, `RubiconEventLoop()` is a shim
  that performs the older event loop policy-based instantiation. (#557)

### Misc

- #551, #552, #554, #555, #556, #559, #560, #561, #562, #564,
  #565, #566, #567, #568, #569, #570, #571, #572, #573, #574,
  #575, #576, #577, #578, #579, #580, #581, #582, #583, #584,
  #585, #586, #587, #588, #589, #590, #591, #592, #593, #594,
  #595, #596, #597

## 0.5.0 (2025-01-07)

### Features

- Retain Objective-C objects when creating Python wrappers and release
  them when the Python wrapped is garbage collected. This means that
  manual `retain` calls and subsequent `release` or `autorelease` calls
  from Python are no longer needed with very few exceptions, for example
  when writing implementations of `copy` that return an existing object.
  (#256)
- Support for Python 3.14 was added. (#529)

### Bugfixes

- Protection was added against a potential race condition when loading
  methods defined on a superclass. (#473)
- A workaround for
  [python/cpython#81061](https://github.com/python/cpython/issues/81061)
  is now conditionally applied only for the Python versions that require
  it (Python 3.9 and earlier). (#517)

### Backward Incompatible Changes

- Manual calls to `release` or `autorelease` no longer cause Rubicon to
  skip releasing an Objective-C object when its Python wrapper is
  garbage collected. This means that fewer `retain` than `release` calls
  will cause segfaults on garbage collection. Review your code carefully
  for unbalanced `retain` and `release` calls before updating. (#256)
- Python 3.8 is no longer a supported platform. (#529)

### Documentation

- Building Rubicon ObjC's documentation now requires the use of Python
  3.12. (#496)

### Misc

- #464, #466, #467, #469, #470, #472, #473, #474, #475, #476,
  #477, #478, #479, #480, #481, #482, #483, #484, #485, #486,
  #487, #488, #489, #490, #491, #492, #493, #494, #499, #500,
  #502, #503, #505, #506, #507, #508, #509, #510, #511, #512,
  #513, #514, #515, #516, #518, #519, #520, #521, #522, #523,
  #524, #525, #526, #527, #528, #530, #531, #532, #533, #534,
  #535, #536, #537, #538, #541, #544, #546, #548, #549, #550

## 0.4.9 (2024-05-03)

### Features

- Objective-C methods with repeated argument names can now be called by
  using a `__` suffix in the Python keyword argument to provide a unique
  name. (#148)
- The error message has been improved when an Objective-C selector
  matching the provided arguments cannot be found. (#461)

### Bugfixes

- The handling of structure and union return types was updated to be
  compatible with changes to ctypes introduced in Python 3.13.0a6.
  (#444)

### Backward Incompatible Changes

- The order of keyword arguments used when invoking methods must now
  match the order they are defined in the Objective-C API. Previously
  arguments could be in any order. (#453)

### Documentation

- The README badges were updated to display correctly on GitHub. (#463)

### Misc

- #440, #441, #442, #443, #447, #448, #449, #450, #452, #454,
  #455, #456, #457, #458, #459, #460

## 0.4.8 (2024-04-03)

### Features

- Name clashes caused by re-registering Objective-C classes and
  protocols can now be automatically avoided by marking the class with
  `auto_rename`. (#181)
- Apple Silicon is now formally tested by Rubicon's continuous
  integration configuration. (#374)
- Support for Python 3.13 was added. (#374)
- The `__repr__` output for `ObjCBoundMethod`, `ObjCClass`,
  `ObjCInstance`, `ObjCMethod`, `ObjCPartialMethod`, and `ObjCProtocol`
  were simplified. (#432)

### Bugfixes

- The `__all__` definition for `rubicon.objc` was corrected to use
  strings, rather than symbols. (#401)

### Documentation

- The documentation contribution guide was updated to use a more
  authoritative reStructuredText reference. (#427)

### Misc

- #381, #382, #383, #384, #385, #386, #387, #388, #389, #390,
  #391, #392, #393, #395, #396, #397, #398, #399, #400, #402,
  #403, #404, #405, #407, #408, #409, #410, #411, #412, #413,
  #414, #415, #416, #417, #418, #420, #421, #422, #423, #424,
  #425, #426, #429, #430, #431, #433, #434, #435, #437, #438

## 0.4.7 (2023-10-19)

### Features

- The `__repr__` and `__str__` implementations for `NSPoint`, `CGPoint`,
  `NSRect`, `CGRect`, `NSSize`, `CGSize`, `NSRange`, `CFRange`,
  `NSEdgeInsets` and `UIEdgeInsets` have been improved.
  ([#222](https://github.com/beeware/rubicon-objc/pulls/222))
- `objc_id` and `objc_block` are now exposed as part of the
  `rubicon.objc` namespace, rather than requiring an import from
  `rubicon.objc.runtime`.
  ([#357](https://github.com/beeware/rubicon-objc/pulls/357))

### Bugfixes

- References to blocks obtained from an Objective-C API can now be
  invoked on M1 hardware.
  ([#225](https://github.com/beeware/rubicon-objc/issues/225))
- Rubicon is now compatible with PEP563 deferred annotations
  (`from __future__ import annotations`).
  ([#308](https://github.com/beeware/rubicon-objc/issues/308))
- iOS now uses a full `NSRunLoop`, rather than a `CFRunLoop`.
  ([#317](https://github.com/beeware/rubicon-objc/issues/317))

### Backward Incompatible Changes

- Support for Python 3.7 was dropped.
  ([#334](https://github.com/beeware/rubicon-objc/pulls/334))

### Documentation

- All code blocks were updated to add a button to copy the relevant
  contents on to the user's clipboard.
  ([#300](https://github.com/beeware/rubicon-objc/pull/300))

### Misc

- #295, #296, #297, #298, #299, #301, #302, #303, #305, #306,
  #307, #310, #311, #312, #314, #315, #319, #320, #321, #326,
  #327, #328, #329, #330, #331, #332, #335, #336, #337, #338,
  #341, #342, #343, #344, #345, #346, #348, #349, #350, #351,
  #353, #354, #355, #356, #358, #359, #360, #361, #362, #363,
  #364, #365, #366, #367, #368, #369, #370, #371, #372, #373,
  #375, #376, #377, #378, #379, #380

## 0.4.6 (2023-04-14)

### Bugfixes

- The error message returned when a selector has the wrong type has been
  improved.
  ([#271](https://github.com/beeware/rubicon-objc/issues/271))
- Rubicon now uses an implicit namespace package, instead of relying on
  the deprecated `pkg_resources` API.
  ([#292](https://github.com/beeware/rubicon-objc/issues/292))

### Misc

- #267, #268, #269, #270, #273, #274, #275, #276, #277, #278,
  #279, #280, #281, #282, #283, #284, #285, #286, #287, #288,
  #289, #290, #291, #294

## 0.4.5 (2023-02-03)

### Bugfixes

- Classes that undergo a class name change between `alloc()` and
  `init()` (e.g., `NSWindow` becomes `NSKVONotifying_Window`) no longer
  trigger instance cache eviction logic.
  ([#258](https://github.com/beeware/rubicon-objc/pull/258))

### Misc

- #259, #260, #262, #263, #264, #265, #266

## 0.4.5rc1 (2023-01-25) { #rc1-2023-01-25 }

### Features

- Support for Python 3.6 was dropped.
  ([#255](https://github.com/beeware/rubicon-objc/pull/255))

### Misc

- #254

## 0.4.4 (2023-01-23)

This version was yanked from PyPI because of an incompatibility with
Toga-iOS 0.3.0dev39, which was the published Toga release at the time.

### Bugfixes

- Background threads will no longer lock up on iOS when an asyncio event
  loop is in use.
  ([#228](https://github.com/beeware/rubicon-objc/issues/228))
- The `ObjCInstance` cache no longer returns a stale wrapper objects if
  a memory address is reused by the Objective-C runtime.
  ([#249](https://github.com/beeware/rubicon-objc/issues/249))
- It is now safe to open an asyncio event loop on a secondary thread.
  Previously this would work, but would intermittently fail with a
  segfault when then loop was closed.
  ([#250](https://github.com/beeware/rubicon-objc/issues/250))
- A potential race condition that would lead to duplicated creation on
  `ObjCInstance` wrapper objects has been resolved.
  ([#251](https://github.com/beeware/rubicon-objc/issues/251))
- A race condition associated with populating the `ObjCClass`
  method/property cache has been resolved.
  ([#252](https://github.com/beeware/rubicon-objc/issues/252))

### Misc

- #225, #237, #240, #241, #242, #243, #244, #245, #247, #248,
  #253

## 0.4.3 (2022-12-05)

### Features

- Support for Python 3.11 has been added.
  ([#224](https://github.com/beeware/rubicon-objc/pull/224))
- Support for Python 3.12 has been added.
  ([#231](https://github.com/beeware/rubicon-objc/pull/231))

### Bugfixes

- Enforce usage of <span class="title-ref">argtypes</span> when calling
  <span class="title-ref">send_super</span>.
  ([#220](https://github.com/beeware/rubicon-objc/pull/220))
- The check identifying the architecture on which Rubicon is running has
  been corrected for x86_64 simulators using a recent
  Python-Apple-support releases.
  ([#235](https://github.com/beeware/rubicon-objc/issues/235))

### Misc

- #227, #228, #229, #232, #233, #234

### 0.4.2 (2021-11-14)

#### Features

- Added `autoreleasepool` context manager to mimic Objective-C
  `@autoreleasepool` blocks.
  ([#213](https://github.com/beeware/rubicon-objc/pull/213))
- Allow storing Python objects in Objective-C properties declared with
  `@objc_property`.
  ([#214](https://github.com/beeware/rubicon-objc/pull/214))
- Added support for Python 3.10.
  ([#218](https://github.com/beeware/rubicon-objc/pull/218))

#### Bugfixes

- Raise `TypeError` when trying to declare a weak property of a
  non-object type.
  ([#215](https://github.com/beeware/rubicon-objc/pull/215))
- Corrected handling of methods when a class overrides a method defined
  in a grandparent.
  ([#216](https://github.com/beeware/rubicon-objc/issues/216))

### 0.4.1 (2021-07-25)

#### Features

- Added official support for Python 3.9.
  ([#193](https://github.com/beeware/rubicon-objc/pull/193))
- Added official support for macOS 11 (Big Sur).
  ([#195](https://github.com/beeware/rubicon-objc/pull/195))
- Autorelease Objective-C instances when the corresponding Python
  instance is destroyed.
  ([#200](https://github.com/beeware/rubicon-objc/issues/200))
- Improved memory management when a Python instance is assigned to a new
  `ObjCInstance` attribute.
  ([#209](https://github.com/beeware/rubicon-objc/pull/209))
- Added support to declare weak properties on custom Objective-C
  classes. ([#210](https://github.com/beeware/rubicon-objc/issues/210))

#### Bugfixes

- Fixed incorrect behavior of
  `~rubicon.objc.api.Block`{.interpreted-text role="class"} when trying
  to create a block with no arguments and using explicit types. This
  previously caused an incorrect exception about missing argument types;
  now a `no-arg` block is created as expected.
  ([#153](https://github.com/beeware/rubicon-objc/issues/153))
- Fixed handling of type annotations when passing a bound Python method
  into `~rubicon.objc.api.Block`{.interpreted-text role="class"}.
  ([#153](https://github.com/beeware/rubicon-objc/issues/153))
- A cooperative entry point for starting event loop has been added. This
  corrects a problem seen when using Python 3.8 on iOS.
  ([#182](https://github.com/beeware/rubicon-objc/pull/182))
- Improved performance of Objective-C method calls and
  [`ObjCInstance`][rubicon.objc.api.ObjCInstance]
  creation in many cases.
  ([#183](https://github.com/beeware/rubicon-objc/issues/183))
- Fix calling of signal handlers added to the asyncio loop with
  `CFRunLoop` integration.
  ([#202](https://github.com/beeware/rubicon-objc/issues/202))
- Allow restarting a stopped event loop.
  ([#205](https://github.com/beeware/rubicon-objc/pull/205))

#### Deprecations and Removals

- Removed automatic conversion of Objective-C numbers (`NSNumber` and
  `NSDecimalNumber`) to Python numbers when received from Objective-C
  (i.e. returned from an Objective-C method or property or passed into
  an Objective-C method implemented in Python). This automatic
  conversion significantly slowed down every Objective-C method call
  that returns an object, even though the conversion doesn't apply to
  most method calls. If you have code that receives an Objective-C
  number and needs to use it as a Python number, please convert it
  explicitly using `~rubicon.objc.api.py_from_ns`{.interpreted-text
  role="func"} or an appropriate Objective-C method.

  As a side effect, `NSNumber` and `NSDecimalNumber` values stored in
  Objective-C collections (`NSArray`, `NSDictionary`) are also no longer
  automatically unwrapped when retrieved from the collection, even when
  using Python syntax to access the collection. For example, if `arr` is
  a `NSArray` of integer `NSNumber`, `arr[0]` now returns an Objective-C
  `NSNumber` and not a Python `int` as before. If you need the contents
  of an Objective-C collection as Python values, you can use
  `~rubicon.objc.api.py_from_ns`{.interpreted-text role="func"} to
  convert either single values (e. g. `py_from_ns(arr[0])`) or the
  entire collection (e. g. `py_from_ns(arr)`).
  ([#183](https://github.com/beeware/rubicon-objc/issues/183))

- Removed macOS 10.12 through 10.14 from our automatic test matrix, due
  to pricing changes in one of our CI services (Travis CI). OS X 10.11
  is still included in the test matrix for now, but will probably be
  removed relatively soon. Automatic tests on macOS 10.15 and 11.0 are
  unaffected as they run on a different CI service (GitHub Actions).

  Rubicon will continue to support macOS 10.14 and earlier on a
  best-effort basis, even though compatibility is no longer tested
  automatically. If you encounter any bugs or other problems with
  Rubicon on these older macOS versions, please report them!
  ([#197](https://github.com/beeware/rubicon-objc/issues/197))

#### Misc

- #185, #189, #194, #196, #208

### 0.4.0 (2020-07-04)

#### Features

- Added macOS 10.15 (Catalina) to the test matrix.
  ([#145](https://github.com/beeware/rubicon-objc/pull/145))
- Added `517`{.interpreted-text role="pep"} and `518`{.interpreted-text
  role="pep"} build system metadata to `pyproject.toml`.
  ([#156](https://github.com/beeware/rubicon-objc/pull/156))
- Added official support for Python 3.8.
  ([#162](https://github.com/beeware/rubicon-objc/pull/162))
- Added a `varargs` keyword argument to
  `~rubicon.objc.runtime.send_message`{.interpreted-text role="func"} to
  allow calling variadic methods more safely.
  ([#174](https://github.com/beeware/rubicon-objc/pull/174))
- Changed `ObjCMethod` to call methods using
  `~rubicon.objc.runtime.send_message`{.interpreted-text role="func"}
  instead of calling `~rubicon.objc.runtime.IMP`{.interpreted-text
  role="class"}s directly. This is mainly an internal change and should
  not affect most existing code, although it may improve compatibility
  with Objective-C code that makes heavy use of runtime reflection and
  method manipulation (such as swizzling).
  ([#177](https://github.com/beeware/rubicon-objc/pull/177))

#### Bugfixes

- Fixed Objective-C method calls in "flat" syntax accepting more
  arguments than the method has. The extra arguments were previously
  silently ignored. An exception is now raised if too many arguments are
  passed. ([#123](https://github.com/beeware/rubicon-objc/issues/123))
- Fixed
  `ObjCInstance.__str__ <rubicon.objc.api.ObjCInstance.__str__>`{.interpreted-text
  role="func"} throwing an exception if the object's Objective-C
  `description` is `nil`.
  ([#125](https://github.com/beeware/rubicon-objc/issues/125))
- Corrected a slow memory leak caused every time an asyncio timed event
  handler triggered.
  ([#146](https://github.com/beeware/rubicon-objc/issues/146))
- Fixed various minor issues in the build and packaging metadata.
  ([#156](https://github.com/beeware/rubicon-objc/pull/156))
- Removed unit test that attempted to pass a struct with bit fields into
  a C function by value. Although this has worked in the past on x86 and
  x86_64, [`ctypes`][] never officially
  supported this, and started generating an error in Python 3.7.6 and
  3.8.1 (see [bpo-39295](https://bugs.python.org/issue39295)).
  ([#157](https://github.com/beeware/rubicon-objc/pull/157))
- Corrected the invocation of `NSApplication.terminate()` when the
  `~rubicon.objc.eventloop.CocoaLifecycle`{.interpreted-text
  role="class"} is ended.
  ([#170](https://github.com/beeware/rubicon-objc/issues/170))
- Fixed `~rubicon.objc.runtime.send_message`{.interpreted-text
  role="func"} not accepting
  [`SEL`][rubicon.objc.runtime.SEL] objects
  for the `selector` parameter. The documentation stated that this is
  allowed, but actually doing so caused a type error.
  ([#177](https://github.com/beeware/rubicon-objc/pull/177))

#### Improved Documentation

- Added detailed
  `reference documentation </reference/index>`{.interpreted-text
  role="doc"} for all public APIs of [`rubicon.objc`][rubicon-objc-module].
  ([#118](https://github.com/beeware/rubicon-objc/pull/118))
- Added a `topic guide for calling regular C functions
  </topics/c-functions>`{.interpreted-text role="doc"} using
  [`ctypes`][] and
  [`rubicon.objc`][rubicon-objc-module].
  ([#147](https://github.com/beeware/rubicon-objc/pull/147))

#### Deprecations and Removals

- Removed the i386 architecture from the test matrix. It is still
  supported on a best-effort basis, but compatibility is not tested
  automatically.
  ([#139](https://github.com/beeware/rubicon-objc/pull/139))

- Tightened the API of
  `~rubicon.objc.runtime.send_message`{.interpreted-text role="func"},
  removing some previously allowed shortcuts and features that were
  rarely used, or likely to be used by accident in an unsafe way.

  /// note | Note

  In most cases, Rubicon's high-level method call syntax provided by
  [`ObjCInstance`][rubicon.objc.api.ObjCInstance] can
  be used instead of
  `~rubicon.objc.runtime.send_message`{.interpreted-text role="func"}.
  This syntax is almost always more convenient to use, more readable and
  less error-prone.
  `~rubicon.objc.runtime.send_message`{.interpreted-text role="func"}
  should only be used in cases not supported by the high-level syntax.

  ///

- Disallowed passing class names as `str`{.interpreted-text
  role="class"}/[`bytes`][] as the
  `receiver` argument of
  `~rubicon.objc.runtime.send_message`{.interpreted-text role="func"}.
  If you need to send a message to a class object (i. e. call a class
  method), use `~rubicon.objc.api.ObjCClass`{.interpreted-text
  role="class"} or `~rubicon.objc.runtime.get_class`{.interpreted-text
  role="func"} to look up the class, and pass the resulting
  [`ObjCClass`][rubicon.objc.api.ObjCClass] or
  [`Class`][rubicon.objc.runtime.Class] object
  as the receiver.

- Disallowed passing [`c_void_p`][ctypes.c_void_p]
  objects as the `receiver` argument of
  `~rubicon.objc.runtime.send_message`{.interpreted-text role="func"}.
  The `receiver` argument now has to be of type
  [`objc_id`][rubicon.objc.runtime.objc_id], or
  one of its subclasses (such as
  [`Class`][rubicon.objc.runtime.Class]), or one
  of its high-level equivalents (such as
  [`ObjCInstance`][rubicon.objc.api.ObjCInstance]). All
  Objective-C objects returned by Rubicon's high-level and low-level
  APIs have one of these types. If you need to send a message to an
  object pointer stored as `~ctypes.c_void_p`{.interpreted-text
  role="class"}, `~ctypes.cast`{.interpreted-text role="func"} it to
  [`objc_id`][rubicon.objc.runtime.objc_id] first.

- Removed default values for
  `~rubicon.objc.runtime.send_message`{.interpreted-text role="func"}'s
  `restype` and `argtypes` keyword arguments. Every
  `~rubicon.objc.runtime.send_message`{.interpreted-text role="func"}
  call now needs to have its return and argument types set explicitly.
  This ensures that all arguments and the return value are converted
  correctly between (Objective-)C and Python.

- Disallowed passing more argument values than there are argument types
  in `argtypes`. This was previously allowed to support calling variadic
  methods

  \- any arguments beyond the types set in `argtypes` would be passed as
  `varargs`. However, this feature was easy to misuse by accident, as it
  allowed passing extra arguments to *any* method, even though most
  Objective-C methods are not variadic. Extra arguments passed this way
  were silently ignored without causing an error or a crash.

  To prevent accidentally passing too many arguments like this, the
  number of arguments now has to exactly match the number of `argtypes`.
  Variadic methods can still be called, but the `varargs` now need to be
  passed as a list into the separate `varargs` keyword argument.
  ([#174](https://github.com/beeware/rubicon-objc/pull/174))

- Removed the `rubicon.objc.core_foundation` module. This was an
  internal module with few remaining contents and should not have any
  external uses. If you need to call Core Foundation functions in your
  code, please load the framework yourself using
  `load_library('CoreFoundation')` and define the types and functions
  that you need.
  ([#175](https://github.com/beeware/rubicon-objc/pull/175))

- Removed the `ObjCMethod` class from the public API, as there was no
  good way to use it from external code.
  ([#177](https://github.com/beeware/rubicon-objc/pull/177))

#### Misc

- #143, #145, #155, #158, #159, #164, #173, #178, #179

### 0.3.1

- Added a workaround for
  [bpo-36880](https://bugs.python.org/issue36880), which caused a
  "deallocating None" crash when returning structs from methods very
  often.
- Added macOS High Sierra (10.13) and macOS Mojave (10.14) to the test
  matrix.
- Renamed the `rubicon.objc.async` module to `rubicon.objc.eventloop` to
  avoid conflicts with the Python 3.6 `async` keyword.
- Removed support for Python 3.4.
- Removed OS X Yosemite (10.10) from the test matrix. This version is
  (and older ones are) still supported on a best-effort basis, but
  compatibility is not tested automatically.

### 0.3.0

- Added Pythonic operators and methods on `NSString` objects, similar to
  those for `NSArray` and `NSDictionary`.

- Removed automatic conversion of `NSString` objects to `str` when
  returned from Objective-C methods. This feature made it difficult to
  call Objective-C methods on `NSString` objects, because there was no
  easy way to prevent the automatic conversion.

  In most cases, this change will not affect existing code, because
  `NSString` objects now support operations similar to `str`. If an
  actual `str` object is required, the `NSString` object can be wrapped
  in a `str` call to convert it.

- Added support for `objc_property`s with non-object types.

- Added public `get_ivar` and `set_ivar` functions for manipulating
  `ivars`.

- Changed the implementation of `objc_property` to use `ivars` instead
  of Python attributes for storage. This fixes name conflicts in some
  situations.

- Added the `~rubicon.objc.runtime.load_library`{.interpreted-text
  role="func"} function for loading `~ctypes.CDLL`{.interpreted-text
  role="class"}s by their name instead of their full path.

- Split the high-level Rubicon API
  ([`ObjCInstance`][rubicon.objc.api.ObjCInstance],
  [`ObjCClass`][rubicon.objc.api.ObjCClass], etc.)
  out of `rubicon.objc.runtime`{.interpreted-text role="mod"} into a
  separate [`rubicon.objc.api`][rubicon-objc-api] module. The
  `~rubicon.objc.runtime`{.interpreted-text role="mod"} module now only
  contains low-level runtime interfaces like
  `~rubicon.objc.runtime.libobjc`{.interpreted-text role="data"}.

  This is mostly an internal change, existing code will not be affected
  unless it imports names directly from
  `rubicon.objc.runtime`{.interpreted-text role="mod"}.

- Moved `~rubicon.objc.types.c_ptrdiff_t`{.interpreted-text
  role="class"} from `rubicon.objc.runtime`{.interpreted-text
  role="mod"} to `rubicon.objc.types`{.interpreted-text role="mod"}.

- Removed some rarely used names
  (`~rubicon.objc.runtime.IMP`{.interpreted-text role="class"},
  [`Class`][rubicon.objc.runtime.Class],
  `~rubicon.objc.runtime.Ivar`{.interpreted-text role="class"},
  `~rubicon.objc.runtime.Method`{.interpreted-text role="class"},
  `~rubicon.objc.runtime.get_ivar`{.interpreted-text role="func"},
  [`objc_id`][rubicon.objc.runtime.objc_id],
  `~rubicon.objc.runtime.objc_property_t`{.interpreted-text
  role="class"}, `~rubicon.objc.runtime.set_ivar`{.interpreted-text
  role="func"}) from the main [`rubicon.objc`][rubicon-objc-module] namespace.

  If needed, these names can be imported explicitly from the
  `rubicon.objc.runtime`{.interpreted-text role="mod"} module.

- Fixed `objc_property` setters on non-macOS platforms. (cculianu)

- Fixed various bugs in the collection `ObjCInstance` subclasses:

- Fixed getting/setting/deleting items or slices with indices lower than
  `-len(obj)`. Previously this crashed Python, now an `IndexError` is
  raised.

- Fixed slices with step size 0. Previously they were ignored and 1 was
  incorrectly used as the step size, now an `IndexError` is raised.

- Fixed equality checks between Objective-C arrays/dictionaries and
  non-sequence/mapping objects. Previously this incorrectly raised a
  `TypeError`, now it returns `False`.

- Fixed equality checks between Objective-C arrays and sequences of
  different lengths. Previously this incorrectly returned `True` if the
  shorter sequence was a prefix of the longer one, now `False` is
  returned.

- Fixed calling `popitem` on an empty Objective-C dictionary. Previously
  this crashed Python, now a `KeyError` is raised.

- Fixed calling `update` with both a mapping and keyword arguments on an
  Objective-C dictionary. Previously the kwargs were incorrectly ignored
  if a mapping was given, now both are respected.

- Fixed calling methods using `kwarg` syntax if a superclass and
  subclass define methods with the same prefix, but different names. For
  example, if a superclass had a method `initWithFoo:bar:` and the
  subclass `initWithFoo:spam:`, the former could not be called on
  instances of the subclass.

- Fixed the internal `ctypes_patch` module so it no longer depends on a
  non-public CPython function.

### 0.2.10

- Rewrote almost all Core Foundation-based functions to use Foundation
  instead.

  > - The functions `from_value` and `NSDecimalNumber.from_decimal` have
  >   been removed and replaced by `ns_from_py`.
  > - The function `at` is now an alias for `ns_from_py`.
  > - The function `is_str` has been removed. `is_str(obj)` calls should
  >   be replaced with `isinstance(obj, NSString)`.
  > - The functions `to_list`, `to_number`, `to_set`, `to_str`, and
  >   `to_value` have been removed and replaced by `py_from_ns`.

- Fixed `declare_property` not applying to subclasses of the class it
  was called on.

- Fixed `repr` of `ObjCBoundMethod` when the wrapped method is not an
  `ObjCMethod`.

- Fixed the encodings of `NSPoint`, `NSSize`, and `NSRect` on 32-bit
  systems.

- Renamed the `async` support package to `eventloop` to avoid a Python
  3.5+ keyword clash.

### 0.2.9

- Improved handling of Boolean types.
- Added support for using primitives as object values (e.g, as the
  key/value in an `NSDictonary`).
- Added support for passing Python lists as Objective-C `NSArray`
  arguments, and Python dictionaries as Objective-C `NSDictionary`
  arguments.
- Corrected support to storing strings and other objects as properties
  on Python-defined Objective-C classes.
- Added support for creating Objective-C blocks from Python callables.
  (ojii)
- Added support for returning compound values (structures and unions)
  from Objective-C methods defined in Python.
- Added support for creating, extending and conforming to Objective-C
  protocols.
- Added an `objc_const` convenience function to look up global
  Objective-C object constants in a DLL.
- Added support for registering custom `ObjCInstance` subclasses to be
  used to represent Objective-C objects of specific classes.
- Added support for integrating `NSApplication` and `UIApplication`
  event loops with Python's asyncio event loop.

### 0.2.8

- Added support for using native Python sequence/mapping syntax with
  `NSArray` and `NSDictionary`. (jeamland)
- Added support for calling Objective-C blocks in Python. (ojii)
- Added functions for declaring custom conversions between Objective-C
  type encodings and `ctypes` types.
- Added functions for splitting and decoding Objective-C method
  signature encodings.
- Added automatic conversion of Python sequences to C arrays or
  structures in method arguments.
- Extended the Objective-C type encoding decoder to support block types,
  bit fields (in structures), typed object pointers, and arbitrary
  qualifiers. If unknown pointer, array, struct or union types are
  encountered, they are created and registered on the fly.
- Changed the `PyObjectEncoding` to match the real definition of
  `PyObject *`.
- Fixed the declaration of `unichar` (was previously `c_wchar`, is now
  `c_ushort`).
- Removed the `get_selector` function. Use the `SEL` constructor
  instead.
- Removed some runtime function declarations that are deprecated or
  unlikely to be useful.
- Removed the encoding constants. Use `encoding_for_ctype` to get the
  encoding of a type.

### 0.2.7

- (#40) Added the ability to explicitly declare no-attribute methods as
  properties. This is to enable a workaround when Apple introduces
  read-only properties as a way to access these methods.

### 0.2.6

- Added a more compact syntax for calling Objective-C methods, using
  Python keyword arguments. (The old syntax is still fully supported and
  will *not* be removed; certain method names even require the old
  syntax.)
- Added a `superclass` property to `ObjCClass`.

### 0.2.5

- Added official support for Python 3.6.
- Added keyword arguments to disable argument and/or return value
  conversion when calling an Objective-C method.
- Added support for (`NS`/`UI`) `EdgeInsets` structs. (Longhanks)
- Improved `str` of Objective-C classes and objects to return the
  `debugDescription`, or for `NSString`s, the string value.
- Changed `ObjCClass` to extend `ObjCInstance` (in addition to `type`),
  and added an `ObjCMetaClass` class to represent metaclasses.
- Fixed some issues on non-x86_64 architectures (i386, ARM32, ARM64).
- Fixed example code in README. (Dayof)
- Removed the last of the Python 2 compatibility code.

### 0.2.4

- Added `objc_property` function for adding properties to custom
  Objective-C subclasses. (Longhanks)

### 0.2.3

- Removed most Python 2 compatibility code.

### 0.2.2

- Dropped support for Python 3.3.
- Added conversion of Python `enum.Enum` objects to their underlying
  values when passed to an Objective-C method.
- Added syntax highlighting to example code in README. (stsievert)
- Fixed the `setup.py` shebang line. (uranusjr)

### 0.2.1

- Fixed setting of `ObjCClass`/`ObjCInstance` attributes that are not
  Objective-C properties.

### 0.2.0

- First beta release.
- Dropped support for Python 2. Python 3 is now required, the minimum
  tested version is Python 3.3.
- Added error detection when attempting to create an Objective-C class
  with a name that is already in use.
- Added automatic conversion between Python `decimal.Decimal` and
  Objective-C `NSDecimal` in method arguments and return values.
- Added PyPy to the list of test platforms.
- When subclassing Objective-C classes, the return and argument types of
  methods are now specified using Python type annotation syntax and
  `ctypes` types.
- Improved property support.

### 0.1.3

- Fixed some issues on ARM64 (iOS 64-bit).

### 0.1.2

- Fixed `NSString` conversion in a few situations.
- Fixed some issues on iOS and 32-bit platforms.

### 0.1.1

- Objective-C classes can now be subclassed using Python class syntax,
  by using an `ObjCClass` as the superclass.
- Removed `ObjCSubclass`, which is made obsolete by the new subclassing
  syntax.

### 0.1.0

- Initial alpha release.
- Objective-C classes and instances can be accessed via `ObjCClass` and
  `ObjCInstance`.
- Methods can be called on classes and instances with Python method call
  syntax.
- Properties can be read and written with Python attribute syntax.
- Method return and argument types are read automatically from the
  method type encoding.
- A small number of commonly used structs are supported as return and
  argument types.
- Python strings are automatically converted to and from `NSString` when
  passed to or returned from a method.
- Subclasses of Objective-C classes can be created with `ObjCSubclass`.
