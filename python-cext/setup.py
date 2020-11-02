# fatal error: Python.h: No such file or directory
# sudo apt-get install python3-dev

from setuptools import setup, find_packages, Extension
import os.path
import sys

c_sources = (
    [
        os.path.join('c_src', 'pydevmem.c'),
        os.path.join('c_src', 'lib', 'devmem2.c'),
        ]
)

define_macros = []
extra_compile_args = []

module = Extension('_devmem',
                   define_macros=define_macros,
                   extra_compile_args=extra_compile_args,
                   sources=c_sources,
                   include_dirs=['c_src'])

setup(
    name='pydevmem',
    author='ranu',
    author_email='ranuzz@outlook.com',
    version="1.0.0",
    description="Python interface to devmem2",
    long_description="",
    url="",
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    ext_modules=[module],
    py_modules=['pydevmem'],

)