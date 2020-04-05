import re

from setuptools import setup

with open('./rubicon/objc/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    version=version,
    # The test_suite kwarg is only used by the setup.py test command,
    # which is deprecated since setuptools 41.5.0:
    # https://setuptools.readthedocs.io/en/latest/history.html#v41-5-0
    # We still use setup.py test in our tox and CI configurations,
    # but once we replace those calls with another test runner,
    # this kwarg can be removed.
    test_suite='tests',
)
