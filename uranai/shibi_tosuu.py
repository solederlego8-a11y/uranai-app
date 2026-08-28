# -*- coding: utf-8 -*-
"""④ 紫微斗数

旧暦（lunardate）に変換して旧暦月を取得し、命宮を求めて 14 主星を配置する。
性別により陰陽の解釈を変え、本日の流日宮との関係でスコアを算出する。
"""
from __future__ import annotations

from . import utils

MODULE_NAME = "紫微斗数"

# 十二宮
PALACES = [
    "命宮", "兄弟宮", "夫妻宮", "子女宮", "財帛宮", "疾厄宮",
    "遷移宮", "奴僕宮", "官禄宮", "田宅宮", "福徳宮", "父母宮",
]

# 14 主星（定位置順に並べる）
MAIN_STARS = [
    "紫微", "天機", "太陽", "武曲", "天同", "廉貞", "天府",
    "太陰", "貪狼", "巨門", "天相", "天梁", "七殺", "破軍",
]

STAR_NATURE = {
    "紫微": "帝王の星。頼られる立場に置かれるほど本領を発揮します",
    "天機": "知恵の星。企画・分析・段取りで真価を発揮します",
    "太陽": "陽光の星。人に与え、照らすことで運が回ります",
    "武曲": "財の星。実務と数字の管理で成果が出ます",
    "天同": "福徳の星。争わず和やかにいることが最大の武器です",
    "廉貞": "情熱の星。こだわりを貫くほど個性が輝きます",
    "天府": "蔵の星。蓄え、守り、安定させる力に優れます",
    "太陰": "月の星。細やかな配慮と美意識が評価されます",
    "貪狼": "欲望の星。好奇心の赴くままに動くと縁が広がります",
    "巨門": "弁舌の星。言葉の使い方ひとつで運が大きく動きます",
    "天相": "補佐の星。人を支える立場で最も力を発揮します",
    "天梁": "長老の星。年長者からの信頼と庇護を受けやすい配置です",
    "七殺": "将軍の星。勝負どころで思い切った決断ができます",
    "破軍": "開拓の星。壊して作り直すことで道が開けます",
}

STAR_COLOR = {
    "紫微": "紫", "天機": "青緑", "太陽": "赤", "武曲": "白", "天同": "水色",
    "廉貞": "臙脂", "天府": "黄", "太陰": "銀", "貪狼": "緑", "巨門": "黒",
    "天相": "生成り", "天梁": "茶", "七殺": "金", "破軍": "藍",
}
STAR_ITEM = {
    "紫微": "上質な名刺入れ", "天機": "手帳とペン", "太陽": "腕時計",
    "武曲": "長財布", "天同": "お気に入りのお菓子", "廉貞": "赤いリップ",
    "天府": "貯金箱", "太陰": "パールのアクセサリー", "貪狼": "香水",
    "巨門": "ボイスメモの使えるスマホ", "天相": "白いシャツ",
    "天梁": "紙の書籍", "七殺": "スポーツシューズ", "破軍": "新しい文房具",
}

# 十二宮のインデックス -> 十二支（命宮の十二支に対応）
PALACE_BRANCH = utils.BRANCHES

# 命宮の十二支 -> 五行
PALACE_ELEMENT = utils.BRANCH_ELEMENT


def palace_index(lunar_month: int, hour) -> int:
    """命宮のインデックスを求める。

    命宮 =（14 − 旧暦月 − 時辰インデックス）% 12
    時刻不明の場合は時辰インデックスを 0 として扱う。
    """
    hour_idx = 0 if hour is None else utils.hour_branch_index(int(hour))
    return (14 - lunar_month - hour_idx) % 12


def place_stars(meikyuu: int) -> dict:
    """命宮を基準に 14 主星を十二宮へ配置する。"""
    layout = {}
    for i, palace in enumerate(PALACES):
        # 命宮からの距離に応じて主星を割り当てる（定位置テーブルの回転）
        star = MAIN_STARS[(meikyuu + i) % len(MAIN_STARS)]
        second = MAIN_STARS[(meikyuu + i + 7) % len(MAIN_STARS)]
        layout[palace] = [star, second]
    return layout


def calculate(user_data: dict) -> dict:
    """紫微斗数を実行し、共通スキーマの dict を返す。"""
    hour = user_data.get("birth_hour")
    today = user_data["today"]
    gender = user_data.get("gender", "unknown")

    lunar_year, lunar_month, lunar_day = utils.to_lunar(utils.birth_date(user_data))
    meikyuu = palace_index(lunar_month, hour)
    layout = place_stars(meikyuu)

    main_star = layout["命宮"][0]
    sub_star = layout["命宮"][1]
    body_star = layout["福徳宮"][0]
    palace_branch = PALACE_BRANCH[meikyuu]
    element = PALACE_ELEMENT[palace_branch]

    # 本日の流日宮：今日の旧暦月日から今日の宮を求め、命宮との距離で判定する
    t_lunar_year, t_lunar_month, t_lunar_day = utils.to_lunar(today)
    today_palace = (14 - t_lunar_month - (t_lunar_day % 12)) % 12
    distance = (today_palace - meikyuu) % 12
    distance_score = [86, 62, 70, 44, 78, 55, 48, 55, 78, 44, 70, 62][distance]

    # 性別による陰陽の解釈（陽男陰女は順行、陰男陽女は逆行）
    yin_yang = "陽" if lunar_year % 2 == 0 else "陰"
    if gender == "male":
        forward = (yin_yang == "陽")
        gender_label = "男性（%s年生まれ）" % yin_yang
    elif gender == "female":
        forward = (yin_yang == "陰")
        gender_label = "女性（%s年生まれ）" % yin_yang
    else:
        forward = True
        gender_label = "中庸（%s年生まれ）" % yin_yang
    direction_bonus = 6 if forward else -6

    score = utils.clamp_score(utils.expand_score(
        distance_score + direction_bonus, utils.daily_seed(user_data, 4)))

    lucky_color = utils.ELEMENT_COLOR[element]
    lucky_item = STAR_ITEM[main_star]
    lucky_dir = utils.BRANCH_DIRECTION[palace_branch]

    summary = "命宮は%s宮、主星%s。今日は%s宮の巡りです。" % (
        palace_branch, main_star, PALACES[distance])

    detail = (
        "あなたの生年月日を旧暦に変換すると%d年%d月%d日となり、命宮は%s宮（十二支の%s）に定まります。"
        "命宮に座するのは%sで、%s。"
        "副星として%sが同宮し、福徳宮には%sが入っています。"
        "命宮の五行は%sであり、これが人生の基調となる気質を決めています。"
        "%sの命式は運の巡り方が%sとなるため、%s。"
        "本日は流日が%s宮（命宮から%dつ目）に巡っており、%s。"
        "この巡りでは%sを心がけると運勢が整います。"
        "身に着ける色は%s、方角は%sを意識してください。"
    ) % (
        lunar_year, lunar_month, lunar_day, palace_branch, palace_branch,
        main_star, STAR_NATURE[main_star],
        sub_star, body_star, element,
        gender_label, "順行" if forward else "逆行",
        "自分から先に動くほど流れに乗れます" if forward
        else "求められてから動くほうが結果につながります",
        PALACES[distance], distance,
        "対外的な動きが評価されやすい配置です" if distance_score >= 70
        else "内側を整えることに時間を使うべき配置です",
        "%s宮のテーマ（%s）" % (PALACES[distance], PALACE_THEME[PALACES[distance]]),
        lucky_color, lucky_dir,
    )

    keywords = [main_star, sub_star, PALACES[distance], element + "の命宮"]

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
            "lunar_birth": "%d年%d月%d日" % (lunar_year, lunar_month, lunar_day),
            "meikyuu_branch": palace_branch,
            "main_star": main_star,
            "sub_star": sub_star,
            "body_star": body_star,
            "element": element,
            "today_palace": PALACES[distance],
            "layout": layout,
            "yin_yang": yin_yang,
        },
    }


# 十二宮のテーマ（詳細文で参照する）
PALACE_THEME = {
    "命宮": "自分自身の立て直し",
    "兄弟宮": "仲間や同僚との連携",
    "夫妻宮": "パートナーとの関係",
    "子女宮": "後輩の育成と創作",
    "財帛宮": "収入と支出の管理",
    "疾厄宮": "体調とコンディション",
    "遷移宮": "外出と移動、外部との接触",
    "奴僕宮": "人に頼る力と委任",
    "官禄宮": "仕事の成果と評価",
    "田宅宮": "住まいと居場所の整備",
    "福徳宮": "心の余裕と楽しみ",
    "父母宮": "目上の人からの支援",
}
