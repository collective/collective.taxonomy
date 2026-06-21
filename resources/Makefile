# Taxonomy JS Development

PNPM   ?= pnpm


.PHONY: install
stamp-pnpm install:
	$(PNPM) install
	touch stamp-pnpm


.PHONY:
build: stamp-pnpm
	$(PNPM) run build


.PHONY:
serve: stamp-pnpm
	$(PNPM) run start


.PHONY:
test: stamp-pnpm
	$(PNPM) run test


.PHONY:
lint: stamp-pnpm
	$(PNPM) run lint


.PHONY: clean
clean:
	rm -rf node_modules build stamp-pnpm cypress/screenshots pnpm-debug.log
