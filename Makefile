VIRTUALENV?=venv

init: setup.venv list
	$(info ****************)
	$(info > init)
	$(info ****************)
	source $(VIRTUALENV)/bin/activate; pip install -r requirements.txt

setup.venv:
	$(info ****************)
	$(info > setup:venv)
	$(info ****************)
	virtualenv $(VIRTUALENV)

delete.venv:
	$(info ****************)
	$(info > delete:venv)
	$(info ****************)
	rm -rf $(VIRTUALENV)

test: setup.venv
	# This runs all of the tests. To run an individual test, run py.test with
	# the -k flag, like "py.test -k test_path_is_not_double_encoded"
	$(info ****************)
	$(info > test)
	$(info ****************)
	source $(VIRTUALENV)/bin/activate; py.test tests -lvs

coverage:
	$(info ****************)
	$(info > coverage)
	$(info ****************)
	source $(VIRTUALENV)/bin/activate; py.test --verbose --cov-report term --cov=requests tests

ci: setup.venv
	$(info ****************)
	$(info > ci)
	$(info ****************)
	source $(VIRTUALENV)/bin/activate; py.test --junitxml=junit.xml

generate.rst: setup.venv
	$(info ****************)
	$(info > generate.rst)
	$(info ****************)
	source $(VIRTUALENV)/bin/activate; rst2html.py README.rst > README.html
	source $(VIRTUALENV)/bin/activate; rst2html.py HISTORY.rst > HISTORY.html
	cat README.rst > RELEASE_NOTES.rst
	cat HISTORY.rst >> RELEASE_NOTES.rst
	source $(VIRTUALENV)/bin/activate; rst2html.py RELEASE_NOTES.rst > RELEASE_NOTES.html

publish.test:
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest

publish:
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi
	python setup.py bdist_wheel --universal upload
	rm -rf build dist .egg seleniumpm.egg-info

clean:
	rm -rf build dist .egg seleniumpm.egg-info
	rm README.html HISTORY.html RELEASE_NOTES.rst RELEASE_NOTES.html

list:
	$(info ************************************)
	$(info > Here is a list of Makefile targets)
	$(info ************************************)
	@grep '^[^#[:space:]].*:' Makefile
