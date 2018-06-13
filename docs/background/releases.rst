Release History
===============

(next version)
--------------

* Added Pythonic operators and methods on ``NSString`` objects, similar to those for ``NSArray`` and ``NSDictionary``.
  * Only a small subset of the standard ``str`` methods is supported at the moment. Additional ``str`` methods may be implemented in the future, but some methods (like ``format``) will never be supported, as they cannot be implemented efficiently based on ``NSString``.
* Removed automatic conversion of ``NSString`` objects to ``str`` when returned from Objective-C methods. This feature made it difficult to call Objective-C methods on ``NSString`` objects, because there was no easy way to prevent the automatic conversion.
  * In most cases, this change will not affect existing code, because ``NSString`` objects now support operations similar to ``str``.
  * If an actual ``str`` object is required, the ``NSString`` object can be wrapped in a ``str`` call to convert it.
* Added support for ``objc_property`` with non-object types.
* Added public ``get_ivar`` and ``set_ivar`` functions for manipulating ivars.
* Changed the implementation of ``objc_property`` to use ivars instead of Python attributes for storage. This fixes name conflicts in some situations.
* Fixed ``objc_property`` setters on non-macOS platforms. (cculianu)
* Fixed various bugs in the collection ``ObjCInstance`` subclasses:
  * Fixed getting/setting/deleting items or slices with indices lower than ``-len(obj)``. Previously this crashed Python, now an ``IndexError`` is raised.
  * Fixed slices with step size 0. Previously they were ignored and 1 was incorrectly used as the step size, now an ``IndexError`` is raised.
  * Fixed equality checks between Objective-C arrays/dictionaries and non-sequence/mapping objects. Previously this incorrectly raised a ``TypeError``, now it returns ``False``.
  * Fixed equality checks between Objective-C arrays and sequences of different lengths. Previously this incorrectly returned ``True`` if the shorter sequence was a prefix of the longer one, now ``False`` is returned.
  * Fixed calling ``popitem`` on an empty Objective-C dictionary. Previously this crashed Python, now a ``KeyError`` is raised.
  * Fixed calling ``update`` with both a mapping and keyword arguments on an Objective-C dictionary. Previously the kwargs were incorrectly ignored if a mapping was given, now both are respected.
* Fixed calling methods using kwarg syntax if a superclass and subclass define methods with the same prefix, but different names. For example, if a superclass had a method ``initWithFoo:bar:`` and the subclass ``initWithFoo:spam:``, the former could not be called on instances of the subclass.

0.2.10
------

* Rewrote almost all Core Foundation-based functions to use Foundation instead.
  * The functions ``from_value`` and ``NSDecimalNumber.from_decimal`` have been removed and replaced by ``ns_from_py``.
  * The function ``at`` is now an alias for ``ns_from_py``.
  * The function ``is_str`` has been removed. ``is_str(obj)`` calls should be replaced with ``isinstance(obj, NSString)``.
  * The functions ``to_list``, ``to_number``, ``to_set``, ``to_str``, and ``to_value`` have been removed and replaced by ``py_from_ns``.
* Fixed ``declare_property`` not applying to subclasses of the class it was called on.
* Fixed ``repr`` of ``ObjCBoundMethod`` when the wrapped method is not an ``ObjCMethod``.
* Fixed the encodings of ``NSPoint``, ``NSSize``, and ``NSRect`` on 32-bit systems.
* Renamed the ``async`` support package to ``eventloop`` to avoid a Python 3.5+ keyword clash.

0.2.9
-----

* Improved handling of boolean types.
* Added support for using primitives as object values (e.g, as the key/value in an NSDictonary).
* Added support for passing Python lists as Objective-C NSArray arguments, and Python dicts as Objective-C NSDictionary arguments.
* Corrected support to storing strings and other objects as properties on Python-defined Objective-C classes.
* Added support for creating Objective-C blocks from Python callables. (ojii)
* Added support for returning compound values (structures and unions) from Objective-C methods defined in Python.
* Added support for creating, extending and conforming to Objective-C protocols.
* Added an ``objc_const`` convenience function to look up global Objective-C object constants in a DLL.
* Added support for registering custom ``ObjCInstance`` subclasses to be used to represent Objective-C objects of specific classes.
* Added support for integrating NSApplication and UIApplication event loops with Python's asyncio event loop.

0.2.8
-----

* Added support for using native Python sequence/mapping syntax with ``NSArray`` and ``NSDictionary``. (jeamland)
* Added support for calling Objective-C blocks in Python. (ojii)
* Added functions for declaring custom conversions between Objective-C type encodings and ``ctypes`` types.
* Added functions for splitting and decoding Objective-C method signature encodings.
* Added automatic conversion of Python sequences to C arrays or structures in method arguments.
* Extended the Objective-C type encoding decoder to support block types, bit fields (in structures), typed object pointers, and arbitrary qualifiers. If unknown pointer, array, struct or union types are encountered, they are created and registered on the fly.
* Changed the ``PyObjectEncoding`` to match the real definition of ``PyObject *``.
* Fixed the declaration of ``unichar`` (was previously ``c_wchar``, is now ``c_ushort``).
* Removed the ``get_selector`` function. Use the ``SEL`` constructor instead.
* Removed some runtime function declarations that are deprecated or unlikely to be useful.
* Removed the encoding constants. Use ``encoding_for_ctype`` to get the encoding of a type.

0.2.7
-----

* (#40) Added the ability to explicitly declare no-attribute methods as
  properties. This is to enable a workaround when Apple introduces readonly
  properties as a way to access these methods.

0.2.6
-----

* Added a more compact syntax for calling Objective-C methods, using Python
  keyword arguments. (The old syntax is still fully supported and will *not*
  be removed; certain method names even require the old syntax.)
* Added a ``superclass`` property to ``ObjCClass``.

0.2.5
-----

* Added official support for Python 3.6.
* Added keyword arguments to disable argument and/or return value conversion
  when calling an Objective-C method.
* Added support for (``NS``/``UI``) ``EdgeInsets`` structs. (Longhanks)
* Improved ``str`` of Objective-C classes and objects to return the
  ``debugDescription``, or for ``NSString``\s, the string value.
* Changed ``ObjCClass`` to extend ``ObjCInstance`` (in addition to ``type``),
  and added an ``ObjCMetaClass`` class to represent metaclasses.
* Fixed some issues on non-x86_64 architectures (i386, ARM32, ARM64).
* Fixed example code in README. (Dayof)
* Removed the last of the Python 2 compatibility code.

0.2.4
-----

* Added ``objc_property`` function for adding properties to custom Objective-C
  subclasses. (Longhanks)

0.2.3
-----

* Removed most Python 2 compatibility code.

0.2.2
-----

* Dropped support for Python 3.3.
* Added conversion of Python ``enum.Enum`` objects to their underlying values
  when passed to an Objective-C method.
* Added syntax highlighting to example code in README. (stsievert)
* Fixed the ``setup.py`` shebang line. (uranusjr)

0.2.1
-----

* Fixed setting of ``ObjCClass``/``ObjCInstance`` attributes that are not
  Objective-C properties.

0.2.0
-----

* First beta release.
* Dropped support for Python 2. Python 3 is now required, the minimum tested
  version is Python 3.3.
* Added error detection when attempting to create an Objective-C class with a
  name that is already in use.
* Added automatic conversion between Python ``decimal.Decimal`` and
  Objective-C ``NSDecimal`` in method arguments and return values.
* Added PyPy to the list of test platforms.
* When subclassing Objective-C classes, the return and argument types of
  methods are now specified using Python type annotation syntax and ``ctypes``
  types.
* Improved property support.

0.1.3
-----

* Fixed some issues on ARM64 (iOS 64-bit).

0.1.2
-----

* Fixed ``NSString`` conversion in a few situations.
* Fixed some issues on iOS and 32-bit platforms.

0.1.1
-----

* Objective-C classes can now be subclassed using Python class syntax, by
  using an ``ObjCClass`` as the superclass.
* Removed ``ObjCSubclass``, which is made obsolete by the new subclassing
  syntax.

0.1.0
-----

* Initial alpha release.
* Objective-C classes and instances can be accessed via ``ObjCClass`` and
  ``ObjCInstance``.
* Methods can be called on classes and instances with Python method call
  syntax.
* Properties can be read and written with Python attribute syntax.
* Method return and argument types are read automatically from the method
  type encoding.
* A small number of commonly used structs are supported as return and
  argument types.
* Python strings are automatically converted to and from ``NSString`` when
  passed to or returned from a method.
* Subclasses of Objective-C classes can be created with ``ObjCSubclass``.
