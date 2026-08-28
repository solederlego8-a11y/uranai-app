# -*- coding: utf-8 -*-
"""⑤ 九星気学

本命星・月命星を算出し、今日の日盤・年盤との相性から本日の運勢を導く。
月盤を組み立てて吉方位を 3 つ算出し、その第一候補をラッキー方位とする。
"""
from __future__ import annotations

from . import utils

MODULE_NAME = "九星気学"

STAR_NAMES = {
    1: "一白水星", 2: "二黒土星", 3: "三碧木星", 4: "四緑木星", 5: "五黄土星",
    6: "六白金星", 7: "七赤金星", 8: "八白土星", 9: "九紫火星",
}
STAR_ELEMENT = {
    1: "水", 2: "土", 3: "木", 4: "木", 5: "土",
    6: "金", 7: "金", 8: "土", 9: "火",
}
STAR_COLOR = {
    1: "白", 2: "黄", 3: "青緑", 4: "緑", 5: "黄",
    6: "白", 7: "赤", 8: "茶", 9: "紫",
}
STAR_NATURE = {
    1: "水のように流れ、どんな器にも収まる柔軟さと忍耐力",
    2: "大地のように受け止め、こつこつ育てる母性と実務力",
    3: "若木のように伸びる、瞬発力と発信力に満ちた行動力",
    4: "風のように広がる、人と人をつなぐ調整力と信用",
    5: "中心に座る帝王の星。良くも悪くも影響力が大きい存在感",
    6: "天の星。責任感と統率力で組織を引っ張る指導力",
    7: "実りと悦びの星。会話と愛嬌で場を和ませる社交力",
    8: "山の星。変化を土台に変える粘りと蓄財力",
    9: "太陽と炎の星。発見され、注目される華やかさと知性",
}
STAR_ITEM = {
    1: "水筒", 2: "エコバッグ", 3: "イヤホン", 4: "扇子またはハンカチ",
    5: "印鑑またはスタンプ", 6: "腕時計", 7: "リップまたはミント",
    8: "小さな石のお守り", 9: "鏡",
}

# 後天定位盤（方位 -> 定位番号）
TEIIBAN = {
    "北": 1, "南西": 2, "東": 3, "南東": 4,
    "北西": 6, "西": 7, "北東": 8, "南": 9,
}


def honmei_star(year: int, month: int, day: int) -> int:
    """本命星を算出する（2月4日以前生まれは前年扱い）。"""
    y = year
    if month < 2 or (month == 2 and day < 4):
        y -= 1
    star = (11 - ((y - 1) % 9)) % 9
    return 9 if star == 0 else star


# 九星月命星テーブル（本命星の系統 × 生月）
GETSUMEI_TABLE = {
    # 本命星が 1,4,7 の場合
    0: {2: 8, 3: 7, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2, 9: 1, 10: 9, 11: 8, 12: 7, 1: 6},
    # 本命星が 2,5,8 の場合
    1: {2: 2, 3: 1, 4: 9, 5: 8, 6: 7, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1, 1: 9},
    # 本命星が 3,6,9 の場合
    2: {2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 9, 8: 8, 9: 7, 10: 6, 11: 5, 12: 4, 1: 3},
}


def getsumei_star(honmei: int, month: int, day: int) -> int:
    """月命星を算出する（節入り前は前月扱い）。"""
    m = month
    if day < utils.SETSUIRI_DAY[month]:
        m -= 1
        if m == 0:
            m = 12
    group = {1: 0, 4: 0, 7: 0, 2: 1, 5: 1, 8: 1, 3: 2, 6: 2, 9: 2}[honmei]
    return GETSUMEI_TABLE[group][m]


def year_star(year: int) -> int:
    """指定年の年盤中宮星を返す。"""
    star = (11 - ((year - 1) % 9)) % 9
    return 9 if star == 0 else star


def month_star_of(year: int, month: int) -> int:
    """指定年月の月盤中宮星を返す（節切りの簡易近似）。"""
    group = {1: 0, 4: 0, 7: 0, 2: 1, 5: 1, 8: 1, 3: 2, 6: 2, 9: 2}[year_star(year)]
    return GETSUMEI_TABLE[group][month]


# 日盤の基準日（1900-01-01 を一白水星の日とする陽遁基準の簡易近似）
DAY_BAN_BASE = utils.SEXAGENARY_BASE_DATE


def day_star_of(target) -> int:
    """指定日の日盤中宮星を返す（9日周期の決定論的循環）。"""
    days = (target - DAY_BAN_BASE).days
    star = days % 9
    return 9 if star == 0 else star


def chart_star_at(center: int, direction: str) -> int:
    """中宮星 center の盤で、指定方位に回座する九星を返す。"""
    n = TEIIBAN[direction]
    star = (n + (center - 5) - 1) % 9 + 1
    return star


def lucky_directions(honmei: int, center: int) -> list:
    """本命星と月盤の中宮星から吉方位を算出する。"""
    result = []
    # 五黄殺・暗剣殺・本命殺・本命的殺の方位を除外する
    gouou_dir = None
    honmei_dir = None
    for d in utils.DIRECTIONS:
        s = chart_star_at(center, d)
        if s == 5:
            gouou_dir = d
        if s == honmei:
            honmei_dir = d
    forbidden = set()
    if gouou_dir:
        forbidden.add(gouou_dir)
        forbidden.add(utils.OPPOSITE_DIRECTION[gouou_dir])
    if honmei_dir:
        forbidden.add(honmei_dir)
        forbidden.add(utils.OPPOSITE_DIRECTION[honmei_dir])

    honmei_el = STAR_ELEMENT[honmei]
    scored = []
    for d in utils.DIRECTIONS:
        if d in forbidden:
            continue
        s = chart_star_at(center, d)
        el = STAR_ELEMENT[s]
        rel = utils.element_relation(honmei_el, el)
        if rel in ("比和", "相生（与える）", "相生（受ける）"):
            scored.append((utils.ELEMENT_RELATION_SCORE[rel], d, s))
    # 相性点の高い順（同点は方位の並び順）で並べる
    scored.sort(key=lambda t: (-t[0], utils.DIRECTIONS.index(t[1])))
    for _, d, s in scored[:3]:
        result.append((d, STAR_NAMES[s]))
    if not result:
        # すべて塞がっている場合は本命星の五行の定位方位を採用する
        result.append((utils.ELEMENT_DIRECTION[honmei_el], STAR_NAMES[honmei]))
    return result


def calculate(user_data: dict) -> dict:
    """九星気学を実行し、共通スキーマの dict を返す。"""
    year = user_data["birth_year"]
    month = user_data["birth_month"]
    day = user_data["birth_day"]
    today = user_data["today"]

    honmei = honmei_star(year, month, day)
    getsumei = getsumei_star(honmei, month, day)

    today_year_star = year_star(today.year)
    today_month_star = month_star_of(today.year, today.month)
    today_day_star = day_star_of(today)

    honmei_el = STAR_ELEMENT[honmei]
    # 今日の日盤中宮星との相性が本日の運勢の核
    day_score = utils.element_relation_score(honmei_el, STAR_ELEMENT[today_day_star])
    year_score = utils.element_relation_score(honmei_el, STAR_ELEMENT[today_year_star])
    # 本命星が今日の盤で回座している方位（傾斜）
    seat = None
    for d in utils.DIRECTIONS:
        if chart_star_at(today_day_star, d) == honmei:
            seat = d
            break
    if seat is None:
        seat = "中央"

    score = utils.clamp_score(utils.expand_score(
        day_score * 0.7 + year_score * 0.3, utils.daily_seed(user_data, 5)))

    kichi = lucky_directions(honmei, today_month_star)
    lucky_dir = kichi[0][0]
    lucky_color = STAR_COLOR[honmei]
    lucky_item = STAR_ITEM[getsumei]

    summary = "本命星%s。今日の日盤は%sの巡りです。" % (
        STAR_NAMES[honmei], STAR_NAMES[today_day_star])

    detail = (
        "あなたの本命星は%s、月命星は%sです。本命星は生涯の基本性質を、"
        "月命星は幼少期に培われた内面の傾向を示します。%sの本質は「%s」にあります。"
        "本日の暦は、年盤の中宮が%s、月盤の中宮が%s、日盤の中宮が%sという配置です。"
        "本命星%sの五行%sと日盤中宮%sの五行%sの関係は「%s」であり、"
        "本日は%s。あなたの本命星は今日の盤で%sに回座しています。"
        "月盤から導いた本日の吉方位は%sです。"
        "外出や打ち合わせはこの方角を意識し、%s色の小物を身に着けると、"
        "気学でいう「方位の恩恵」を受け取りやすくなります。"
    ) % (
        STAR_NAMES[honmei], STAR_NAMES[getsumei], STAR_NAMES[honmei], STAR_NATURE[honmei],
        STAR_NAMES[today_year_star], STAR_NAMES[today_month_star], STAR_NAMES[today_day_star],
        STAR_NAMES[honmei], honmei_el, STAR_NAMES[today_day_star],
        STAR_ELEMENT[today_day_star],
        utils.element_relation(honmei_el, STAR_ELEMENT[today_day_star]),
        "積極的に人と会い、動くほど運が開けます" if day_score >= 70
        else "移動や交渉を控え、手元を整えるほうが得策です",
        seat,
        "・".join("%s（%s）" % (d, s) for d, s in kichi),
        lucky_color,
    )

    keywords = [STAR_NAMES[honmei], STAR_NAMES[getsumei] + "（月命）",
                honmei_el + "の気", "吉方位" + lucky_dir]

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
            "honmei": STAR_NAMES[honmei],
            "getsumei": STAR_NAMES[getsumei],
            "today_year_star": STAR_NAMES[today_year_star],
            "today_month_star": STAR_NAMES[today_month_star],
            "today_day_star": STAR_NAMES[today_day_star],
            "seat": seat,
            "lucky_directions": ["%s（%s）" % (d, s) for d, s in kichi],
            "element": honmei_el,
        },
    }
