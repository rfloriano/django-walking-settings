#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rfloriano/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
from django.conf import settings

from tests_module.base import TestCase  # NOQA


class BaseWalkingSettingsTestCase(TestCase):
    def setUp(self):
        self._shadow = set(dir(settings))

    def tearDown(self):
        new_shadow = set(dir(settings))
        diff = new_shadow - self._shadow
        # remove new settings, override_settings only create then
        for key in diff:
            delattr(settings, key)
