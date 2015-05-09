#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rflorianobr/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
from types import ModuleType
from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings

EXCLUDE_PROPERTY = ['is_overridden', 'default_settings', 'settings']


class SettingsView(View):
    def get(self, request):
        params = {}
        for key in dir(settings):
            value = getattr(settings, key)
            if (key in EXCLUDE_PROPERTY or
               key.startswith('__') or
               isinstance(value, ModuleType)):
                continue
            if isinstance(value, set):
                value = list(value)
            params[key] = value
        return JsonResponse(params)
