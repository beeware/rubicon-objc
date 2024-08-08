Contributing to the documentation
=================================

Here are some tips for working on this documentation. You're welcome to add
more and help us out!

First of all, you should check the `reStructuredText (reST) Primer
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ to
learn how to write your ``.rst`` file.

Create a ``.rst`` file
----------------------

Look at the structure and choose the best category to put your ``.rst`` file.
Make sure that it is referenced in the index of the corresponding category,
so it will show on in the documentation. If you have no idea how to do this,
study the other index files for clues.

Build documentation locally
---------------------------

.. Docs are always built on Python 3.12. See also the RTD and tox config.

To build the documentation locally, :ref:`set up a development environment
<setup-dev-environment>`. However, you **must** have a Python 3.12 interpreter
installed and available on your path (i.e., ``python3.12`` must start a Python
3.12 interpreter).

You'll also need to install the Enchant spell checking library.
Enchant can be installed using `Homebrew <https://brew.sh>`__:

.. code-block:: console

  (venv) $ brew install enchant

If you're on an M1 machine, you'll also need to manually set the location
of the Enchant library:

.. code-block:: console

  (venv) $ export PYENCHANT_LIBRARY_PATH=/opt/homebrew/lib/libenchant-2.2.dylib

Once your development environment is set up, run:

.. code-block:: console

  (venv) $ tox -e docs

The output of the file should be in the ``docs/_build/html`` folder. If there
are any markup problems, they'll raise an error.

Documentation linting
---------------------

Before committing and pushing documentation updates, run linting for the
documentation:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ tox -e docs-lint

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ tox -e docs-lint

  .. group-tab:: Windows

    .. code-block:: doscon

      C:\...>tox -e docs-lint

This will validate the documentation does not contain:

* invalid syntax and markup
* dead hyperlinks
* misspelled words

If a valid spelling of a word is identified as misspelled, then add the word to
the list in ``docs/spelling_wordlist``. This will add the word to the
spellchecker's

Rebuilding all documentation
----------------------------

To force a rebuild for all of the documentation:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ tox -e docs-all

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ tox -e docs-all

  .. group-tab:: Windows

    .. code-block:: doscon

      C:\...>tox -e docs-all

The documentation should be fully rebuilt in the ``docs/_build/html`` folder.
If there are any markup problems, they'll raise an error.

Live documentation preview
--------------------------

To support rapid editing of documentation, Rubicon also has a "live preview" mode:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ tox -e docs-live

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ tox -e docs-live

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>tox -e docs-live

This will build the documentation, start a web server to serve the build documentation,
and watch the file system for any changes to the documentation source. If a change is
detected, the documentation will be rebuilt, and any browser viewing the modified page
will be automatically refreshed.

Live preview mode will only monitor the ``docs`` directory for changes. If you're
updating the inline documentation associated with Toga source code, you'll need to use
the ``docs-live-src`` target to build docs:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ tox -e docs-live-src

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ tox -e docs-live-src

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>tox -e docs-live-src

This behaves the same as ``docs-live``, but will also monitor any changes to the
``src/rubicon/objc`` folder, reflecting any changes to inline documentation.
However, the rebuild process takes much longer, so you may not want to use this
target unless you're actively editing inline documentation.
