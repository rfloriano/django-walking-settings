#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rflorianobr/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
import json
from preggy import expect
from django.test import override_settings

from walking_settings.tests import BaseWalkingSettingsTestCase
from walking_settings.models import Settings


class ViewTestCase(BaseWalkingSettingsTestCase):
    @override_settings(DEBUG=True)
    def test_can_access_settings_via_web(self):
        resp = self.client.get('/walking-settings/help')
        expect(resp.status_code).to_equal(200)
        data = json.loads(resp.content)
        expect(data).not_to_include('MY_SUPER_VAR')

        Settings.objects.create(name='MY_SUPER_VAR', value='foo bar')
        resp = self.client.get('/walking-settings/help')
        expect(resp.status_code).to_equal(200)
        data = json.loads(resp.content)
        expect(data).to_include('MY_SUPER_VAR')
        expect(data['MY_SUPER_VAR']).to_include('foo bar')

    @override_settings(DEBUG=True)
    def test_cant_see_protected_settings(self):
        Settings.objects.create(name='__MY_SUPER_VAR', value='foo bar')
        resp = self.client.get('/walking-settings/help')
        expect(resp.status_code).to_equal(200)
        data = json.loads(resp.content)
        expect(data).not_to_include('MY_SUPER_VAR')
