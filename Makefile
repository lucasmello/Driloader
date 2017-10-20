# Change the default python binary. Default value is '/usr/bin/python3'
PYTHON_EXE ?= /usr/bin/python3

# Change virtual env name. Default value is 'venv'
VENV_NAME ?= venv

# Change the default python binary
VENV_PATH = ./$(VENV_NAME)/bin/activate

# The shell make should use
SHELL = /bin/bash


# Used when make is called with no target
default: help


# Create virtual env
venv:
	@echo '[venv] Creating virtual env from default python3 installation.'
	virtualenv -p $(PYTHON_EXE) venv
	@echo


# Remove virtual env
delvenv:
	@echo '[delvenv] Removing virtual env.'
	rm -rf ./$(VENV_NAME)
	@echo


# Install packages from requirements.txt
install: venv
	@echo '[install] Installing requirements.'
	$(call run_in_venv, pip install -r requirements.txt)
	@echo


# Run tests with pytest
test: install
	@echo '[test] Running unit tests.'
	$(call run_in_venv,pytest -s --verbose --durations=5 ./tests)
	@echo


# Run pylint
lint: install
	@echo '[pylint] Running linter.'
	$(call run_in_venv, python lint.py)
	@echo


# Create egg from source
build: install
	@echo '[build] Creating Python egg from source.'
	$(call run_in_venv, python setup.py install)
	@echo


# Remove build files
clean:
	@echo '[clean] Removing build files.'
	rm -rf build/ driloader.egg-info/
	@echo


# Sort imports as PEP8
isort: install
	@echo '[isort] Sorting imports following PEP8'
	$(call run_in_venv, isort **/*.py)
	@echo


# Display this help
help:
	@ echo
	@ echo '  Usage:'
	@ echo ''
	@ echo '	make <target> [flags...]'
	@ echo ''
	@ echo '  Targets:'
	@ echo ''
	@ awk '/^#/{ comment = substr($$0,3) } comment && /^[a-zA-Z][a-zA-Z0-9_-]+ ?:/{ print "   ", $$1, comment }' ./Makefile | column -t -s ':' | sort
	@ echo ''
	@ echo '  Flags:'
	@ echo ''
	@ awk '/^#/{ comment = substr($$0,3) } comment && /^[a-zA-Z][a-zA-Z0-9_-]+ ?\?=/{ print "   ", $$1, $$2, comment }' ./Makefile | column -t -s '?=' | sort
	@ echo ''

# Function to abastract virtual env calls inside bash
define run_in_venv
	@( \
		source $(VENV_PATH); \
		$(1); \
	)
endef
