# -*- coding: utf-8 -*-
from distutils.core import setup
import os
import autoroute

setup(
    name = 'django-auto-route',
    version = autoroute.__version__,
    description = autoroute.__doc__,
    author = autoroute.__author__,
    author_email = 'ticshot@gmail.com',
    url = 'https://github.com/HakurouKen/django-auto-route/',
    py_modules = ['autoroute'],
    install_requires = [
        "django>=1.6"
    ],
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    license = autoroute.__license__
)
