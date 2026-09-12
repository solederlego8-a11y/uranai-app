# -*- coding: utf-8 -*-
"""占術ガイド記事（日本語11本・英語11本）と一覧ページを静的HTMLとして生成する。

    python scripts/build_guides.py

出力:
    docs/guides.html, docs/guides/<slug>.html
    docs/en/guides.html, docs/en/guides/<slug>.html
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from site_common import Links, esc, render_page, write_file  # noqa: E402
from uranai.guides import GUIDES  # noqa: E402
from uranai.guides_en import GUIDES_EN  # noqa: E402


def _related(guides: list, slug: str) -> list:
    """自分以外の記事を並び順に沿って4件（app.py guide_detail と同じ回転）。"""
    others = [g for g in guides if g["slug"] != slug]
    start = [g["slug"] for g in guides].index(slug)
    rotated = others[start:] + others[:start]
    return rotated[:4]


# ---------------------------------------------------------------- 日本語
def guide_page_ja(guide: dict) -> str:
    L = Links("guides")
    slug = guide["slug"]
    module = esc(guide["module"])

    toc = "".join(
        '      <li><a href="#section-%d">%s</a></li>\n' % (i, esc(s["heading"]))
        for i, s in enumerate(guide["sections"], 1))

    sections = ""
    for i, s in enumerate(guide["sections"], 1):
        paras = "".join('    <p class="guide-paragraph">%s</p>\n' % esc(p)
                        for p in s["paragraphs"])
        sections += (
            '  <section class="guide-section" id="section-%d">\n'
            '    <h2 class="guide-heading">%s</h2>\n'
            '%s'
            '  </section>\n' % (i, esc(s["heading"]), paras))

    related = ""
    for other in _related(GUIDES, slug):
        t = other["title"]
        label = t.split("｜")[1] if "｜" in t else t
        related += (
            '    <li>\n'
            '      <a href="%s">\n'
            '        <strong>%s</strong>\n'
            '        <span>%s</span>\n'
            '      </a>\n'
            '    </li>\n' % (L.guide(other["slug"]), esc(other["module"]), esc(label)))

    content = (
        '<nav class="breadcrumb" aria-label="パンくずリスト">\n'
        '  <a href="%(index)s">トップ</a>\n'
        '  <span aria-hidden="true">›</span>\n'
        '  <a href="%(guides)s">占術ガイド</a>\n'
        '  <span aria-hidden="true">›</span>\n'
        '  <span>%(module)s</span>\n'
        '</nav>\n'
        '\n'
        '<article class="card guide-article">\n'
        '  <p class="guide-tag">%(module)s</p>\n'
        '  <h1 class="guide-title">%(title)s</h1>\n'
        '  <p class="guide-lead">%(lead)s</p>\n'
        '\n'
        '  <nav class="guide-toc" aria-label="目次">\n'
        '    <p class="guide-toc-title">目次</p>\n'
        '    <ol>\n'
        '%(toc)s'
        '    </ol>\n'
        '  </nav>\n'
        '\n'
        '%(sections)s'
        '\n'
        '  <p class="guide-disclaimer">\n'
        '    ※本記事は占術の考え方を紹介するものであり、その内容について科学的根拠を保証するものではありません。\n'
        '    鑑定結果はエンターテインメントとしてお楽しみください。\n'
        '  </p>\n'
        '</article>\n'
        '\n'
        '<!-- ADSENSE_SLOT -->\n'
        '<div class="ad-container ad-guide">広告スペース</div>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">%(module)sを実際に鑑定してみる</h2>\n'
        '  <p>\n'
        '    当サイトの総合鑑定では、%(module)sを含む11種の占術をまとめて計算します。\n'
        '    5項目を入力するだけで、%(module)sの個別結果も「詳しく見る」から確認できます。\n'
        '  </p>\n'
        '  <a class="submit-button link-button" href="%(index)s">今日の総合鑑定を見る</a>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">ほかの占術の解説を読む</h2>\n'
        '  <ul class="guide-related">\n'
        '%(related)s'
        '  </ul>\n'
        '  <a class="guide-card-link" href="%(guides)s">占術ガイドの一覧へ</a>\n'
        '</section>\n'
    ) % {
        "index": L.index, "guides": L.guides, "module": module,
        "title": esc(guide["title"]), "lead": esc(guide["lead"]),
        "toc": toc, "sections": sections, "related": related,
    }

    return render_page(
        lang="ja", from_dir="guides", page="guide", content=content,
        canonical_path="guides/%s.html" % slug,
        pair_path="en/guides/%s.html" % slug,
        title="%s｜今日の総合鑑定" % guide["title"],
        description=guide["description"])


def guides_index_ja() -> str:
    L = Links("")
    cards = ""
    for g in GUIDES:
        toc = "".join("      <li>%s</li>\n" % esc(s["heading"]) for s in g["sections"])
        cards += (
            '  <article class="guide-card">\n'
            '    <p class="guide-card-tag">%(module)s</p>\n'
            '    <h2 class="guide-card-title">\n'
            '      <a href="%(url)s">%(title)s</a>\n'
            '    </h2>\n'
            '    <p class="guide-card-desc">%(desc)s</p>\n'
            '    <ul class="guide-card-toc">\n'
            '%(toc)s'
            '    </ul>\n'
            '    <a class="guide-card-link" href="%(url)s">\n'
            '      この記事を読む\n'
            '    </a>\n'
            '  </article>\n'
        ) % {"module": esc(g["module"]), "url": L.guide(g["slug"]),
             "title": esc(g["title"]), "desc": esc(g["description"]), "toc": toc}

    content = (
        '<section class="hero">\n'
        '  <p class="hero-lead">占術ガイド</p>\n'
        '  <h1 class="hero-title">11種の占い方を<br><span class="accent">ひとつずつ解説</span></h1>\n'
        '  <p class="hero-desc">\n'
        '    当サイトの総合鑑定で使っている11種の占術について、\n'
        '    それぞれの成り立ち、どんな情報を使うのか、基本となる用語、\n'
        '    そして当サイトがどう計算しているのかを解説しています。\n'
        '    鑑定結果に出てきた用語の意味を調べたいときにもご利用ください。\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="guide-index">\n'
        '%(cards)s'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">まずは占ってみる</h2>\n'
        '  <p>\n'
        '    解説を読む前に、実際の鑑定結果を見てみるのもおすすめです。\n'
        '    5項目を入力するだけで、11種すべての結果と総合鑑定が表示されます。\n'
        '  </p>\n'
        '  <a class="submit-button link-button" href="%(index)s">今日の総合鑑定を見る</a>\n'
        '</section>\n'
    ) % {"cards": cards, "index": L.index}

    return render_page(
        lang="ja", from_dir="", page="guides", content=content,
        canonical_path="guides.html", pair_path="en/guides.html",
        title="占い方の解説一覧｜11種の占術をやさしく読み解く",
        description=("四柱推命・西洋占星術・紫微斗数・九星気学・姓名判断など11種の占術"
                     "それぞれの成り立ち、使う情報、当サイトでの計算方法をやさしく解説します。"))


# ------------------------------------------------------------------ 英語
def guide_page_en(guide: dict) -> str:
    L = Links("en/guides")
    slug = guide["slug"]
    module = esc(guide["module"])

    toc = "".join(
        '      <li><a href="#section-%d">%s</a></li>\n' % (i, esc(s["heading"]))
        for i, s in enumerate(guide["sections"], 1))

    sections = ""
    for i, s in enumerate(guide["sections"], 1):
        paras = "".join('    <p class="guide-paragraph">%s</p>\n' % esc(p)
                        for p in s["paragraphs"])
        sections += (
            '  <section class="guide-section" id="section-%d">\n'
            '    <h2 class="guide-heading">%s</h2>\n'
            '%s'
            '  </section>\n' % (i, esc(s["heading"]), paras))

    related = ""
    for other in _related(GUIDES_EN, slug):
        related += (
            '    <li>\n'
            '      <a href="%s">\n'
            '        <strong>%s</strong>\n'
            '        <span>%s</span>\n'
            '      </a>\n'
            '    </li>\n' % (L.en_guide(other["slug"]), esc(other["module"]),
                            esc(other["description"])))

    content = (
        '<nav class="breadcrumb" aria-label="Breadcrumb">\n'
        '  <a href="%(index)s">Home</a>\n'
        '  <span aria-hidden="true">›</span>\n'
        '  <a href="%(guides)s">Divination Guides</a>\n'
        '  <span aria-hidden="true">›</span>\n'
        '  <span>%(module)s</span>\n'
        '</nav>\n'
        '\n'
        '<article class="card guide-article">\n'
        '  <p class="guide-tag">%(module)s</p>\n'
        '  <h1 class="guide-title">%(title)s</h1>\n'
        '  <p class="guide-lead">%(lead)s</p>\n'
        '\n'
        '  <nav class="guide-toc" aria-label="Table of contents">\n'
        '    <p class="guide-toc-title">Contents</p>\n'
        '    <ol>\n'
        '%(toc)s'
        '    </ol>\n'
        '  </nav>\n'
        '\n'
        '%(sections)s'
        '\n'
        '  <p class="guide-disclaimer">\n'
        '    * This article introduces the ideas behind this divination tradition and makes\n'
        '    no claim to scientific validity. Please enjoy your reading as entertainment.\n'
        '  </p>\n'
        '</article>\n'
        '\n'
        '<!-- ADSENSE_SLOT -->\n'
        '<div class="ad-container ad-guide">Advertisement</div>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">Try a %(module)s reading of your own</h2>\n'
        '  <p>\n'
        '    This site\'s combined reading calculates %(module)s together with ten\n'
        '    other traditions in one go. Enter five details and you can check your\n'
        '    individual %(module)s result from the "see the individual readings"\n'
        '    section too.\n'
        '  </p>\n'
        '  <a class="submit-button link-button" href="%(index)s">Get Today\'s Fortune</a>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">Read about the other traditions</h2>\n'
        '  <ul class="guide-related">\n'
        '%(related)s'
        '  </ul>\n'
        '  <a class="guide-card-link" href="%(guides)s">Back to all guides</a>\n'
        '</section>\n'
    ) % {
        "index": L.en_index, "guides": L.en_guides, "module": module,
        "title": esc(guide["title"]), "lead": esc(guide["lead"]),
        "toc": toc, "sections": sections, "related": related,
    }

    return render_page(
        lang="en", from_dir="en/guides", page="guide", content=content,
        canonical_path="en/guides/%s.html" % slug,
        pair_path="guides/%s.html" % slug,
        title="%s | Today's Fortune" % guide["title"],
        description=guide["description"])


def guides_index_en() -> str:
    L = Links("en")
    cards = ""
    for g in GUIDES_EN:
        toc = "".join("      <li>%s</li>\n" % esc(s["heading"]) for s in g["sections"])
        cards += (
            '  <article class="guide-card">\n'
            '    <p class="guide-card-tag">%(module)s</p>\n'
            '    <h2 class="guide-card-title">\n'
            '      <a href="%(url)s">%(title)s</a>\n'
            '    </h2>\n'
            '    <p class="guide-card-desc">%(desc)s</p>\n'
            '    <ul class="guide-card-toc">\n'
            '%(toc)s'
            '    </ul>\n'
            '    <a class="guide-card-link" href="%(url)s">\n'
            '      Read this article\n'
            '    </a>\n'
            '  </article>\n'
        ) % {"module": esc(g["module"]), "url": L.en_guide(g["slug"]),
             "title": esc(g["title"]), "desc": esc(g["description"]), "toc": toc}

    content = (
        '<section class="hero">\n'
        '  <p class="hero-lead">Divination Guides</p>\n'
        '  <h1 class="hero-title">Eleven traditions,<br><span class="accent">explained one by one</span></h1>\n'
        '  <p class="hero-desc">\n'
        '    Here\'s a plain-language walkthrough of each of the eleven traditions used in\n'
        '    this site\'s combined reading — where each one comes from, what information it\n'
        '    uses, its basic terminology, and how this site calculates it. Come back here\n'
        '    any time you want to look up a term that showed up in your reading.\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="guide-index">\n'
        '%(cards)s'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">Try a reading first</h2>\n'
        '  <p>\n'
        '    Before you read further, you might enjoy seeing an actual reading. Enter\n'
        '    five details and you\'ll get all eleven individual results plus one combined\n'
        '    verdict.\n'
        '  </p>\n'
        '  <a class="submit-button link-button" href="%(index)s">Get Today\'s Fortune</a>\n'
        '</section>\n'
    ) % {"cards": cards, "index": L.en_index}

    return render_page(
        lang="en", from_dir="en", page="guides", content=content,
        canonical_path="en/guides.html", pair_path="guides.html",
        title="Divination Guides | Today's Fortune",
        description=("Plain-language guides to all 11 divination traditions used in this "
                     "site's combined reading — BaZi, Western astrology, Zi Wei Dou Shu, "
                     "Nine Star Ki, name analysis, and more."))


def build_guides() -> list:
    written = []
    written.append(write_file("guides.html", guides_index_ja()))
    for g in GUIDES:
        written.append(write_file("guides/%s.html" % g["slug"], guide_page_ja(g)))
    written.append(write_file("en/guides.html", guides_index_en()))
    for g in GUIDES_EN:
        written.append(write_file("en/guides/%s.html" % g["slug"], guide_page_en(g)))
    return written


if __name__ == "__main__":
    for path in build_guides():
        print("wrote", os.path.relpath(path))
