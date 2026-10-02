"""Structural tests for the preset catalogue and the page renderer.

Run:  python3 -m unittest discover -s tests -v
"""
import importlib.machinery
import importlib.util
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent

# import the extension-less `iterm-studio` script as a module
_loader = importlib.machinery.SourceFileLoader("iterm_studio", str(ROOT / "iterm-studio"))
_spec = importlib.util.spec_from_loader("iterm_studio", _loader)
its = importlib.util.module_from_spec(_spec)
_loader.exec_module(its)

HEX = re.compile(r"#[0-9a-f]{6}$")
CATS = {"dark", "light", "warm", "neon", "mono", "stack"}
FLAVORS = {"lean2", "powerline", "pill", "minimal", "rainbow"}


class Presets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "presets.json").read_text())
        cls.presets = cls.data["presets"]

    def test_count(self):
        self.assertGreaterEqual(len(self.presets), 100, "want at least 100 presets")

    def test_unique_ids(self):
        ids = [p["id"] for p in self.presets]
        self.assertEqual(len(ids), len(set(ids)), "preset ids must be unique")

    def test_id_slug_form(self):
        for p in self.presets:
            self.assertRegex(p["id"], r"^[a-z0-9]+(-[a-z0-9]+)*$", p["id"])

    def test_colours_are_hex(self):
        for p in self.presets:
            c = p["colors"]
            self.assertEqual(len(c["ansi"]), 16, f"{p['id']}: need 16 ansi colours")
            for key in ("fg", "bg", "cursor", "cursorText", "selection", "selectedText"):
                self.assertRegex(c[key], HEX, f"{p['id']}.{key}")
            for i, h in enumerate(c["ansi"]):
                self.assertRegex(h, HEX, f"{p['id']}.ansi[{i}]")

    def test_category_and_flavor(self):
        for p in self.presets:
            self.assertIn(p["category"], CATS, p["id"])
            self.assertIn(p["flavor"], FLAVORS, p["id"])

    def test_window_shape(self):
        for p in self.presets:
            w = p["window"]
            self.assertIsInstance(w["transparency"], (int, float))
            self.assertGreaterEqual(w["transparency"], 0)
            self.assertLess(w["transparency"], 1)
            self.assertGreaterEqual(w["blur"], 0)
            self.assertIn(w["cursor"], {"block", "bar", "underline"})

    def test_tools_are_known(self):
        for p in self.presets:
            for t in p["tools"]:
                self.assertIn(t, its.TOOLS, f"{p['id']} references unknown tool {t!r}")

    def test_stacks(self):
        stacks = [p for p in self.presets if p["category"] == "stack"]
        self.assertGreaterEqual(len(stacks), 20, "want at least 20 stack presets")
        for s in stacks:
            self.assertGreaterEqual(len(s["tools"]), 3, f"{s['id']}: a stack should bundle 3+ tools")
            self.assertEqual(len(s["tools"]), len(set(s["tools"])), f"{s['id']}: duplicate tool")

    def test_tool_hooks_reference_known_tools(self):
        for k in list(its.TOOL_INIT) + list(its.TOOL_ALIAS):
            self.assertIn(k, its.TOOLS, f"TOOL_INIT/ALIAS key {k!r} is not in TOOLS")

    def test_blurbs_present(self):
        missing = [p["id"] for p in self.presets if not p["blurb"].strip()]
        self.assertEqual(missing, [], f"presets without a blurb: {missing}")

    def test_presets_js_matches_json(self):
        js = (ROOT / "presets.js").read_text().strip()
        self.assertTrue(js.startswith("window.ITERM_STUDIO_PRESETS = "))
        self.assertTrue(js.endswith(";"))
        arr = json.loads(js[len("window.ITERM_STUDIO_PRESETS = "):-1])
        self.assertEqual(len(arr), len(self.presets))
        self.assertEqual([p["id"] for p in arr], [p["id"] for p in self.presets])


class Renderer(unittest.TestCase):
    def test_web_mode_strips_doc_wrapper(self):
        html = its.render_app("web")
        self.assertNotIn("__MODE__", html)
        self.assertNotIn("/*__PRESETS__*/[]", html)
        self.assertNotRegex(html[:200], r"(?i)<html")
        self.assertIn('MODE = "web"', html)
        self.assertIn("window.ITERM_STUDIO_PRESETS = [{", html)

    def test_local_mode_has_token_and_doctype(self):
        html = its.render_app("local", "deadbeef" * 4)
        self.assertTrue(html.lstrip().lower().startswith("<!doctype html>"))
        self.assertIn('MODE = "local"', html)
        self.assertIn("deadbeef" * 4, html)

    def test_app_template_markers_exist(self):
        tpl = (ROOT / "app.html").read_text()
        for marker in ("__MODE__", "__TOKEN__", "/*__PRESETS__*/[]"):
            self.assertIn(marker, tpl)

    def test_support_link(self):
        tpl = (ROOT / "app.html").read_text()
        m = re.search(r'<a\b[^>]*\bid="support"[^>]*>([^<]*)</a>', tpl)
        self.assertIsNotNone(m, "support link missing from app.html footer")
        tag = m.group(0)
        self.assertIn('href="https://marcfors.com/donate?from=iterm-studio"', tag)
        self.assertIn('target="_blank"', tag)
        self.assertIn('rel="noopener noreferrer"', tag)
        self.assertEqual(m.group(1), "Support \u00b7 1,99 \u20ac")
        # every shipped locale carries a translated label
        self.assertIn('support:"Support \u00b7 1,99 \u20ac"', tpl)
        self.assertIn('support:"Apoyar \u00b7 1,99 \u20ac"', tpl)


if __name__ == "__main__":
    unittest.main()
