"""Render the static (web-mode) picker into ./site for GitHub Pages.

Reuses render_app() from the `iterm-studio` script so the hosted page and the
`iterm-studio serve` page never drift.
"""
import importlib.machinery
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

_loader = importlib.machinery.SourceFileLoader("iterm_studio", str(ROOT / "iterm-studio"))
_spec = importlib.util.spec_from_loader("iterm_studio", _loader)
its = importlib.util.module_from_spec(_spec)
_loader.exec_module(its)

site = ROOT / "site"
site.mkdir(exist_ok=True)
(site / "index.html").write_text(its.render_app("web", full_document=True))
(site / ".nojekyll").write_text("")  # serve files starting with _ and skip Jekyll

n = len(its.DATA["presets"])
print(f"wrote site/index.html — {n} presets, {(site / 'index.html').stat().st_size} bytes")
