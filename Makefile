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
	$(PYTHON_INTERPRETER) src/data/pull_data.py

model:
	$(PYTHON_INTERPRETER) src/models/make_model.py

api:
	export FLASK_APP="regression_api" && cd src/api && $(PYTHON_INTERPRETER) -m flask run

all: data model

# HELPERS #####################################################################
test_api:
	$(PYTHON_INTERPRETER) src/api/test_requests.py

format:
	venv/bin/python -m black src/*.py

clean:
	rm -f data/external/*.csv
	rm -f data/interim/*.csv
	rm -f data/processed/*.csv
	rm -f data/raw/*.csv
	rm -f models/*.pickle
	rm -rf transportationhubpipeline
