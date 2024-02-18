#!/usr/bin/env python

from setuptools import setup
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

install_requires = [
    'Django>=3.2',
]
version = ('1.7.0')

setup(
    name='webtemplate-dbca',
    version=version,
    install_requires=install_requires,
    tests_require=install_requires,
    test_suite='runtests.runtests',
    packages=['webtemplate_dbca'],
    include_package_data=True,
    author='Ashley Felton',
    author_email='asi@dbca.wa.gov.au',
    maintainer='Ashley Felton',
    maintainer_email='asi@dbca.wa.gov.au',
    license='Apache License, Version 2.0',
    url='https://github.com/dbca-wa/webtemplate',
    description='Base HTML templates for DBCA Django projects',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords=['django', 'html', 'template', 'bootstrap'],
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
