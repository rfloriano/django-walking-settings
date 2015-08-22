#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from walking_settings import core


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            'variables',
            nargs='*',
            default=dir(settings),
            help='Variable name that you look for.'
        )

    def handle(self, *args, **options):
        core.load_settings()
        for var in options['variables']:
            try:
                value = getattr(settings, var)
            except Exception as e:
                raise CommandError(e)
            self.stdout.write('{0}={1}'.format(var, value))
