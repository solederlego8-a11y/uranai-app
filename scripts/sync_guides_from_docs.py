# -*- coding: utf-8 -*-
"""docs/（GitHub Pages 静的版）のガイド記事から、Flask 版に無い拡充セクションを抽出して
uranai/guides_extra.py を生成する。

docs/guides/*.html と docs/en/guides/*.html は extend_article.py 等で直接拡充されており、
uranai/guides.py・guides_en.py（Render/Flask 版のデータ源）と乖離していた。
このスクリプトで両者を同期し、Render 側でも同じ本文が配信されるようにする。

使い方:
    python scripts/sync_guides_from_docs.py
"""
from __future__ import annotations

import html as _html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from uranai.guides import GUIDES  # noqa: E402
from uranai.guides_en import GUIDES_EN  # noqa: E402

SECTION_RE = re.compile(
    r'<section class="guide-section" id="section-(\d+)">(.*?)</section>',
    re.S,
)
HEADING_RE = re.compile(r'<h2 class="guide-heading">(.*?)</h2>', re.S)
TAG_RE = re.compile(r"<[^>]+>")


def _norm(s: str) -> str:
    return re.sub(r"\s+", "", _html.unescape(TAG_RE.sub("", s)))


def extract_extra(html: str, existing_headings: list[str]) -> list[dict]:
    known = {_norm(h) for h in existing_headings}
    extras = []
    for _sid, inner in SECTION_RE.findall(html):
        m = HEADING_RE.search(inner)
        if not m:
            continue
        heading = m.group(1).strip()
        if _norm(heading) in known:
            continue
        body = inner[m.end():].strip()
        extras.append({"heading": heading, "html": body})
    return extras


def build(lang: str, guides: list[dict], subdir: str) -> dict:
    out = {}
    for g in guides:
        path = os.path.join(ROOT, "docs", subdir, "%s.html" % g["slug"])
        if not os.path.exists(path):
            print("skip (no docs file):", path)
            continue
        with open(path, encoding="utf-8") as f:
            html = f.read()
        extras = extract_extra(html, [s["heading"] for s in g["sections"]])
        out[g["slug"]] = extras
        total = len(_norm(g["lead"])) + sum(
            len(_norm(p)) for s in g["sections"] for p in s["paragraphs"]
        ) + sum(len(_norm(e["heading"] + e["html"])) for e in extras)
        print("%s %-14s +%2d sections  ~%d chars" % (lang, g["slug"], len(extras), total))
    return out


def main() -> None:
    ja = build("ja", GUIDES, "guides")
    en = build("en", GUIDES_EN, os.path.join("en", "guides"))
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""docs/ から同期した拡充セクション（自動生成・手編集禁止）',
        "",
        "再生成: python scripts/sync_guides_from_docs.py",
        '"""',
        "from __future__ import annotations",
        "",
        "EXTRA_SECTIONS = {",
    ]
    for lang, data in (("ja", ja), ("en", en)):
        lines.append("    %r: {" % lang)
        for slug, extras in data.items():
            lines.append("        %r: [" % slug)
            for e in extras:
                lines.append("            {")
                lines.append("                %r: %r," % ("heading", e["heading"]))
                lines.append("                %r: %r," % ("html", e["html"]))
                lines.append("            },")
            lines.append("        ],")
        lines.append("    },")
    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append("def get_extra_sections(lang: str, slug: str) -> list[dict]:")
    lines.append("    return EXTRA_SECTIONS.get(lang, {}).get(slug, [])")
    lines.append("")
    target = os.path.join(ROOT, "uranai", "guides_extra.py")
    with open(target, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print("wrote", target)


if __name__ == "__main__":
    main()
