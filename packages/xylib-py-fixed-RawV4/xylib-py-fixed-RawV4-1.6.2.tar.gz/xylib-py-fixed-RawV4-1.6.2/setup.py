#!/usr/bin/env python

# This setup.py builds xylib as a python extension, which is experimental.
# The normal way of building xylib is using configure && make. Or cmake.
long_description="""\
xylib is a library for reading obscure file formats with data from
powder diffraction, spectroscopy and other experimental methods.
For the list of supported formats see https://github.com/wojdyr/xylib .

This module includes bindings to xylib and xylib itself.
The first two numbers in the version are the version of included xylib.

Prerequisites for building: SWIG and Boost libraries (headers only).
"""
from setuptools import setup
from distutils.core import Extension
from distutils.command.sdist import sdist
from glob import glob
import sys

# as per http://stackoverflow.com/a/21236111/104453
from distutils.command.build import build
class CustomBuild(build):
    sub_commands = [('build_ext', build.has_ext_modules),
                    ('build_py', build.has_pure_modules),
                    ('build_clib', build.has_c_libraries),
                    ('build_scripts', build.has_scripts)]

sources = glob('xylib/*.cpp') + ['xylib.i']

swig_opts = ['-c++', '-modern', '-modernargs']
if sys.version_info[0] == 3:
    swig_opts += ['-py3']

setup(name='xylib-py-fixed-RawV4',
      version='1.6.2',
      description='Python bindings to xylib including a fix for RawV4 files. Xylib is written by Marcin Wojdyr (wojdyr@gmail.com). This package'
                  'includes a fix for RawV4 files that is necessary as a depdency for package xrdpattern',
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Scientific/Engineering :: Chemistry',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
      author='Daniel Hollarek',
      author_email='daniel.hollarek@googlemail.com',
      license='LGPL2.1',
      url='https://github.com/wojdyr/xylib',
      ext_modules=[Extension('_xylib',
                             sources=sources,
                             language='c++',
                             swig_opts=swig_opts,
                             include_dirs=['.'],
                             libraries=[])],
      py_modules=['xylib'],
      cmdclass={'build': CustomBuild})
