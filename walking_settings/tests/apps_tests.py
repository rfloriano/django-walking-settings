#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rflorianobr/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
import mock
from preggy import expect
from django.db.utils import OperationalError
from django.apps import apps

from walking_settings.tests import BaseWalkingSettingsTestCase


class AppsTestCase(BaseWalkingSettingsTestCase):
    @mock.patch('walking_settings.core.load_settings')
    def test_if_appconfig_call_load_settings(self, load_settings_mock):
        ws_config = apps.get_app_config('walking_settings')
        ws_config.ready()
        expect(load_settings_mock.called).to_be_true()

    @mock.patch('walking_settings.core.load_settings',
                side_effect=OperationalError('foo bar'))
    @mock.patch('walking_settings.apps.logger.warning')
    def test_if_appconfig_call_log_warning(
        self,
        logging_mock,
        load_settings_mock
    ):
        ws_config = apps.get_app_config('walking_settings')
        ws_config.ready()
        expect(load_settings_mock.called).to_be_true()
        expect(logging_mock.called).to_be_true()
        logging_mock.assert_called_once_with(
            'foo bar. This is normal if you are running makemigrate or \
migrate at first time')
