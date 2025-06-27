=====================================
Calling plain C functions from Python
=====================================

Most Objective-C APIs are exposed through Objective-C classes and methods, but
some parts are implemented as plain C functions. You might also want to want to
use a pure C library that provides no Objective-C interface at all. Calling C
functions is quite different from calling Objective-C methods and requires some
additional work, which will be explained in this how-to.

.. seealso::

    The `ctypes tutorial
    <https://docs.python.org/3/library/ctypes.html#ctypes-tutorial>`_ in the
    Python documentation, which explains how to call C functions in general
    (without a specific focus on Apple platforms and Objective-C).

A simple example: ``puts``
--------------------------

We'll start with a simple example: calling the ``puts`` function from the C
standard library. ``puts`` takes a C string and outputs it to standard output
--- it's the C equivalent of a simple ``print`` call.

Before we can call the function, we need to look it up first. To do this, we
need to find and load the library in which the function is defined. In the case
of standard C functions, this is the standard C library, ``libc``. Because this
library is commonly used, Rubicon already loads it by default and exposes it in
Python as :attr:`rubicon.objc.runtime.libc`.

.. code-block:: pycon

    >>> from rubicon.objc.runtime import libc
    >>> libc
    <CDLL '/usr/lib/libc.dylib', handle 7fff60d0cb90 at 0x105850b38>

.. note::

    For a list of all C libraries that Rubicon loads and exposes by default,
    see the :ref:`predefined-c-libraries` section of the
    :mod:`rubicon.objc.runtime` reference documentation.

    To access a library that is not predefined by Rubicon, you can use the
    :func:`~rubicon.objc.runtime.load_library` function:

    .. code-block:: pycon

        >>> from rubicon.objc.runtime import load_library
        >>> libm = load_library("m")
        >>> libm
        <CDLL '/usr/lib/libm.dylib', handle 7fff60d0cb90 at 0x10596be10>

C functions are accessed as attributes on their library:

.. code-block:: pycon

    >>> libc.puts
    <_FuncPtr object at 0x110178f20>

However, unlike Objective-C methods, we cannot call C functions right away ---
we must first declare the function's argument and return types. (Rubicon cannot
do this automatically like with Objective-C methods, because plain C doesn't
provide the runtime type information necessary for this.) This type information
is found in C header files, in this case ``stdio.h`` (which defines standard C
input/output functions, including ``puts``).

The exact location of the macOS C headers varies depending on your version of
macOS and the developer tools --- it is not a fixed path. To open the header
directory in the Finder, run the following command in the terminal:

.. code-block:: console

    $ open "$(xcrun --show-sdk-path)/usr/include"

.. note::

    This command requires a version of the macOS developer tools to be
    installed. If you do not have Xcode or the command-line developer tools
    installed yet, run this command in the terminal to install the command-line
    developer tools:

    .. code-block:: console

        $ xcode-select --install

Once you have opened the relevant header file in a text editor, you need to
search for the declaration of the function you're looking for. In the case of
``puts``, it looks like this:

.. code-block:: c

    int puts(const char *);

This means that ``puts`` returns an ``int`` and takes a single argument of type
``const char *`` (a pointer to one or more characters, i.e. a C string). This
translates to the following Python ``ctypes`` code:

.. code-block:: pycon

    >>> from ctypes import c_char_p, c_int
    >>> libc.puts.restype = c_int
    >>> libc.puts.argtypes = [c_char_p]

Now that we have provided all of the necessary type information, we can call
``libc.puts``.

For the ``c_char_p`` argument, we pass a byte string with the message we want
to print out. ``ctypes`` automatically converts the byte string object to a
``c_char_p`` (``char *``) as the C function expects it. The string specifically
needs to be a byte string (``bytes``), because C's ``char *`` strings are
byte-based, unlike normal Python strings (``str``), which are Unicode-based.

.. code-block:: pycon

    >>> res = libc.puts(b"Hello!")
    Hello!

.. note::

    If you're running this code from an editor or IDE and don't see ``Hello!``
    printed out, try running the code from a Python REPL in a terminal window
    instead. Some editors/IDEs, such as Python's IDLE, can only capture and
    display output produced by high-level Python functions (such as ``print``),
    but not output from low-level C functions (such as ``puts``).

    The return value of ``puts`` is ignored in this example. It indicates
    whether or not the call was successful. If ``puts`` succeeds, it returns a
    non-negative integer (the exact value is not significant and has no defined
    meaning). If ``puts`` encounters an error, it returns the ``EOF`` constant
    (on Apple OSes, this is ``-1``).

    The ``puts`` function generally doesn't fail, except for edge cases that
    are unlikely to happen in practice. With most other C functions, you need
    to be more careful about checking the return value, to make sure that
    errors from the function call are detected and handled. Unlike in Python,
    if you forget to check whether a C function call failed, any errors from
    that call are silently ignored, which often leads to bad behavior or
    crashes.

Most real examples of C functions are more complicated than ``puts``, but the
basic procedure for calling them is the same: import or load the function's C
library, set the function's return type and argument types based on the
relevant header, and then call the function as needed.

Each C library only needs to be imported/loaded once, and the ``restype`` and
``argtypes`` only need to be set once per function. This is usually done at
module level near the beginning of the module, similar to Python imports.

Inline functions (e.g. ``NSLocationInRange``)
---------------------------------------------

Regular C functions can be called as explained above, but there is also a
second kind of C function that needs to be handled differently: inline
functions. Unlike regular C functions, inline functions cannot be called
through a library object at runtime. Instead, their implementation is only
provided as source code in a header file.

When an inline function is called from regular C code, the C compiler copies
(inlines) the inline function's implementation into the calling code. To call
an inline C function from Python, we need to do the same thing --- copy the
code from the header into our own code --- but in addition we need to
translate the C code from the header into equivalent Python/``ctypes`` code.

As an example we will use the function ``NSLocationInRange`` from the
Foundation framework. This function checks whether an index lies inside a
``NSRange`` value. The definition of this function, from the Foundation header
``NSRange.h``, looks like this:

.. code-block:: objc

    NS_INLINE BOOL NSLocationInRange(NSUInteger loc, NSRange range) {
        return (!(loc < range.location) && (loc - range.location) < range.length) ? YES : NO;
    }

In this case, the translation to Python consists (roughly) of the following
steps:

1. The outer part of the function definition needs to be translated to Python's
   ``def`` syntax. The return type and argument types can be omitted in the
   Python code --- because Python is dynamically typed, these explicit types
   are not needed.
2. The ``YES`` and ``NO`` constants in the ``return`` expressions need to be
   replaced with their Python equivalents, ``True`` and ``False``.
3. Some operators in the ``return`` expression need to be changed: C ``!cond``
   translates to Python ``not cond``, C ``left && right`` becomes
   ``left and right``, and C ``cond ? true_val : false_val`` becomes
   ``true_val if cond else false_val``.

The translated Python code looks like this:

.. code-block:: python

    def NSLocationInRange(loc, range):
        return True if (not (loc < range.location) and (loc - range.location) < range.length) else False

You can then put this translated function into your Python code and call it in
place of the corresponding C inline function.

.. note::

    Python code translated from C like this is sometimes more complicated than
    necessary and can be simplified. In this case for example,
    ``True if cond else False`` can be simplified to just ``cond``,
    ``not (x < y)`` can be simplified to ``x >= y``, and a few redundant
    parentheses can be removed. A cleaner version of the translated code might
    look like this:

    .. code-block:: python

        def NSLocationInRange(loc, range):
            return loc >= range.location and loc - range.location < range.length

Global variables and constants (e.g. ``NSFoundationVersionNumber``)
-------------------------------------------------------------------

Some C libraries expose not just functions, but also global variables. An
example of this is the Foundation framework, which defines the global variable
``NSFoundationVersionNumber`` in ``<Foundation/NSObjCRuntime.h>``:

.. code-block:: objc

    FOUNDATION_EXPORT double NSFoundationVersionNumber;

Like functions, global variables are accessed via the library that they are
defined by. The syntax is somewhat different for global variables though -
instead of reading them directly as attributes of the library object, you use
the ``in_dll`` method of the variable's *type*. (Every ``ctypes`` type has an
``in_dll`` method.)

.. code-block:: pycon

    >>> from ctypes import c_double
    >>> from rubicon.objc.runtime import Foundation
    >>> NSFoundationVersionNumber = c_double.in_dll(Foundation, "NSFoundationVersionNumber")
    >>> NSFoundationVersionNumber
    c_double(1575.23)

Note that ``in_dll`` doesn't return the variable's value directly - instead it
returns a ``ctypes`` data object that has the variable's type, in this case
``c_double``. To access the variable's actual value, you can use the data
object's ``value`` attribute:

.. code-block:: pycon

    >>> NSFoundationVersionNumber.value
    1575.23

Objective-C object constants
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A special case of global variables is often found in Objective-C libraries:
object constants. These are global Objective-C object variables with a
``const`` modifier, meaning that they cannot be modified. Constants of type
``NSString *`` are especially common and can be found in many places, such as
Foundation's ``<Foundation/NSMetadataAttribute.h>``:

.. code-block:: objc

    FOUNDATION_EXPORT NSString * const NSMetadataItemFSNameKey;

Because they are so common, Rubicon provides the convenience function
``objc_const`` specifically for accessing Objective-C object constants:

.. code-block:: pycon

    >>> from rubicon.objc import objc_const
    >>> from rubicon.objc.runtime import Foundation
    >>> NSMetadataItemFSNameKey = objc_const(Foundation, "NSMetadataItemFSNameKey")
    >>> NSMetadataItemFSNameKey
    <ObjCStrInstance: __NSCFConstantString at 0x10eecf350: kMDItemFSName>

.. note::

    Sometimes it's not obvious that a constant is an Objective-C object,
    because its actual type is hidden behind a ``typedef``. This is common with
    the "extensible string enum" pattern, where a set of related string
    constants are defined together. An example can be found in
    ``<Foundation/NSCalendar.h>``:

    .. code-block:: objc

        typedef NSString * NSCalendarIdentifier NS_EXTENSIBLE_STRING_ENUM;

        FOUNDATION_EXPORT NSCalendarIdentifier const NSCalendarIdentifierGregorian;
        FOUNDATION_EXPORT NSCalendarIdentifier const NSCalendarIdentifierBuddhist;
        FOUNDATION_EXPORT NSCalendarIdentifier const NSCalendarIdentifierChinese;
        // ... many more ...

    Even though the constants use the type name ``NSCalendarIdentifier``, their
    actual type is still ``NSString *``, based on the ``typedef`` before.

    In some cases, constants use a ``typedef`` from a different header (or even
    a different library) than the one defining the constants, which can make it
    even harder to tell that they are actually Objective-C objects.

A complex example: ``dispatch_get_main_queue``
----------------------------------------------

As a final example, we'll look at the function ``dispatch_get_main_queue`` from
the ``libdispatch`` library. This is a very complex function definition, which
involves many of the concepts introduced above, as well as heavy use of C
pre-processor macros. If you don't have a lot of experience with the C
pre-processor, you may want to skip this section.

.. This example is based on the response to a question from the beeware/general Gitter chat: https://gitter.im/beeware/general?at=5b54e95357f4f664b794cde2

First, we need to look at the function's definition, which is found in the
header ``<dispatch/queue.h>``:

.. code-block:: objc

    DISPATCH_INLINE DISPATCH_ALWAYS_INLINE DISPATCH_CONST DISPATCH_NOTHROW
    dispatch_queue_main_t
    dispatch_get_main_queue(void)
    {
        return DISPATCH_GLOBAL_OBJECT(dispatch_queue_main_t, _dispatch_main_q);
    }

This is an inline function, which you can see based on the fact that it has a
function body and the ``DISPATCH_INLINE``/``DISPATCH_ALWAYS_INLINE``
attributes. This means that we cannot look it up directly using ``ctypes`` -
instead we have to translate the function body from C to Python.

We can ignore the first line of the function definition - they contain function
attributes intended for the compiler, which we don't need. The second and third
line indicate the function's signature - it takes no arguments and returns a
value of type ``dispatch_queue_main_t``.

The body is a little more complex: it uses ``DISPATCH_GLOBAL_OBJECT``, which is
actually a C macro. Its definition can be found in ``<dispatch/object.h>``:

.. code-block:: objc

    #define DISPATCH_GLOBAL_OBJECT(type, object) ((OS_OBJECT_BRIDGE type)&(object))

If we substitute the macro's parameters (``type`` and ``object``) for their
real values in our case (``dispatch_queue_main_t`` and ``_dispatch_main_q``),
we get the expression
``((OS_OBJECT_BRIDGE dispatch_queue_main_t)&(_dispatch_main_q))``.
``OS_OBJECT_BRIDGE`` is also a macro, this time from ``<os/object.h>``:

.. code-block:: objc

    #define OS_OBJECT_BRIDGE __bridge

It expands to ``__bridge``, which is an attribute related to Objective-C's
automatic reference counting (ARC) feature. In the context of Rubicon, ARC is
not relevant (Rubicon performs its own reference management for Objective-C
objects), so we can ignore this attribute. This leaves us with the expression
``((dispatch_queue_main_t)&(_dispatch_main_q))``, which we can substitute for
the macro call in our original function:

.. code-block:: objc

    dispatch_queue_main_t
    dispatch_get_main_queue(void)
    {
        return (dispatch_queue_main_t)&(_dispatch_main_q));
    }

With the macro expansion done, we can now see what the function does: it takes
a pointer to the global variable ``_dispatch_main_q`` and casts it to the type
``dispatch_queue_main_t``.

First, let's look at the definition of the ``_dispatch_main_q`` variable, from
``<dispatch/queue.h>``:

.. code-block:: objc

    DISPATCH_EXPORT
    struct dispatch_queue_s _dispatch_main_q;

The variable's type, ``struct dispatch_queue_s``, is an *opaque* structure type
- it is not defined in any public header. This means that we don't know what
fields the structure has, or even how large it is. As a result, we cannot
perform any operations on the structure itself, but we can work with *pointers*
to the structure - which is exactly what ``dispatch_get_main_queue`` does.

Even though ``struct dispatch_queue_s`` is opaque, we still need to define it
in Python so that we can look up the ``_dispatch_main_q`` variable:

.. code-block:: python

    from ctypes import Structure
    from rubicon.objc.runtime import load_library

    # On Mac, libdispatch is part of libSystem.
    libSystem = load_library("System")
    libdispatch = libSystem

    class struct_dispatch_queue_s(Structure):
        pass # No _fields_, because this is an opaque structure.

    _dispatch_main_q = struct_dispatch_queue_s.in_dll(libdispatch, "_dispatch_main_q")

Now we need to look at the definition of the ``dispatch_queue_main_t`` type.
This definition is not very obvious to find - it's actually this line in
``<dispatch/queue.h>``:

.. code-block:: objc

    DISPATCH_DECL_SUBCLASS(dispatch_queue_main, dispatch_queue_serial);

``DISPATCH_DECL_SUBCLASS`` is a macro from ``<dispatch/object.h>``, defined
like this:

.. code-block:: objc

    #define DISPATCH_DECL_SUBCLASS(name, base) OS_OBJECT_DECL_SUBCLASS(name, base)

It directly calls another macro, ``OS_OBJECT_DECL_SUBCLASS``, defined in
``<os/object.h>``:

.. code-block:: objc

    #define OS_OBJECT_DECL_SUBCLASS(name, super) \
            OS_OBJECT_DECL_IMPL(name, <OS_OBJECT_CLASS(super)>)

Let's substitute this macro into our original code:

.. code-block:: objc

    OS_OBJECT_DECL_IMPL(dispatch_queue_main, <OS_OBJECT_CLASS(dispatch_queue_serial)>);

Next is the ``OS_OBJECT_DECL_IMPL`` macro, also defined in ``<os/object.h>``:

.. code-block:: objc

    #define OS_OBJECT_DECL_IMPL(name, ...) \
            OS_OBJECT_DECL_PROTOCOL(name, __VA_ARGS__) \
            typedef NSObject<OS_OBJECT_CLASS(name)> \
                    * OS_OBJC_INDEPENDENT_CLASS name##_t

After we substitute this macro into our code, it looks like this:

.. code-block:: objc

    OS_OBJECT_DECL_PROTOCOL(dispatch_queue_main, <OS_OBJECT_CLASS(dispatch_queue_serial)>) \
    typedef NSObject<OS_OBJECT_CLASS(dispatch_queue_main)> \
        * OS_OBJC_INDEPENDENT_CLASS dispatch_queue_main_t;

And another macro, ``OS_OBJECT_DECL_PROTOCOL``, also from ``<os/object.h>``:

.. code-block:: objc

    #define OS_OBJECT_DECL_PROTOCOL(name, ...) \
            @protocol OS_OBJECT_CLASS(name) __VA_ARGS__ \
            @end

Which we can substitute into our code:

.. code-block:: objc

    @protocol OS_OBJECT_CLASS(dispatch_queue_main) <OS_OBJECT_CLASS(dispatch_queue_serial)> \
    @end \
    typedef NSObject<OS_OBJECT_CLASS(dispatch_queue_main)> \
        * OS_OBJC_INDEPENDENT_CLASS dispatch_queue_main_t;

Now let's take care of the ``OS_OBJECT_CLASS`` macro, defined like this in ``<os/object.h>``:

.. code-block:: objc

    #define OS_OBJECT_CLASS(name) OS_##name

And substituted into our code:

.. code-block:: objc

    @protocol OS_dispatch_queue_main <OS_dispatch_queue_serial> \
    @end \
    typedef NSObject<OS_dispatch_queue_main> \
        * OS_OBJC_INDEPENDENT_CLASS dispatch_queue_main_t;

Finally we're left with the ``OS_OBJECT_INDEPENDENT_CLASS`` macro, which is a
compiler attribute that we can ignore.

.. code-block:: objc

    @protocol OS_dispatch_queue_main <OS_dispatch_queue_serial>
    @end
    typedef NSObject<OS_dispatch_queue_main> * dispatch_queue_main_t;

Now we're done with macro expansion and can see what the code actually does -
it defines an Objective-C protocol called ``OS_dispatch_queue_main`` and
defines ``dispatch_queue_main_t`` as a pointer type to an object conforming to
that protocol. For our purposes, most of these details don't matter - the
important part is that ``dispatch_queue_main_t`` is actually an Objective-C
object pointer type. Because Rubicon doesn't differentiate between object
pointer types, we can replace ``dispatch_queue_main_t`` in our original
function with the generic ``id`` type:

.. code-block:: objc

    id
    dispatch_get_main_queue(void)
    {
        return (id)&(_dispatch_main_q));
    }

This code can finally be translated to Python:

.. code-block:: python

    from ctypes import byref, cast
    from rubicon.objc import ObjCInstance
    from rubicon.objc.runtime import objc_id

    # This requires the _dispatch_main_q Python code from before.

    def dispatch_get_main_queue():
        return ObjCInstance(cast(byref(_dispatch_main_q), objc_id))

Further information
-------------------

* `cdecl.org <https://cdecl.org/>`_: An online service to translate C type syntax into more understandable English.
* `cppreference.com <https://en.cppreference.com/w/>`_: A reference site about the standard C and C++ languages and libraries.
* `Apple's reference documentation <https://developer.apple.com/documentation/>`_: Official API documentation for Apple platforms. Make sure to change the language to Objective-C in the top-right corner, otherwise you'll get Swift documentation, which can differ significantly from Objective-C.
* macOS man pages, sections 2 and 3: Documentation for the C functions provided by macOS. View these using the ``man`` command, or by typing a function name into the search box of the macOS Terminal's Help menu.
