#!/usr/bin/env python
# coding: utf-8

import os
import re
from setuptools import setup

# PyPi supports only reStructuredText, so pandoc should be installed
# before uploading package
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = ''

# Dynamically set __version__
this_dir = os.path.dirname(os.path.realpath(__file__))
version_path = os.path.join(this_dir, "smbprotocol_legacy", "version.py")
with open(version_path, 'r') as f:
    m = re.search(
        r"^__version__ = \"(\d+\.\d+\..*)\"$",
        f.read(),
        re.MULTILINE
    )
    __version__ = m.group(1)


setup(
    name='smbprotocol_legacy',
    version=__version__,
    packages=['smbprotocol_legacy'],
    install_requires=[
        'cryptography>=2.0',
        'ntlm-auth',
        'pyasn1',
        'six',
    ],
    extras_require={
        ':python_version<"2.7"': [
            'ordereddict'
        ],
        'kerberos:sys_platform=="win32"': [],
        'kerberos:sys_platform!="win32"': [
            'gssapi>=1.4.1'
        ]
    },
    author='Jordan Borean',
    author_email='jborean93@gmail.com',
    url='https://github.com/jborean93/smbprotocol',
    description='Interact with a server using the SMB 2/3 Protocol',
    long_description=long_description,
    keywords='smb smb2 smb3 cifs python',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
