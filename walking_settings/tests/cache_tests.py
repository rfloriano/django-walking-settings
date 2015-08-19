#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rfloriano/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
from preggy import expect
from django.conf import settings

from walking_settings.tests import BaseWalkingSettingsTestCase
from walking_settings.models import Settings
from walking_settings import core


class WalkingSettingsCacheTestCase(BaseWalkingSettingsTestCase):
    def setUp(self, *args, **kwargs):
        super(WalkingSettingsCacheTestCase, self).setUp(*args, **kwargs)
        self.real_pid = core.cache.pid
        self.fake_pid = core.cache.pid = self.real_pid + 1000
        core.cache._add_pid_to_cached_pids()
        core.cache.pid = self.real_pid

    def test_can_create_django_settings_via_settings_models(self):
        expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
        Settings.objects.create(
            name='MY_SUPER_VAR',
            value='--my-super-value--'
        )
        expect(settings.MY_SUPER_VAR).to_equal('--my-super-value--')
        expect(core.cache.get_changes()).to_be_empty()
        expect(core.cache._get_cached_pids()).to_equal(
            [self.real_pid, self.fake_pid]
        )
        expect(core.cache._get_cached_changes()).to_equal({
            self.fake_pid: {
                'MY_SUPER_VAR': {'action': 'set', 'value': '--my-super-value--'}
            },
            self.real_pid: {}
        })
