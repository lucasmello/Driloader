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
	@echo "[venv] Creating virtual env from default python3 installation."
	virtualenv -p $(PYTHON_EXE) venv

# Install packages from requirements.txt
install: venv
	@echo "[install] Installing requirements."
	@( \
		source $(VENV_PATH); \
		pip install -r requirements.txt; \
	)

# Run tests with pytest
test: install
	@echo "[test] Running unit tests."
	@( \
		source $(VENV_PATH); \
		pytest -s --verbose ./tests; \
	)

# Remove build files
clean:
	@echo "[clean] Removing build files."
	@echo "TBD"

# Remove virtual env
del-venv:
	@echo "[del-venv] Removing virtual env"
	rm -rv ./$(VENV_NAME)

# Display this help
help:
	@ echo
	@ echo '  Usage:'
	@ echo ''
	@ echo '    make <target> [flags...]'
	@ echo ''
	@ echo '  Targets:'
	@ echo ''
	@ awk '/^#/{ comment = substr($$0,3) } comment && /^[a-zA-Z][a-zA-Z0-9_-]+ ?:/{ print "   ", $$1, comment }' ./Makefile | column -t -s ':' | sort
	@ echo ''
	@ echo '  Flags:'
	@ echo ''
	@ awk '/^#/{ comment = substr($$0,3) } comment && /^[a-zA-Z][a-zA-Z0-9_-]+ ?\?=/{ print "   ", $$1, $$2, comment }' ./Makefile | column -t -s '?=' | sort
	@ echo ''
