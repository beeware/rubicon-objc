.. _contribute:

============================
How to contribute to Rubicon
============================

If you experience problems with Rubicon, `log them on GitHub`_. If you want
to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _log them on Github: https://github.com/pybee/rubicon-objc/issues
.. _fork the code: https://github.com/pybee/rubicon-objc
.. _submit a pull request: https://github.com/pybee/rubicon-objc/pulls

Set up your development environment
===================================

The recommended way of setting up your development environment for Rubicon is
to install a virtual environment, install the required dependencies and start
coding::

    $ python3 -m venv venv
    $ source venv/bin/activate.sh
    $ git clone git@github.com:pybee/rubicon-objc.git
    $ cd rubicon-objc
    $ pip install -e .

In order to test the capabilities of Rubicon, the test suite contains an
Objective-C library with some known classes. To run the test suite, you'll need
to compile this library::

    $ make

This will produce `tests/objc/librubiconharness.dylib`.

In order for Rubicon to find this file, it will need to be on your dynamic
library path. You can set this by setting an environment variable::

    $ export DYLD_LIBRARY_PATH=$(pwd)/tests/objc

You can then run the test suite::

    $ python setup.py test

Now you are ready to start hacking on Rubicon. Have fun!
