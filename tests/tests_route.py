# -*- coding: utf-8 -*-
from django import test
from autoroute import Inspector
from django.core.urlresolvers import resolve
from app import views

class DefaultTestCase(test.SimpleTestCase):
    ''' Test cases for autoroute. '''

    def test_auto_generated(self):
        resolver = resolve('/app/views/auto-generated/')
        self.assertEqual(resolver.func,views.auto_generated)

    def test_with_name(self):
        resolver = resolve('/app/views/with-name/')
        self.assertEqual(resolver.func,views.with_name)
        self.assertEqual(resolver.url_name,'with-name')

    def test_custom(self):
        resolver = resolve('/app/views/custom/')
        self.assertEqual(resolver.func,views.custom_route)
        self.assertEqual(resolver.url_name,'custom-name')
