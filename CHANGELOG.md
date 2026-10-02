# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
this project aims to follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Support · 1,99 € link in the picker footer (English and Spanish) and a README badge.
- **20 stack presets** (was 2): Modern CLI, Dev Stack, Fast Path, Git Power,
  Cloud Native, Container Ops, Infra as Code, Data Wrangler, Python/Node/Rust/Go
  Dev, Observability, Search & Nav, Editor TUI, Shell Sugar, Docs Writer,
  Security, Network, Media. Preset total 121 → 139.
- Stacks now wire up **shell integration**: a `# >>> iterm-studio tools >>>`
  block in `~/.zshrc` with `eval "$(… init zsh)"` hooks (zoxide, atuin, fzf,
  direnv, pyenv, fnm) and aliases (`ls`→eza, `cat`→bat, `top`→btop, …), each
  guarded so an uninstalled tool is a no-op. Applied whether or not
  `--with-tools` runs `brew install`; removed when you switch to a plain theme.
- `TOOLS` allow-list expanded from 14 to ~70 Homebrew formulae.

### Fixed
- Repeated apply/switch no longer accumulates blank lines in `~/.zshrc` /
  `~/.p10k.zsh` (`_tidy` collapses 3+ newlines on every managed write).

## [1.0.0] — 2026-08-31

### Added
- **121 presets** across six families (dark, light, warm, neon, mono, stacks) —
  well-known schemes (Tokyo Night, Catppuccin, Rosé Pine, Gruvbox, Kanagawa,
  Nightfox, Dracula, Nord, Solarized, Ayu, Material, GitHub, …) plus ~55
  procedurally-generated single-hue palettes.
- `iterm-studio serve` — a loopback web app where **one click applies a style
  for real** (no copy-paste). Random per-run token + Host/Origin allow-list.
- `iterm-studio apply <id> [--with-tools] [--set-default]`, `revert`, `list`,
  `current`, `version`.
- Applies as a self-contained set: an iTerm2 Dynamic Profile named **Studio**,
  a marked block in `~/.p10k.zsh` (prompt shape + palette), and a marked block
  in `~/.zshrc` (syntax-highlight + autosuggest colours). Full `revert`.
- Five Powerlevel10k prompt shapes: `lean2`, `powerline`, `pill`, `minimal`,
  `rainbow`, with a right-aligned command-execution-time segment.
- Picker UI: live search, category filters with counts, per-viewer language
  (English / Español), keyboard-accessible controls, `prefers-reduced-motion`
  and `prefers-color-scheme` support, consistent one-session preview per card.
- **Power-ups** shelf — starship, eza, bat, fzf, zoxide, atuin, git-delta,
  tmux, btop, tlrc, thefuck, nerd-fonts — one-click install in `serve` mode.
- CI: ruff + `py_compile`, preset build-drift check, structural preset tests,
  and an `app.html` JavaScript syntax check.

[Unreleased]: https://example.com/compare/v1.0.0...HEAD
[1.0.0]: https://example.com/releases/tag/v1.0.0
