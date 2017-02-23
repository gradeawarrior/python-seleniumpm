#!/usr/bin/env python

import os
import re
import sys

from codecs import open

# from distutils.core import setup
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = ['seleniumpm', 'seleniumpm.webelements', 'seleniumpm.examples', 'seleniumpm.examples.widgets']

requires = ['selenium~=2.53.6']
test_requirements = ['pytest>=2.8.0', 'pytest-httpbin==0.0.7', 'pytest-cov']

with open('seleniumpm/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

readme_file = 'README.rst'
with open(readme_file, 'r', 'utf-8') as f:
    readme = f.read()
with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name='seleniumpm',
    version=version,
    description='Selenium Pagemodel implementation for Python.',
    long_description=readme + "\n\n" + history,
    author='Peter Salas',
    author_email='selenium-pagemodel@googlegroups.com',
    url='https://github.com/gradeawarrior/python-seleniumpm',
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE'], 'seleniumpm': ['*.pem']},
    package_dir={'seleniumpm': 'seleniumpm'},
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    keywords=['testing', 'seleniumpm', 'selenium', 'pagemodel', 'pageobjectmodel'],
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
)
