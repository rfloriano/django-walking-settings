# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# # This file is part of django-walking-settings.
# # https://github.com/rflorianobr/django-walking-settings

# # Licensed under the MIT license:
# # http://www.opensource.org/licenses/MIT-license
# # Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>
# import json
# import mock
# from preggy import expect
# from django.conf import settings
# from django.test import override_settings
# from django.db.utils import OperationalError
# from django.apps import apps

# from tests_module.base import TestCase
# from walking_settings.models import Settings


# class WalkingSettingsTestCase(BaseWalkingSettingsTestCase):
#     def test_can_create_django_settings_via_settings_models(self):
#         expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
#         Settings.objects.create(
#             name='MY_SUPER_VAR',
#             value='--my-super-value--'
#         )
#         expect(settings.MY_SUPER_VAR).to_equal('--my-super-value--')

#     @override_settings(MY_SUPER_VAR='--my-initial-value--')
#     def test_can_override_django_settings_via_settings_models(self):
#         expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_true()
#         expect(settings.MY_SUPER_VAR).to_equal('--my-initial-value--')
#         Settings.objects.create(
#             name='MY_SUPER_VAR',
#             value='--my-super-value--'
#         )
#         expect(settings.MY_SUPER_VAR).to_equal('--my-super-value--')

#     @override_settings(MY_SUPER_VAR='--my-initial-value--')
#     def test_can_settings_models_and_default_value_is_used_again(self):
#         expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_true()
#         expect(settings.MY_SUPER_VAR).to_equal('--my-initial-value--')
#         var = Settings.objects.create(
#             name='MY_SUPER_VAR',
#             value='--my-super-value--'
#         )
#         expect(settings.MY_SUPER_VAR).to_equal('--my-super-value--')
#         var.delete()
#         expect(settings.MY_SUPER_VAR).to_equal('--my-initial-value--')

#     def test_can_get_unicode_data(self):
#         var = Settings.objects.create(
#             name='MY_SUPER_VAR',
#             value='--my-super-value--'
#         )
#         expect(str(var)).to_equal('MY_SUPER_VAR')


# class TypesTestCase(BaseWalkingSettingsTestCase):
#     def test_can_create_dict_settings(self):
#         expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
#         Settings.objects.create(
#             name='MY_SUPER_VAR',
#             value='{"foo": 1, "bar": 2}'
#         )
#         expect(isinstance(settings.MY_SUPER_VAR, dict)).to_be_true()
#         expect(settings.MY_SUPER_VAR).to_include("foo")
#         expect(settings.MY_SUPER_VAR["foo"]).to_equal(1)
#         expect(settings.MY_SUPER_VAR).to_include("bar")
#         expect(settings.MY_SUPER_VAR["bar"]).to_equal(2)

#     def test_can_create_number_settings(self):
#         expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
#         Settings.objects.create(
#             name='MY_SUPER_VAR',
#             value='1'
#         )
#         expect(isinstance(settings.MY_SUPER_VAR, int)).to_be_true()
#         expect(settings.MY_SUPER_VAR).to_equal(1)

#     def test_can_create_float_settings(self):
#         expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
#         Settings.objects.create(
#             name='MY_SUPER_VAR',
#             value='0.1'
#         )
#         expect(isinstance(settings.MY_SUPER_VAR, float)).to_be_true()
#         expect(settings.MY_SUPER_VAR).to_equal(0.1)

#     def test_can_create_bool_settings(self):
#         expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
#         Settings.objects.create(
#             name='MY_SUPER_VAR',
#             value='True'
#         )
#         expect(isinstance(settings.MY_SUPER_VAR, bool)).to_be_true()
#         expect(settings.MY_SUPER_VAR).to_equal(True)

#     def test_can_create_str_settings(self):
#         expect(hasattr(settings, 'MY_SUPER_VAR')).to_be_false()
#         Settings.objects.create(
#             name='MY_SUPER_VAR',
#             value='foo bar'
#         )
#         expect(isinstance(settings.MY_SUPER_VAR, str)).to_be_true()
#         expect(settings.MY_SUPER_VAR).to_equal('foo bar')


# class ViewTestCase(BaseWalkingSettingsTestCase):
#     @override_settings(DEBUG=True)
#     def test_can_access_settings_via_web(self):
#         resp = self.client.get('/walking-settings/help')
#         expect(resp.status_code).to_equal(200)
#         data = json.loads(resp.content)
#         expect(data).not_to_include('MY_SUPER_VAR')

#         Settings.objects.create(name='MY_SUPER_VAR', value='foo bar')
#         resp = self.client.get('/walking-settings/help')
#         expect(resp.status_code).to_equal(200)
#         data = json.loads(resp.content)
#         expect(data).to_include('MY_SUPER_VAR')
#         expect(data['MY_SUPER_VAR']).to_include('foo bar')

#     @override_settings(DEBUG=True)
#     def test_cant_see_protected_settings(self):
#         Settings.objects.create(name='__MY_SUPER_VAR', value='foo bar')
#         resp = self.client.get('/walking-settings/help')
#         expect(resp.status_code).to_equal(200)
#         data = json.loads(resp.content)
#         expect(data).not_to_include('MY_SUPER_VAR')


# class AppsTestCase(BaseWalkingSettingsTestCase):
#     @mock.patch('walking_settings.core.load_settings')
#     def test_if_appconfig_call_load_settings(self, load_settings_mock):
#         ws_config = apps.get_app_config('walking_settings')
#         ws_config.ready()
#         expect(load_settings_mock.called).to_be_true()

#     @mock.patch('walking_settings.core.load_settings',
#                 side_effect=OperationalError('foo bar'))
#     @mock.patch('walking_settings.apps.logger.warning')
#     def test_if_appconfig_call_log_warning(
#         self,
#         logging_mock,
#         load_settings_mock
#     ):
#         ws_config = apps.get_app_config('walking_settings')
#         ws_config.ready()
#         expect(load_settings_mock.called).to_be_true()
#         expect(logging_mock.called).to_be_true()
#         logging_mock.assert_called_once_with(
#             'foo bar. This is normal if you are running makemigrate or \
# migrate at first time')


# class MiddlewareTestCase(BaseWalkingSettingsTestCase):
#     @override_settings(DEBUG=True)
#     @mock.patch('walking_settings.core.load_settings')
#     def test_middleware_init(self, load_settings_mock):
#         middlewares = list(settings.MIDDLEWARE_CLASSES)
#         middlewares.insert(0, 'walking_settings.middleware.WalkingSettingsMiddleware')
#         with self.settings(MIDDLEWARE_CLASSES=middlewares):
#             resp = self.client.get('/walking-settings/help')
#             expect(resp.status_code).to_equal(200)
#             expect(load_settings_mock.called).to_be_true()
