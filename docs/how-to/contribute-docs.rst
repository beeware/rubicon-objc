Contributing to the documentation
=================================

Here are some tips for working on this documentation. You're welcome to add
more and help us out!

First of all, you should check the `Restructured Text (reST) and Sphinx
CheatSheet <https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html>`_ to
learn how to write your ``.rst`` file.

Create a ``.rst`` file
----------------------

Look at the structure and choose the best category to put your ``.rst`` file.
Make sure that it is referenced in the index of the corresponding category,
so it will show on in the documentation. If you have no idea how to do this,
study the other index files for clues.

Build documentation locally
---------------------------

To build the documentation locally, :ref:`set up a development environment
<setup-dev-environment>`.

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
