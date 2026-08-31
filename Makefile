.PHONY: help serve build test lint link clean

BIN := $(HOME)/.local/bin/iterm-studio

help:
	@echo "make link    symlink ./iterm-studio into ~/.local/bin"
	@echo "make serve   run the one-click picker (http://127.0.0.1:8787)"
	@echo "make build   regenerate presets.json / presets.js from build.py"
	@echo "make test    run unit tests + app.html JS syntax check"
	@echo "make lint    ruff (if installed) + py_compile"

link:
	@mkdir -p $(HOME)/.local/bin
	@ln -sf "$(CURDIR)/iterm-studio" "$(BIN)"
	@echo "linked $(BIN) -> $(CURDIR)/iterm-studio"

serve:
	@./iterm-studio serve

build:
	@python3 build.py

test:
	@python3 -m unittest discover -s tests -v
	@node tests/check_app_js.mjs

lint:
	@ruff check . 2>/dev/null || echo "(ruff not installed — skipping)"
	@python3 -m py_compile iterm-studio build.py tests/test_presets.py && echo "py_compile OK"

clean:
	@find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .ruff_cache
