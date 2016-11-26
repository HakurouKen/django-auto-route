#!/usr/bin/env python
import sys
from os import path
from django.conf import settings

ROOT = path.join(
    path.dirname(path.abspath(__file__)),
    'test_django_proj'
)
sys.path.append(ROOT)

SETTINGS = dict(
    DEBUG=True,
    BASE_DIR=ROOT,
    ROOT_URLCONF='app.urls',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'app'
    )
)

import django
from distutils.version import LooseVersion
django_version = django.get_version()
if LooseVersion(django_version) < LooseVersion('1.6'):
    raise ValueError('Django 1.6 or later required.')

if not settings.configured:
    settings.configure(**SETTINGS)

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(["", "test"])
