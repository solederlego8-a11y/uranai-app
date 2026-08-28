# -*- coding: utf-8 -*-
"""⑥ 算命学

日柱の干支を日主とし、天中殺（空亡）を判定する。
人体星図の 5 星を年月日時柱と性別から簡易配置し、
今日が天中殺期間かどうかを本日のスコアに反映する。
"""
from __future__ import annotations

from . import utils

MODULE_NAME = "算命学"

# 十大主星
TEN_STARS = [
    "貫索星", "石門星", "鳳閣星", "調舒星", "禄存星",
    "司禄星", "車騎星", "牽牛星", "龍高星", "玉堂星",
]
STAR_NATURE = {
    "貫索星": "頑固なほどの自立心。自分の決めた道を最後まで貫きます",
    "石門星": "和合の星。人を集め、輪の中心になる社交性を持ちます",
    "鳳閣星": "自然体の表現力。楽しみながら結果を出すのが得意です",
    "調舒星": "繊細な感性。孤独の中で創造性が磨かれるタイプです",
    "禄存星": "奉仕と愛情の星。人に与えることで財が巡ってきます",
    "司禄星": "蓄積の星。こつこつ貯める・守ることに長けています",
    "車騎星": "突進力の星。動きながら考えるスピード型です",
    "牽牛星": "名誉の星。プライドと責任感で信用を積み上げます",
    "龍高星": "冒険と探究の星。未知の分野に踏み込むほど伸びます",
    "玉堂星": "学問の星。知識を体系化し、人に教えることに向きます",
}
STAR_ITEM = {
    "貫索星": "使い込んだ愛用品", "石門星": "人数分のお菓子",
    "鳳閣星": "お気に入りの飲み物", "調舒星": "音楽プレイヤー",
    "禄存星": "小さなプレゼント", "司禄星": "家計簿アプリの入ったスマホ",
    "車騎星": "歩きやすい靴", "牽牛星": "きちんとした上着",
    "龍高星": "旅の写真", "玉堂星": "読みかけの本",
}

# 天中殺（空亡）のテーブル：日柱干支番号を 10 で割った旬 -> 天中殺の十二支
TENCHUSATSU_TABLE = {
    0: ("戌亥天中殺", ["戌", "亥"]),
    1: ("申酉天中殺", ["申", "酉"]),
    2: ("午未天中殺", ["午", "未"]),
    3: ("辰巳天中殺", ["辰", "巳"]),
    4: ("寅卯天中殺", ["寅", "卯"]),
    5: ("子丑天中殺", ["子", "丑"]),
}

TENCHUSATSU_MEANING = {
    "戌亥天中殺": "天とのつながりを試される時期。精神性と学びがテーマになります",
    "申酉天中殺": "友人・仲間との関係が試される時期。人選が運命を分けます",
    "午未天中殺": "目上・親との関係が試される時期。素直さが鍵になります",
    "辰巳天中殺": "自分自身の在り方が試される時期。焦らず土台を固めましょう",
    "寅卯天中殺": "家庭・住まいが試される時期。足元の整備が最優先です",
    "子丑天中殺": "先祖・ルーツが試される時期。過去の整理が運を開きます",
}


def tenchusatsu_of(day_index: int) -> tuple:
    """日柱干支番号から天中殺を判定する。"""
    junk = (day_index % 60) // 10
    return TENCHUSATSU_TABLE[junk]


def star_from(stem_a: str, stem_b: str) -> str:
    """2 つの十干の関係から十大主星を求める。"""
    a_el = utils.STEM_ELEMENT[stem_a]
    b_el = utils.STEM_ELEMENT[stem_b]
    same = utils.STEM_YINYANG[stem_a] == utils.STEM_YINYANG[stem_b]
    if a_el == b_el:
        return "貫索星" if same else "石門星"
    if utils.ELEMENT_GENERATES[a_el] == b_el:
        return "鳳閣星" if same else "調舒星"
    if utils.ELEMENT_CONTROLS[a_el] == b_el:
        return "禄存星" if same else "司禄星"
    if utils.ELEMENT_CONTROLS[b_el] == a_el:
        return "車騎星" if same else "牽牛星"
    return "龍高星" if same else "玉堂星"


def calculate(user_data: dict) -> dict:
    """算命学を実行し、共通スキーマの dict を返す。"""
    year = user_data["birth_year"]
    month = user_data["birth_month"]
    day = user_data["birth_day"]
    hour = user_data.get("birth_hour")
    today = user_data["today"]
    gender = user_data.get("gender", "unknown")

    year_index = utils.four_pillar_year_index(year, month, day)
    month_index = utils.four_pillar_month_index(year, month, day)
    day_index = utils.sexagenary_index_of_date(utils.birth_date(user_data))
    hour_index = utils.four_pillar_hour_index(day_index, hour)

    nisshu = utils.stem_of(day_index)
    nisshu_element = utils.STEM_ELEMENT[nisshu]

    # 人体星図の 5 星（中央・北・南・東・西）を配置する
    center = star_from(nisshu, utils.stem_of(month_index))          # 胸（中央）＝主星
    north = star_from(nisshu, utils.stem_of(year_index))            # 頭（北）
    south = star_from(nisshu, utils.stem_of(hour_index))            # 腹（南）
    east_stem = utils.STEMS[(utils.STEMS.index(nisshu)
                             + utils.BRANCHES.index(utils.branch_of(year_index))) % 10]
    west_stem = utils.STEMS[(utils.STEMS.index(nisshu)
                             + utils.BRANCHES.index(utils.branch_of(month_index))) % 10]
    east = star_from(nisshu, east_stem)                             # 右手（東）
    west = star_from(nisshu, west_stem)                             # 左手（西）
    # 性別により左右（東西）の意味を入れ替えて解釈する
    if gender == "female":
        east, west = west, east
    jintai = {"中央（胸）": center, "北（頭）": north, "南（腹）": south,
              "東（右手）": east, "西（左手）": west}

    name, branches = tenchusatsu_of(day_index)
    today_index = utils.sexagenary_index_of_date(today)
    today_branch = utils.branch_of(today_index)
    is_tenchusatsu = today_branch in branches

    # 今日の日干と日主の関係で通変（主星）を求める
    today_star = star_from(nisshu, utils.stem_of(today_index))
    star_score = {
        "貫索星": 70, "石門星": 78, "鳳閣星": 88, "調舒星": 58, "禄存星": 82,
        "司禄星": 84, "車騎星": 66, "牽牛星": 76, "龍高星": 72, "玉堂星": 86,
    }[today_star]
    base = star_score
    if is_tenchusatsu:
        base -= 28  # 天中殺日は新規の決断を控えるべき日
    branch_score = utils.branch_affinity_score(utils.branch_of(day_index), today_branch)
    score = utils.clamp_score(utils.expand_score(
        base * 0.7 + branch_score * 0.3, utils.daily_seed(user_data, 6)))

    lucky_color = utils.ELEMENT_COLOR[nisshu_element]
    lucky_item = STAR_ITEM[center]
    # 天中殺の方位の反対方位を吉方位とする
    tenchu_dir = utils.BRANCH_DIRECTION[branches[0]]
    lucky_dir = utils.OPPOSITE_DIRECTION[tenchu_dir]

    summary = "%s。今日は%sの巡り%sです。" % (
        name, today_star, "（天中殺日）" if is_tenchusatsu else "")

    detail = (
        "あなたの日柱は%sで、日主は%s（五行は%s）です。"
        "人体星図は中央（胸）に%s、北（頭）に%s、南（腹）に%s、東に%s、西に%sが配置されます。"
        "中心となる主星は%sで、%s。"
        "あなたの天中殺は%sで、%s。"
        "本日は%s日にあたり、日干から見た巡りの星は%sです。%s"
        "地支の相性は%s点で、%s。"
        "天中殺の方位である%sは今日は避け、その反対の%sに向かって動くと運気が整います。"
        "身に着ける色は日主の五行%sに対応する%sを選んでください。"
    ) % (
        utils.sexagenary_name(day_index), nisshu, nisshu_element,
        center, north, south, east, west,
        center, STAR_NATURE[center],
        name, TENCHUSATSU_MEANING[name],
        utils.sexagenary_name(today_index), today_star,
        "本日は天中殺の日にあたるため、新規の契約・引っ越し・大きな決断は先送りが賢明です。"
        if is_tenchusatsu else
        "本日は天中殺を外れており、通常どおり動いて差し支えありません。",
        branch_score,
        "人間関係が追い風になります" if branch_score >= 70 else "人間関係は控えめな距離感が無難です",
        tenchu_dir, lucky_dir, nisshu_element, lucky_color,
    )

    keywords = [center, today_star, name,
                "天中殺日" if is_tenchusatsu else "通常日"]

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
            "nisshu": nisshu,
            "day_pillar": utils.sexagenary_name(day_index),
            "tenchusatsu": name,
            "is_tenchusatsu_today": is_tenchusatsu,
            "jintai_zu": jintai,
            "today_star": today_star,
        },
    }
