#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rfloriano/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
from datetime import datetime

from django.conf import settings


_last_modified = None


def load_settings(query=None):
    global _last_modified
    from walking_settings.models import Settings
    if query is None:
        query = Settings.objects.all()
    for data in query:
        set_settings(
            data.name,
            data.value,
            hasattr(settings, data.name)
        )
    _last_modified = datetime.utcnow()


def set_settings(name, value, keep_old=False):
    from walking_settings.models import ShadowSettings
    if keep_old:
        old_value = getattr(settings, name, '<NOVALUE>')
        if old_value != '<NOVALUE>':
            shadow, _ = ShadowSettings.objects.get_or_create(name=name)
            shadow.value = old_value
            shadow.save()
    try:
        value = eval(value)
    except Exception:
        pass
    setattr(settings, name, value)


def del_settings(name):
    from walking_settings.models import ShadowSettings
    try:
        old_settings = ShadowSettings.objects.get(name=name)
        set_settings(name, old_settings.value, False)
        old_settings.delete()
    except ShadowSettings.DoesNotExist:
        delattr(settings, name)


def add_settings(sender, instance, created, **kwargs):
    set_settings(instance.name, instance.value, created)


def delete_settings(sender, instance, **kwargs):
    del_settings(instance.name)
