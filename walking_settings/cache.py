#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rfloriano/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
import os

from django.core.cache import cache


CACHE_CHANGES_KEY = 'walking-settings-changes'


class WalkingSettingsCache(object):
    def __init__(self):
        self.cache = cache
        self.pid = os.getpid()
        self._add_pid_to_cached_pids()

    def _add_pid_to_cached_pids(self):
        self.cache.set(CACHE_CHANGES_KEY, self._get_cached_changes())

    def _get_cached_changes(self):
        data = self.cache.get(CACHE_CHANGES_KEY) or {}
        if self.pid not in data:
            data[self.pid] = {}
        return data

    def _pid_is_alive(self, pid):
        try:
            os.kill(pid, 0)  # check if proccess exists
        except OSError:
            return False
        return True

    def set_changes(self, action, key, value=None):
        data = self.cache.get(CACHE_CHANGES_KEY)
        dead_pids = []
        for pid, actions in data.items():
            if pid == self.pid:
                # this cache is between processes,
                # NOT for the same process to avoide overhead
                continue
            if not self._pid_is_alive(pid):
                dead_pids.append(pid)
            actions[key] = {'action': action, 'value': value}
        for pid in dead_pids:
            del data[pid]
        self.cache.set(CACHE_CHANGES_KEY, data)

    def get_changes(self):
        return self.cache.get(CACHE_CHANGES_KEY)[self.pid]
