# -*- coding: utf-8 -*-
"""⑧ インド占星術（ジョーティシュ）

アヤナムシャ補正（約23.85度）を適用したサイデリアル星座（ラーシ）と、
27 のナクシャトラ（月宿）を判定し、本日のトランジットとの相性を評価する。
"""
from __future__ import annotations

from . import utils
from .seiyo_uranai import SIGNS, sun_sign

MODULE_NAME = "インド占星術"

AYANAMSA = 23.85  # ラヒリ・アヤナムシャの近似値（度）

RASHI = [
    "メーシャ（牡羊）", "ヴリシャバ（牡牛）", "ミトゥナ（双子）", "カルカ（蟹）",
    "シンハ（獅子）", "カニヤー（乙女）", "トゥラー（天秤）", "ヴリシュチカ（蠍）",
    "ダヌ（射手）", "マカラ（山羊）", "クンバ（水瓶）", "ミーナ（魚）",
]
RASHI_LORD = [
    "火星", "金星", "水星", "月", "太陽", "水星",
    "金星", "火星", "木星", "土星", "土星", "木星",
]
RASHI_COLOR = {
    0: "赤", 1: "白", 2: "緑", 3: "銀", 4: "金", 5: "緑",
    6: "白", 7: "臙脂", 8: "黄", 9: "紺", 10: "藍", 11: "黄",
}
RASHI_ITEM = {
    0: "赤い糸のブレスレット", 1: "白檀の香", 2: "緑色のノート",
    3: "銀色の小物", 4: "金色のペン", 5: "エメラルドグリーンの小物",
    6: "白い花", 7: "赤い石のお守り", 8: "黄色のスカーフ",
    9: "黒い革の小物", 10: "藍色のハンカチ", 11: "黄色の紐",
}
RASHI_DIR = {
    0: "東", 1: "南東", 2: "北", 3: "北西", 4: "東", 5: "北",
    6: "南東", 7: "北", 8: "北東", 9: "西", 10: "西", 11: "北東",
}

NAKSHATRA = [
    "アシュヴィニー", "バラニー", "クリッティカー", "ローヒニー", "ムリガシラー",
    "アールドラー", "プナルヴァス", "プシュヤ", "アーシュレーシャー", "マガー",
    "プールヴァ・パールグニー", "ウッタラ・パールグニー", "ハスタ", "チトラー",
    "スヴァーティー", "ヴィシャーカー", "アヌラーダー", "ジェーシュター", "ムーラ",
    "プールヴァ・アーシャーダー", "ウッタラ・アーシャーダー", "シュラヴァナ",
    "ダニシュター", "シャタビシャー", "プールヴァ・バードラパダー",
    "ウッタラ・バードラパダー", "レーヴァティー",
]
NAKSHATRA_MEANING = [
    "馬の頭。素早い行動と治癒の力", "抑制の星。忍耐が実を結ぶ", "炎の刃。純化と決断",
    "赤い牛。豊穣と美の恩恵", "鹿の頭。探索と好奇心", "涙の星。破壊のあとの再生",
    "帰還の星。やり直しが利く", "養育の星。守られ、育てられる",
    "抱擁する蛇。深い洞察と執着", "王座。伝統と誇り",
    "前の吉星。享楽と創造", "後の吉星。契約と結束", "手のひら。技術と器用さ",
    "輝く宝石。美と多才", "独立の風。自由と交渉力", "枝分かれ。目標達成の執念",
    "友愛の星。仲間との協働", "年長の星。権威と責任", "根。根本から掘り起こす力",
    "不敗の前。粘り強い勝利", "不敗の後。最終的な勝利",
    "耳を傾ける。学びと聴く力", "太鼓。リズムと富",
    "百人の医師。癒やしと秘密", "前の足。情熱と献身",
    "後の足。深い安定と智慧", "豊かさ。旅立ちと保護",
]
NAKSHATRA_COLOR = [
    "赤", "白", "白", "白", "銀", "緑", "灰", "赤", "黒", "生成り",
    "茶", "青", "緑", "黒", "黒", "金", "赤", "生成り", "黄",
    "黒", "茶", "藍", "銀", "青緑", "灰", "紫", "茶",
]

# ターラー（本命ナクシャトラから今日のナクシャトラまでの距離）による吉凶
TARA_TABLE = [
    ("ジャンマ（誕生）", 62), ("サンパット（財）", 90), ("ヴィパット（災）", 34),
    ("クシェーマ（安泰）", 86), ("プラティヤク（障害）", 40), ("サーダカ（成就）", 92),
    ("ヴァダ（危険）", 30), ("ミトラ（友好）", 84), ("アティミトラ（親友）", 88),
]


def rashi_index(month: int, day: int) -> int:
    """サイデリアル星座（ラーシ）のインデックスを返す。

    西洋のトロピカル太陽星座からアヤナムシャ分（約23.85度＝ほぼ1星座）
    ずらす近似で求める。
    """
    tropical = SIGNS.index(sun_sign(month, day))
    shift = int(AYANAMSA // 30) + 1  # 約24度のずれは実質1サイン分の後退
    return (tropical - shift) % 12


def nakshatra_index(year: int, month: int, day: int) -> int:
    """ナクシャトラ（27宿）のインデックスを返す。"""
    return (year * 12 + month * 30 + day) % 27


def calculate(user_data: dict) -> dict:
    """インド占星術を実行し、共通スキーマの dict を返す。"""
    year = user_data["birth_year"]
    month = user_data["birth_month"]
    day = user_data["birth_day"]
    hour = user_data.get("birth_hour")
    today = user_data["today"]
    longitude, _ = utils.get_geo(user_data.get("prefecture", "unknown"))

    r_idx = rashi_index(month, day)
    n_idx = nakshatra_index(year, month, day)

    # ラグナ（アセンダント）：出生時刻と出生地経度から簡易近似
    if hour is None:
        lagna_idx = r_idx
        lagna_note = "出生時刻が不明のため、ラグナは太陽ラーシと同一として扱っています"
    else:
        lagna_idx = (r_idx + int(((hour - 6) % 24) / 2)
                     + int((longitude - 82.5) / 15.0)) % 12
        lagna_note = "出生時刻%d時と出生地の経度%.2f度からラグナを算出しています" % (hour, longitude)

    # 今日のトランジット
    t_rashi = rashi_index(today.month, today.day)
    t_nakshatra = nakshatra_index(today.year, today.month, today.day)

    tara_index = (t_nakshatra - n_idx) % 9
    tara_name, tara_score = TARA_TABLE[tara_index]

    rashi_diff = (t_rashi - r_idx) % 12
    rashi_bonus = [8, -2, 5, -5, 7, -3, 2, -3, 7, -5, 5, -2][rashi_diff]

    score = utils.clamp_score(utils.expand_score(
        tara_score * 0.8 + rashi_bonus, utils.daily_seed(user_data, 8)))

    lucky_color = NAKSHATRA_COLOR[n_idx]
    lucky_item = RASHI_ITEM[r_idx]
    lucky_dir = RASHI_DIR[r_idx]

    summary = "%s／%s。今日のターラーは%sです。" % (
        RASHI[r_idx].split("（")[0], NAKSHATRA[n_idx], tara_name.split("（")[0])

    detail = (
        "インド占星術ではアヤナムシャ（歳差補正、約%.2f度）を差し引いたサイデリアル方式を用います。"
        "あなたの太陽ラーシは%s、支配星は%sです。"
        "生まれ月のナクシャトラ（月宿）は第%d宿の%sで、その象意は「%s」です。"
        "ラグナ（上昇宮）は%sとなります。%s。"
        "本日、月は%s（第%d宿）を運行しており、あなたの本命宿から数えて%d番目にあたるため、"
        "ターラーは「%s」となります。%s"
        "太陽ラーシの関係は%dサイン離れており、%s。"
        "本日は%sの方角を向いて一日の予定を立て、%s色を身近に置くことで、"
        "宿の主星からの加護を受け取りやすくなります。"
    ) % (
        AYANAMSA, RASHI[r_idx], RASHI_LORD[r_idx],
        n_idx + 1, NAKSHATRA[n_idx], NAKSHATRA_MEANING[n_idx],
        RASHI[lagna_idx], lagna_note,
        NAKSHATRA[t_nakshatra], t_nakshatra + 1, tara_index + 1,
        tara_name,
        "積極的な行動が実を結ぶ配置です。" if tara_score >= 80
        else "今日は守りを固め、重要な決断は先送りするのが賢明です。",
        rashi_diff,
        "気力が充実しやすい配置です" if rashi_bonus >= 0 else "エネルギーの消耗に注意が必要な配置です",
        lucky_dir, lucky_color,
    )

    keywords = [
        RASHI[r_idx].split("（")[0], NAKSHATRA[n_idx],
        tara_name.split("（")[0], RASHI_LORD[r_idx],
    ]

    return {
        "name": MODULE_NAME,
        "summary": summary[:50],
        "detail": detail,
        "lucky_color": lucky_color,
        "lucky_item": lucky_item,
        "lucky_dir": lucky_dir,
        "score": score,
        "keywords": keywords,
        "raw": {
            "rashi": RASHI[r_idx],
            "rashi_lord": RASHI_LORD[r_idx],
            "nakshatra": NAKSHATRA[n_idx],
            "nakshatra_number": n_idx + 1,
            "lagna": RASHI[lagna_idx],
            "today_nakshatra": NAKSHATRA[t_nakshatra],
            "tara": tara_name,
            "ayanamsa": AYANAMSA,
        },
    }
