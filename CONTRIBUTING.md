# Contributing

## Layout

| File | Role |
|---|---|
| `iterm-studio` | CLI + loopback server. Python 3.9+, standard library only. |
| `build.py` | **source of truth** for presets → writes `presets.json` + `presets.js`. |
| `presets.json` / `presets.js` | generated; commit them, but never hand-edit. |
| `app.html` | picker UI template. `__MODE__`, `__TOKEN__`, `/*__PRESETS__*/[]` are filled at serve time. |
| `tests/` | run by CI and locally. |

## Adding a preset

Edit `build.py` only.

- **A known scheme:** add a `P(id, name, category, flavor, "<fg bg cur curT sel selT>", "<16 ansi>")`
  line in the curated block. All colours are 6-hex, no `#`.
- **A generated family:** add a tuple to `GEN` (`id, name, category, flavor, baseHue, mode, saturation, tint`).
- Add a one-line entry to `BLURB`.
- `category` ∈ `dark light warm neon mono stack`; `flavor` ∈ `lean2 powerline pill minimal rainbow`.

Then:

```bash
python3 build.py            # regenerates presets.json / presets.js
python3 -m unittest discover -s tests -v
```

Commit `build.py` **and** the regenerated `presets.json` / `presets.js` together —
CI fails if they are out of sync.

## Before opening a PR

```bash
ruff check .                       # or: python3 -m py_compile iterm-studio build.py
python3 -m unittest discover -s tests -v
node tests/check_app_js.mjs
```

## Manual smoke test

```bash
./iterm-studio serve --port 8787
# click Apply on a card, then `iterm-studio revert`
```

## Style

- Python: ruff defaults, 4-space indent, standard library only in `iterm-studio`
  (it must run on a clean macOS with no `pip install`).
- No new runtime dependencies without discussion.
