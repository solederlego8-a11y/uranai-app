# -*- coding: utf-8 -*-
"""Python 版占いエンジンから JS 移植版の正解データ（tests/fixtures/cases.json）を生成する。

使い方:  python tests/gen_cases.py
出力:    tests/fixtures/cases.json
  {
    "generated_by": "...",
    "cases": [ {"id", "input", "expected_ja", "expected_en"} ... ],
    "validation_cases": [ {"id", "form", "lang", "expected": {"user_data"|null, "error"}} ... ]
  }
  - input.today は 'YYYY-MM-DD' 文字列。
  - expected_ja は build_report() の戻り値そのもの。
  - expected_en は translate_report() が追加する "_en" 系キーのみ（ファイル肥大化を防ぐため）。
    translate_report() は dict(report) に "_en" キーを足すだけなので、完全な英語版の期待値は
      full_en = {**expected_ja, **expected_en,
                 "detail_results_en": [{**expected_ja.detail_results[i], **expected_en.detail_results_en[i]} ...]}
    で厳密に復元できる（tests/verify.js はこの復元結果と deep equal 比較する）。
  - validation_cases は app.parse_user_data() の結果（today は固定日付で評価）。

【注意】Python 3.11 で実行すること（3.12 以降は sum() の浮動小数点加算が
補正付きになり、スコアの丸め境界でごく稀に結果がずれる可能性がある）。
乱数は使わず、すべて決定論的に入力を組み立てる。
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from lunardate import LunarDate  # noqa: E402

from uranai import build_report  # noqa: E402
from uranai.i18n import translate_report  # noqa: E402
from uranai.utils import PREFECTURES, WORLD_CITIES  # noqa: E402

import app as flask_app  # noqa: E402

OUT_PATH = os.path.join(ROOT, "tests", "fixtures", "cases.json")

GENDERS = ["male", "female", "unknown"]
BIRTHPLACES = list(PREFECTURES) + list(WORLD_CITIES) + ["unknown"]

TODAYS = [
    "2026-09-11", "2026-01-01", "2026-02-03", "2026-02-04", "2026-12-31",
    "2024-02-29", "2025-07-07", "2026-03-20", "2027-01-15", "2026-10-31",
    "2026-05-05", "2026-11-23", "2026-06-06", "2026-08-08", "2033-12-07",
]

# 姓名の文字種バリエーション（漢字辞書あり/なし・かな・カナ・英字・記号・全角・非BMP等）
NAMES = [
    ("山田", "太郎"), ("佐藤", "花子"), ("鈴木", "一郎"), ("高橋", "美咲"),
    ("田中", "健"), ("伊藤", "翔太"), ("渡辺", "結衣"), ("小林", "颯"),
    ("加藤", "凛"), ("斎藤", "陽菜"), ("やまだ", "たろう"), ("さとう", "はなこ"),
    ("ヤマダ", "タロウ"), ("スズキ", "イチロー"), ("Smith", "John"),
    ("garcia", "maria"), ("O'Brien", "Anne-Marie"), ("Müller", "Jürgen"),
    ("Ｙａｍａｄａ", "Ｔａｒｏ"), ("龘龘", "𠮷野"), ("鑑鷲", "驚籠"),
    ("一二三", "四五六"), ("七八九", "十百千"), ("山 田", "太 郎"),
    ("東京都民", "無名"), ("々", "ゝ"), ("ヴィクトル", "ジョージ"),
    ("きゃりー", "ぱみゅぱみゅ"), ("Σωκράτης", "Иван"), ("王", "力"),
    ("長谷川", "翔平"), ("小鳥遊", "きょうこ"), ("五十嵐", "麗"),
    ("十二", "三十三"), ("Lee", "Yu"), ("陳", "美玲"), ("Nguyễn", "Văn"),
    ("abcdefghij", "klmnopqrst"), ("あいうえおかきくけこ", "さしすせそたちつてと"),
    ("澤", "歩"), ("鷗外", "森"), ("😀山", "田🎉"), ("Ａ１", "２Ｂ"),
    ("１２３", "４５６"), ("a b", "c d"), ("藤原", "道長"), ("織田", "信長"),
    ("徳川", "家康"), ("豊臣", "秀吉"), ("葛飾", "北斎"),
]

HOURS = [None, 0, 1, 5, 6, 11, 12, 13, 17, 18, 22, 23]


def _leap_month_solar_dates():
    """旧暦の閏月に当たる新暦日付（1900〜2026年、閏月のある年ごとに1日）を lunardate から求める。"""
    res = []
    k = 0
    for y in range(1900, 2027):
        lm = LunarDate.leap_month_for_year(y)
        if lm:
            for d in ((1, 15, 29)[k % 3], 15, 1):
                try:
                    res.append(LunarDate(y, lm, d, True).to_solar_date())
                    break
                except ValueError:
                    continue
            k += 1
    return res


def _make_case(idx, last, first, y, m, d, hour, gender, place, today):
    return {
        "id": "case%03d" % idx,
        "input": {
            "last_name": last, "first_name": first,
            "birth_year": y, "birth_month": m, "birth_day": d,
            "birth_hour": hour, "gender": gender, "prefecture": place,
            "today": today,
        },
    }


def build_inputs():
    inputs = []
    n = 0

    def add(last, first, y, m, d, hour, gender, place, today):
        nonlocal n
        n += 1
        inputs.append(_make_case(n, last, first, y, m, d, hour, gender, place, today))

    # 1) 年代スイープ（1900〜2026 を 3 年刻み）: 月日・時刻・性別・出生地・today を巡回
    i = 0
    for y in range(1900, 2027, 3):
        m = (i * 5) % 12 + 1
        d = (i * 7) % 28 + 1
        add(*NAMES[i % len(NAMES)], y, m, d, HOURS[i % len(HOURS)],
            GENDERS[i % 3], BIRTHPLACES[(i * 11) % len(BIRTHPLACES)],
            TODAYS[i % len(TODAYS)])
        i += 1

    # 2) 境界日付（1900年1月の旧暦負日・甲子基準日・立春・節入り・閏年 2/29・年末年始）
    boundary_dates = [
        (1900, 1, 1), (1900, 1, 30), (1900, 1, 31), (1900, 2, 1), (1900, 2, 3),
        (1900, 2, 4), (1900, 12, 31), (1923, 12, 31), (1924, 1, 1), (1924, 1, 2),
        (1924, 2, 3), (1924, 2, 4), (1924, 2, 29), (1904, 2, 29), (1920, 2, 29),
        (1960, 2, 29), (1988, 2, 29), (2000, 2, 29), (2004, 2, 29), (2016, 2, 29),
        (2020, 2, 29), (2024, 2, 29), (1999, 12, 31), (2000, 1, 1), (2000, 1, 5),
        (2000, 1, 6), (2000, 12, 6), (2000, 12, 7), (1985, 3, 5), (1985, 3, 6),
        (1985, 7, 6), (1985, 7, 7), (1985, 8, 7), (1985, 8, 8), (1985, 11, 6),
        (1985, 11, 7), (2026, 9, 11), (2026, 9, 10), (2026, 1, 1), (2025, 12, 31),
        (1950, 6, 21), (1950, 6, 22), (1975, 10, 23), (1975, 10, 24),
        (1999, 1, 19), (1999, 1, 20), (2010, 12, 21), (2010, 12, 22),
    ]
    for k, (y, m, d) in enumerate(boundary_dates):
        add(*NAMES[(k * 3) % len(NAMES)], y, m, d, HOURS[(k * 5) % len(HOURS)],
            GENDERS[(k + 1) % 3], BIRTHPLACES[(k * 13 + 7) % len(BIRTHPLACES)],
            TODAYS[(k * 2) % len(TODAYS)])

    # 3) 旧暦の閏月に当たる日
    for k, sd in enumerate(_leap_month_solar_dates()):
        add(*NAMES[(k * 7 + 1) % len(NAMES)], sd.year, sd.month, sd.day,
            HOURS[(k * 3) % len(HOURS)], GENDERS[k % 3],
            BIRTHPLACES[(k * 17 + 3) % len(BIRTHPLACES)], TODAYS[(k * 3 + 1) % len(TODAYS)])

    # 4) 出生時刻 0〜23 時 + 不明（固定の生年月日で）
    for h in [None] + list(range(24)):
        k = 0 if h is None else h + 1
        add(*NAMES[(k * 2) % len(NAMES)], 1990, 5, 15, h, GENDERS[k % 3],
            BIRTHPLACES[(k * 19 + 5) % len(BIRTHPLACES)], TODAYS[k % len(TODAYS)])

    # 5) 出生地スイープ（47都道府県 + 49世界都市 + unknown、時刻あり）
    #    ＝ 姓名バリエーション全件のスイープを兼ねる（NAMES を順に巡回）
    for k, place in enumerate(BIRTHPLACES):
        add(*NAMES[k % len(NAMES)], 1970 + (k * 3) % 50, (k * 7) % 12 + 1,
            (k * 3) % 28 + 1, HOURS[1 + k % (len(HOURS) - 1)], GENDERS[k % 3], place,
            TODAYS[(k * 7) % len(TODAYS)])

    # 6) today スイープ（同一人物で today だけ変える）
    for k, today in enumerate(TODAYS):
        add("山田", "太郎", 1990, 5, 15, None, "male", "東京都", today)
        add("佐藤", "花子", 1985, 12, 24, 8, "female", "new_york", today)

    return inputs


def _user_data(inp):
    ud = dict(inp)
    ud["today"] = date.fromisoformat(inp["today"])
    return ud


def build_validation_cases():
    """app.parse_user_data() の期待値（today を 2026-09-11 に固定して評価）。"""
    fixed_today = date(2026, 9, 11)
    flask_app.today_jst = lambda: fixed_today  # 未来日付チェックを固定日で行う

    forms = [
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "1990", "birth_month": "5",
          "birth_day": "15", "birth_hour": "", "gender": "male", "prefecture": "東京都"}, "ja"),
        ({"last_name": " 山田 ", "first_name": "太郎", "birth_year": "1990", "birth_month": "5",
          "birth_day": "15", "birth_hour": "12", "gender": "female", "prefecture": "new_york"}, "en"),
        ({"last_name": "", "first_name": "太郎", "birth_year": "1990", "birth_month": "5",
          "birth_day": "15"}, "ja"),
        ({"last_name": "山田", "first_name": "   ", "birth_year": "1990", "birth_month": "5",
          "birth_day": "15"}, "en"),
        ({"last_name": "あいうえおかきくけこさ", "first_name": "太郎", "birth_year": "1990",
          "birth_month": "5", "birth_day": "15"}, "ja"),
        ({"last_name": "山田", "first_name": "abcdefghijk", "birth_year": "1990",
          "birth_month": "5", "birth_day": "15"}, "en"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "", "birth_month": "5",
          "birth_day": "15"}, "ja"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "1990", "birth_month": "abc",
          "birth_day": "15"}, "en"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "1899", "birth_month": "5",
          "birth_day": "15"}, "ja"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "2027", "birth_month": "1",
          "birth_day": "1"}, "en"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "2023", "birth_month": "2",
          "birth_day": "29"}, "ja"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "1990", "birth_month": "13",
          "birth_day": "1"}, "en"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "2026", "birth_month": "9",
          "birth_day": "12"}, "ja"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "2026", "birth_month": "9",
          "birth_day": "11", "gender": "unknown", "prefecture": "沖縄県"}, "en"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "1990", "birth_month": "5",
          "birth_day": "15", "birth_hour": "x"}, "ja"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "1990", "birth_month": "5",
          "birth_day": "15", "birth_hour": "24"}, "en"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "1990", "birth_month": "5",
          "birth_day": "15", "birth_hour": "-1"}, "ja"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "1990", "birth_month": "5",
          "birth_day": "15", "birth_hour": " 23 ", "gender": "other", "prefecture": "Mars"}, "en"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "2000", "birth_month": "2",
          "birth_day": "29", "birth_hour": "0", "gender": "", "prefecture": ""}, "ja"),
        ({"last_name": "Smith", "first_name": "John", "birth_year": "1975", "birth_month": "11",
          "birth_day": "30", "birth_hour": "7", "gender": "male", "prefecture": "london"}, "en"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "1990", "birth_month": "4",
          "birth_day": "31"}, "ja"),
        ({"last_name": "山田", "first_name": "太郎", "birth_year": "1900", "birth_month": "1",
          "birth_day": "1", "birth_hour": "23", "gender": "female", "prefecture": "北海道"}, "ja"),
    ]
    cases = []
    for k, (form, lang) in enumerate(forms):
        ud, err = flask_app.parse_user_data(form, lang=lang)
        if ud is not None:
            ud = dict(ud)
            ud["today"] = ud["today"].isoformat()
        cases.append({
            "id": "valid%03d" % (k + 1),
            "form": form,
            "lang": lang,
            "expected": {"user_data": ud, "error": err},
        })
    return cases


def _en_delta(en):
    """translate_report() の戻り値から "_en" 系キーだけを抜き出す。"""
    delta = {k: v for k, v in en.items() if k.endswith("_en")}
    delta["detail_results_en"] = [
        {k: v for k, v in r.items() if k.endswith("_en")} for r in en["detail_results_en"]
    ]
    return delta


def main():
    inputs = build_inputs()
    cases = []
    for c in inputs:
        ud = _user_data(c["input"])
        report = build_report(ud)
        en = translate_report(report, ud)
        # translate_report は dict(report) + "_en" キーという契約なので、ここで検証しておく
        assert all(en[k] == v for k, v in report.items())
        assert all(en["detail_results_en"][i][k] == v
                   for i, r in enumerate(report["detail_results"]) for k, v in r.items())
        cases.append({
            "id": c["id"],
            "input": c["input"],
            "expected_ja": report,
            "expected_en": _en_delta(en),
        })

    payload = {
        "generated_by": "tests/gen_cases.py (Python %d.%d.%d, lunardate table)" % sys.version_info[:3],
        "case_count": len(cases),
        "cases": cases,
        "validation_cases": build_validation_cases(),
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    print("wrote %s: %d cases, %d validation cases (%.1f MB)" % (
        OUT_PATH, len(cases), len(payload["validation_cases"]),
        os.path.getsize(OUT_PATH) / 1e6))


if __name__ == "__main__":
    main()
