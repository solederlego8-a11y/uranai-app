# -*- coding: utf-8 -*-
"""② 西洋占星術

太陽星座・月星座（簡易近似）・アセンダント（出生時刻×出生地の簡易近似）を求め、
「今日の太陽が位置する星座」との角度（アスペクト）から本日の運勢を算出する。
"""
from __future__ import annotations

from . import utils

MODULE_NAME = "西洋占星術"

SIGNS = [
    "牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座",
    "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座",
]

ELEMENT_OF_SIGN = {
    "牡羊座": "火", "獅子座": "火", "射手座": "火",
    "牡牛座": "地", "乙女座": "地", "山羊座": "地",
    "双子座": "風", "天秤座": "風", "水瓶座": "風",
    "蟹座": "水", "蠍座": "水", "魚座": "水",
}
ELEMENT_DIRECTION = {"火": "南", "地": "北", "風": "東", "水": "西"}

SIGN_COLOR = {
    "牡羊座": "赤", "牡牛座": "緑", "双子座": "黄", "蟹座": "銀",
    "獅子座": "金", "乙女座": "紺", "天秤座": "桃", "蠍座": "臙脂",
    "射手座": "紫", "山羊座": "黒", "水瓶座": "水色", "魚座": "藤色",
}
SIGN_ITEM = {
    "牡羊座": "赤いペン", "牡牛座": "香りのよいハンドクリーム",
    "双子座": "文庫本", "蟹座": "写真立て", "獅子座": "金色のアクセサリー",
    "乙女座": "小さなメモ帳", "天秤座": "香り付きのハンカチ", "蠍座": "黒い手帳",
    "射手座": "旅の地図やガイドブック", "山羊座": "革のベルト",
    "水瓶座": "ワイヤレスイヤホン", "魚座": "ラベンダーのアロマ",
}
SIGN_KEYWORD = {
    "牡羊座": "先手", "牡牛座": "安定", "双子座": "情報", "蟹座": "共感",
    "獅子座": "自信", "乙女座": "精度", "天秤座": "調和", "蠍座": "集中",
    "射手座": "冒険", "山羊座": "実績", "水瓶座": "革新", "魚座": "直感",
}

# 角度差 -> アスペクト名と基礎点
ASPECT_TABLE = {
    0: ("コンジャンクション（合）", 82),
    1: ("セミセクスタイル", 62),
    2: ("セクスタイル（60度）", 85),
    3: ("スクエア（90度）", 42),
    4: ("トライン（120度）", 92),
    5: ("クインカンクス", 48),
    6: ("オポジション（180度）", 55),
    7: ("クインカンクス", 48),
    8: ("トライン（120度）", 92),
    9: ("スクエア（90度）", 42),
    10: ("セクスタイル（60度）", 85),
    11: ("セミセクスタイル", 62),
}


def sun_sign(month: int, day: int) -> str:
    """生年月日（月・日）から太陽星座を判定する。"""
    boundaries = [
        (1, 20, "水瓶座"), (2, 19, "魚座"), (3, 21, "牡羊座"), (4, 20, "牡牛座"),
        (5, 21, "双子座"), (6, 22, "蟹座"), (7, 23, "獅子座"), (8, 23, "乙女座"),
        (9, 23, "天秤座"), (10, 24, "蠍座"), (11, 23, "射手座"), (12, 22, "山羊座"),
    ]
    prev_sign = "山羊座"  # 1月19日以前は山羊座
    for m, d, name in boundaries:
        if month == m:
            return name if day >= d else prev_sign
        if month < m:
            return prev_sign
        prev_sign = name
    return prev_sign


def moon_sign(year: int, month: int, day: int) -> str:
    """月星座の簡易近似（月の公転周期 約27.3日を月×日で近似）。"""
    index = (month * 31 + day * 13 + year) % 12
    return SIGNS[index]


def ascendant_sign(sun: str, hour, longitude: float) -> str:
    """アセンダントの簡易近似。

    太陽星座を基点に、出生時刻（2時間で1サイン進む）と
    出生地の経度差（東経135度＝日本標準時子午線からのズレ）で補正する。
    出生時刻不明時は太陽星座と同一とする。
    """
    if hour is None:
        return sun
    base = SIGNS.index(sun)
    # 日の出（およそ6時）にアセンダント＝太陽星座となる想定
    shift = int(((hour - 6) % 24) / 2)
    lon_shift = int((longitude - 135.0) / 15.0)
    return SIGNS[(base + shift + lon_shift) % 12]


def calculate(user_data: dict) -> dict:
    """西洋占星術を実行し、共通スキーマの dict を返す。"""
    year = user_data["birth_year"]
    month = user_data["birth_month"]
    day = user_data["birth_day"]
    hour = user_data.get("birth_hour")
    today = user_data["today"]
    longitude, latitude = utils.get_geo(user_data.get("prefecture", "unknown"))

    natal_sun = sun_sign(month, day)
    natal_moon = moon_sign(year, month, day)
    natal_asc = ascendant_sign(natal_sun, hour, longitude)
    transit_sun = sun_sign(today.month, today.day)

    # 本人の太陽星座と今日の太陽のアスペクトからスコアを算出
    diff = (SIGNS.index(transit_sun) - SIGNS.index(natal_sun)) % 12
    aspect_name, base = ASPECT_TABLE[diff]

    # 月星座と今日の太陽の関係で微調整（日替わりの揺らぎ）
    moon_diff = (SIGNS.index(transit_sun) - SIGNS.index(natal_moon)) % 12
    moon_bonus = [6, 1, 5, -4, 7, -2, 0, -2, 7, -4, 5, 1][moon_diff]
    score = utils.clamp_score(utils.expand_score(
        base * 0.85 + moon_bonus, utils.daily_seed(user_data, 2)))

    asc_element = ELEMENT_OF_SIGN[natal_asc]
    lucky_color = SIGN_COLOR[natal_sun]
    lucky_item = SIGN_ITEM[natal_moon]
    lucky_dir = ELEMENT_DIRECTION[asc_element]

    summary = "%sのあなたに今日の太陽は%s。%sの流れです。" % (
        natal_sun, aspect_name.split("（")[0], "追い風" if score >= 60 else "静観")

    detail = (
        "あなたの出生図は太陽が%s、月が%s、アセンダントが%sという配置です。"
        "太陽は人生で目指す方向性、月は素の感情、アセンダントは他人が最初に受け取るあなたの印象を示します。"
        "本日、天空の太陽は%sを運行しており、あなたの出生太陽%sとの角度は%sを形成しています。"
        "これは「%s」という質を持つ関係で、%s"
        "また月星座%sとの関係も重なり、感情面では%s傾向が出ます。"
        "アセンダント%sは%sのエレメントに属するため、行動の起点を%sの方角に置くと、"
        "今日のあなたの魅力が最も自然に伝わります。身に着ける色は%sを選んでください。"
    ) % (
        natal_sun, natal_moon, natal_asc,
        transit_sun, natal_sun, aspect_name,
        aspect_name,
        "自分から動くほど良い結果につながる配置です。" if base >= 80
        else "無理に押し切らず、周囲の反応を見てから動くのが賢明な配置です。",
        natal_moon,
        "落ち着いて余裕を保てる" if moon_bonus >= 0 else "些細なことが気になりやすい",
        natal_asc, asc_element, lucky_dir, lucky_color,
    )

    keywords = [
        SIGN_KEYWORD[natal_sun], SIGN_KEYWORD[natal_moon],
        aspect_name.split("（")[0], asc_element + "のエレメント",
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
            "sun_sign": natal_sun,
            "moon_sign": natal_moon,
            "ascendant": natal_asc,
            "transit_sun": transit_sun,
            "aspect": aspect_name,
            "element": asc_element,
            "longitude": longitude,
            "latitude": latitude,
        },
    }
