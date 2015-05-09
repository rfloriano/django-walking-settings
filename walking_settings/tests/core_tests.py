#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rflorianobr/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
from preggy import expect
from django.conf import settings
from django.test import override_settings

from walking_settings.tests import BaseWalkingSettingsTestCase
from walking_settings.models import Settings


class WalkingSettingsTestCase(BaseWalkingSettingsTestCase):
    def test_can_create_django_settings_via_settings_models(self):
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
        Settings.objects.create(
            name='MY_SUPER_VAR',
            value='--my-super-value--'
        )
        expect(settings.MY_SUPER_VAR).to_equal('--my-super-value--')

    @override_settings(MY_SUPER_VAR_TEST='--my-initial-value--')
    def test_can_override_django_settings_via_settings_models(self):
        expect(hasattr(settings, 'MY_SUPER_VAR_TEST')).to_be_true()
        expect(settings.MY_SUPER_VAR_TEST).to_equal('--my-initial-value--')
        Settings.objects.create(
            name='MY_SUPER_VAR_TEST',
            value='--my-super-value--'
        )
        expect(settings.MY_SUPER_VAR_TEST).to_equal('--my-super-value--')

    @override_settings(MY_SUPER_VAR='--my-initial-value--')
    def test_can_settings_models_and_default_value_is_used_again(self):
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_true()
        expect(settings.MY_SUPER_VAR).to_equal('--my-initial-value--')
        var = Settings.objects.create(
            name='MY_SUPER_VAR',
            value='--my-super-value--'
        )
        expect(settings.MY_SUPER_VAR).to_equal('--my-super-value--')
        var.delete()
        expect(settings.MY_SUPER_VAR).to_equal('--my-initial-value--')

    def test_can_get_unicode_data(self):
        var = Settings.objects.create(
            name='MY_SUPER_VAR',
            value='--my-super-value--'
        )
        expect(str(var)).to_equal('MY_SUPER_VAR')


class TypesTestCase(BaseWalkingSettingsTestCase):
    def test_can_create_dict_settings(self):
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
        Settings.objects.create(
            name='MY_SUPER_VAR',
            value='{"foo": 1, "bar": 2}'
        )
        expect(isinstance(settings.MY_SUPER_VAR, dict)).to_be_true()
        expect(settings.MY_SUPER_VAR).to_include("foo")
        expect(settings.MY_SUPER_VAR["foo"]).to_equal(1)
        expect(settings.MY_SUPER_VAR).to_include("bar")
        expect(settings.MY_SUPER_VAR["bar"]).to_equal(2)

    def test_can_create_number_settings(self):
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
        Settings.objects.create(
            name='MY_SUPER_VAR',
            value='1'
        )
        expect(isinstance(settings.MY_SUPER_VAR, int)).to_be_true()
        expect(settings.MY_SUPER_VAR).to_equal(1)

    def test_can_create_float_settings(self):
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
        Settings.objects.create(
            name='MY_SUPER_VAR',
            value='0.1'
        )
        expect(isinstance(settings.MY_SUPER_VAR, float)).to_be_true()
        expect(settings.MY_SUPER_VAR).to_equal(0.1)

    def test_can_create_bool_settings(self):
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
        Settings.objects.create(
            name='MY_SUPER_VAR',
            value='True'
        )
        expect(isinstance(settings.MY_SUPER_VAR, bool)).to_be_true()
        expect(settings.MY_SUPER_VAR).to_equal(True)

    def test_can_create_str_settings(self):
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
        Settings.objects.create(
            name='MY_SUPER_VAR',
            value='foo bar'
        )
        expect(isinstance(settings.MY_SUPER_VAR, str)).to_be_true()
        expect(settings.MY_SUPER_VAR).to_equal('foo bar')
