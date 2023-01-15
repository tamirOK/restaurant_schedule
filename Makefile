.DEFAULT: help
.PHONY: help

VENV=.venv
PYTHON=$(VENV)/bin/python3

help:
	@echo "Please use one of the following commands:"
	@echo "   help - show help information"
	@echo "   test - run project tests"
	@echo "   run  - run project locally"
	@echo "   lint - run flake8 linter"

bootstrap: $(VENV)/bin/activate
$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install setuptools==65.5.0 wheel==0.38.4
	$(PYTHON) -m pip install -e .[dev,test]

test: bootstrap
	$(PYTHON) -m pytest tests

run: bootstrap
	$(PYTHON) -m api

lint:
	$(PYTHON) -m flake8 api tests

clean:
	rm -rf .venv .pytest_cache restaurant_schedule.egg-info
