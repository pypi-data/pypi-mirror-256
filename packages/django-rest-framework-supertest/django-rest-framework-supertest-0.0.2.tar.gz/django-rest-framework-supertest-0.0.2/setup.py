#!/usr/bin/env python
import os

from setuptools import find_packages, setup

readme = ''
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

setup(
    name='django-rest-framework-supertest',
    version='0.0.2',
    description="A set of utilities to test django-rest-framework API's",
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Eduardo Oliveira',
    author_email='eduardo_y05@outlook.com',
    url='https://github.com/inventare/django-rest-framework-supertest',
    license='MIT',
    packages=find_packages(
        exclude=("tests.*", "tests"),
    ),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='django,api,rest_framework',
)
