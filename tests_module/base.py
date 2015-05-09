#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rflorianobr/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
from django.test import TestCase as DjangoTestCase, Client
from django.contrib.auth.models import User


class TestCase(DjangoTestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        try:
            User.objects.create_superuser('test', 'test@foo.com', 'test')
        except:
            pass
        super(TestCase, cls).setUpClass(*args, **kwargs)

    def setUp(self):
        self.client = Client()
        self.client.login(username='test', password='test')
