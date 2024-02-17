#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

__readme = None
with open('README.md', 'r', encoding='utf-8') as fd:
    __readme = fd.read()

setup(  name = 'integration_test_plugin',
        version = '1.0.0',
        description = 'A plugin which enable testing of target executables on Python3 unittest framework.',
        long_description = __readme,
        long_description_content_type = 'text/markdown',
        url='https://github.com/Bacondish2023/integration_test_plugin',
        author = 'Hidekazu TAKAHASHI',
        author_email = '139677991+Bacondish2023@users.noreply.github.com',
        license = 'MIT License',

        classifiers=[
            'Topic :: Software Development :: Testing',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
        ],

        keywords='development testing-tool',

        python_requires='>=3.6',

        packages = [
            'integration_test_plugin',
            ],
        )
