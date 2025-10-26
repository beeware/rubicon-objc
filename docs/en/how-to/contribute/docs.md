# Contributing to the documentation { #contribute-docs }

Here are some tips for working on this documentation. You're welcome to
add more and help us out!

Rubicon's documentation is written using [MkDocs and Markdown](https://www.markdownguide.org/basic-syntax/). We aim to follow the [Diataxis](https://diataxis.fr) framework for structuring documentation.

## Build documentation locally

To build the documentation locally, [set up a development environment][setup-dev-environment]. However, you
**must** have a Python 3.12 interpreter installed and available on your
path (i.e., `python3.12` must start a Python 3.12 interpreter).

Once your development environment is set up, run:

```console
(venv) $ tox -e docs
```

The output of the file should be in the `_build/html` folder. If
there are any markup problems, they'll raise an error.

## Live documentation preview

To support rapid editing of documentation, Rubicon also has a "live
preview" mode:

/// tab | macOS

```console
(venv) $ tox -e docs-live
```

///

/// tab | Linux

```console
(venv) $ tox -e docs-live
```

///

/// tab | Windows

```doscon
(venv) C:\...>tox -e docs-live
```

///

This will build the documentation, start a web server to serve the build
documentation, and watch the file system for any changes to the
documentation source. If a change is detected, the documentation will be
rebuilt, and any browser viewing the modified page will be automatically
refreshed.

### Documentation linting

The build process will identify many issues within the Markdown, but Toga performs some additional "lint" checks. To run the lint checks:

/// tab | macOS

```console
(venv) $ tox -e docs-lint
```

///

/// tab | Linux

```console
(venv) $ tox -e docs-lint
```

///

/// tab | Windows

```doscon
(venv) C:\...>tox -e docs-lint
```

///

This will validate the documentation does not contain:

- dead hyperlinks
- misspelled words

If a valid spelling of a word is identified as misspelled, then add the word to the list in `docs/spelling_wordlist`. This will add the word to the spellchecker's dictionary. When adding to this list, remember:

- We prefer US spelling, with some liberties for programming-specific colloquialism (e.g., "apps") and verbing of nouns (e.g., "scrollable")
- Any reference to a product name should use the product's preferred capitalization. (e.g., "macOS", "GTK", "pytest", "Pygame", "PyScript").
- If a term is being used "as code", then it should be quoted as a literal rather than being added to the dictionary.
