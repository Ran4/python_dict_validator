.venv/bin/activate:
	virtualenv --python=python3 .venv

.venv/lib/python3.6/site-packages/dictvalidator.egg-link: .venv/bin/activate
	. .venv/bin/activate \
	    && pip install -e ..

.PHONY: install
install: .venv/lib/python3.6/site-packages/dictvalidator.egg-link
	@:

.PHONY: uninstall
uninstall: .venv/bin/activate
	. .venv/bin/activate \
	    && pip uninstall dictvalidator

test: .venv/lib/python3.6/site-packages/dictvalidator.egg-link
	. .venv/bin/activate && \
	    python3 -c "import dictvalidator; assert 'dict_validator' in dir(dictvalidator), 'Could not find \'dict_validator\' in dictvalidator module'"
	@echo "Success!"


.PHONY: clean
clean:
	rm -rf .venv
