#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rflorianobr/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
from tests_module.base import TestCase
from walking_settings.models import Settings


class BaseWalkingSettingsTestCase(TestCase):
    def tearDown(self):
        try:
            Settings.objects.all().delete()
        except Exception:
            pass
