Changelog
=========

0.2.8
-----

* Added support for using native Python sequence/mapping syntax with ``NSArray`` and ``NSDictionary``. (jeamland)
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
