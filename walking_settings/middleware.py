# -*- coding: utf-8 -*-
from walking_settings import core


class WalkingSettingsMiddleware(object):
    def __init__(self, *args, **kwargs):
        core.load_settings()
