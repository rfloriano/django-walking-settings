#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rfloriano/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
import mock
from preggy import expect
from django.conf import settings
from django.test import override_settings
from django.db import models

from walking_settings.tests import BaseWalkingSettingsTestCase
from walking_settings.models import Settings
from walking_settings import core
from walking_settings.cache import CACHE_CHANGES_KEY


class WalkingSettingsTestCase(BaseWalkingSettingsTestCase):
    def test_can_create_django_settings_via_settings_models(self):
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
        Settings.objects.create(
            name='MY_SUPER_VAR',
            value='--my-super-value--'
        )
        expect(settings.MY_SUPER_VAR).to_equal('--my-super-value--')

    def test_can_delete_django_settings_via_settings_models(self):
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
        conf = Settings.objects.create(
            name='MY_SUPER_VAR',
            value='--my-super-value--'
        )
        expect(settings.MY_SUPER_VAR).to_equal('--my-super-value--')
        conf.delete()
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()

    @override_settings(MY_SUPER_VAR='--my-initial-value--')
    def test_can_override_django_settings_via_settings_models(self):
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_true()
        expect(settings.MY_SUPER_VAR).to_equal('--my-initial-value--')
        Settings.objects.create(
            name='MY_SUPER_VAR',
            value='--my-super-value--'
        )
        expect(settings.MY_SUPER_VAR).to_equal('--my-super-value--')

    @override_settings(MY_SUPER_VAR='--my-initial-value--')
    def test_delete_settings_models_and_default_value_is_used_again(self):
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_true()
        expect(settings.MY_SUPER_VAR).to_equal('--my-initial-value--')
        conf = Settings.objects.create(
            name='MY_SUPER_VAR',
            value='--my-super-value--'
        )
        expect(settings.MY_SUPER_VAR).to_equal('--my-super-value--')
        conf.delete()
        expect(settings.MY_SUPER_VAR).to_equal('--my-initial-value--')

    @override_settings(MY_SUPER_VAR='--my-initial-value--')
    def test_delete_settings_models_and_default_value_is_used_again_2(self):
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_true()
        expect(settings.MY_SUPER_VAR).to_equal('--my-initial-value--')
        conf = Settings.objects.create(
            name='MY_SUPER_VAR',
            value='--my-super-value--'
        )
        expect(settings.MY_SUPER_VAR).to_equal('--my-super-value--')
        expect(
            Settings.objects.get(name='MY_SUPER_VAR').value
        ).to_equal(u'--my-super-value--')

        conf.value = '--my-super-value-2--'
        conf.save()
        expect(settings.MY_SUPER_VAR).to_equal('--my-super-value-2--')
        expect(
            Settings.objects.get(name='MY_SUPER_VAR').value
        ).to_equal(u'--my-super-value-2--')

        conf.delete()

        expect(settings.MY_SUPER_VAR).to_equal('--my-initial-value--')

    def test_can_get_unicode_data(self):
        conf = Settings.objects.create(
            name='MY_SUPER_VAR',
            value='--my-super-value--'
        )
        expect(str(conf)).to_equal('MY_SUPER_VAR')


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


class LoadTestCase(BaseWalkingSettingsTestCase):
    fixtures = ['settings-data.json']

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        models.signals.post_save.disconnect(core.add_settings, sender=Settings)
        models.signals.post_delete.disconnect(core.delete_settings, sender=Settings)
        super(LoadTestCase, cls).setUpClass(*args, **kwargs)
        core.cache._initialized = False

    @classmethod
    def tearDownClass(cls, *args, **kwargs):
        models.signals.post_save.connect(core.add_settings, sender=Settings)
        models.signals.post_delete.connect(core.delete_settings, sender=Settings)
        super(LoadTestCase, cls).tearDownClass(*args, **kwargs)

    def set_cache(self, action, name, value=None):
        cache = {'action': action}
        if value:
            cache['value'] = value
        core.cache.cache.set(CACHE_CHANGES_KEY, {
            core.cache.pid: {name: cache}
        })

    @mock.patch('logging.warn')
    def test_can_load_settings(self, mocked_logging):
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
        core.load_settings()
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_true()

        obj = Settings.objects.create(
            name='MY_SUPER_VAR_2',
            value='foo bar'
        )
        self.set_cache('set', obj.name, obj.value)
        expect(hasattr(settings, 'MY_SUPER_VAR_2')).to_be_false()
        core.load_settings()
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_true()
        expect(hasattr(settings, 'MY_SUPER_VAR_2')).to_be_true()

        self.set_cache('del', obj.name)
        core.load_settings()
        expect(hasattr(settings, 'MY_SUPER_VAR_2')).to_be_false()

        self.set_cache('unknow', obj.name)
        core.load_settings()
        mocked_logging.assert_called_with(
            'Unknow action for unknow, ignoring MY_SUPER_VAR_2'
        )
