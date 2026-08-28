# -*- coding: utf-8 -*-
"""⑪ チベット占星術

十二支・五大元素・九宮数（メワ）・八卦（パルカ）を算出する。
八卦は性別により計算式が異なり、「回答しない」の場合は男性式を用いる。
本日の運勢は今日の干支と本人の干支の相性から導く。
"""
from __future__ import annotations

from . import utils

MODULE_NAME = "チベット占星術"

# チベット暦の十二支（日本と同じ十二支に対応）
TIBET_ANIMALS = [
    "ネズミ", "ウシ", "トラ", "ウサギ", "龍", "ヘビ",
    "ウマ", "ヒツジ", "サル", "トリ", "イヌ", "ブタ",
]

# 五大元素
TIBET_ELEMENTS = ["木", "火", "土", "金", "水"]
ELEMENT_NATURE = {
    "木": "伸びる力。成長と拡大を司り、計画を前へ進めます",
    "火": "燃える力。情熱と変化を司り、人を惹きつけます",
    "土": "支える力。安定と蓄積を司り、基盤を築きます",
    "金": "断つ力。決断と純化を司り、無駄を削ぎ落とします",
    "水": "巡る力。知性と柔軟を司り、状況に適応します",
}
ELEMENT_COLOR = {"木": "緑", "火": "赤", "土": "黄", "金": "白", "水": "藍"}

# 九宮数（メワ）の意味
MEWA_MEANING = {
    1: "白のメワ。清らかさと再出発を象徴します",
    2: "黒のメワ。障害を乗り越えることで力が増します",
    3: "青のメワ。活力と行動力に恵まれます",
    4: "緑のメワ。調和と人縁に恵まれます",
    5: "黄のメワ。中心に立ち、影響力を持ちます",
    6: "白のメワ。権威と保護を受けます",
    7: "赤のメワ。情熱と交流に恵まれます",
    8: "白のメワ。蓄積と安定を得ます",
    9: "赤のメワ。名誉と発展を象徴します",
}

# 八卦（パルカ）
PARKHA = ["リ（離）", "クン（坤）", "ダ（兌）", "ケン（乾）",
          "カン（坎）", "ゴン（艮）", "シン（震）", "ソン（巽）"]
PARKHA_DIR = {
    "リ（離）": "南", "クン（坤）": "南西", "ダ（兌）": "西", "ケン（乾）": "北西",
    "カン（坎）": "北", "ゴン（艮）": "北東", "シン（震）": "東", "ソン（巽）": "南東",
}
PARKHA_ITEM = {
    "リ（離）": "赤い房のお守り", "クン（坤）": "土の器",
    "ダ（兌）": "小さな鈴", "ケン（乾）": "金属のペンダント",
    "カン（坎）": "水を入れた小瓶", "ゴン（艮）": "山の写真または石",
    "シン（震）": "木製のブレスレット", "ソン（巽）": "風を通す薄いスカーフ",
}
PARKHA_MEANING = {
    "リ（離）": "火の卦。明るさと知性で人を導きます",
    "クン（坤）": "地の卦。受け止め、育てる包容力を持ちます",
    "ダ（兌）": "沢の卦。喜びと会話で場を和ませます",
    "ケン（乾）": "天の卦。統率力と強い意志を持ちます",
    "カン（坎）": "水の卦。困難を潜り抜ける胆力があります",
    "ゴン（艮）": "山の卦。動かぬ意志と静けさを持ちます",
    "シン（震）": "雷の卦。瞬発力と決断の速さがあります",
    "ソン（巽）": "風の卦。柔らかく浸透していく影響力を持ちます",
}


def animal_index(year: int) -> int:
    """生年から十二支インデックスを返す（1924年＝子年）。"""
    return (year - 1924) % 12


def element_of(animal_idx: int) -> str:
    """十二支インデックスから五大元素を返す。"""
    return TIBET_ELEMENTS[animal_idx // 2 % 5]


def mewa_number(year: int, month: int, day: int) -> int:
    """九宮数（メワ）を返す。九星気学と同じ計算式を用いる。"""
    y = year
    if month < 2 or (month == 2 and day < 4):
        y -= 1
    star = (11 - ((y - 1) % 9)) % 9
    return 9 if star == 0 else star


def parkha_index(year: int, gender: str) -> int:
    """八卦（パルカ）のインデックスを返す。

    男性:（100 − 生年%100）// 3 % 8
    女性:（生年%100 + 4）// 3 % 8
    「回答しない」の場合は男性の式を用いる。
    """
    if gender == "female":
        return (year % 100 + 4) // 3 % 8
    return (100 - year % 100) // 3 % 8


def calculate(user_data: dict) -> dict:
    """チベット占星術を実行し、共通スキーマの dict を返す。"""
    year = user_data["birth_year"]
    month = user_data["birth_month"]
    day = user_data["birth_day"]
    today = user_data["today"]
    gender = user_data.get("gender", "unknown")

    a_idx = animal_index(year)
    element = element_of(a_idx)
    mewa = mewa_number(year, month, day)
    p_idx = parkha_index(year, gender)
    parkha = PARKHA[p_idx]

    # 今日の干支との相性
    today_index = utils.sexagenary_index_of_date(today)
    today_branch = utils.branch_of(today_index)
    my_branch = utils.BRANCHES[a_idx]
    affinity = utils.branch_affinity_score(my_branch, today_branch)

    # 元素と今日の日干の五行の関係
    today_stem_element = utils.STEM_ELEMENT[utils.stem_of(today_index)]
    element_score = utils.element_relation_score(element, today_stem_element)

    score = utils.clamp_score(utils.expand_score(
        affinity * 0.6 + element_score * 0.4, utils.daily_seed(user_data, 11)))

    lucky_color = ELEMENT_COLOR[element]
    lucky_item = PARKHA_ITEM[parkha]
    lucky_dir = PARKHA_DIR[parkha]

    gender_label = {"male": "男性式", "female": "女性式",
                    "unknown": "男性式（性別未回答のため）"}[gender]

    summary = "%s年・%sの元素・%s。今日は%s年の巡りです。" % (
        TIBET_ANIMALS[a_idx], element, parkha, utils.BRANCH_ANIMAL[today_branch])

    detail = (
        "チベット占星術では、十二支・五大元素・九宮数（メワ）・八卦（パルカ）の"
        "4 つの要素を組み合わせて運命を読みます。"
        "あなたは%s年の生まれで、五大元素は%sです。%s。"
        "九宮数は%dで、%s。"
        "八卦は%sを算出しました（%sで計算）。%s。"
        "本日は%s（%s年）の日で、あなたの%sとの十二支相性は%d点です。%s。"
        "また、あなたの元素%sと本日の天干の五行%sの関係は「%s」であり、%s。"
        "パルカ%sが示す%sの方角へ向かい、%sを身につけると、"
        "チベット暦でいう「ラ（魂の力）」が高まる一日になります。"
    ) % (
        TIBET_ANIMALS[a_idx], element, ELEMENT_NATURE[element],
        mewa, MEWA_MEANING[mewa],
        parkha, gender_label, PARKHA_MEANING[parkha],
        utils.sexagenary_name(today_index), utils.BRANCH_ANIMAL[today_branch],
        TIBET_ANIMALS[a_idx], affinity,
        "人との縁が味方になります" if affinity >= 70 else "無理な接触は避け、距離を保つのが得策です",
        element, today_stem_element,
        utils.element_relation(element, today_stem_element),
        "エネルギーが満ちやすい日です" if element_score >= 70 else "消耗しやすいため休息を意識してください",
        parkha, lucky_dir, lucky_item,
    )

    keywords = [
        TIBET_ANIMALS[a_idx] + "年", element + "の元素",
        "メワ%d" % mewa, parkha.split("（")[0],
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
            "animal": TIBET_ANIMALS[a_idx],
            "element": element,
            "mewa": mewa,
            "parkha": parkha,
            "today_animal": utils.BRANCH_ANIMAL[today_branch],
            "affinity": affinity,
        },
    }
