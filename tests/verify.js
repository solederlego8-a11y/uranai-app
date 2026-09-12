/* =========================================================================
 * tests/verify.js — docs/js/uranai.js を Python 版の正解データと突き合わせる
 *
 *   node tests/verify.js [--only case012,valid003] [--max-diffs 5] [--quiet]
 *
 *  tests/fixtures/cases.json（tests/gen_cases.py が生成）の
 *    cases            : buildReport(input, "ja") / buildReport(input, "en")
 *    validation_cases : validate(form, lang, { today: "2026-09-11" })
 *  を deep equal（キー順不問）で検証し、不一致はパス付きで差分表示する。
 *  終了コード: 全件 PASS なら 0、それ以外は 1。
 * ========================================================================= */
"use strict";

var fs = require("fs");
var path = require("path");

var ROOT = path.resolve(__dirname, "..");
var ENGINE = process.env.URANAI_JS || path.join(ROOT, "docs", "js", "uranai.js");
var FIXTURE = path.join(ROOT, "tests", "fixtures", "cases.json");
var VALIDATION_TODAY = "2026-09-11";

var args = process.argv.slice(2);
var only = null, maxDiffs = 5, quiet = false;
for (var i = 0; i < args.length; i++) {
  if (args[i] === "--only") { only = args[++i].split(","); }
  else if (args[i] === "--max-diffs") { maxDiffs = parseInt(args[++i], 10); }
  else if (args[i] === "--quiet") { quiet = true; }
}

var Uranai = require(ENGINE);
var fixture = JSON.parse(fs.readFileSync(FIXTURE, "utf8"));

function typeOf(v) {
  if (v === null) { return "null"; }
  if (Array.isArray(v)) { return "array"; }
  return typeof v;
}

function show(v) {
  var s = JSON.stringify(v);
  if (s === undefined) { s = String(v); }
  return s.length > 160 ? s.slice(0, 157) + "..." : s;
}

// 期待値 exp と実測 act の差分を [{path, expected, actual}] で返す（キー順は問わない）
function diff(exp, act, p, out) {
  if (out.length > 200) { return out; }
  var te = typeOf(exp), ta = typeOf(act);
  if (te !== ta) {
    out.push({ path: p, expected: show(exp), actual: show(act) + " (" + ta + ")" });
    return out;
  }
  if (te === "array") {
    if (exp.length !== act.length) {
      out.push({ path: p + ".length", expected: exp.length, actual: act.length });
    }
    var n = Math.min(exp.length, act.length);
    for (var i = 0; i < n; i++) { diff(exp[i], act[i], p + "[" + i + "]", out); }
    return out;
  }
  if (te === "object") {
    var ke = Object.keys(exp), ka = Object.keys(act);
    ke.forEach(function (k) {
      if (!Object.prototype.hasOwnProperty.call(act, k)) {
        out.push({ path: p + "." + k, expected: show(exp[k]), actual: "<missing>" });
      } else {
        diff(exp[k], act[k], p + "." + k, out);
      }
    });
    ka.forEach(function (k) {
      if (!Object.prototype.hasOwnProperty.call(exp, k)) {
        out.push({ path: p + "." + k, expected: "<absent>", actual: show(act[k]) });
      }
    });
    return out;
  }
  if (te === "number" ? !(exp === act || (isNaN(exp) && isNaN(act))) : exp !== act) {
    out.push({ path: p, expected: show(exp), actual: show(act) });
  }
  return out;
}

// gen_cases.py docstring の手順で英語版の完全な期待値を復元する
function fullEnglish(expectedJa, expectedEn) {
  var full = {};
  Object.keys(expectedJa).forEach(function (k) { full[k] = expectedJa[k]; });
  Object.keys(expectedEn).forEach(function (k) { full[k] = expectedEn[k]; });
  full.detail_results_en = expectedJa.detail_results.map(function (r, i) {
    var merged = {};
    Object.keys(r).forEach(function (k) { merged[k] = r[k]; });
    var en = expectedEn.detail_results_en[i] || {};
    Object.keys(en).forEach(function (k) { merged[k] = en[k]; });
    return merged;
  });
  return full;
}

function report(label, diffs, failures) {
  if (!diffs.length) { return; }
  failures.push(label);
  if (quiet) { return; }
  console.log("FAIL " + label + " (" + diffs.length + " diff" + (diffs.length > 1 ? "s" : "") + ")");
  diffs.slice(0, maxDiffs).forEach(function (d) {
    console.log("    " + d.path);
    console.log("      expected: " + d.expected);
    console.log("      actual:   " + d.actual);
  });
  if (diffs.length > maxDiffs) {
    console.log("    ... " + (diffs.length - maxDiffs) + " more");
  }
}

function selected(id) { return !only || only.indexOf(id) >= 0; }

var pass = 0, failures = [], errors = 0;

fixture.cases.forEach(function (c) {
  if (!selected(c.id)) { return; }
  ["ja", "en"].forEach(function (lang) {
    var label = c.id + " [" + lang + "]";
    var expected = lang === "ja" ? c.expected_ja : fullEnglish(c.expected_ja, c.expected_en);
    var actual;
    try {
      // buildReport は入力を書き換えない前提だが、念のためコピーを渡す
      actual = Uranai.buildReport(JSON.parse(JSON.stringify(c.input)), lang);
    } catch (e) {
      errors++;
      failures.push(label);
      if (!quiet) { console.log("ERROR " + label + ": " + (e && e.stack || e)); }
      return;
    }
    var diffs = diff(expected, actual, "report", []);
    if (diffs.length) { report(label, diffs, failures); } else { pass++; }
  });
});

(fixture.validation_cases || []).forEach(function (v) {
  if (!selected(v.id)) { return; }
  var label = v.id + " [validate " + v.lang + "]";
  var actual;
  try {
    var r = Uranai.validate(JSON.parse(JSON.stringify(v.form)), v.lang, { today: VALIDATION_TODAY });
    actual = { user_data: r.userData === undefined ? null : r.userData, error: r.error === undefined ? null : r.error };
  } catch (e) {
    errors++;
    failures.push(label);
    if (!quiet) { console.log("ERROR " + label + ": " + (e && e.stack || e)); }
    return;
  }
  var diffs = diff(v.expected, actual, "validate", []);
  if (diffs.length) { report(label, diffs, failures); } else { pass++; }
});

var total = pass + failures.length;
console.log("");
console.log("engine : " + ENGINE);
console.log("fixture: " + fixture.generated_by + " (" + fixture.cases.length + " cases, " +
  (fixture.validation_cases || []).length + " validation cases)");
console.log("RESULT : PASS " + pass + " / FAIL " + failures.length + " / TOTAL " + total +
  (errors ? " (" + errors + " threw)" : ""));
if (failures.length && quiet) {
  console.log("failed : " + failures.slice(0, 40).join(", ") + (failures.length > 40 ? " ..." : ""));
}
process.exit(failures.length ? 1 : 0);
