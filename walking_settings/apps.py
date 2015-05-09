#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rflorianobr/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
import logging
from django.apps import AppConfig
from django.db.utils import OperationalError

from walking_settings import core

logger = logging.getLogger('django')


class WalkingSettingsConfig(AppConfig):
    name = 'walking_settings'
    verbose_name = "Walkings settings"

    def ready(self):
        try:
            core.load_settings()
        except OperationalError, e:
            logger.warning(
                '{0}. This is normal if you are running makemigrate or migrate \
at first time'.format(e.message))
