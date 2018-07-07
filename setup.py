#!/usr/bin/env python
import io
import re

from setuptools import find_packages, setup

with io.open('./rubicon/objc/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='rubicon-objc',
    version=version,
    description='A bridge between an Objective C runtime environment and Python.',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    url='http://pybee.org/rubicon',
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.4',
    namespace_packages=['rubicon'],
    license='New BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Objective C',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
    ],
    test_suite='tests',
    package_urls={
        'Funding': 'https://pybee.org/contributing/membership/',
        'Documentation': 'https://rubicon-objc.readthedocs.io/en/latest/',
        'Tracker': 'https://github.com/pybee/rubicon-objc/issues',
        'Source': 'https://github.com/pybee/rubicon-objc',
    },
)
