# -*- coding: utf-8 -*-
"""ブログ記事と PR 商材一覧を GitHub Pages 用の静的HTML（docs/）として生成する。

    python scripts/build_blog.py

出力・更新:
    docs/blog/<slug>.html          … uranai/blog.py の POSTS ＋ uranai/blog_content/<slug>.html
    docs/picks.html                … 記事で紹介している商材一覧（PR）
    docs/guides.html               … <!-- blog-index:start/end --> の間（ブログ記事カード）
    docs/guides/<slug>.html        … <!-- guide-blog:start/end --> の間（関連ブログ記事）
    docs/sitemap.xml               … ブログ記事・picks の URL を追記

build_site.py の全体実行は docs/ 側で手を入れた GA4・CV計測・FAQ schema・拡充本文・
CSS を巻き戻すため、ブログ関連はこのスクリプト単体で反映する（build_site.py からも呼ばれる）。
Flask 版（Render）は app.py の /blog/<slug>・/picks が同じ uranai/blog.py から同じHTMLを出す。
生成後に必ず:
    python C:/Users/info/growth_plan/scripts/inject_faq_schema.py docs/blog   （FAQPage は生成時に付与済みなので skip になる）
    python C:/Users/info/scripts/inject-cv-tracking.py
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from site_common import DOCS, absolute, href, render_page, today_jst, write_file  # noqa: E402
from uranai import blog  # noqa: E402


def make_urls(from_dir: str):
    def urls(kind, arg):
        if kind == "home":
            return href(from_dir, "")
        if kind == "blog_index":
            return href(from_dir, "guides.html") + "#blog"
        if kind == "picks":
            return href(from_dir, "picks.html")
        if kind == "guide":
            return href(from_dir, "guides/%s.html" % arg)
        if kind == "post":
            return href(from_dir, "blog/%s.html" % arg)
        raise ValueError(kind)
    return urls


def _ga4_block() -> str:
    """docs/index.html に注入済みの GA4 スニペット（サイト専用ID）をそのまま流用する。"""
    path = os.path.join(DOCS, "index.html")
    if not os.path.exists(path):
        return ""
    s = open(path, encoding="utf-8").read()
    m = re.search(r"<!-- ga4 -->\n.*?</script>\n.*?</script>\n", s, re.S)
    return m.group(0) if m else ""


def _finish(page_html: str, head_extra: str = "") -> str:
    """render_page の出力を、手で更新済みの docs/ 既存ページの体裁に合わせる。"""
    ga4 = _ga4_block()
    if ga4 and "<!-- ga4 -->" not in page_html:
        page_html = page_html.replace("<head>\n", "<head>\n" + ga4 + "\n", 1)
    if head_extra:
        page_html = page_html.replace("  <!-- ADSENSE_HEAD -->\n",
                                      "  <!-- ADSENSE_HEAD -->\n" + head_extra, 1)
    page_html = page_html.replace(">占術ガイド</a>", ">ブログ・占術ガイド</a>")
    page_html = page_html.replace('<div class="ad-container ad-header">広告スペース</div>',
                                  '<div class="ad-container ad-header"></div>')
    return page_html


def post_page(post: dict) -> str:
    urls = make_urls("blog")
    body = blog.render_body(blog.load_body(post["slug"]), urls)
    rel = "blog/%s.html" % post["slug"]
    page = render_page(
        lang="ja", from_dir="blog", page="guide",
        content=blog.article_html(post, body, urls),
        canonical_path=rel, pair_path=None,
        title="%s｜今日の総合鑑定" % post["title"], description=post["description"])
    return _finish(page, blog.jsonld(post, absolute(rel), body))


def picks_page() -> str:
    page = render_page(
        lang="ja", from_dir="", page="guide", content=blog.picks_html(make_urls("")),
        canonical_path="picks.html", pair_path=None,
        title="%s｜今日の総合鑑定" % blog.PICKS_TITLE, description=blog.PICKS_DESC)
    return _finish(page)


def _replace_marked(s: str, start: str, end: str, new: str, anchor: str) -> str:
    """start〜end マーカー間を new で置換。マーカーが無ければ anchor の直前に挿入。"""
    if start in s:
        i = s.index(start)
        j = s.index(end, i) + len(end) + 1  # 末尾の改行も含める
        return s[:i] + new + s[j:]
    if not new:
        return s
    if anchor not in s:
        raise ValueError("挿入位置が見つかりません: %r" % anchor[:40])
    return s.replace(anchor, new + "\n" + anchor, 1)


def patch_guides_index() -> str:
    path = os.path.join(DOCS, "guides.html")
    s = open(path, encoding="utf-8").read()
    s = _replace_marked(s, "<!-- blog-index:start -->", "<!-- blog-index:end -->",
                        blog.blog_index_section(make_urls("")),
                        '<section class="guide-index">')
    return write_file("guides.html", s)


GUIDE_ANCHOR = '<section class="card">\n  <h2 class="card-title">ほかの占術の解説を読む</h2>'


def patch_guide_pages() -> list:
    out = []
    gdir = os.path.join(DOCS, "guides")
    for name in sorted(os.listdir(gdir)):
        if not name.endswith(".html"):
            continue
        slug = name[:-5]
        path = os.path.join(gdir, name)
        s = open(path, encoding="utf-8").read()
        new = blog.guide_related_section(slug, make_urls("guides"))
        s2 = _replace_marked(s, "<!-- guide-blog:start -->", "<!-- guide-blog:end -->", new, GUIDE_ANCHOR)
        if s2 != s:
            out.append(write_file("guides/%s" % name, s2))
    return out


def blog_sitemap_paths() -> list:
    return ["blog/%s.html" % p["slug"] for p in blog.POSTS] + ["picks.html"]


def patch_sitemap() -> str:
    path = os.path.join(DOCS, "sitemap.xml")
    s = open(path, encoding="utf-8").read()
    lastmod = today_jst().isoformat()
    add = ""
    for p in blog_sitemap_paths():
        loc = absolute(p)
        if "<loc>%s</loc>" % loc not in s:
            add += "  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n" % (loc, lastmod)
    if add:
        s = s.replace("</urlset>", add + "</urlset>", 1)
    return write_file("sitemap.xml", s)


def build_blog(patch_existing: bool = True) -> list:
    written = [write_file("blog/%s.html" % p["slug"], post_page(p)) for p in blog.POSTS]
    written.append(write_file("picks.html", picks_page()))
    if patch_existing:
        written.append(patch_guides_index())
        written += patch_guide_pages()
        written.append(patch_sitemap())
    return written


if __name__ == "__main__":
    for path in build_blog():
        print("wrote", os.path.relpath(path, os.path.dirname(DOCS)))
