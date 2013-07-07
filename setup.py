#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.1.1'

from distutils.core import setup

requires = ('jsondb')

setup(
    name='jsondb-redis',
    version=__version__,
    url='https://github.com/shaung/jsondb-redis/',
    download_url='https://github.com/shaung/jsondb-redis/tarball/master',
    license='BSD',
    author='shaung',
    author_email='_@shaung.org',
    description='Redis backend for jsondb',
    long_description=open('README.md').read(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Database',
    ],
    platforms='any',
    install_requires=requires,
    packages=[
        'jsondb_backend',
        'jsondb_backend.redis_backend',
    ],
)
