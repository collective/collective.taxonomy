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


# Acceptance tests: start the backend first, with
# `make acceptance-backend-start` in the repository root.
.PHONY: install-acceptance
install-acceptance: stamp-pnpm
	$(PNPM) exec playwright install --with-deps chromium


.PHONY: acceptance-test
acceptance-test: stamp-pnpm
	$(PNPM) exec playwright test --ui


.PHONY: ci-acceptance-test
ci-acceptance-test: stamp-pnpm
	PLAYWRIGHT_HTML_OPEN=never $(PNPM) exec playwright test --reporter=list,html


.PHONY: clean
clean:
	rm -rf node_modules build stamp-pnpm playwright-report acceptance/results pnpm-debug.log
