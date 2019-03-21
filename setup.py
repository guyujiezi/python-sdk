#!/usr/bin/env python
import setuptools
import io
import re


pkg_author = 'guyujiezi'
pkg_name = 'guyujiezi'
pkg_url = 'https://github.com/guyujiezi/python-sdk'
pkg_desc = 'SDK of GuYuJieZi for Python language'
pkg_requires = []
pkg_version = {}

with io.open('README.md', 'r', encoding='utf8') as f:
    long_description = f.read()

with io.open('src/%s/version.py' % (pkg_name, ), 'r', encoding='utf8') as f:
    exec(f.read(), pkg_version)

setuptools.setup(
    author=pkg_author,
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description=pkg_desc,
    include_package_data=True,
    install_requires=pkg_requires,
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    name=pkg_name,
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    url=pkg_url,
    version=pkg_version['__version__'],
    zip_safe=True
)
