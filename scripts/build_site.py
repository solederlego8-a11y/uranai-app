# -*- coding: utf-8 -*-
"""Flask 版テンプレートを GitHub Pages 用の静的サイト（docs/）へ展開する。

    python scripts/build_site.py

- static/ の CSS・画像・main.js を docs/ へコピー
- index / result / about / privacy / contact / 404 の日英ページを生成
- scripts/build_guides.py を呼んで占術ガイドを生成
- sitemap.xml / robots.txt / ads.txt / .nojekyll を生成

docs/js/app.js（フォーム・結果描画）と docs/js/uranai.js（占術ロジック）は
このスクリプトでは生成しない。
"""
from __future__ import annotations

import os
import shutil
import sys
from string import Template

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from site_common import (  # noqa: E402
    AD_NETWORK, BASE_URL, CONTACT_EMAIL, DOCS, POLICY_UPDATED_ON,
    POLICY_UPDATED_ON_EN, ROOT, SITE_OPERATOR, Links, absolute, esc,
    render_page, today_jst, write_file,
)
from build_guides import build_guides  # noqa: E402
from uranai import MODULES  # noqa: E402
from uranai.guides import GUIDES  # noqa: E402
from uranai.guides_en import GUIDES_EN  # noqa: E402
from uranai.i18n import GENDER_EN, module_name_en, prefecture_en  # noqa: E402
from uranai.utils import PREFECTURES, WORLD_CITIES, world_city_label  # noqa: E402

YEAR_MIN = 1900
YEAR_MAX = today_jst().year

GENDER_CHOICES = [("male", "男性"), ("female", "女性"), ("unknown", "回答しない")]
HOUR_CHOICES = [("", "不明")] + [(str(h), "%d時台" % h) for h in range(24)]
GENDER_CHOICES_EN = [(v, GENDER_EN[v]) for v, _ in GENDER_CHOICES]
HOUR_CHOICES_EN = [("", "Unknown")] + [(str(h), "%d:00" % h) for h in range(24)]
PREFECTURES_EN = [(p, prefecture_en(p)) for p in PREFECTURES]
WORLD_CITIES_EN = [(c, world_city_label(c)) for c in WORLD_CITIES]

CHART_JS = ('  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"\n'
            '          integrity="sha384-9nhczxUqK87bcKHh20fSQcTGD4qq5GhayNYSYWqwBkINBhOfQLg/P5HG5lF1urn4"\n'
            '          crossorigin="anonymous"></script>\n')


def _options(pairs, indent="          "):
    return "".join('%s<option value="%s">%s</option>\n' % (indent, esc(v), esc(label))
                   for v, label in pairs)


# ----------------------------------------------------------------- index
def index_ja() -> str:
    L = Links("")
    today = today_jst()
    years = _options([(y, "%d年" % y) for y in range(YEAR_MAX, YEAR_MIN - 1, -1)])
    months = _options([(m, "%d月" % m) for m in range(1, 13)])
    days = _options([(d, "%d日" % d) for d in range(1, 32)])
    hours = _options(HOUR_CHOICES, indent="        ")
    genders = "".join(
        '        <label class="radio-chip">\n'
        '          <input type="radio" name="gender" value="%s"%s>\n'
        '          <span>%s</span>\n'
        '        </label>\n' % (v, ' checked' if v == "unknown" else '', label)
        for v, label in GENDER_CHOICES)
    prefs = _options([(p, p) for p in PREFECTURES], indent="        ")

    content = Template(
        '<section class="hero">\n'
        '  <p class="hero-lead">生年月日と名前だけ。入力は5項目。</p>\n'
        '  <h1 class="hero-title">十一の占術を束ねた<br><span class="accent">今日の総合鑑定</span></h1>\n'
        '  <p class="hero-desc">\n'
        '    姓名判断・四柱推命・西洋占星術・紫微斗数・九星気学・算命学・数秘術・\n'
        '    インド占星術・宿曜占星術・マヤ暦・チベット占星術。\n'
        '    11種すべてを計算し、<strong>今日の総合評価・ラッキーカラー・アイテム・方位・ナンバー</strong>を\n'
        '    ひとつの結論としてお伝えします。\n'
        '  </p>\n'
        '  <p class="hero-date" id="hero-date">本日は $y年$m月$d日です</p>\n'
        '</section>\n'
        '\n'
        '<div id="form-alert" class="alert" role="alert" hidden></div>\n'
        '\n'
        '<section class="card form-card">\n'
        '  <h2 class="card-title">鑑定に必要な5項目</h2>\n'
        '  <form id="uranai-form" action="$result" method="get" novalidate>\n'
        '\n'
        '    <div class="field">\n'
        '      <label class="field-label" for="last_name">① 姓・名（漢字）<span class="required">必須</span></label>\n'
        '      <div class="field-row">\n'
        '        <input type="text" id="last_name" name="last_name" placeholder="姓（例：山田）"\n'
        '               maxlength="10" required value="">\n'
        '        <input type="text" id="first_name" name="first_name" placeholder="名（例：太郎）"\n'
        '               maxlength="10" required value="">\n'
        '      </div>\n'
        '      <p class="field-note">姓名判断と数秘術に使用します。ローマ字の入力は不要です。</p>\n'
        '    </div>\n'
        '\n'
        '    <div class="field">\n'
        '      <label class="field-label" for="birth_year">② 生年月日<span class="required">必須</span></label>\n'
        '      <div class="field-row">\n'
        '        <select id="birth_year" name="birth_year" required>\n'
        '          <option value="">年</option>\n'
        '$years'
        '        </select>\n'
        '        <select id="birth_month" name="birth_month" required>\n'
        '          <option value="">月</option>\n'
        '$months'
        '        </select>\n'
        '        <select id="birth_day" name="birth_day" required>\n'
        '          <option value="">日</option>\n'
        '$days'
        '        </select>\n'
        '      </div>\n'
        '      <p class="field-note">11種すべての占術で使用する、最も重要な項目です。</p>\n'
        '    </div>\n'
        '\n'
        '    <div class="field">\n'
        '      <label class="field-label" for="birth_hour">③ 出生時刻<span class="optional">任意</span></label>\n'
        '      <select id="birth_hour" name="birth_hour">\n'
        '$hours'
        '      </select>\n'
        '      <p class="field-note">\n'
        '        四柱推命の時柱・紫微斗数の時辰・西洋占星術のアセンダントに使用します。\n'
        '        「不明」の場合は正午（12時）として計算します。\n'
        '      </p>\n'
        '    </div>\n'
        '\n'
        '    <div class="field">\n'
        '      <label class="field-label">④ 性別<span class="optional">任意</span></label>\n'
        '      <div class="radio-row">\n'
        '$genders'
        '      </div>\n'
        '      <p class="field-note">四柱推命・紫微斗数・算命学・チベット占星術の解釈に使用します。</p>\n'
        '    </div>\n'
        '\n'
        '    <div class="field">\n'
        '      <label class="field-label" for="prefecture">⑤ 出生地（都道府県）<span class="optional">任意</span></label>\n'
        '      <select id="prefecture" name="prefecture">\n'
        '        <option value="unknown">不明・海外</option>\n'
        '$prefs'
        '      </select>\n'
        '      <p class="field-note">\n'
        '        西洋占星術・インド占星術のアセンダント近似計算に使用します。\n'
        '        「不明・海外」の場合は東京（東経139.69度／北緯35.69度）で代替します。\n'
        '      </p>\n'
        '    </div>\n'
        '\n'
        '    <button type="submit" class="submit-button">今日の総合鑑定を見る</button>\n'
        '    <p class="form-footnote">入力内容はサーバーに保存されません。</p>\n'
        '  </form>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">占い方を知りたい方へ</h2>\n'
        '  <p>\n'
        '    四柱推命の日主とは何か、九星気学の本命星はどう出すのか、宿曜占星術の27宿とは何か。\n'
        '    当サイトで使っている11種の占術について、成り立ちから計算方法までを解説しています。\n'
        '  </p>\n'
        '  <a class="submit-button link-button" href="$guides">占術ガイドを読む</a>\n'
        '</section>\n'
        '\n'
        '<section class="card feature-card">\n'
        '  <h2 class="card-title">このアプリの特徴</h2>\n'
        '  <ul class="feature-list">\n'
        '    <li><strong>結論がひとつ。</strong>11種の結果を重み付き平均で統合し、100点満点の総合評価と大吉〜凶のランクを提示します。</li>\n'
        '    <li><strong>日替わり。</strong>「今日の日付」を計算に組み込むため、同じ人でも日付が変われば結果が変わります。</li>\n'
        '    <li><strong>完全に決定論的。</strong>乱数は一切使用していません。同じ入力・同じ日付なら必ず同じ結果になります。</li>\n'
        '    <li><strong>個別結果も確認可能。</strong>11種それぞれの鑑定は、結論の下のアコーディオンから読めます。</li>\n'
        '  </ul>\n'
        '</section>\n'
    ).substitute(y=today.year, m=today.month, d=today.day, result=L.result,
                 guides=L.guides, years=years, months=months, days=days,
                 hours=hours, genders=genders, prefs=prefs)

    scripts = ('  <script src="%s"></script>\n  <script src="%s"></script>\n'
               % (L.js_uranai, L.js_app))
    return render_page(
        lang="ja", from_dir="", page="index", content=content,
        canonical_path="", pair_path="en/",
        title="今日の総合鑑定｜5項目の入力で11種の占術をまとめて鑑定",
        scripts=scripts)


def index_en() -> str:
    L = Links("en")
    today = today_jst()
    years = _options([(y, str(y)) for y in range(YEAR_MAX, YEAR_MIN - 1, -1)])
    months = _options([(m, str(m)) for m in range(1, 13)])
    days = _options([(d, str(d)) for d in range(1, 32)])
    hours = _options(HOUR_CHOICES_EN, indent="        ")
    genders = "".join(
        '        <label class="radio-chip">\n'
        '          <input type="radio" name="gender" value="%s"%s>\n'
        '          <span>%s</span>\n'
        '        </label>\n' % (v, ' checked' if v == "unknown" else '', label)
        for v, label in GENDER_CHOICES_EN)
    cities = _options(WORLD_CITIES_EN)
    prefs = _options(PREFECTURES_EN)

    content = Template(
        '<section class="hero">\n'
        '  <p class="hero-lead">Just your name and date of birth. 5 fields.</p>\n'
        '  <h1 class="hero-title">Eleven traditions, combined into<br><span class="accent">Today\'s Fortune</span></h1>\n'
        '  <p class="hero-desc">\n'
        '    Name Analysis, Four Pillars of Destiny (BaZi), Western Astrology, Zi Wei Dou Shu,\n'
        '    Nine Star Ki, Sanmei-gaku, Numerology, Vedic Astrology, Sukuyo Astrology,\n'
        '    the Mayan Calendar, and Tibetan Astrology.\n'
        '    We calculate all eleven and combine them into <strong>one verdict</strong>: today\'s\n'
        '    overall score, lucky colour, lucky item, lucky direction, and lucky number.\n'
        '  </p>\n'
        '  <p class="hero-date" id="hero-date">Today is $today</p>\n'
        '</section>\n'
        '\n'
        '<div id="form-alert" class="alert" role="alert" hidden></div>\n'
        '\n'
        '<section class="card form-card">\n'
        '  <h2 class="card-title">The 5 details we need</h2>\n'
        '  <form id="uranai-form" action="$result" method="get" novalidate>\n'
        '\n'
        '    <div class="field">\n'
        '      <label class="field-label" for="last_name">① Name, in Kanji/Chinese characters<span class="required">Required</span></label>\n'
        '      <div class="field-row">\n'
        '        <input type="text" id="last_name" name="last_name" placeholder="Family name (e.g. 山田)"\n'
        '               maxlength="10" required value="">\n'
        '        <input type="text" id="first_name" name="first_name" placeholder="Given name (e.g. 太郎)"\n'
        '               maxlength="10" required value="">\n'
        '      </div>\n'
        '      <p class="field-note">\n'
        '        Used for Name Analysis and Numerology. This reading is built around\n'
        '        Japanese/Chinese-character names — if you don\'t have a name written this\n'
        '        way, you can enter the kanji spelling of your name\'s sound, or a name a\n'
        '        Japanese-speaking friend has written for you. Romanised input is not needed;\n'
        '        our built-in tables convert the characters automatically.\n'
        '      </p>\n'
        '    </div>\n'
        '\n'
        '    <div class="field">\n'
        '      <label class="field-label" for="birth_year">② Date of birth<span class="required">Required</span></label>\n'
        '      <div class="field-row">\n'
        '        <select id="birth_year" name="birth_year" required>\n'
        '          <option value="">Year</option>\n'
        '$years'
        '        </select>\n'
        '        <select id="birth_month" name="birth_month" required>\n'
        '          <option value="">Month</option>\n'
        '$months'
        '        </select>\n'
        '        <select id="birth_day" name="birth_day" required>\n'
        '          <option value="">Day</option>\n'
        '$days'
        '        </select>\n'
        '      </div>\n'
        '      <p class="field-note">The single most important field — used by all eleven systems.</p>\n'
        '    </div>\n'
        '\n'
        '    <div class="field">\n'
        '      <label class="field-label" for="birth_hour">③ Time of birth<span class="optional">Optional</span></label>\n'
        '      <select id="birth_hour" name="birth_hour">\n'
        '$hours'
        '      </select>\n'
        '      <p class="field-note">\n'
        '        Used for the Four Pillars\' hour pillar, Zi Wei Dou Shu\'s time branch, and the\n'
        '        Ascendant in Western astrology. If unknown, we calculate as if you were born at noon.\n'
        '      </p>\n'
        '    </div>\n'
        '\n'
        '    <div class="field">\n'
        '      <label class="field-label">④ Gender<span class="optional">Optional</span></label>\n'
        '      <div class="radio-row">\n'
        '$genders'
        '      </div>\n'
        '      <p class="field-note">Used to interpret the Four Pillars, Zi Wei Dou Shu, Sanmei-gaku, and Tibetan Astrology.</p>\n'
        '    </div>\n'
        '\n'
        '    <div class="field">\n'
        '      <label class="field-label" for="prefecture">⑤ Place of birth<span class="optional">Optional</span></label>\n'
        '      <select id="prefecture" name="prefecture">\n'
        '        <option value="unknown">Unknown / not listed</option>\n'
        '        <optgroup label="Major cities worldwide">\n'
        '$cities'
        '        </optgroup>\n'
        '        <optgroup label="Japan (by prefecture)">\n'
        '$prefs'
        '        </optgroup>\n'
        '      </select>\n'
        '      <p class="field-note">\n'
        '        Used for the Ascendant approximation in Western and Vedic astrology. Pick\n'
        '        the city closest to where you were born; if your city isn\'t listed or you\'d\n'
        '        rather not say, choose "Unknown / not listed" and we\'ll use Tokyo\n'
        '        (139.69°E / 35.69°N) as a substitute coordinate.\n'
        '      </p>\n'
        '    </div>\n'
        '\n'
        '    <button type="submit" class="submit-button">Get Today\'s Fortune</button>\n'
        '    <p class="form-footnote">Nothing you enter here is stored on our server.</p>\n'
        '  </form>\n'
        '</section>\n'
        '\n'
        '<section class="card feature-card">\n'
        '  <h2 class="card-title">What makes this different</h2>\n'
        '  <ul class="feature-list">\n'
        '    <li><strong>One conclusion.</strong> All eleven results are combined with a weighted average into a single score out of 100 and a rank from "Excellent Fortune" to "Caution".</li>\n'
        '    <li><strong>A new reading every day.</strong> Today\'s date is built into every calculation, so the result changes day to day even for the same person.</li>\n'
        '    <li><strong>Fully deterministic.</strong> No randomness is used anywhere. The same input on the same day will always produce the same result.</li>\n'
        '    <li><strong>Individual results included.</strong> Each of the eleven readings can be explored in the accordion below the main verdict.</li>\n'
        '  </ul>\n'
        '</section>\n'
    ).substitute(today=today.strftime("%B %d, %Y"), result=L.en_result,
                 years=years, months=months, days=days, hours=hours,
                 genders=genders, cities=cities, prefs=prefs)

    scripts = ('  <script src="%s"></script>\n  <script src="%s"></script>\n'
               % (L.js_uranai, L.js_app))
    return render_page(
        lang="en", from_dir="en", page="index", content=content,
        canonical_path="en/", pair_path="",
        title="Today's Fortune | Combine 11 Divination Systems in One Reading",
        scripts=scripts)


# ---------------------------------------------------------------- result
def result_ja() -> str:
    L = Links("")
    content = (
        '<noscript>\n'
        '  <div class="alert" role="alert">\n'
        '    鑑定結果の表示にはJavaScriptが必要です。ブラウザの設定でJavaScriptを有効にしてから、\n'
        '    <a href="%(index)s">入力フォーム</a>からもう一度お試しください。\n'
        '  </div>\n'
        '</noscript>\n'
        '<div id="result-root" aria-live="polite"></div>\n'
    ) % {"index": L.index}
    scripts = CHART_JS + ('  <script src="%s"></script>\n  <script src="%s"></script>\n'
                          % (L.js_uranai, L.js_app))
    return render_page(
        lang="ja", from_dir="", page="result", content=content,
        canonical_path="result.html", pair_path=None,
        title="今日の総合鑑定｜鑑定結果", scripts=scripts, noindex=True)


def result_en() -> str:
    L = Links("en")
    content = (
        '<noscript>\n'
        '  <div class="alert" role="alert">\n'
        '    JavaScript is required to display your reading. Please enable JavaScript in\n'
        '    your browser and try again from the <a href="%(index)s">input form</a>.\n'
        '  </div>\n'
        '</noscript>\n'
        '<div id="result-root" aria-live="polite"></div>\n'
    ) % {"index": L.en_index}
    scripts = CHART_JS + ('  <script src="%s"></script>\n  <script src="%s"></script>\n'
                          % (L.js_uranai, L.js_app))
    return render_page(
        lang="en", from_dir="en", page="result", content=content,
        canonical_path="en/result.html", pair_path=None,
        title="Today's Fortune | Your Reading", scripts=scripts, noindex=True)


# ----------------------------------------------------------------- about
def about_ja() -> str:
    L = Links("")
    modules = "".join("    <li>%s</li>\n" % esc(name) for name, _ in MODULES)
    content = Template(
        '<section class="card">\n'
        '  <h1 class="card-title">このサイトについて</h1>\n'
        '  <p class="about-lead">\n'
        '    「今日の総合鑑定」は、命占（生年月日をもとに宿命を読む占い）10種と姓名判断を合わせた\n'
        '    11種の占術をすべて計算し、その結果を1つの結論に統合して提示するWebアプリケーションです。\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">使用している11種の占術</h2>\n'
        '  <ol class="about-modules">\n'
        '$modules'
        '  </ol>\n'
        '  <p class="about-note">\n'
        '    それぞれの占術は伝統的な計算式に基づいて実装していますが、\n'
        '    節入り時刻・天体位置・アセンダントなど厳密な天文計算を要する部分については、\n'
        '    実用上の精度を保った簡易近似式を用いています。\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">結論の出し方</h2>\n'
        '  <dl class="about-steps">\n'
        '    <div class="about-step">\n'
        '      <dt>総合スコア</dt>\n'
        '      <dd>\n'
        '        11種それぞれが算出した1〜100点のスコアを、占術ごとの重み\n'
        '        （四柱推命1.5／インド占星術・マヤ暦・チベット占星術0.5／その他1.0）で\n'
        '        加重平均し、100点満点に正規化しています。\n'
        '      </dd>\n'
        '    </div>\n'
        '    <div class="about-step">\n'
        '      <dt>運勢ランク</dt>\n'
        '      <dd>81〜100点＝大吉／61〜80点＝中吉／41〜60点＝小吉／21〜40点＝末吉／1〜20点＝凶。</dd>\n'
        '    </div>\n'
        '    <div class="about-step">\n'
        '      <dt>ラッキーカラー・アイテム・方位</dt>\n'
        '      <dd>\n'
        '        11種それぞれが導いた候補のうち、最も多く挙がったものを多数決で採用します。\n'
        '        同数の場合は占術ごとの優先順位で決定します。\n'
        '      </dd>\n'
        '    </div>\n'
        '    <div class="about-step">\n'
        '      <dt>ラッキーナンバー</dt>\n'
        '      <dd>数秘術のパーソナルデーナンバー（ライフパス＋今日の月＋今日の日）を採用しています。</dd>\n'
        '    </div>\n'
        '  </dl>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">結果は毎日変わります</h2>\n'
        '  <p>\n'
        '    すべての占術が「今日の日付」を計算に組み込んでいます。\n'
        '    四柱推命なら今日の日柱と本人の日主の相性、九星気学なら今日の日盤と本命星の相性、\n'
        '    数秘術ならパーソナルデーナンバー、というように、\n'
        '    それぞれの流儀で「本人の宿命」と「今日という日」の関係を読み取ります。\n'
        '    そのため、同じ方でも日付が変われば結果は変わります。\n'
        '  </p>\n'
        '  <p>\n'
        '    一方で、<strong>乱数は一切使用していません。</strong>\n'
        '    同じ入力・同じ日付であれば、何度占っても必ず同じ結果が出ます。\n'
        '    日替わりの変化は、生年月日・氏名・今日の日付から計算した剰余演算のみで実現しています。\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">入力項目について</h2>\n'
        '  <ul class="about-inputs">\n'
        '    <li><strong>姓・名（漢字）</strong>：姓名判断、数秘術のデスティニーナンバーに使用します。ローマ字への変換はアプリ内部で行うため、ローマ字入力は不要です。</li>\n'
        '    <li><strong>生年月日</strong>：11種すべてで使用します。</li>\n'
        '    <li><strong>出生時刻（任意）</strong>：四柱推命の時柱、紫微斗数の時辰、西洋占星術・インド占星術のアセンダントに使用します。不明の場合は正午（12時）として計算します。</li>\n'
        '    <li><strong>性別（任意）</strong>：四柱推命の解釈、紫微斗数の陰陽、算命学、チベット占星術の八卦に使用します。「回答しない」も選択できます。</li>\n'
        '    <li><strong>出生地（任意）</strong>：西洋占星術・インド占星術のアセンダント近似計算に使用します。不明・海外の場合は東京（東経139.69度／北緯35.69度）で代替します。</li>\n'
        '  </ul>\n'
        '  <p class="about-note">入力された情報はサーバーに保存されません。鑑定結果の生成にのみ使用されます。</p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">免責事項</h2>\n'
        '  <p>\n'
        '    当サイトが提供する鑑定結果は、<strong>エンターテインメントを目的としたもの</strong>です。\n'
        '    占術は文化的・歴史的な体系であり、その内容について科学的根拠を保証するものではありません。\n'
        '    健康・医療・法律・投資・進路など、人生の重要な判断の材料としてのご利用はお控えください。\n'
        '    結果の利用によって生じたいかなる損害についても、当サイトは責任を負いかねます。\n'
        '  </p>\n'
        '  <a class="submit-button link-button" href="$index">占ってみる</a>\n'
        '</section>\n'
    ).substitute(modules=modules, index=L.index)
    return render_page(
        lang="ja", from_dir="", page="about", content=content,
        canonical_path="about.html", pair_path="en/about.html",
        title="このサイトについて｜今日の総合鑑定")


def about_en() -> str:
    L = Links("en")
    modules = "".join("    <li>%s</li>\n" % esc(module_name_en(name)) for name, _ in MODULES)
    content = Template(
        '<section class="card">\n'
        '  <h1 class="card-title">About This Site</h1>\n'
        '  <p class="about-lead">\n'
        '    "Today\'s Fortune" is a web app that runs eleven different divination\n'
        '    systems — ten traditions based on your date of birth, plus a name-based\n'
        '    reading — and combines all of them into a single conclusion.\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">The 11 traditions used</h2>\n'
        '  <ol class="about-modules">\n'
        '$modules'
        '  </ol>\n'
        '  <p class="about-note">\n'
        '    Each system is implemented from its traditional calculation method. For\n'
        '    parts that would otherwise require precise astronomical calculation\n'
        '    (solar term timing, planetary positions, the Ascendant, and similar),\n'
        '    we use well-established simplified approximations that keep practical\n'
        '    accuracy while running instantly.\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">How the verdict is calculated</h2>\n'
        '  <dl class="about-steps">\n'
        '    <div class="about-step">\n'
        '      <dt>Overall score</dt>\n'
        '      <dd>\n'
        '        Each of the 11 systems produces a score from 1 to 100. These are\n'
        '        combined with a weighted average (Four Pillars of Destiny counts 1.5x;\n'
        '        Vedic Astrology, the Mayan Calendar, and Tibetan Astrology each count\n'
        '        0.5x; everything else counts 1x) and normalised back to a 100-point scale.\n'
        '      </dd>\n'
        '    </div>\n'
        '    <div class="about-step">\n'
        '      <dt>Fortune rank</dt>\n'
        '      <dd>81-100 = Excellent Fortune, 61-80 = Good Fortune, 41-60 = Modest Fortune, 21-40 = Waning Fortune, 1-20 = Caution.</dd>\n'
        '    </div>\n'
        '    <div class="about-step">\n'
        '      <dt>Lucky colour, item, and direction</dt>\n'
        '      <dd>\n'
        '        Whichever value comes up most often across the 11 systems\' individual\n'
        '        suggestions wins by majority vote. Ties are broken by a fixed priority\n'
        '        order among the systems.\n'
        '      </dd>\n'
        '    </div>\n'
        '    <div class="about-step">\n'
        '      <dt>Lucky number</dt>\n'
        '      <dd>Taken directly from the Numerology system\'s Personal Day Number (Life Path Number plus today\'s month and day, reduced).</dd>\n'
        '    </div>\n'
        '  </dl>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">The result changes every day</h2>\n'
        '  <p>\n'
        '    Every one of the 11 systems factors in today\'s date. Four Pillars of\n'
        '    Destiny looks at the relationship between today\'s day-pillar and your own;\n'
        '    Nine Star Ki looks at today\'s day chart against your birth star;\n'
        '    Numerology uses your Personal Day Number — each tradition reads the\n'
        '    relationship between "who you are" and "what today is" in its own way.\n'
        '    That\'s why the same person gets a different result on a different day.\n'
        '  </p>\n'
        '  <p>\n'
        '    At the same time, <strong>no randomness is used anywhere in this app.</strong>\n'
        '    Given the same input and the same date, the result will always be\n'
        '    identical. The day-to-day change comes entirely from deterministic\n'
        '    calculations based on your date of birth, your name, and today\'s date.\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">About the information you enter</h2>\n'
        '  <ul class="about-inputs">\n'
        '    <li><strong>Name (in Kanji/Chinese characters)</strong>: used for Name Analysis and the Numerology Destiny Number. The conversion to Roman letters happens automatically inside the app, so you never need to type romanised text yourself.</li>\n'
        '    <li><strong>Date of birth</strong>: used by all 11 systems.</li>\n'
        '    <li><strong>Time of birth (optional)</strong>: used for the Four Pillars\' hour pillar, Zi Wei Dou Shu\'s time branch, and the Ascendant in Western and Vedic astrology. If unknown, we calculate as if you were born at noon.</li>\n'
        '    <li><strong>Gender (optional)</strong>: used to interpret the Four Pillars, Zi Wei Dou Shu, Sanmei-gaku, and Tibetan Astrology\'s trigram. "Prefer not to say" is also a valid choice.</li>\n'
        '    <li><strong>Place of birth (optional)</strong>: used for the Ascendant approximation in Western and Vedic astrology. Choose from Japan\'s 47 prefectures or dozens of major cities worldwide; if your city isn\'t listed or you\'d rather not say, we substitute Tokyo (139.69°E / 35.69°N).</li>\n'
        '  </ul>\n'
        '  <p class="about-note">Nothing you enter is saved on our servers. It is used only to generate your reading.</p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">Disclaimer</h2>\n'
        '  <p>\n'
        '    The readings on this site are provided <strong>for entertainment\n'
        '    purposes only</strong>. Each system reflects a cultural and historical\n'
        '    tradition, and no scientific validity is claimed or guaranteed. Please\n'
        '    do not use these results as material for important decisions involving\n'
        '    health, medicine, law, finance, or your career path.\n'
        '    This site accepts no liability for any loss arising from the use of its results.\n'
        '  </p>\n'
        '  <a class="submit-button link-button" href="$index">Get your reading</a>\n'
        '</section>\n'
    ).substitute(modules=modules, index=L.en_index)
    return render_page(
        lang="en", from_dir="en", page="about", content=content,
        canonical_path="en/about.html", pair_path="about.html",
        title="About This Site | Today's Fortune")


# --------------------------------------------------------------- privacy
def privacy_ja() -> str:
    L = Links("")
    content = Template(
        '<section class="card">\n'
        '  <h1 class="card-title">プライバシーポリシー</h1>\n'
        '  <p class="about-lead">\n'
        '    当サイト「今日の総合鑑定」（以下「当サイト」）は、ご利用者の個人情報の保護を重要な責務と考え、\n'
        '    以下の方針に基づいて取り扱います。\n'
        '  </p>\n'
        '  <p class="about-note">最終更新日：$updated</p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">1. 入力していただく情報の取り扱い</h2>\n'
        '  <p>\n'
        '    当サイトの鑑定機能では、氏名・生年月日・出生時刻・性別・出生地の5項目を入力していただきます。\n'
        '    これらの情報は、送信されたリクエストの中で鑑定結果を計算するためだけに使用され、\n'
        '    <strong>サーバー上のデータベースやファイルに保存することはありません。</strong>\n'
        '    鑑定結果ページの表示が完了した時点で、入力内容はサーバーのメモリから破棄されます。\n'
        '  </p>\n'
        '  <p>\n'
        '    当サイトは、入力された氏名・生年月日等を第三者に提供・販売することはありません。\n'
        '    また、これらの情報を用いて個人を特定・追跡することもありません。\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">2. Cookie（クッキー）の使用について</h2>\n'
        '  <p>\n'
        '    当サイトでは、後述する広告配信およびアクセス解析のためにCookieを使用する場合があります。\n'
        '    Cookieとは、ウェブサイトがご利用者のブラウザに保存する小さなテキストファイルで、\n'
        '    氏名や住所などの個人を直接特定する情報を含むものではありません。\n'
        '  </p>\n'
        '  <p>\n'
        '    Cookieの使用を希望されない場合は、お使いのブラウザの設定からCookieを無効にすることができます。\n'
        '    ただし、その場合でも当サイトの鑑定機能は問題なくご利用いただけます。\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">3. 第三者配信の広告サービスについて</h2>\n'
        '  <p>\n'
        '    当サイトでは、第三者配信の広告サービス「$ad_network」を利用する予定です（または利用しています）。\n'
        '  </p>\n'
        '  <ul class="about-inputs">\n'
        '    <li>\n'
        '      広告配信事業者は、ご利用者の興味に応じた広告を表示するためにCookieを使用することがあります。\n'
        '    </li>\n'
        '    <li>\n'
        '      Googleを含む第三者配信事業者は、Cookieを使用して、\n'
        '      ご利用者が当サイトや他のサイトに過去にアクセスした際の情報に基づいて広告を配信します。\n'
        '    </li>\n'
        '    <li>\n'
        '      Googleが広告Cookieを使用することにより、ご利用者は\n'
        '      <a href="https://adssettings.google.com/authenticated" target="_blank" rel="noopener noreferrer">Google広告設定</a>\n'
        '      でパーソナライズ広告を無効にできます。\n'
        '    </li>\n'
        '    <li>\n'
        '      パーソナライズ広告に使用される第三者配信事業者のCookieを無効にする方法については、\n'
        '      <a href="https://optout.aboutads.info/" target="_blank" rel="noopener noreferrer">aboutads.info</a>\n'
        '      をご参照ください。\n'
        '    </li>\n'
        '    <li>\n'
        '      詳細は\n'
        '      <a href="https://policies.google.com/technologies/ads?hl=ja" target="_blank" rel="noopener noreferrer">「広告 – ポリシーと規約 – Google」</a>\n'
        '      をご確認ください。\n'
        '    </li>\n'
        '  </ul>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">4. アクセス解析ツールについて</h2>\n'
        '  <p>\n'
        '    当サイトでは、サイトの利用状況を把握するためにアクセス解析ツールを利用する場合があります。\n'
        '    これらのツールはCookieを使用してトラフィックデータを収集しますが、\n'
        '    収集されるデータは匿名であり、個人を特定するものではありません。\n'
        '    この機能はCookieを無効にすることで収集を拒否できます。\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">5. 免責事項</h2>\n'
        '  <p>\n'
        '    当サイトが提供する鑑定結果は、<strong>エンターテインメントを目的としたもの</strong>です。\n'
        '    各占術は文化的・歴史的な体系であり、その内容について科学的根拠を保証するものではありません。\n'
        '    健康・医療・法律・投資・進路など、人生の重要な判断の材料としてのご利用はお控えください。\n'
        '  </p>\n'
        '  <p>\n'
        '    当サイトに掲載された内容によって生じた損害等について、\n'
        '    当サイトの運営者は一切の責任を負いかねます。\n'
        '    また、当サイトから移動された先のウェブサイトで提供される情報・サービスについても、\n'
        '    責任を負うものではありません。\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">6. 著作権について</h2>\n'
        '  <p>\n'
        '    当サイトに掲載されている文章・プログラム等の著作権は、当サイトの運営者に帰属します。\n'
        '    法的に認められた引用の範囲を超える転載・複製はご遠慮ください。\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">7. プライバシーポリシーの変更</h2>\n'
        '  <p>\n'
        '    当サイトは、法令の変更やサービス内容の変更に伴い、本ポリシーを予告なく変更することがあります。\n'
        '    変更後のプライバシーポリシーは、当ページに掲載した時点から効力を生じるものとします。\n'
        '  </p>\n'
        '  <a class="submit-button link-button" href="$contact">お問い合わせはこちら</a>\n'
        '</section>\n'
    ).substitute(updated=esc(POLICY_UPDATED_ON), ad_network=esc(AD_NETWORK),
                 contact=L.contact)
    return render_page(
        lang="ja", from_dir="", page="privacy", content=content,
        canonical_path="privacy.html", pair_path="en/privacy.html",
        title="プライバシーポリシー｜今日の総合鑑定")


def privacy_en() -> str:
    L = Links("en")
    content = Template(
        '<section class="card">\n'
        '  <h1 class="card-title">Privacy Policy</h1>\n'
        '  <p class="about-lead">\n'
        '    "Today\'s Fortune" (this site) considers the protection of visitors\'\n'
        '    personal information an important responsibility, and handles it\n'
        '    according to the policy below.\n'
        '  </p>\n'
        '  <p class="about-note">Last updated: $updated</p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">1. How the information you enter is handled</h2>\n'
        '  <p>\n'
        '    The reading feature on this site asks for five items: your name, date\n'
        '    of birth, time of birth, gender, and place of birth. This information\n'
        '    is used only, within the request that generates it, to calculate your\n'
        '    reading. <strong>None of it is stored in any database or file on our\n'
        '    server.</strong> Once your result page has finished rendering, the\n'
        '    information you entered is discarded from server memory.\n'
        '  </p>\n'
        '  <p>\n'
        '    We do not provide or sell any name, date of birth, or other information\n'
        '    you enter to any third party, and we do not use it to identify or track\n'
        '    any individual.\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">2. Use of cookies</h2>\n'
        '  <p>\n'
        '    This site may use cookies for the advertising and analytics purposes\n'
        '    described below. A cookie is a small text file that a website stores\n'
        '    in your browser; it does not directly identify you by name, address,\n'
        '    or similar personal details.\n'
        '  </p>\n'
        '  <p>\n'
        '    If you would prefer not to have cookies used, you can disable them in\n'
        '    your browser\'s settings. The reading feature on this site will continue\n'
        '    to work correctly even with cookies disabled.\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">3. Third-party advertising services</h2>\n'
        '  <p>\n'
        '    This site uses (or intends to use) the third-party advertising service\n'
        '    "$ad_network".\n'
        '  </p>\n'
        '  <ul class="about-inputs">\n'
        '    <li>\n'
        '      Advertising providers may use cookies to serve ads based on your interests.\n'
        '    </li>\n'
        '    <li>\n'
        '      Google and other third-party vendors may use cookies to serve ads\n'
        '      based on a visitor\'s prior visits to this site or other sites.\n'
        '    </li>\n'
        '    <li>\n'
        '      Visitors can opt out of personalised advertising by visiting\n'
        '      <a href="https://adssettings.google.com/authenticated" target="_blank" rel="noopener noreferrer">Google Ads Settings</a>.\n'
        '    </li>\n'
        '    <li>\n'
        '      For information on disabling the use of third-party vendor cookies\n'
        '      for personalised advertising, visit\n'
        '      <a href="https://optout.aboutads.info/" target="_blank" rel="noopener noreferrer">aboutads.info</a>.\n'
        '    </li>\n'
        '    <li>\n'
        '      For further detail, see\n'
        '      <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener noreferrer">"How Google uses information from sites or apps that use our services"</a>.\n'
        '    </li>\n'
        '  </ul>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">4. Analytics tools</h2>\n'
        '  <p>\n'
        '    This site may use analytics tools to understand how it is used. These\n'
        '    tools may use cookies to collect traffic data, but the data collected\n'
        '    is anonymous and does not identify any individual. This collection can\n'
        '    be declined by disabling cookies.\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">5. Disclaimer</h2>\n'
        '  <p>\n'
        '    The readings provided on this site are for <strong>entertainment\n'
        '    purposes only</strong>. Each divination system reflects a cultural and\n'
        '    historical tradition, and no scientific validity is claimed or\n'
        '    guaranteed for its content. Please do not use these results as\n'
        '    material for important decisions involving your health, medical care,\n'
        '    legal matters, finances, or career path.\n'
        '  </p>\n'
        '  <p>\n'
        '    The operator of this site accepts no liability for any damage arising\n'
        '    from content published here, nor for any information or service\n'
        '    provided by external websites linked from this site.\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">6. Copyright</h2>\n'
        '  <p>\n'
        '    Copyright in the text and program code published on this site belongs\n'
        '    to its operator. Please refrain from reproduction or republication\n'
        '    beyond what is legally recognised as fair quotation.\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">7. Changes to this policy</h2>\n'
        '  <p>\n'
        '    This site may revise this policy without prior notice, in response to\n'
        '    changes in law or in the service itself. Any revised policy takes\n'
        '    effect from the moment it is posted on this page.\n'
        '  </p>\n'
        '  <a class="submit-button link-button" href="$contact">Contact us</a>\n'
        '</section>\n'
    ).substitute(updated=esc(POLICY_UPDATED_ON_EN), ad_network=esc(AD_NETWORK),
                 contact=L.en_contact)
    return render_page(
        lang="en", from_dir="en", page="privacy", content=content,
        canonical_path="en/privacy.html", pair_path="privacy.html",
        title="Privacy Policy | Today's Fortune")


# --------------------------------------------------------------- contact
def contact_ja() -> str:
    L = Links("")
    operator = (esc(SITE_OPERATOR) if SITE_OPERATOR else
                '<span class="unset-notice">未設定（scripts/site_common.py の SITE_OPERATOR を設定してください）</span>')
    email = ('<a href="mailto:%s">%s</a>' % (esc(CONTACT_EMAIL), esc(CONTACT_EMAIL))
             if CONTACT_EMAIL else
             '<span class="unset-notice">未設定（scripts/site_common.py の CONTACT_EMAIL を設定してください）</span>')
    notice = "" if (SITE_OPERATOR and CONTACT_EMAIL) else (
        '\n'
        '  <p class="alert" role="alert">\n'
        '    運営者名・連絡先が未設定です。Google AdSenseの審査では運営者情報の明示が求められるため、\n'
        '    公開前に <code>scripts/site_common.py</code> の <code>SITE_OPERATOR</code> と <code>CONTACT_EMAIL</code> を設定して再生成してください。\n'
        '    この注意書きは、両方を設定すると自動的に表示されなくなります。\n'
        '  </p>\n')
    content = Template(
        '<section class="card">\n'
        '  <h1 class="card-title">お問い合わせ・運営者情報</h1>\n'
        '  <p class="about-lead">\n'
        '    当サイトに関するご質問・ご指摘・掲載内容の削除依頼などは、\n'
        '    以下の連絡先までお願いいたします。\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">運営者情報</h2>\n'
        '  <dl class="input-list">\n'
        '    <div class="input-row">\n'
        '      <dt>サイト名</dt>\n'
        '      <dd>今日の総合鑑定</dd>\n'
        '    </div>\n'
        '    <div class="input-row">\n'
        '      <dt>運営者</dt>\n'
        '      <dd>$operator</dd>\n'
        '    </div>\n'
        '    <div class="input-row">\n'
        '      <dt>連絡先</dt>\n'
        '      <dd>$email</dd>\n'
        '    </div>\n'
        '    <div class="input-row">\n'
        '      <dt>サイトの内容</dt>\n'
        '      <dd>生年月日と氏名をもとに、11種の占術を統合して「今日の総合鑑定」を提示する占いWebアプリケーション</dd>\n'
        '    </div>\n'
        '  </dl>\n'
        '$notice'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">お問い合わせにあたって</h2>\n'
        '  <ul class="about-inputs">\n'
        '    <li>個別の鑑定内容に関する詳細な解説やご相談には、原則としてお応えしておりません。</li>\n'
        '    <li>計算結果の不具合・表示崩れ・リンク切れなどのご報告は歓迎いたします。お使いの端末とブラウザをあわせてお知らせください。</li>\n'
        '    <li>当サイトは占いの結果について、その的中や効果を保証するものではありません。詳しくは<a href="$privacy">プライバシーポリシー</a>の免責事項をご覧ください。</li>\n'
        '    <li>お返事までにお時間をいただく場合があります。あらかじめご了承ください。</li>\n'
        '  </ul>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">個人情報の取り扱い</h2>\n'
        '  <p>\n'
        '    お問い合わせの際にお預かりしたメールアドレス・お名前などの個人情報は、\n'
        '    ご返信および内容の確認のためにのみ使用し、第三者に提供することはありません。\n'
        '    詳細は<a href="$privacy">プライバシーポリシー</a>をご確認ください。\n'
        '  </p>\n'
        '  <a class="submit-button link-button" href="$index">トップページへ戻る</a>\n'
        '</section>\n'
    ).substitute(operator=operator, email=email, notice=notice,
                 privacy=L.privacy, index=L.index)
    return render_page(
        lang="ja", from_dir="", page="contact", content=content,
        canonical_path="contact.html", pair_path="en/contact.html",
        title="お問い合わせ・運営者情報｜今日の総合鑑定")


def contact_en() -> str:
    L = Links("en")
    operator = (esc(SITE_OPERATOR) if SITE_OPERATOR else
                '<span class="unset-notice">Not set (please configure SITE_OPERATOR in scripts/site_common.py)</span>')
    email = ('<a href="mailto:%s">%s</a>' % (esc(CONTACT_EMAIL), esc(CONTACT_EMAIL))
             if CONTACT_EMAIL else
             '<span class="unset-notice">Not set (please configure CONTACT_EMAIL in scripts/site_common.py)</span>')
    content = Template(
        '<section class="card">\n'
        '  <h1 class="card-title">Contact / Operator Info</h1>\n'
        '  <p class="about-lead">\n'
        '    For questions, corrections, or removal requests regarding this site,\n'
        '    please reach us at the contact below.\n'
        '  </p>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">Operator Information</h2>\n'
        '  <dl class="input-list">\n'
        '    <div class="input-row">\n'
        '      <dt>Site name</dt>\n'
        '      <dd>Today\'s Fortune</dd>\n'
        '    </div>\n'
        '    <div class="input-row">\n'
        '      <dt>Operator</dt>\n'
        '      <dd>$operator</dd>\n'
        '    </div>\n'
        '    <div class="input-row">\n'
        '      <dt>Contact</dt>\n'
        '      <dd>$email</dd>\n'
        '    </div>\n'
        '    <div class="input-row">\n'
        '      <dt>What this site does</dt>\n'
        '      <dd>A fortune-telling web app that combines 11 divination systems based on your date of birth and name into a single "Today\'s Fortune" verdict.</dd>\n'
        '    </div>\n'
        '  </dl>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">Before you write to us</h2>\n'
        '  <ul class="about-inputs">\n'
        '    <li>We generally cannot provide detailed interpretation of, or personal consultation about, an individual reading.</li>\n'
        '    <li>Reports of calculation errors, display issues, or broken links are welcome — please include your device and browser.</li>\n'
        '    <li>This site makes no guarantee that any reading will come true or have any real effect. See the disclaimer in our <a href="$privacy">Privacy Policy</a> for details.</li>\n'
        '    <li>A reply may take some time. Thank you for your patience.</li>\n'
        '  </ul>\n'
        '</section>\n'
        '\n'
        '<section class="card">\n'
        '  <h2 class="card-title">Handling of personal information</h2>\n'
        '  <p>\n'
        '    Any name, email address, or other personal information you provide when\n'
        '    contacting us is used only to reply to and confirm your enquiry, and is\n'
        '    never provided to any third party. See our\n'
        '    <a href="$privacy">Privacy Policy</a> for further detail.\n'
        '  </p>\n'
        '  <a class="submit-button link-button" href="$index">Back to home</a>\n'
        '</section>\n'
    ).substitute(operator=operator, email=email, privacy=L.en_privacy, index=L.en_index)
    return render_page(
        lang="en", from_dir="en", page="contact", content=content,
        canonical_path="en/contact.html", pair_path="contact.html",
        title="Contact / Operator Info | Today's Fortune")


# ------------------------------------------------------------------- 404
def not_found() -> str:
    """404.html は任意のパスで表示されるため、リンク・アセットは公開URLの絶対URLにする。"""
    return (
        '<!DOCTYPE html>\n'
        '<html lang="ja">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '  <title>ページが見つかりません｜今日の総合鑑定</title>\n'
        '  <meta name="robots" content="noindex">\n'
        '  <link rel="icon" href="%(fav)s" sizes="32x32">\n'
        '  <link rel="stylesheet" href="%(css)s">\n'
        '</head>\n'
        '<body>\n'
        '  <header class="site-header">\n'
        '    <div class="container header-inner">\n'
        '      <a class="brand" href="%(index)s">\n'
        '        <span class="brand-mark">卜</span>\n'
        '        <span class="brand-text">\n'
        '          <strong>今日の総合鑑定</strong>\n'
        '          <small>命占十種 ＋ 姓名判断</small>\n'
        '        </span>\n'
        '      </a>\n'
        '    </div>\n'
        '  </header>\n'
        '  <main class="container">\n'
        '    <section class="card">\n'
        '      <h1 class="card-title">404 – ページが見つかりません</h1>\n'
        '      <p>お探しのページは見つかりませんでした。もう一度占ってみてください。</p>\n'
        '      <p>The page you were looking for could not be found. Please try getting a reading instead.</p>\n'
        '      <a class="submit-button link-button" href="%(index)s">トップページへ</a>\n'
        '      <p style="margin-top:14px"><a href="%(en_index)s">English version (Home)</a></p>\n'
        '    </section>\n'
        '  </main>\n'
        '  <footer class="site-footer">\n'
        '    <div class="container">\n'
        '      <p class="copyright">&copy; 今日の総合鑑定</p>\n'
        '    </div>\n'
        '  </footer>\n'
        '</body>\n'
        '</html>\n'
    ) % {"fav": absolute("img/favicon-32.png"), "css": absolute("css/style.css"),
         "index": absolute(""), "en_index": absolute("en/")}


# ------------------------------------------------------- sitemap / robots
SITE_PATHS = ["", "about.html", "guides.html", "privacy.html", "contact.html",
              "en/", "en/about.html", "en/privacy.html", "en/contact.html", "en/guides.html"]


def sitemap_xml() -> str:
    paths = list(SITE_PATHS)
    paths += ["guides/%s.html" % g["slug"] for g in GUIDES]
    paths += ["en/guides/%s.html" % g["slug"] for g in GUIDES_EN]
    lastmod = today_jst().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in paths:
        lines.append("  <url><loc>%s</loc><lastmod>%s</lastmod></url>" % (absolute(p), lastmod))
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def robots_txt() -> str:
    return "User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % BASE_URL


# ---------------------------------------------------------------- assets
def copy_assets() -> list:
    static = os.path.join(ROOT, "static")
    pairs = [
        (os.path.join(static, "css", "style.css"), os.path.join(DOCS, "css", "style.css")),
        (os.path.join(static, "js", "main.js"), os.path.join(DOCS, "js", "main.js")),
    ]
    images = os.path.join(static, "images")
    for name in sorted(os.listdir(images)):
        pairs.append((os.path.join(images, name), os.path.join(DOCS, "img", name)))
    written = []
    for src, dst in pairs:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        written.append(dst)
    return written


def build_site() -> list:
    written = copy_assets()
    pages = {
        "index.html": index_ja(),
        "result.html": result_ja(),
        "about.html": about_ja(),
        "privacy.html": privacy_ja(),
        "contact.html": contact_ja(),
        "en/index.html": index_en(),
        "en/result.html": result_en(),
        "en/about.html": about_en(),
        "en/privacy.html": privacy_en(),
        "en/contact.html": contact_en(),
        "404.html": not_found(),
        "sitemap.xml": sitemap_xml(),
        "robots.txt": robots_txt(),
        "ads.txt": "",
        ".nojekyll": "",
    }
    for rel, text in pages.items():
        written.append(write_file(rel, text))
    written += build_guides()
    return written


if __name__ == "__main__":
    for path in build_site():
        print("wrote", os.path.relpath(path, ROOT))
