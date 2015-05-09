#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rflorianobr/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
from django.conf.urls import patterns, url
from django.conf import settings

from walking_settings.views import SettingsView


urlpatterns = patterns('')

if settings.DEBUG:
    urlpatterns += patterns('', url(
        r'help', SettingsView.as_view(), name='settings'),
    )
