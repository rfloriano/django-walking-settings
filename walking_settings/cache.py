#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rfloriano/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
import os

from django.core.cache import cache


CACHE_PID_KEY = 'walking-settings-pids'
CACHE_CHANGES_KEY = 'walking-settings-changes'


class WalkingSettingsCache(object):
    def __init__(self):
        self.cache = cache
        self.pid = os.getpid()
        self._add_pid_to_cached_pids()

    def _add_pid_to_cached_pids(self):
        pids = self._alive_cached_pids()
        if self.pid not in pids:
            pids.append(self.pid)
        self.cache.set(CACHE_PID_KEY, pids)
        self.cache.set(CACHE_CHANGES_KEY, self._get_cached_changes())

    def _alive_cached_pids(self):
        return self._get_cached_pids()
        # how to check if pids are from more then one machines running pids process
        # cached = self._get_cached_pids()
        # pid_list = list(cached)  # copy the list
        # for cached_pid in pid_list:
        #     try:
        #         os.kill(cached_pid, 0)  # check if proccess exists
        #     except OSError:
        #         cached.remove(cached_pid)
        # return cached

    def _get_cached_pids(self):
        return self.cache.get(CACHE_PID_KEY) or []

    def _get_cached_changes(self):
        data = self.cache.get(CACHE_CHANGES_KEY) or {}
        if self.pid not in data:
            data[self.pid] = {}
        return data

    def set_changes(self, action, key, value=None):
        data = self.cache.get(CACHE_CHANGES_KEY)
        for pid, actions in data.items():
            if pid == self.pid:
                # this cache is between processes,
                # NOT for the same process to avoide overhead
                continue
            actions[key] = {'action': action, 'value': value}
        self.cache.set(CACHE_CHANGES_KEY, data)

    def get_changes(self):
        return self.cache.get(CACHE_CHANGES_KEY)[self.pid]
