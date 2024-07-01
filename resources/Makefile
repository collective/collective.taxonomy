# Taxonomy JS Development

YARN   ?= npx yarn


.PHONY: install
stamp-yarn install:
	$(YARN) install
	touch stamp-yarn


.PHONY:
build: stamp-yarn
	$(YARN) run build


.PHONY:
serve: stamp-yarn
	$(YARN) run start


.PHONY:
test: stamp-yarn
	$(YARN) run test


.PHONY:
lint: stamp-yarn
	$(YARN) run lint
