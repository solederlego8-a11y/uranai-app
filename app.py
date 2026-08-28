# -*- coding: utf-8 -*-
"""総合鑑定占いアプリ（Flask）

5項目の入力から11種の占術（命占10種＋姓名判断）をすべて計算し、
「今日の総合鑑定」として1つの結論にまとめて表示する。
"""
from __future__ import annotations

import os
from datetime import date

from flask import Flask, Response, render_template, request

from uranai import MODULES, build_report
from uranai.aggregator import CATEGORY_LABEL
from uranai.guides import GUIDES, get_guide
from uranai.utils import PREFECTURES

app = Flask(__name__)

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

GENDER_CHOICES = [
    ("male", "男性"),
    ("female", "女性"),
    ("unknown", "回答しない"),
]

HOUR_CHOICES = [("", "不明")] + [(str(h), "%d時台" % h) for h in range(24)]

# 入力フォームの選択肢に渡す年の範囲
YEAR_MIN = 1900
YEAR_MAX = date.today().year


def _form_context(form=None, error=None) -> dict:
    """入力フォームの描画に必要なコンテキストを組み立てる。"""
    return {
        "prefectures": PREFECTURES,
        "genders": GENDER_CHOICES,
        "hours": HOUR_CHOICES,
        "year_min": YEAR_MIN,
        "year_max": YEAR_MAX,
        "today": date.today(),
        "form": form or {},
        "error": error,
    }


def parse_user_data(form) -> tuple:
    """フォームの入力値を検証し、内部表現の dict に整形する。

    戻り値: (user_data, エラーメッセージ)  ※エラー時 user_data は None
    """
    last_name = (form.get("last_name") or "").strip()
    first_name = (form.get("first_name") or "").strip()
    if not last_name or not first_name:
        return None, "姓と名の両方を入力してください。"
    if len(last_name) > 10 or len(first_name) > 10:
        return None, "姓・名はそれぞれ10文字以内で入力してください。"

    try:
        birth_year = int(form.get("birth_year", ""))
        birth_month = int(form.get("birth_month", ""))
        birth_day = int(form.get("birth_day", ""))
    except (TypeError, ValueError):
        return None, "生年月日を正しく選択してください。"

    if not (YEAR_MIN <= birth_year <= YEAR_MAX):
        return None, "生年は%d年から%d年の範囲で選択してください。" % (YEAR_MIN, YEAR_MAX)
    try:
        birth = date(birth_year, birth_month, birth_day)
    except ValueError:
        return None, "存在しない日付です。生年月日を確認してください。"
    if birth > date.today():
        return None, "生年月日に未来の日付は指定できません。"

    hour_raw = (form.get("birth_hour") or "").strip()
    if hour_raw == "":
        birth_hour = None  # 不明。各占術側で正午（12時）として補完する
    else:
        try:
            birth_hour = int(hour_raw)
        except ValueError:
            return None, "出生時刻を正しく選択してください。"
        if not (0 <= birth_hour <= 23):
            return None, "出生時刻は0時から23時の範囲で選択してください。"

    gender = form.get("gender") or "unknown"
    if gender not in [g for g, _ in GENDER_CHOICES]:
        gender = "unknown"

    prefecture = form.get("prefecture") or "unknown"
    if prefecture not in PREFECTURES:
        prefecture = "unknown"  # 「不明・海外」は東京（東経139.69度）で代替

    return {
        "last_name": last_name,
        "first_name": first_name,
        "birth_year": birth_year,
        "birth_month": birth_month,
        "birth_day": birth_day,
        "birth_hour": birth_hour,
        "gender": gender,
        "prefecture": prefecture,
        "today": date.today(),
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


@app.route("/sitemap.xml", methods=["GET"])
def sitemap_xml():
    """検索エンジン向けの sitemap.xml を生成する。"""
    base = request.url_root.rstrip("/")
    paths = ["/", "/about", "/guides", "/privacy", "/contact"]
    paths += ["/guides/%s" % g["slug"] for g in GUIDES]
    lastmod = date.today().isoformat()
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
    """404 は入力フォームへ誘導する。"""
    return render_template("index.html", **_form_context(
        error="お探しのページは見つかりませんでした。もう一度占ってみてください。")), 404


@app.errorhandler(500)
def server_error(_error):
    """500 も入力フォームへ誘導する。"""
    return render_template("index.html", **_form_context(
        error="鑑定中に問題が発生しました。お手数ですが、もう一度お試しください。")), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
