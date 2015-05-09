#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rflorianobr/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^walking-settings', include('walking_settings.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
