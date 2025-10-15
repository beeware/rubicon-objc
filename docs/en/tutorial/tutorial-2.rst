===================================
Tutorial 2 - Writing your own class
===================================

Eventually, you'll come across an Objective-C API that requires you to provide
a class instance as an argument. For example, when using macOS and iOS GUI
classes, you often need to define "delegate" classes to describe how a GUI
element will respond to mouse clicks and key presses.

Let's define a ``Handler`` class, with two methods:

    * an ``-initWithValue:`` constructor that accepts an integer; and

    * a ``-pokeWithValue:andName:`` method that accepts an integer and a
      string, prints the string, and returns a float that is one half of the
      value.

The declaration for this class would be::

    from rubicon.objc import NSObject, objc_method


    class Handler(NSObject):
        @objc_method
        def initWithValue_(self, v: int):
            self.value = v
            return self

        @objc_method
        def pokeWithValue_andName_(self, v: int, name) -> float:
            print("My name is", name)
            return v / 2.0

This code has several interesting implementation details:

    * The ``Handler`` class extends ``NSObject``. This instructs Rubicon to
      construct the class in a way that it can be registered with the
      Objective-C runtime.

    * Each method that we want to expose to Objective-C is decorated with
      ``@objc_method``.The method names match the Objective-C descriptor that
      you want to expose, but with colons replaced by underscores. This matches
      the "long form" way of invoking methods discussed in :doc:`tutorial-1`.

    * The ``v`` argument on ``initWithValue_()`` uses a Python 3 type
      annotation to declare it's type. Objective-C is a language with static
      typing, so any methods defined in Python must provide this typing
      information. Any argument that isn't annotated is assumed to be of type
      ``id`` - that is, a pointer to an Objective-C object.

    * The ``pokeWithValue_andName_()`` method has it's integer argument
      annotated, and has it's return type annotated as float. Again, this is
      to support Objective-C typing operations. Any function that has no
      return type annotation is assumed to return ``id``. A return type
      annotation of ``None`` will be interpreted as a ``void`` method in
      Objective-C. The ``name`` argument doesn't need to be annotated because it
      will be passed in as a string, and strings are ``NSObject`` subclasses
      in Objective-C.

    * ``initWithValue_()`` is a constructor, so it returns ``self``.

Having declared the class, you can then instantiate and use it:

.. code-block:: pycon

    >>> my_handler = Handler.alloc().initWithValue(42)
    >>> print(my_handler.value)
    42
    >>> print(my_handler.pokeWithValue(37, andName="Alice"))
    My name is Alice
    18.5

Objective-C properties
======================

When we defined the initializer for ``Handler``, we stored the provided value
as the ``value`` attribute of the class. However, as this attribute wasn't
declared to Objective-C, it won't be visible to the Objective-C runtime.
You can access ``value`` from within Python - but Objective-C code won't be
able to access it.

To expose value to the Objective-C runtime, we need to make one small change,
and explicitly declare value as an Objective-C property::

    from rubicon.objc import NSObject, objc_method, objc_property

    class PureHandler(NSObject):
        value = objc_property()

        @objc_method
        def initWithValue_(self, v: int):
            self.value = v
            return self

This doesn't change anything about how you access or modify the attribute - it
just means that Objective-C code will be able to see the attribute as well.

Class naming
============

In this revised example, you'll note that we also used a different class name
- ``PureHandler``. This was deliberate, because Objective-C doesn't have any
concept of namespaces. As a result, you can only define one class of any given
name in a process - so, you won't be able to define a second ``Handler`` class in
the same Python shell. If you try, you'll get an error:

.. code-block:: pycon

    >>> class Handler(NSObject):
    ...     pass
    Traceback (most recent call last)
    ...
    RuntimeError: An Objective-C class named b'Handler' already exists

You'll need to be careful (and sometimes, painfully verbose) when choosing class
names.

To allow a class name to be reused, you can set the class variable
:attr:`~rubicon.objc.api.ObjCClass.auto_rename` to ``True``. This option enables
automatic renaming of the Objective C class if a naming collision is detected:

.. code-block:: pycon

    >>> ObjCClass.auto_rename = True

This option can also be enabled on a per-class basis by using the
``auto_rename`` argument in the class declaration:

.. code-block:: pycon

    >>> class Handler(NSObject, auto_rename=True):
    ...     pass

If this option is used, the Objective C class name will have a numeric suffix
(e.g., `Handler_2`). The Python class name will be unchanged.

What, no ``__init__()``?
========================

You'll also notice that our example code *doesn't* have an ``__init__()``
method like you'd normally expect of Python code. As we're defining an
Objective-C class, we need to follow the Objective-C object life cycle - which
means defining initializer methods that are visible to the Objective-C runtime,
and invoking them over that bridge.

Next steps
==========

???
