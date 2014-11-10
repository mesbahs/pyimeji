# -*- coding: utf-8 -*-
import re
import sys
from setuptools import setup


requires = [
    'six',
    'docopt',
    'requests',
    'AppDirs',
]


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='pyimeji',
    version="0.1.0",
    description='A python wrapper for the imeji API',
    long_description=read("README.rst"),
    author='Robert Forkel',
    author_email='xrotwang@googlemail.com',
    url='https://github.com/clld/pyimeji',
    install_requires=requires,
    license=read("LICENSE"),
    zip_safe=False,
    keywords='imeji',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    py_modules=["imeji"],
    entry_points={
        'console_scripts': [
            "imeji = pyimeji.cli:main"
        ]
    },
    tests_require=['nose'],
)