# convenience makefile to boostrap & run buildout
SHELL := /bin/bash
# Run test if not on Travis or Python 3 and Plone 5.2
NOT_TRAVIS_OR_PYTHON3_PLONE52 := $(shell if [ -z "$$TRAVIS" ] || ([ "$$PLONE_VERSION" == "5.2" ] && [ "$$TRAVIS_PYTHON_VERSION" == "3.7" ]); then echo "true"; else echo "false"; fi)

version = 3

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help:  ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: Build
build: build-backend build-frontend  ## Build

build-backend:
	@echo "$(GREEN)==> Setup Build$(RESET)"
	virtualenv --clear --python=python3 .
	bin/pip install --upgrade pip
	bin/pip install -r requirements.txt
ifeq ("$(NOT_TRAVIS_OR_PYTHON3_PLONE52)", "true")
	bin/pip install black
endif
	bin/buildout

build-frontend:
	@echo "$(GREEN)==> Build Frontend$(RESET)"
	cd src/collective/taxonomy/javascripts && yarn
	cd src/collective/taxonomy/javascripts && yarn build

.PHONY: Start
start:  ## Start
	if [ "$$(command -v tmux)" ]; then               \
		tmux new-session "make start-backend"     \; \
			split-window -h "make start-frontend" \; \
			select-pane -t 0;                        \
	else                                             \
		make start-backend;                          \
	fi

start-backend:
	@echo "$(GREEN)==> Start Plone Backend$(RESET)"
	NODE_ENV=development bin/instance fg

start-frontend:
	@echo "$(GREEN)==> Start Webpack Watcher$(RESET)"
	cd src/collective/taxonomy/javascripts && yarn start

.PHONY: Start Cypress
start-cypress:  ## Start Cypress
	@echo "$(GREEN)==> Start Cypress$(RESET)"
	bin/instance start && while ! nc -z localhost 8080; do sleep 1; done
	cd src/collective/taxonomy/javascripts && yarn run cypress open
	bin/instance stop

.PHONY: Test
test: code-format-check code-analysis test-backend test-frontend test-cypress  ## Test

.PHONY: Code Format Check
code-format-check: code-format-check-backend code-format-check-frontend  ## Code Format Check

code-format-check-backend:
	@echo "$(GREEN)==> Run Python code format check$(RESET)"
ifeq ("$(NOT_TRAVIS_OR_PYTHON3_PLONE52)", "true")
	bin/black --check src/
endif

code-format-check-frontend:
	@echo "$(GREEN)==> Run Javascript code format check$(RESET)"
	cd src/collective/taxonomy/javascripts && yarn prettier

.PHONY: Code Format
code-format: code-format-backend code-format-frontend  ## Code Format

code-format-backend:
	@echo "$(GREEN)==> Run Python code format$(RESET)"
	bin/black src/

code-format-frontend:
	@echo "$(GREEN)==> Run Javascript code format$(RESET)"
	cd src/collective/taxonomy/javascripts && yarn prettier:fix

code-analysis:
	@echo "$(green)==> Run static code analysis$(reset)"
ifeq ("$(NOT_TRAVIS_OR_PYTHON3_PLONE52)", "true")
	bin/code-analysis
endif

test-backend:
	@echo "$(GREEN)==> Run Backend Tests$(RESET)"
	bin/test --all

test-frontend:
	@echo "$(GREEN)==> Run Frontend Tests$(RESET)"
	cd src/collective/taxonomy/javascripts && yarn test

test-cypress:
	@echo "$(GREEN)==> Run Cypress Test$(RESET)"
ifeq ("$(NOT_TRAVIS_OR_PYTHON3_PLONE52)", "true")
	bin/instance start && while ! nc -z localhost 8080; do sleep 1; done
	cd src/collective/taxonomy/javascripts && yarn run cypress run --config video=false
	bin/instance stop
endif

test-cypress-foreground:
	@echo "$(GREEN)==> Run Cypress Test Displaying Browser$(RESET)"
	bin/instance start && while ! nc -z localhost 8080; do sleep 1; done
	cd src/collective/taxonomy/javascripts && yarn run cypress run --headed --no-exit
	bin/instance stop

.PHONY: Clean
clean:  ## Clean
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	git clean -Xdf

.PHONY: all clean
