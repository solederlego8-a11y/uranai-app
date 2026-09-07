# -*- coding: utf-8 -*-
"""総合鑑定占いアプリ（Flask）

5項目の入力から11種の占術（命占10種＋姓名判断）をすべて計算し、
「今日の総合鑑定」として1つの結論にまとめて表示する。
"""
from __future__ import annotations

import os
from datetime import date, datetime

import pytz
from flask import Flask, Response, render_template, request, url_for

from uranai import MODULES, build_report
from uranai.aggregator import CATEGORY_LABEL
from uranai.guides import GUIDES, get_guide
from uranai.guides_en import GUIDES_EN, get_guide_en
from uranai.i18n import (
    GENDER_EN,
    PREFECTURE_EN,
    module_name_en,
    prefecture_en,
    translate_report,
)
from uranai.utils import PREFECTURES, WORLD_CITIES, world_city_label

app = Flask(__name__)

# 「今日」は常に日本時間（JST）基準で判定する。
# Renderのサーバーは協定世界時（UTC）で動作しているため、単純に
# datetime.date.today() を使うと、日本時間の深夜0時〜9時の間
# （＝UTCではまだ前日）に「前日の運勢」が表示されてしまう。
# 世界中どこからアクセスしても同じ「今日」を共有できるよう、
# サーバーの所在地に関わらずJSTで日付を固定する。
JST = pytz.timezone("Asia/Tokyo")


def today_jst() -> date:
    """日本時間（JST）基準の「今日」を返す。"""
    return datetime.now(JST).date()

# ---------------------------------------------------------------------------
# サイト運営情報・広告設定（環境変数で与える。未設定でもアプリは動作する）
#   ADSENSE_CLIENT_ID : 例 "ca-pub-1234567890123456"。設定すると AdSense の
#                       一括読み込みタグと /ads.txt が自動的に有効になる。
#   SITE_OPERATOR     : 運営者名（お問い合わせページに表示）
#   CONTACT_EMAIL     : 連絡先メールアドレス（お問い合わせページに表示）
# ---------------------------------------------------------------------------
ADSENSE_CLIENT_ID = os.environ.get("ADSENSE_CLIENT_ID", "").strip()
SITE_OPERATOR = os.environ.get("SITE_OPERATOR", "").strip()
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "").strip()

# ポリシー更新日（プライバシーポリシーに表示する）
POLICY_UPDATED_ON = "2026年8月28日"


@app.context_processor
def inject_site_config():
    """全テンプレートで参照できるサイト共通設定を渡す。"""
    return {
        "adsense_client_id": ADSENSE_CLIENT_ID,
        "site_operator": SITE_OPERATOR,
        "contact_email": CONTACT_EMAIL,
    }


# ---------------------------------------------------------------------------
# hreflang / canonical タグ用の日英ページ対応表
#
# 各エンドポイントについて「対になるもう一方の言語のエンドポイント」を
# 定義し、テンプレート側で <link rel="alternate" hreflang="..."> と
# <link rel="canonical"> を自動的に出力できるようにする。
# 対応するページが存在しないエンドポイント（/result 等、フォーム送信専用の
# ページ）は辞書に含めず、テンプレート側は None を安全に無視する。
# ---------------------------------------------------------------------------
HREFLANG_PAIR = {
    "index": "index_en", "index_en": "index",
    "about": "about_en", "about_en": "about",
    "privacy": "privacy_en", "privacy_en": "privacy",
    "contact": "contact_en", "contact_en": "contact",
    "guides": "guides_en", "guides_en": "guides",
    "guide_detail": "guide_detail_en", "guide_detail_en": "guide_detail",
}
EN_ENDPOINTS = {"index_en", "about_en", "privacy_en", "contact_en",
                 "guides_en", "guide_detail_en"}


@app.context_processor
def inject_hreflang():
    """現在のページに対応する日本語版・英語版URLをテンプレートへ渡す。"""
    endpoint = request.endpoint
    view_args = request.view_args or {}
    ja_url = en_url = canonical_url = None
    if endpoint:
        try:
            canonical_url = url_for(endpoint, **view_args, _external=True)
        except Exception:
            canonical_url = None
        pair = HREFLANG_PAIR.get(endpoint)
        if pair:
            try:
                pair_url = url_for(pair, **view_args, _external=True)
            except Exception:
                pair_url = None
            if endpoint in EN_ENDPOINTS:
                en_url, ja_url = canonical_url, pair_url
            else:
                ja_url, en_url = canonical_url, pair_url
    return {
        "canonical_url": canonical_url,
        "hreflang_ja": ja_url,
        "hreflang_en": en_url,
    }

GENDER_CHOICES = [
    ("male", "男性"),
    ("female", "女性"),
    ("unknown", "回答しない"),
]

HOUR_CHOICES = [("", "不明")] + [(str(h), "%d時台" % h) for h in range(24)]

# ---------------------------------------------------------------------------
# 英語版（グローバル向け）の選択肢
#   value は日本語版と共通（parse_user_data がそのまま使えるようにするため）、
#   ラベルだけを英語に差し替える。
# ---------------------------------------------------------------------------
GENDER_CHOICES_EN = [(value, GENDER_EN[value]) for value, _ in GENDER_CHOICES]
HOUR_CHOICES_EN = [("", "Unknown")] + [(str(h), "%d:00" % h) for h in range(24)]
PREFECTURES_EN = [(pref, prefecture_en(pref)) for pref in PREFECTURES]
# 英語版のみ：日本の都道府県に加えて、世界の主要都市も出生地として選べるようにする
# （日本語版の選択肢・ロジックには一切影響しない）。
WORLD_CITIES_EN = [(city, world_city_label(city)) for city in WORLD_CITIES]
VALID_BIRTHPLACES = set(PREFECTURES) | set(WORLD_CITIES)

ERROR_MESSAGES_JA = {
    "name_required": "姓と名の両方を入力してください。",
    "name_too_long": "姓・名はそれぞれ10文字以内で入力してください。",
    "birth_date_invalid": "生年月日を正しく選択してください。",
    "year_out_of_range": "生年は%d年から%d年の範囲で選択してください。",
    "date_does_not_exist": "存在しない日付です。生年月日を確認してください。",
    "future_date": "生年月日に未来の日付は指定できません。",
    "hour_invalid": "出生時刻を正しく選択してください。",
    "hour_out_of_range": "出生時刻は0時から23時の範囲で選択してください。",
}
ERROR_MESSAGES_EN = {
    "name_required": "Please enter both your family name and given name.",
    "name_too_long": "Please keep each name field to 10 characters or fewer.",
    "birth_date_invalid": "Please select a valid date of birth.",
    "year_out_of_range": "Please choose a birth year between %d and %d.",
    "date_does_not_exist": "That date doesn't exist. Please check your date of birth.",
    "future_date": "Date of birth cannot be in the future.",
    "hour_invalid": "Please select a valid birth hour.",
    "hour_out_of_range": "Birth hour must be between 0 and 23.",
}

# 入力フォームの選択肢に渡す年の範囲
YEAR_MIN = 1900
YEAR_MAX = today_jst().year


def _form_context(form=None, error=None) -> dict:
    """入力フォームの描画に必要なコンテキストを組み立てる。"""
    return {
        "prefectures": PREFECTURES,
        "genders": GENDER_CHOICES,
        "hours": HOUR_CHOICES,
        "year_min": YEAR_MIN,
        "year_max": YEAR_MAX,
        "today": today_jst(),
        "form": form or {},
        "error": error,
    }


def _form_context_en(form=None, error=None) -> dict:
    """英語版入力フォームの描画に必要なコンテキストを組み立てる。"""
    return {
        "prefectures": PREFECTURES_EN,
        "world_cities": WORLD_CITIES_EN,
        "genders": GENDER_CHOICES_EN,
        "hours": HOUR_CHOICES_EN,
        "year_min": YEAR_MIN,
        "year_max": YEAR_MAX,
        "today": today_jst(),
        "form": form or {},
        "error": error,
    }


def parse_user_data(form, lang: str = "ja") -> tuple:
    """フォームの入力値を検証し、内部表現の dict に整形する。

    戻り値: (user_data, エラーメッセージ)  ※エラー時 user_data は None
    lang="en" の場合、エラーメッセージを英語で返す。
    """
    msg = ERROR_MESSAGES_EN if lang == "en" else ERROR_MESSAGES_JA

    last_name = (form.get("last_name") or "").strip()
    first_name = (form.get("first_name") or "").strip()
    if not last_name or not first_name:
        return None, msg["name_required"]
    if len(last_name) > 10 or len(first_name) > 10:
        return None, msg["name_too_long"]

    try:
        birth_year = int(form.get("birth_year", ""))
        birth_month = int(form.get("birth_month", ""))
        birth_day = int(form.get("birth_day", ""))
    except (TypeError, ValueError):
        return None, msg["birth_date_invalid"]

    if not (YEAR_MIN <= birth_year <= YEAR_MAX):
        return None, msg["year_out_of_range"] % (YEAR_MIN, YEAR_MAX)
    try:
        birth = date(birth_year, birth_month, birth_day)
    except ValueError:
        return None, msg["date_does_not_exist"]
    if birth > today_jst():
        return None, msg["future_date"]

    hour_raw = (form.get("birth_hour") or "").strip()
    if hour_raw == "":
        birth_hour = None  # 不明。各占術側で正午（12時）として補完する
    else:
        try:
            birth_hour = int(hour_raw)
        except ValueError:
            return None, msg["hour_invalid"]
        if not (0 <= birth_hour <= 23):
            return None, msg["hour_out_of_range"]

    gender = form.get("gender") or "unknown"
    if gender not in [g for g, _ in GENDER_CHOICES]:
        gender = "unknown"

    prefecture = form.get("prefecture") or "unknown"
    if prefecture not in VALID_BIRTHPLACES:
        # 英語版では世界の主要都市も選択できる（VALID_BIRTHPLACES に含まれる）。
        # それ以外の「不明・海外」は東京（東経139.69度）で代替する。
        prefecture = "unknown"

    return {
        "last_name": last_name,
        "first_name": first_name,
        "birth_year": birth_year,
        "birth_month": birth_month,
        "birth_day": birth_day,
        "birth_hour": birth_hour,
        "gender": gender,
        "prefecture": prefecture,
        "today": today_jst(),
    }, None


@app.route("/", methods=["GET"])
def index():
    """入力フォーム（5項目のみ）を表示する。"""
    return render_template("index.html", **_form_context())


@app.route("/result", methods=["GET", "POST"])
def result():
    """11種の占術を実行し、今日の総合鑑定を表示する。"""
    if request.method == "GET":
        # 直接アクセスされた場合は入力フォームへ戻す
        return render_template("index.html", **_form_context())

    user_data, error = parse_user_data(request.form)
    if error:
        return render_template(
            "index.html", **_form_context(form=request.form, error=error)), 400

    report = build_report(user_data)

    gender_label = dict(GENDER_CHOICES).get(user_data["gender"], "回答しない")
    hour_label = ("不明（正午として計算）" if user_data["birth_hour"] is None
                  else "%d時台" % user_data["birth_hour"])
    prefecture_label = (user_data["prefecture"] if user_data["prefecture"] in PREFECTURES
                        else "不明・海外（東京で代替）")

    return render_template(
        "result.html",
        report=report,
        user_data=user_data,
        gender_label=gender_label,
        hour_label=hour_label,
        prefecture_label=prefecture_label,
        category_label=CATEGORY_LABEL,
        module_count=len(MODULES),
    )


@app.route("/about", methods=["GET"])
def about():
    """このアプリについて（占術の説明・免責事項）を表示する。"""
    return render_template("about.html", modules=[name for name, _ in MODULES])


# ---------------------------------------------------------------------------
# 英語版（グローバル向け）ルート
#
# 内部の計算ロジック（build_report 以下）は日本語のまま完全に共通利用し、
# uranai.i18n.translate_report() で表示直前に英語へ変換する。
# 11種の個別鑑定の長文（detail）は現時点では日本語のみのため、英語版の
# アコーディオンでは「モジュール名・スコア・翻訳済みラッキー要素」を表示し、
# 詳しい文章は日本語版へのリンクで案内する（誤って機械翻訳のふりをしない）。
# ---------------------------------------------------------------------------
@app.route("/en/", methods=["GET"])
def index_en():
    """英語版の入力フォームを表示する。"""
    return render_template("en/index.html", **_form_context_en())


@app.route("/en/result", methods=["GET", "POST"])
def result_en():
    """英語版：11種の占術を実行し、今日の総合鑑定を表示する。"""
    if request.method == "GET":
        return render_template("en/index.html", **_form_context_en())

    user_data, error = parse_user_data(request.form, lang="en")
    if error:
        return render_template(
            "en/index.html", **_form_context_en(form=request.form, error=error)), 400

    report = build_report(user_data)
    report = translate_report(report, user_data)

    gender_label = GENDER_EN.get(user_data["gender"], "Prefer not to say")
    hour_label = ("Unknown (calculated as noon)" if user_data["birth_hour"] is None
                  else "%d:00" % user_data["birth_hour"])
    _pref = user_data["prefecture"]
    if _pref in PREFECTURES:
        prefecture_label = prefecture_en(_pref)
    elif _pref in WORLD_CITIES:
        prefecture_label = world_city_label(_pref)
    else:
        prefecture_label = "Unknown / overseas (Tokyo used as a substitute)"

    return render_template(
        "en/result.html",
        report=report,
        user_data=user_data,
        gender_label=gender_label,
        hour_label=hour_label,
        prefecture_label=prefecture_label,
        module_count=len(MODULES),
    )


@app.route("/en/about", methods=["GET"])
def about_en():
    """英語版：このアプリについて。"""
    module_names_en = [module_name_en(name) for name, _ in MODULES]
    return render_template("en/about.html", modules=module_names_en)


@app.route("/en/privacy", methods=["GET"])
def privacy_en():
    """英語版：プライバシーポリシー。"""
    return render_template(
        "en/privacy.html", updated_on=POLICY_UPDATED_ON, ad_network="Google AdSense")


@app.route("/en/contact", methods=["GET"])
def contact_en():
    """英語版：お問い合わせ・運営者情報。"""
    return render_template("en/contact.html")


@app.route("/guides", methods=["GET"])
def guides():
    """占術ガイドの一覧を表示する。"""
    return render_template("guides.html", guides=GUIDES)


@app.route("/guides/<slug>", methods=["GET"])
def guide_detail(slug):
    """占術ガイドの個別記事を表示する。"""
    guide = get_guide(slug)
    if guide is None:
        return render_template("index.html", **_form_context(
            error="お探しの記事は見つかりませんでした。")), 404
    # 関連記事として、自分以外の記事を並び順に沿って4件表示する
    others = [g for g in GUIDES if g["slug"] != slug]
    start = [g["slug"] for g in GUIDES].index(slug)
    rotated = others[start:] + others[:start]
    return render_template("guide.html", guide=guide, others=rotated[:4])


@app.route("/en/guides", methods=["GET"])
def guides_en():
    """英語版：占術ガイドの一覧を表示する。"""
    return render_template("en/guides.html", guides=GUIDES_EN)


@app.route("/en/guides/<slug>", methods=["GET"])
def guide_detail_en(slug):
    """英語版：占術ガイドの個別記事を表示する。"""
    guide = get_guide_en(slug)
    if guide is None:
        return render_template("en/index.html", **_form_context_en(
            error="Sorry, we couldn't find that article.")), 404
    others = [g for g in GUIDES_EN if g["slug"] != slug]
    start = [g["slug"] for g in GUIDES_EN].index(slug)
    rotated = others[start:] + others[:start]
    return render_template("en/guide.html", guide=guide, others=rotated[:4])


@app.route("/sitemap.xml", methods=["GET"])
def sitemap_xml():
    """検索エンジン向けの sitemap.xml を生成する。"""
    base = request.url_root.rstrip("/")
    paths = ["/", "/about", "/guides", "/privacy", "/contact",
              "/en/", "/en/about", "/en/privacy", "/en/contact", "/en/guides"]
    paths += ["/guides/%s" % g["slug"] for g in GUIDES]
    paths += ["/en/guides/%s" % g["slug"] for g in GUIDES_EN]
    lastmod = today_jst().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path in paths:
        lines.append("  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>"
                     % (base, path, lastmod))
    lines.append("</urlset>")
    return Response("\n".join(lines) + "\n", mimetype="application/xml")


@app.route("/healthz", methods=["GET"])
def healthz():
    """稼働監視用のヘルスチェック。

    Render 無料プランのスリープ対策として、UptimeRobot などの
    外部監視サービスから定期的に叩くことを想定した軽量エンドポイント。
    """
    return Response("ok\n", mimetype="text/plain")


@app.route("/privacy", methods=["GET"])
def privacy():
    """プライバシーポリシー（AdSense審査の必須要件）を表示する。"""
    return render_template(
        "privacy.html",
        updated_on=POLICY_UPDATED_ON,
        ad_network="Google AdSense",
    )


@app.route("/contact", methods=["GET"])
def contact():
    """お問い合わせ・運営者情報を表示する。"""
    return render_template("contact.html")


@app.route("/ads.txt", methods=["GET"])
def ads_txt():
    """AdSense の ads.txt を配信する。

    ADSENSE_CLIENT_ID が未設定のうちは 404 を返す（誤った内容を配信しないため）。
    """
    if not ADSENSE_CLIENT_ID:
        return Response("ads.txt is not configured yet.\n",
                        status=404, mimetype="text/plain")
    publisher_id = ADSENSE_CLIENT_ID.replace("ca-pub-", "").strip()
    body = "google.com, pub-%s, DIRECT, f08c47fec0942fa0\n" % publisher_id
    return Response(body, mimetype="text/plain")


@app.route("/robots.txt", methods=["GET"])
def robots_txt():
    """クローラ向けの robots.txt を配信する。"""
    base = request.url_root.rstrip("/")
    body = "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % base
    return Response(body, mimetype="text/plain")


@app.errorhandler(404)
def not_found(_error):
    """404 は入力フォームへ誘導する（/en/ 配下なら英語版へ）。"""
    if request.path.startswith("/en/") or request.path == "/en":
        return render_template("en/index.html", **_form_context_en(
            error="The page you were looking for could not be found. Please try getting a reading instead.")), 404
    return render_template("index.html", **_form_context(
        error="お探しのページは見つかりませんでした。もう一度占ってみてください。")), 404


@app.errorhandler(500)
def server_error(_error):
    """500 も入力フォームへ誘導する（/en/ 配下なら英語版へ）。"""
    if request.path.startswith("/en/") or request.path == "/en":
        return render_template("en/index.html", **_form_context_en(
            error="Something went wrong while generating your reading. Please try again.")), 500
    return render_template("index.html", **_form_context(
        error="鑑定中に問題が発生しました。お手数ですが、もう一度お試しください。")), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
