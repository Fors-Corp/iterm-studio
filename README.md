# iTerm Studio

Pick a terminal look from **121 presets** and apply it to this Mac — colours,
transparency, blur, cursor, font, and a matching Powerlevel10k prompt — in one
click.

**Browse all 121 → https://marcfs31.github.io/iterm-studio/**

[![CI](https://github.com/marcfs31/iterm-studio/actions/workflows/ci.yml/badge.svg)](https://github.com/marcfs31/iterm-studio/actions/workflows/ci.yml)
[![Pages](https://github.com/marcfs31/iterm-studio/actions/workflows/pages.yml/badge.svg)](https://github.com/marcfs31/iterm-studio/actions/workflows/pages.yml)

The hosted page is the read-only gallery — each **Apply** copies the exact
command. For real one-click applying, run `iterm-studio serve` locally (below).

## Quick start

```bash
make link          # symlink ./iterm-studio into ~/.local/bin (once)
iterm-studio serve  # opens http://127.0.0.1:8787 in your browser
```

Click a card's **Apply**. It runs for real — no copy-paste. Keep the terminal
open while you experiment; `Ctrl-C` stops the server.

The picker has live search, category filters (dark / light / warm / neon / mono /
stacks), and an English / Español toggle. Every preview shows the *same* shell
session so you're comparing colour, not content.

### Command line

```bash
iterm-studio list
iterm-studio apply kanagawa
iterm-studio apply dev-stack --with-tools      # also `brew install`s the toolbelt
iterm-studio apply tokyo-night --set-default   # make "Studio" the default iTerm profile
iterm-studio revert
iterm-studio current
iterm-studio version
```

## What "apply" changes

| Target | What |
|---|---|
| `~/Library/Application Support/iTerm2/DynamicProfiles/iterm-studio.json` | an iTerm2 profile named **Studio** — 16 ANSI colours + fg/bg/cursor/selection, transparency, blur, cursor shape, font, unlimited scrollback |
| `~/.p10k.zsh` | a block between `# >>> iterm-studio prompt >>>` markers — prompt shape (`lean2` / `powerline` / `pill` / `minimal` / `rainbow`) + palette + a `command_execution_time` segment |
| `~/.zshrc` | a block between `# >>> iterm-studio shell >>>` markers — zsh-syntax-highlighting + autosuggestion colours to match |

Colours show once you select the **Studio** profile in iTerm (⌘I), or pass
`--set-default`. The prompt updates on the next new shell (`exec zsh`).

`iterm-studio revert` deletes the profile and both managed blocks and restores
the previous default-profile GUID. Your original `~/.p10k.zsh` is also kept at
`~/.p10k.zsh.iterm-studio-orig`.

## Power-ups

The picker also has a shelf of standalone tools — starship, eza, bat, fzf,
zoxide, atuin, git-delta, tmux, btop, tlrc, thefuck, nerd-fonts — each a
one-click `brew install` in `serve` mode.

## Local server security

Binds `127.0.0.1` only. Every `/api/*` call needs a random per-run token
embedded in the served page, plus a `Host` / `Origin` allow-list (DNS-rebinding
guard). Preset ids and tool names are allow-listed. The server runs only while
you keep it open.

## Development

```bash
make build    # regenerate presets.json / presets.js  (edit build.py, never the JSON)
make test     # unit tests + app.html JS syntax check
make lint     # ruff + py_compile
```

See [CONTRIBUTING.md](CONTRIBUTING.md). Standard library only — `iterm-studio`
must run on a clean macOS with no `pip install`.

## Files

| File | Role |
|---|---|
| `iterm-studio` | CLI + local one-click server (Python 3.9+, stdlib only) |
| `build.py` | source of truth for the 121 presets |
| `presets.json` / `presets.js` | generated — committed, never hand-edited |
| `app.html` | the picker UI (`__MODE__` = `local` when served, `web` when published) |
| `tests/` | run by CI (`.github/workflows/ci.yml`) and `make test` |

## License

[MIT](LICENSE) © 2026 Marc Fors
