from django.db import models
from django.conf import settings
from django.contrib.auth import models as auth_models


def create_testuser(app, created_models, verbosity, **kwargs):
    if not settings.DEBUG:
        return
    try:
        auth_models.User.objects.get(username='test')
    except auth_models.User.DoesNotExist:
        print '*' * 80
        print 'Creating test user -- login: test, password: test'
        print '*' * 80
        assert auth_models.User.objects.create_superuser(
            'test', 'x@x.com', 'test')
    else:
        print 'Test user already exists.'

models.signals.post_syncdb.connect(
    create_testuser,
    sender=auth_models,
    dispatch_uid='common.models.create_testuser'
    )
