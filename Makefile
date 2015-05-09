# This file is part of django-walking-settings.
# https://github.com/rfloriano/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>

# lists all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
# required for list
no_targets__:

# install all dependencies (do not forget to create a virtualenv first)
setup:
	@pip install -U -e .\[tests\]
	$(MAKE) db_testproject
	$(MAKE) createsuperuser_testproject

# run your django application
run_testproject:
	@python tests_module/testproject/manage.py runserver 0.0.0.0:8000

migrate_testproject:
	@python tests_module/testproject/manage.py migrate

makemigrations_testproject:
	@python tests_module/testproject/manage.py makemigrations

db_testproject: makemigrations_testproject migrate_testproject

drop_testproject:
	@rm -rf tests_module/testproject/db.sqlite3
	$(MAKE) db_testproject

createsuperuser_testproject:
	@python tests_module/testproject/manage.py createsuperuser

# test your application (tests in the tests/ directory)
test: unit

unit:
	@REUSE_DB=1 coverage run tests_module/testproject/manage.py test
	@coverage report -m --fail-under=90

focus:
	@REUSE_DB=1 coverage run tests_module/testproject/manage.py test --settings=testproject.settings_focus

# show coverage in html format
coverage-html: unit
	@coverage html

# run tests against all supported python versions
tox:
	@tox

#docs:
	#@cd docs && make html && open _build/html/index.html
