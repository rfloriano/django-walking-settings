# -*- coding: utf-8 -*-
from walking_settings import core


class WalkingSettingsMiddleware(object):
    def process_request(self, *args, **kwargs):
        core.load_settings()
