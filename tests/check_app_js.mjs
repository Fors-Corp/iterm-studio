// Parses the <script> in app.html to catch syntax errors in CI.
// Usage:  node tests/check_app_js.mjs
import { readFileSync } from "node:fs";
import vm from "node:vm";

const html = readFileSync(new URL("../app.html", import.meta.url), "utf8");
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) {
  console.error("check_app_js: no <script> block found in app.html");
  process.exit(1);
}

const src = m[1]
  .replace("__MODE__", "web")
  .replace("__TOKEN__", "")
  .replace("/*__PRESETS__*/[]", "[]");

try {
  new vm.Script(src, { filename: "app.html#script" });
} catch (e) {
  console.error("check_app_js: syntax error —", e.message);
  process.exit(1);
}
console.log("check_app_js: OK");
