.PHONY: all validate generate export build-site test audit discover serve

all: generate validate test

generate:
	python3 scripts/validate_catalog.py --fix-order
	python3 scripts/generate_badges.py
	python3 scripts/generate_docs.py
	python3 scripts/export_catalog.py
	python3 scripts/build_site.py

validate:
	python3 scripts/validate_catalog.py --check-sync --strict-warnings
	python3 scripts/build_site.py --check
	python3 scripts/export_catalog.py --check

export:
	python3 scripts/export_catalog.py

build-site:
	python3 scripts/build_site.py

test:
	python3 -m unittest discover -s tests -v
	node --check docs/catalog-logic.js
	node --check docs/insights.js
	node --check docs/app.js
	node --test tests/test_web.mjs

audit:
	python3 scripts/health-check.py --use-gh-cli
	$(MAKE) generate

discover:
	python3 scripts/discover_candidates.py --use-gh-cli --limit 15

serve:
	python3 -m http.server 8765 --directory docs
