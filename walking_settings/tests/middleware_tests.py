#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rflorianobr/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
import mock
from preggy import expect
from django.conf import settings
from django.test import override_settings

from walking_settings.tests import BaseWalkingSettingsTestCase


class MiddlewareTestCase(BaseWalkingSettingsTestCase):
    @override_settings(DEBUG=True)
    @mock.patch('walking_settings.core.load_settings')
    def test_middleware_init(self, load_settings_mock):
        middlewares = list(settings.MIDDLEWARE_CLASSES)
        middlewares.insert(0, 'walking_settings.middleware.WalkingSettingsMiddleware')
        with self.settings(MIDDLEWARE_CLASSES=middlewares):
            resp = self.client.get('/walking-settings/help')
            expect(resp.status_code).to_equal(200)
            expect(load_settings_mock.called).to_be_true()
