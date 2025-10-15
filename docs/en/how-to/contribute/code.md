# How to contribute code to Rubicon

If you experience problems with Rubicon, [log them on
GitHub](https://github.com/beeware/rubicon-objc/issues). If you want to
contribute code, please [fork the
code](https://github.com/beeware/rubicon-objc) and [submit a pull
request](https://github.com/beeware/rubicon-objc/pulls).

## Set up your development environment { #setup-dev-environment }

The recommended way of setting up your development environment for
Rubicon is to clone the repository, create a virtual environment, and
install the required dependencies:

``` console
$ git clone https://github.com/beeware/rubicon-objc.git
$ cd rubicon-objc
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ python3 -m pip install -Ue ".[dev]"
```

Rubicon uses a tool called [Pre-Commit](https://pre-commit.com) to
identify simple issues and standardize code formatting. It does this by
installing a git hook that automatically runs a series of code linters
prior to finalizing any git commit. To enable pre-commit, run:

``` console
(venv) $ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

When you commit any change, pre-commit will run automatically. If there
are any issues found with the commit, this will cause your commit to
fail. Where possible, pre-commit will make the changes needed to correct
the problems it has found:

``` console
(venv) $ git add some/interesting_file.py
(venv) $ git commit -m "Minor change"
black....................................................................Failed
- hook id: black
- files were modified by this hook

reformatted some/interesting_file.py

All done! ✨ 🍰 ✨
1 file reformatted.

flake8...................................................................Passed
check toml...........................................(no files to check)Skipped
check yaml...........................................(no files to check)Skipped
check for case conflicts.................................................Passed
check docstring is first.................................................Passed
fix end of files.........................................................Passed
trim trailing whitespace.................................................Passed
isort....................................................................Passed
pyupgrade................................................................Passed
docformatter.............................................................Passed
```

You can then re-add any files that were modified as a result of the
pre-commit checks, and re-commit the change.

``` console
(venv) $ git add some/interesting_file.py
(venv) $ git commit -m "Minor change"
black....................................................................Passed
flake8...................................................................Passed
check toml...........................................(no files to check)Skipped
check yaml...........................................(no files to check)Skipped
check for case conflicts.................................................Passed
check docstring is first.................................................Passed
fix end of files.........................................................Passed
trim trailing whitespace.................................................Passed
isort....................................................................Passed
pyupgrade................................................................Passed
docformatter.............................................................Passed
[bugfix e3e0f73] Minor change
1 file changed, 4 insertions(+), 2 deletions(-)
```

Rubicon uses [tox](https://tox.wiki/en/latest/) to manage the testing
process. To set up a testing environment and run the full test suite,
run:

``` console
(venv) $ tox
```

By default this will run the test suite multiple times, once on each
Python version supported by Rubicon, as well as running some pre-commit
checks of code style and validity. This can take a while, so if you want
to speed up the process while developing, you can run the tests on one
Python version only:

``` console
(venv) $ tox -e py
```

Or, to run using a specific version of Python:

``` console
(venv) $ tox -e py310
```

substituting the version number that you want to target. You can also
specify one of the pre-commit checks
<span class="title-ref">flake8</span>,
<span class="title-ref">docs</span> or
<span class="title-ref">package</span> to check code formatting,
documentation syntax and packaging metadata, respectively.

Now you are ready to start hacking on Rubicon. Have fun!
