#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rflorianobr/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
from django.db import models
from django.utils.translation import ugettext_lazy as _

from walking_settings import core


class BaseSettings(models.Model):
    name = models.CharField(_('name'), max_length=200)
    value = models.CharField(_('value'), max_length=500)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class Settings(BaseSettings):
    class Meta:
        verbose_name = _('Settings')
        verbose_name_plural = _('Settings')


class ShadowSettings(BaseSettings):
    class Meta:
        verbose_name = _('Shadow settings')
        verbose_name_plural = _('Shadow settings')


models.signals.post_save.connect(core.add_settings, sender=Settings)
models.signals.post_delete.connect(core.delete_settings, sender=Settings)
