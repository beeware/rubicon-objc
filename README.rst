
.. image:: http://pybee.org/rubicon/static/images/rubicon-72.png
    :target: https://pybee.org/rubicon

.. image:: https://travis-ci.org/pybee/rubicon-objc.svg?branch=master
    :target: https://travis-ci.org/pybee/rubicon-objc

Rubicon-ObjC
============

Rubicon-ObjC is a bridge between Objective C and Python. It enables you to:

* Use Python to instantiate objects defined in Objective C,
* Use Python to invoke methods on objects defined in Objective C, and
* Subclass and extend Objective C classes in Python.

It also includes wrappers of the some key data types from the Core Foundation
framework (e.g., NSString).

Quickstart
----------

Rubicon uses a combination of `ctypes`, plus Objective-C's own reflection
APIs, to enable Objective C objects to be referenced in a Python process.

To install Rubicon, use pip::

    $ pip install rubicon-objc

Then, in a Python shell::

    >>> from ctypes import cdll
    >>> from ctypes import util
    >>> from rubicon.objc import ObjCClass, objc_method

    # Use ctypes to import a framework into the Python process
    >>> cdll.LoadLibrary(util.find_library('Foundation'))

    # Wrap an Objective C class contained in the framework
    >>> NSURL = ObjCClass("NSURL")

    # Then instantiate the Objective C class, using the API
    # that is exposed through Objective C. The Python method name
    # is the concatenated version of the Objective C method descriptor,
    # with colons replaced with underscores. So, the equivalent of
    # [NSURL URLWithString:@"http://pybee.org"];
    # would be:
    >>> NSURL.URLWithString_("http://pybee.org/")

    # To create a new Objective C class, define a Python class that
    # has the methods you want to define, decorate it to indicate that it
    # should be exposed to the Objective C runtime, and annotate it to
    # describe the type of any arguments that aren't of type ``id``:
    >>> class Handler(NSObject):
    ...     @objc_method
    ...     def initWithValue_(self, v: int):
    ...         self.value = v
    ...         return self
    ...
    ...     @objc_method
    ...     def pokeWithValue_(self, v: int) -> None:
    ...         print ("Poking with", v)
    ...         print ("Internal value is", self.value)

    # Then use the class:
    >>> my_handler = Handler.alloc().initWithValue_(42)
    >>> my_handler.pokeWithValue_(37)

Testing
-------

To run the Rubicon test suite:

1. Compile the Rubicon test library. A ``Makefile`` has been provided to make
this easy. Type::

    $ make

to compile it.

.. admonition:: Cross platform support

    This Makefile currently only works under OS/X; however, the build commands
    aren't complicated; it should be fairly easy to reproduce the build on other
    platforms. Pull requests to make the ``Makefile`` cross-platform are welcome.

2. Put the Rubicon support library somewhere that it will be found by dynamic
   library discovery. This means:

   a. Under OS X, put the ``tests/objc`` directory in your ``DYLD_LIBRARY_PATH``

   b. Under Linux, put the ``tests/objc`` directory in your ``LD_LIBRARY_PATH``

   c. Under Windows.... something :-)


3. Run the test suite::

    $ python setup.py test

   A ``tox`` configuration has also been provided; to run the tests across all
   supported platforms, run::

    $ tox

.. Documentation
.. -------------

.. Full documentation for Rubicon can be found on `Read The Docs`_.

Community
---------

Rubicon is part of the `BeeWare suite`_. You can talk to the community through:

* `@pybeeware on Twitter`_

* The `BeeWare Users Mailing list`_, for questions about how to use the BeeWare suite.

* The `BeeWare Developers Mailing list`_, for discussing the development of new features in the BeeWare suite, and ideas for new tools for the suite.

Contributing
------------

If you experience problems with this backend, `log them on GitHub`_. If you
want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _BeeWare suite: http://pybee.org
.. _Read The Docs: http://rubicon-objc.readthedocs.org
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _BeeWare Users Mailing list: https://groups.google.com/forum/#!forum/beeware-users
.. _BeeWare Developers Mailing list: https://groups.google.com/forum/#!forum/beeware-developers
.. _log them on Github: https://github.com/pybee/rubicon-objc/issues
.. _fork the code: https://github.com/pybee/rubicon-objc
.. _submit a pull request: https://github.com/pybee/rubicon-objc/pulls
