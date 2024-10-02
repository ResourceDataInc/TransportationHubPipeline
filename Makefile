#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = TransportationHubPipeline
PYTHON_VERSION = 3.10
SYSTEM_PYTHON_INTERPRETER = python3
PYTHON_INTERPRETER = $(shell pwd)/venv/bin/python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

# SETUP #########################################################################
## Set up python interpreter environment
.PHONY: env
env:
	rm -rf venv/
	$(SYSTEM_PYTHON_INTERPRETER) -m venv venv
	venv/bin/pip install -r requirements.txt

## Install python dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt


# WORKFLOW ######################################################################
## Pull data down from Snowflake
.PHONY: data
data:
	rm -rf data
	mkdir -p data/external
	mkdir -p data/interim
	mkdir -p data/processed
	mkdir -p data/raw
	$(PYTHON_INTERPRETER) $(shell pwd)/transportationhubpipeline/data/make_dataset.py

## Build the machine learning models
.PHONY: train
train:
	$(PYTHON_INTERPRETER) $(shell pwd)/transportationhubpipeline/models/train_model.py

## Deploy a machine learning model to a local API
.PHONY: deploy
deploy:
	export FLASK_APP="predict_model" && cd $(shell pwd)/transportationhubpipeline/models && $(PYTHON_INTERPRETER) -m flask run

## Delete generated files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find data/raw/ -type f -name "*.csv" -delete
	find models/ -type f -name "*.pickle" -delete
	find models/ -type d -name "__pycache__" -delete


# CODE QUALITY ##################################################################
## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 transportationhubpipeline
	isort --check --diff --profile black transportationhubpipeline
	black --check --config pyproject.toml transportationhubpipeline

## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml transportationhubpipeline

## Expand requirements.txt with any new libraries
.PHONY: req
req:
	venv/bin/pip freeze > requirements.txt

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
