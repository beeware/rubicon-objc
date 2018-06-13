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
coding:

.. code-block:: sh

    $ python3 -m venv venv
    $ source venv/bin/activate.sh
    (venv) $ git clone https://github.com/pybee/rubicon-objc.git
    (venv) $ cd rubicon-objc
    (venv) $ pip install -e .

In order to test the capabilities of Rubicon, the test suite contains an
Objective-C library with some known classes. To run the test suite, you'll need
to compile this library:

.. code-block:: sh

    (venv) $ make

This will produce ``tests/objc/librubiconharness.dylib``.

You can then run the test suite:

.. code-block:: sh

    (venv) $ tox

By default this will run the test suite multiple times, once on each Python version supported by Rubicon. This can take a while, so if you want to speed up the process while developing, you can run the tests on one Python version only:

.. code-block:: sh

    (venv) $ tox -e py36-default

Now you are ready to start hacking on Rubicon. Have fun!
