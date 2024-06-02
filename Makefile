###############################################################################
# Makefile
###############################################################################

PROJECTDIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PYTHON_INTERPRETER = $(PROJECTDIR)/venv/bin/python

.PHONY: env format data model

# FUNCTIONS ###################################################################
env:
	rm -rf venv/
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

data:
	$(PYTHON_INTERPRETER) src/pull_data.py

model:
	$(PYTHON_INTERPRETER) src/make_model.py

deploy:
	export FLASK_APP="regression_api" && cd src && $(PYTHON_INTERPRETER) -m flask run

all: data model

# HELPERS #####################################################################
format:
	venv/bin/python -m black src/*.py

clean:
	rm data/*.csv
	rm models/*.pickle
