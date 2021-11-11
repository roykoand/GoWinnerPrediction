.PHONY: help
help:
	@echo "Write in the form make <target> VENV=<name_env>"
	@echo "List of targets:"
	@echo "	clean			delete __pycache__/, .pytest_cache/"
	@echo "	tests 			run all the tests in the tests/"
	@echo "	create_env		create new environment and install requirements.txt packages"
	@echo "	linter			run the pylint"

.ONESHELL:
create_env:
	virtualenv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

.PHONY: clean 
clean:
	find . \( -name '__pycache__' -o -name ".pytest_cache" \) -type d | xargs rm -fr
	
.PHONY: tests
.ONESHELL:
tests: 
	. $(VENV)/bin/activate
	python -m pytest tests/

.ONESHELL:
linter:
	. $(VENV)/bin/activate
	find ./src -type f -name "*.py" | xargs pylint 