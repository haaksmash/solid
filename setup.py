#!/usr/bin/env python
"""
Copyright (C) 2014 Haak Saxberg

This file is part of Solid, a state machine package for Python.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from distutils.core import setup, Command
from setuptools import find_packages


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])

        raise SystemExit(errno)


setup(
    name="solid",
    version='0.1.1',
    description="Pythonic state machines",
    long_description=open("README.txt").read(),
    author="Haak Saxberg",
    author_email="haak.erling@gmail.com",
    url="http://github.com/haaksmash/solid",
    packages=find_packages(),
    cmdclass={'test': PyTest},
    scripts=[
    ],
    install_requires=[
    ],
)
