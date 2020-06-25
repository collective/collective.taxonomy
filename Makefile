# convenience makefile to boostrap & run buildout
SHELL := /bin/bash

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
	bin/buildout

build-frontend:
	@echo "$(GREEN)==> Build Frontend$(RESET)"
	(cd src/collective/taxonomy/javascripts && yarn)
	(cd src/collective/taxonomy/javascripts && yarn build)

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
	(cd src/collective/taxonomy/javascripts && yarn start)

.PHONY: Test
test: code-analysis test-backend test-frontend  ## Test

code-analysis:
	@echo "$(green)==> Run static code analysis$(reset)"
	bin/code-analysis

test-backend:
	@echo "$(GREEN)==> Run Backend Tests$(RESET)"
	bin/test --all

test-frontend:
	@echo "$(GREEN)==> Run Frontend Tests$(RESET)"
	(cd src/collective/taxonomy/javascripts && yarn test)

.PHONY: Clean
clean:  ## Clean
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	git clean -Xdf

.PHONY: all clean
