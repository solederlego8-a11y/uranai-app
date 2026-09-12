# -*- coding: utf-8 -*-
"""静的サイト生成の共通部品（base.html / en/base.html の展開、URL計算）。

Flask 版の inject_site_config() / inject_hreflang() が注入していた
meta / OGP / hreflang / AdSense 設定をここで静的に展開する。
"""
from __future__ import annotations

import html
import os
import posixpath
import sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# 公開URL（GitHub Pages・サブディレクトリ配下）
BASE_URL = "https://solederlego8-a11y.github.io/uranai-app/"

# 運営者情報（Flask 版では環境変数 SITE_OPERATOR / CONTACT_EMAIL）
SITE_OPERATOR = ""
CONTACT_EMAIL = ""

POLICY_UPDATED_ON = "2026年8月28日"
POLICY_UPDATED_ON_EN = "August 28, 2026"
AD_NETWORK = "Google AdSense"

JST = timezone(timedelta(hours=9))


def today_jst():
    return datetime.now(JST).date()


def esc(value) -> str:
    """Jinja2 の autoescape 相当。"""
    return html.escape(str(value), quote=True)


def href(from_dir: str, to_path: str) -> str:
    """docs/ 直下からの相対パス同士を、ページの置き場所基準の相対リンクにする。

    to_path が '' または '/' 終わりならディレクトリ（index）へのリンク。
    """
    src = from_dir or "."
    if to_path == "" or to_path.endswith("/"):
        target = to_path.rstrip("/") or "."
        rel = posixpath.relpath(target, src)
        return "./" if rel == "." else rel + "/"
    return posixpath.relpath(to_path, src)


def absolute(path: str) -> str:
    return BASE_URL + path


class Links:
    """ページの置き場所に応じた相対リンク集。"""

    def __init__(self, from_dir: str):
        self.from_dir = from_dir
        self.index = href(from_dir, "")
        self.result = href(from_dir, "result.html")
        self.about = href(from_dir, "about.html")
        self.guides = href(from_dir, "guides.html")
        self.privacy = href(from_dir, "privacy.html")
        self.contact = href(from_dir, "contact.html")
        self.en_index = href(from_dir, "en/")
        self.en_result = href(from_dir, "en/result.html")
        self.en_about = href(from_dir, "en/about.html")
        self.en_guides = href(from_dir, "en/guides.html")
        self.en_privacy = href(from_dir, "en/privacy.html")
        self.en_contact = href(from_dir, "en/contact.html")
        self.css = href(from_dir, "css/style.css")
        self.js_main = href(from_dir, "js/main.js")
        self.js_app = href(from_dir, "js/app.js")
        self.js_uranai = href(from_dir, "js/uranai.js")
        self.favicon = href(from_dir, "img/favicon-32.png")
        self.apple_icon = href(from_dir, "img/apple-touch-icon.png")

    def guide(self, slug: str) -> str:
        return href(self.from_dir, "guides/%s.html" % slug)

    def en_guide(self, slug: str) -> str:
        return href(self.from_dir, "en/guides/%s.html" % slug)

    def as_dict(self) -> dict:
        return {k: v for k, v in vars(self).items() if not k.startswith("_")}


DEFAULT_TITLE_JA = "今日の総合鑑定｜11種の占術で読み解く一日"
DEFAULT_DESC_JA = ("姓名判断・四柱推命・西洋占星術など11種の占術を統合し、"
                   "今日の総合評価・ラッキーカラー・ラッキーアイテム・ラッキー方位を"
                   "1つの結論として提示します。")
DEFAULT_TITLE_EN = "Today's Fortune | 11 Divination Systems Combined"
DEFAULT_DESC_EN = ("Name analysis, Four Pillars of Destiny, Western astrology and 8 more "
                   "traditions combined into one verdict: today's score, lucky colour, "
                   "lucky item and lucky direction.")


def render_page(*, lang: str, from_dir: str, page: str, content: str,
                canonical_path: str, pair_path: str | None,
                title: str | None = None, description: str | None = None,
                scripts: str = "", noindex: bool = False) -> str:
    """base.html / en/base.html を展開して1ページ分のHTMLを返す。

    canonical_path / pair_path は docs/ 直下からのパス（'' は index）。
    pair_path が None のページ（result）は hreflang を出さない（Flask 版と同じ）。
    """
    L = Links(from_dir)
    is_en = lang == "en"
    title = title or (DEFAULT_TITLE_EN if is_en else DEFAULT_TITLE_JA)
    description = description or (DEFAULT_DESC_EN if is_en else DEFAULT_DESC_JA)
    canonical = absolute(canonical_path)

    hreflang_lines = []
    if pair_path is not None:
        pair = absolute(pair_path)
        ja_url, en_url = (pair, canonical) if is_en else (canonical, pair)
        if is_en:
            hreflang_lines.append('  <link rel="alternate" hreflang="en" href="%s">' % en_url)
            hreflang_lines.append('  <link rel="alternate" hreflang="ja" href="%s">' % ja_url)
        else:
            hreflang_lines.append('  <link rel="alternate" hreflang="ja" href="%s">' % ja_url)
            hreflang_lines.append('  <link rel="alternate" hreflang="en" href="%s">' % en_url)
        hreflang_lines.append('  <link rel="alternate" hreflang="x-default" href="%s">' % ja_url)
    hreflang = ("\n".join(hreflang_lines) + "\n") if hreflang_lines else ""
    robots = '  <meta name="robots" content="noindex, follow">\n' if noindex else ""

    og_image = absolute("img/og-image-en.png" if is_en else "img/og-image-ja.png")
    site_name = "Today's Fortune" if is_en else "今日の総合鑑定"
    locale = "en_US" if is_en else "ja_JP"

    head = (
        '<!DOCTYPE html>\n'
        '<html lang="%(lang)s">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '  <title>%(title)s</title>\n'
        '  <meta name="description" content="%(desc)s">\n'
        '%(robots)s'
        '  <link rel="canonical" href="%(canonical)s">\n'
        '%(hreflang)s'
        '  <link rel="icon" href="%(favicon)s" sizes="32x32">\n'
        '  <link rel="apple-touch-icon" href="%(apple)s">\n'
        '  <meta property="og:type" content="website">\n'
        '  <meta property="og:site_name" content="%(site_name)s">\n'
        '  <meta property="og:locale" content="%(locale)s">\n'
        '  <meta property="og:title" content="%(title)s">\n'
        '  <meta property="og:description" content="%(desc)s">\n'
        '  <meta property="og:url" content="%(canonical)s">\n'
        '  <meta property="og:image" content="%(og_image)s">\n'
        '  <meta property="og:image:width" content="1200">\n'
        '  <meta property="og:image:height" content="630">\n'
        '  <meta name="twitter:card" content="summary_large_image">\n'
        '  <meta name="twitter:title" content="%(title)s">\n'
        '  <meta name="twitter:description" content="%(desc)s">\n'
        '  <meta name="twitter:image" content="%(og_image)s">\n'
        '  <link rel="stylesheet" href="%(css)s">\n'
        '  <!-- ADSENSE_HEAD -->\n'
        '</head>\n'
    ) % {
        "lang": lang, "title": esc(title), "desc": esc(description),
        "robots": robots, "canonical": canonical, "hreflang": hreflang,
        "favicon": L.favicon, "apple": L.apple_icon, "site_name": site_name,
        "locale": locale, "og_image": og_image, "css": L.css,
    }

    if is_en:
        body = (
            '<body data-page="%(page)s">\n'
            '  <div id="loading-overlay" class="loading-overlay" hidden>\n'
            '    <div class="loading-box">\n'
            '      <div class="loading-spinner" aria-hidden="true"></div>\n'
            '      <p class="loading-text">Consulting eleven traditions at once...</p>\n'
            '    </div>\n'
            '  </div>\n'
            '\n'
            '  <header class="site-header">\n'
            '    <div class="container header-inner">\n'
            '      <a class="brand" href="%(en_index)s">\n'
            '        <span class="brand-mark">卜</span>\n'
            '        <span class="brand-text">\n'
            '          <strong>Today\'s Fortune</strong>\n'
            '          <small>10 Divination Systems + Name Analysis</small>\n'
            '        </span>\n'
            '      </a>\n'
            '      <nav class="site-nav">\n'
            '        <a href="%(en_index)s">Get your reading</a>\n'
            '        <a href="%(en_guides)s">Guides</a>\n'
            '        <a href="%(en_about)s">About</a>\n'
            '        <a href="%(index)s" class="lang-switch">日本語</a>\n'
            '      </nav>\n'
            '    </div>\n'
            '  </header>\n'
            '\n'
            '  <!-- ADSENSE_SLOT -->\n'
            '  <div class="container">\n'
            '    <div class="ad-container ad-header">Advertisement</div>\n'
            '  </div>\n'
            '\n'
            '  <main class="container">\n'
            '%(content)s'
            '  </main>\n'
            '\n'
            '  <footer class="site-footer">\n'
            '    <div class="container">\n'
            '      <p class="disclaimer">\n'
            '        <strong>Disclaimer:</strong>\n'
            '        The readings on this site are provided for entertainment purposes only.\n'
            '        They are calculated using traditional formulas and simplified astronomical\n'
            '        approximations from each divination system, and no scientific validity is\n'
            '        claimed or guaranteed. Please do not rely on these results for medical,\n'
            '        legal, financial, or other important decisions. This site accepts no\n'
            '        liability for any loss arising from the use of its results.\n'
            '      </p>\n'
            '      <nav class="footer-nav">\n'
            '        <a href="%(en_index)s">Home</a>\n'
            '        <a href="%(en_guides)s">Guides</a>\n'
            '        <a href="%(en_about)s">About</a>\n'
            '        <a href="%(en_privacy)s">Privacy Policy</a>\n'
            '        <a href="%(en_contact)s">Contact / Operator Info</a>\n'
            '        <a href="%(index)s">日本語版</a>\n'
            '      </nav>\n'
            '      <p class="copyright">&copy; Today\'s Fortune</p>\n'
            '    </div>\n'
            '  </footer>\n'
            '\n'
            '%(scripts)s'
            '  <script src="%(js_main)s"></script>\n'
            '</body>\n'
            '</html>\n'
        )
    else:
        body = (
            '<body data-page="%(page)s">\n'
            '  <div id="loading-overlay" class="loading-overlay" hidden>\n'
            '    <div class="loading-box">\n'
            '      <div class="loading-spinner" aria-hidden="true"></div>\n'
            '      <p class="loading-text">十一の暦を照らし合わせています……</p>\n'
            '    </div>\n'
            '  </div>\n'
            '\n'
            '  <header class="site-header">\n'
            '    <div class="container header-inner">\n'
            '      <a class="brand" href="%(index)s">\n'
            '        <span class="brand-mark">卜</span>\n'
            '        <span class="brand-text">\n'
            '          <strong>今日の総合鑑定</strong>\n'
            '          <small>命占十種 ＋ 姓名判断</small>\n'
            '        </span>\n'
            '      </a>\n'
            '      <nav class="site-nav">\n'
            '        <a href="%(index)s">占う</a>\n'
            '        <a href="%(guides)s">占術ガイド</a>\n'
            '        <a href="%(about)s">このサイトについて</a>\n'
            '        <a href="%(en_index)s" class="lang-switch">EN</a>\n'
            '      </nav>\n'
            '    </div>\n'
            '  </header>\n'
            '\n'
            '  <!-- ADSENSE_SLOT -->\n'
            '  <div class="container">\n'
            '    <div class="ad-container ad-header">広告スペース</div>\n'
            '  </div>\n'
            '\n'
            '  <main class="container">\n'
            '%(content)s'
            '  </main>\n'
            '\n'
            '  <footer class="site-footer">\n'
            '    <div class="container">\n'
            '      <p class="disclaimer">\n'
            '        <strong>免責事項：</strong>\n'
            '        当サイトの鑑定結果はエンターテインメントを目的としたものです。\n'
            '        算出には各占術の伝統的な計算式および簡易近似式を用いており、\n'
            '        科学的根拠を保証するものではありません。\n'
            '        医療・法律・投資など重要な判断の材料としてのご利用はお控えください。\n'
            '        結果の利用によって生じたいかなる損害についても、当サイトは責任を負いかねます。\n'
            '      </p>\n'
            '      <nav class="footer-nav">\n'
            '        <a href="%(index)s">トップ</a>\n'
            '        <a href="%(guides)s">占術ガイド</a>\n'
            '        <a href="%(about)s">このサイトについて</a>\n'
            '        <a href="%(privacy)s">プライバシーポリシー</a>\n'
            '        <a href="%(contact)s">お問い合わせ・運営者情報</a>\n'
            '      </nav>\n'
            '      <p class="copyright">&copy; 今日の総合鑑定</p>\n'
            '    </div>\n'
            '  </footer>\n'
            '\n'
            '%(scripts)s'
            '  <script src="%(js_main)s"></script>\n'
            '</body>\n'
            '</html>\n'
        )
    params = L.as_dict()
    params.update({"page": page, "content": content, "scripts": scripts})
    return head + body % params


def write_file(rel_path: str, text: str) -> str:
    """docs/ 配下にUTF-8 (LF) で書き出し、書いたパスを返す。"""
    out = os.path.join(DOCS, rel_path.replace("/", os.sep))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return out
