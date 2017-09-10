.. _tutorial-1:

=================
Your first bridge
=================

In this example, we're going to use Rubicon to access the Objective-C
Foundation library, and the `NSURL` class in that library. `NSURL` is the
class used to represent and manipulate URLs.

This tutorial assumes you've set up your environment as described in the
:ref:`Getting started guide <get-started>`.

Accessing NSURL
---------------

Start Python, and use ctypes to import a framework into the Python
interpreter:

.. code-block:: python

    >>> from ctypes import cdll, util
    >>> cdll.LoadLibrary(util.find_library("Foundation"))

This loads Apple's Objective-C Foundation libraries into memory. You can now
reference any class that is defined in that library. Next, we need to get a
handle to the `NSURL` class:

.. code-block:: python

    >>> from rubicon.objc import ObjCClass
    >>> NSURL = ObjCClass("NSURL")

This gives us an `NSURL` class in Python which is transparently bridged to the
`NSURL` class in the Objective-C runtime. Any method or property described in
`Apple's documentation on NSURL <>`__  can be accessed over this bridge.

Let's create an instance of an `NSURL` object. The `NSURL` documentation
describes a static constructor `+URLWithString:`; we can invoke this
constructor as::

    >>> base = NSURL.URLWithString("http://pybee.org/")

That is, the name of the method in Python is identical to the method in
Objective-C. The first argument is declared as being an `NSString *`; Rubicon
converts the Python `str` into an `NSString` instance as part of invoking the
method.

`NSURL` has another static constructor: `+URLWithString:relativeToURL:`. We
can also invoke this constructor:

    >>> full = NSURL.URLWithString("contributing/", relativeToURL=base)

The second argument (`relativeToURL`) is accessed as a keyword argument. This
argument is declared as being of type `NSURL *`; since `base` is an instance
of NSURL, Rubicon can pass through this instance.

Sometimes, an Objective-C method definition will use have the same keyword
argument name twice. This is legal in Objective-C, but not in Python, as you
can't repeat a keyword argument in a method call. In this case, you can use a
"long form" of the method to explicitly invoke a descriptor by replacing
colons with underscores::

    >>> base = NSURL.URLWithString_("http://pybee.org/")
    >>> full = NSURL.URLWithString_relativeToURL_("contributing", base)

Instance methods
----------------

So far, we've been using the `+URLWithString:` static constructor. However, `NSURL`
also provides an initializer method `-initWithString:`. To use this method, you
first have to instruct the Objective-C runtime to allocate memory for the instance,
then invoke the initializer:

    >>> base = NSURL.alloc().initWithString("http://pybee.org/")

Now that you have an instance of `NSURL`, you'll want to manipulate it.
`NSURL` describes an `absoluteURL` property; this property can be
accessed as a Python attribute::

    >>> absolute = full.absoluteURL

You can also invoke methods on the instance::

    >>> full.toString()


Time to take over the world!
----------------------------

You now have access to *any* method, on *any* class, in any library, in the
entire macOS or iOS ecosystem! If you can invoke something in Objective-C, you
can invoke it in Python - all you need to do is:

    * load the library with ctypes;
    * register the classes you want to use; and
    * Use those classes as if they were written in Python.

Next steps
----------

The next step is to write your own classes, and expose them into the
Objective-C runtime. That's the subject of the :ref:`next tutorial
<tutorial-2>`.
