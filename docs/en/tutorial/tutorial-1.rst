.. _tutorial-1:

=================
Your first bridge
=================

In this example, we're going to use Rubicon to access the Objective-C
Foundation library, and the ``NSURL`` class in that library. ``NSURL`` is the
class used to represent and manipulate URLs.

This tutorial assumes you've set up your environment as described in the
:doc:`Getting started guide </how-to/get-started>`.

Accessing NSURL
===============

Start Python, and get a reference to an Objective-C class. In this example,
we're going to use the ``NSURL`` class, Objective-C's representation of URLs:

.. code-block:: pycon

    >>> from rubicon.objc import ObjCClass
    >>> NSURL = ObjCClass("NSURL")

This gives us an ``NSURL`` class in Python which is transparently bridged to
the ``NSURL`` class in the Objective-C runtime. Any method or property
described in `Apple's documentation on NSURL
<https://developer.apple.com/documentation/foundation/nsurl?language=objc>`__
can be accessed over this bridge.

Let's create an instance of an ``NSURL`` object. The ``NSURL`` documentation
describes a static constructor ``+URLWithString:``; we can invoke this
constructor as:

.. code-block:: pycon

    >>> base = NSURL.URLWithString("https://beeware.org/")

That is, the name of the method in Python is identical to the method in
Objective-C. The first argument is declared as being an ``NSString *``; Rubicon
converts the Python :class:`str` into an ``NSString`` instance as part of
invoking the method.

``NSURL`` has another static constructor: ``+URLWithString:relativeToURL:``. We
can also invoke this constructor:

.. code-block:: pycon

    >>> full = NSURL.URLWithString("contributing/", relativeToURL=base)

The second argument (``relativeToURL``) is accessed as a keyword argument. This
argument is declared as being of type ``NSURL *``; since ``base`` is an
instance of ``NSURL``, Rubicon can pass through this instance.

Sometimes, an Objective-C method definition will use the same keyword argument
name twice (for example, ``NSLayoutConstraint`` has a
``+constraintWithItem:attribute:relatedBy:toItem:attribute:multiplier:constant:``
selector, using the ``attribute`` keyword twice). This is legal in Objective-C,
but not in Python, as you can't repeat a keyword argument in a method call. In
this case, you can use a ``__`` suffix on the ambiguous keyword argument to make
it unique. Any content after and including the ``__`` will be stripped when
making the Objective-C call:

.. code-block:: pycon

    >>> constraint = NSLayoutConstraint.constraintWithItem(
    ...     first_item,
    ...     attribute__1=first_attribute,
    ...     relatedBy=relation,
    ...     toItem=second_item,
    ...     attribute__2=second_attribute,
    ...     multiplier=2.0,
    ...     constant=1.0
    ... )

Instance methods
================

So far, we've been using the ``+URLWithString:`` static constructor. However,
``NSURL`` also provides an initializer method ``-initWithString:``. To use this
method, you first have to instruct the Objective-C runtime to allocate memory
for the instance, then invoke the initializer:

.. code-block:: pycon

    >>> base = NSURL.alloc().initWithString("https://beeware.org/")

Now that you have an instance of ``NSURL``, you'll want to manipulate it.
``NSURL`` describes an ``absoluteURL`` property; this property can be accessed
as a Python attribute:

.. code-block:: pycon

    >>> absolute = full.absoluteURL

You can also invoke methods on the instance:

.. code-block:: pycon

    >>> longer = absolute.URLByAppendingPathComponent('how/first-time/')

If you want to output an object at the console, you can use the Objective-C
property ``description``, or for debugging output, ``debugDescription``:

.. code-block:: pycon

    >>> longer.description
    'https://beeware.org/contributing/how/first-time/'

    >>> longer.debugDescription
    'https://beeware.org/contributing/how/first-time/'

Internally, ``description`` and ``debugDescription`` are hooked up to their
Python equivalents, ``__str__()`` and ``__repr__()``, respectively:

.. code-block:: pycon

    >>> str(absolute)
    'https://beeware.org/contributing/'

    >>> repr(absolute)
    '<ObjCInstance: NSURL at 0x1114a3cf8: https://beeware.org/contributing/>'

    >>> print(absolute)
    https://beeware.org/contributing/

Time to take over the world!
============================

You now have access to *any* method, on *any* class, in any library, in the
entire macOS or iOS ecosystem! If you can invoke something in Objective-C, you
can invoke it in Python - all you need to do is:

    * load the library with ctypes;
    * register the classes you want to use; and
    * Use those classes as if they were written in Python.

Next steps
==========

The next step is to write your own classes, and expose them into the
Objective-C runtime. That's the subject of the :doc:`next tutorial
<./tutorial-2>`.
