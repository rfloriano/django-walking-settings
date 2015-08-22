#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rfloriano/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
from datetime import datetime

from django.conf import settings

from walking_settings.cache import WalkingSettingsCache

_last_modified = None
__old_walking_settings = {}
cache = WalkingSettingsCache()


class NoValue(object):
    pass


def load_settings(query=None):
    global _last_modified
    if query is None:
        from walking_settings.models import Settings
        query = Settings.objects.all()
    for data in query:
        set_settings(data.name, data.value)
    _last_modified = datetime.utcnow()


def set_settings(name, value):
    old_value = getattr(settings, name, NoValue)
    if old_value != NoValue and name not in __old_walking_settings:
        __old_walking_settings[name] = old_value

    try:
        value = eval(value)
    except Exception:
        pass
    setattr(settings, name, value)
    cache.set_changes('set', name, value)


def del_settings(name):
    if name in __old_walking_settings:
        setattr(settings, name, __old_walking_settings[name])
    else:
        delattr(settings, name)
    cache.set_changes('del', name)


def add_settings(sender, instance, created, **kwargs):
    set_settings(instance.name, instance.value)


def delete_settings(sender, instance, **kwargs):
    del_settings(instance.name)
