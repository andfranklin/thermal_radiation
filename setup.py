#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'numpy>=1.13.0'
    # TODO: put package requirements here
]

setup_requirements = [
    'pytest-runner',
    # TODO(andfranklin): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='thermal_radiation',
    version='0.1.0',
    description="A framework to aid in the analysis of thermal networks involving thermal radiation.",
    long_description=readme + '\n\n' + history,
    author="Andrew Franklin",
    author_email='andfranklin3@gmail.com',
    url='https://github.com/andfranklin/thermal_radiation',
    packages=find_packages(include=['thermal_radiation']),
    entry_points={
        'console_scripts': [
            'thermal_radiation=thermal_radiation.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='thermal_radiation',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
