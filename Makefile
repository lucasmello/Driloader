# Used when make is called with no target
default: help

# Install packages from Pipfile
install:
	pipenv install --dev

# Run tests with pytest
test:
	pytest -s --verbose --durations=5 ./tests


# Run tests with pytest and coverage
test-cov:
	pytest -s --verbose --cov-report term-missing --cov=driloader ./tests

# Run pylint
lint:
	python lint.py


# Create egg from source
build:
	python setup.py install


# Remove build files
clean:
	rm -rf build/ driloader.egg-info/


# Sort imports as PEP8
isort:
	isort **/*.py


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

