PYTHON_VERSION ?= 3.10.0 # Default Python version
VENV_NAME ?= venv-gfv2
PYENV_ROOT := $(HOME)/.pyenv
PATH := $(PYENV_ROOT)/bin:$(PATH)
VENV_ROOT := ${HOME}/.pyenv/versions/${VENV_NAME}
VENV_PIP := ${VENV_ROOT}/bin/pip
VENV_PYTHON3_EXECUTABLE := ${VENV_ROOT}/bin/python3

export PYENV_ROOT PATH

.PHONY: venv install test run clean help

venv: # creates python virtual environment.
	pyenv local $(PYTHON_VERSION)
	pyenv virtualenv $(VENV_NAME)
	@echo "virtualenv created for the project ."
	@echo "\t- name: $(VENV_NAME)"
	@echo "Please activate it before proceeding ahead ."
	@echo "\t- command: 'pyenv activate $(VENV_NAME)'"

install: # install all the required dependencies.
	$(VENV_PIP) install -r requirements.py3.10._.txt

test: check-env # executes all the tests. # -- not yet configured
	# No Test Configurantion . Need to add .

run: # starts the project
	$(VENV_PYTHON3_EXECUTABLE) app.py
run-combined: # starts the project in combination with ui application
	$(VENV_PYTHON3_EXECUTABLE) app.py --execute combined

setup: venv install # executes setup on your machine.

all: setup test run # executing complete setup , test & run from scratch.

soft-clean: # only cleaning the temporary & cache files
	bash -c "find . -type d -name "__pycache__" -print0 | xargs -0 rm -rf"
	bash -c "find . -type f -name "*.pyc" -print0 | xargs -0 rm -f"
	bash -c "find . -type f -name "*.pyo" -print0 | xargs -0 rm -f"

clean: soft-clean # completely cleaning the additional resources created for execution on your system.
	pyenv virtualenv-delete $(VENV_NAME)
	pyenv local --unset

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done


check-env: .env
	@ echo "checking for .env file ..."

	@ ## | --- check for existance of '.env' file --- | ##

	@if [ -s .env ]; then \
		echo "\t - successfully found '.env' file"; \
	else \
		echo -e "\e[31m .env file not exists. Please create it from .env.template file \e[0m"; \
		exit 0; \
	fi \
	
	@ ## 

	@ ## | --- check for important variables in environment file --- | ##

	@ # DEBUG < .env variable #
	@ # NOT WORKING : ^DEBUG[ \t]*=[ \t]*[a-zA-Z0-9\"\@\!\#\$\%\^\&\*\(\)\_\-\=\+\[\]\{\}\:\;|'\/\.\,\?\\]+

	@if grep -Eq "^DEBUG[ \t]*=[ \t]*[a-zA-Z]+" ".env"; then \
		continue; \
	else \
		echo -e "\e[31m Varibale 'DEBUG' not-found / in-valid in .env file \e[0m"; \
		exit 1; \
	fi \

	@ # PORT < .env variable #
	@if grep -Eq "^PORT[ \t]*=[ \t]*[0-9]+$\" ".env"; then \
		continue; \
	else \
		echo -e "\e[31m Varibale 'PORT' not-found / in-valid in .env file \e[0m"; \
		exit 1; \
	fi \

	@echo "\t - successfully scanned '.env' file for all required env variables"
	@ ## | -------------------------------------------------------- | ##
