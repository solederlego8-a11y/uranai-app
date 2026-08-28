# -*- coding: utf-8 -*-
"""③ 四柱推命

年柱・月柱・日柱・時柱の四柱を立て、五行バランスを評価する。
本日の運勢は「今日の日柱」と「本人の日主（日柱の天干）」の関係から算出する。
"""
from __future__ import annotations

from . import utils

MODULE_NAME = "四柱推命"

# 日主の十干ごとの性質
NISSHU_NATURE = {
    "甲": "大樹のようにまっすぐ伸びる、正直で曲がったことを嫌う気質",
    "乙": "草花のようにしなやかで、環境に合わせて生き抜く適応力",
    "丙": "太陽のように周囲を照らす、明るく開放的な発信力",
    "丁": "灯火のように静かに照らす、繊細で情の深い洞察力",
    "戊": "山のようにどっしり構える、動じない安定感と包容力",
    "己": "田畑のように受け入れて育てる、面倒見のよい育成力",
    "庚": "鉄のように硬く鋭い、決断力と実行力に富む気質",
    "辛": "宝石のように磨かれた、美意識と繊細な感性",
    "壬": "大河のように流れ続ける、自由で発想の広がる気質",
    "癸": "雨露のようにしみ通る、慎重で分析力に優れた気質",
}

# 通変星（日主から見た今日の日干の関係）
def tsuuhensei(nisshu: str, target_stem: str) -> str:
    """日主から見た対象天干の通変星名を返す。"""
    a_el = utils.STEM_ELEMENT[nisshu]
    b_el = utils.STEM_ELEMENT[target_stem]
    same_polarity = utils.STEM_YINYANG[nisshu] == utils.STEM_YINYANG[target_stem]
    if a_el == b_el:
        return "比肩" if same_polarity else "劫財"
    if utils.ELEMENT_GENERATES[a_el] == b_el:
        return "食神" if same_polarity else "傷官"
    if utils.ELEMENT_CONTROLS[a_el] == b_el:
        return "偏財" if same_polarity else "正財"
    if utils.ELEMENT_CONTROLS[b_el] == a_el:
        return "偏官" if same_polarity else "正官"
    return "偏印" if same_polarity else "印綬"


TSUUHENSEI_SCORE = {
    "比肩": 68, "劫財": 58, "食神": 88, "傷官": 52, "偏財": 82,
    "正財": 86, "偏官": 44, "正官": 78, "偏印": 56, "印綬": 84,
}
TSUUHENSEI_ADVICE = {
    "比肩": "自分のペースを守ること。他人に合わせすぎると消耗します",
    "劫財": "出費と人からの誘いに注意。財布の紐は締めておくべき日",
    "食神": "食べる・話す・楽しむが吉。人に何かを与えると倍で返ります",
    "傷官": "言葉が鋭くなりがち。批評より提案の形にすると通ります",
    "偏財": "動いたぶんだけ収穫がある日。人脈と情報が財に変わります",
    "正財": "堅実な取引・積み立て・見積りが吉。地道な作業が実ります",
    "偏官": "プレッシャーが強まる日。無理に戦わず時間を味方につけて",
    "正官": "評価される日。責任ある立場を引き受けると信用が積み上がります",
    "偏印": "気が散りやすい日。ひとつに絞ると成果が出ます",
    "印綬": "学びと相談が吉。年上の人からの助言が問題を解決します",
}

# 五行バランスの偏りに対するコメント
BALANCE_COMMENT = {
    "木": "発展と成長の気",
    "火": "情熱と表現の気",
    "土": "安定と信頼の気",
    "金": "決断と規律の気",
    "水": "知性と柔軟の気",
}

# 月柱の天干 -> ラッキーアイテム
ITEM_BY_MONTH_STEM = {
    "甲": "木製のボールペン", "乙": "小さな観葉植物", "丙": "サングラス",
    "丁": "アロマキャンドル", "戊": "陶器のマグカップ", "己": "布製のポーチ",
    "庚": "金属製のキーホルダー", "辛": "シルバーのアクセサリー",
    "壬": "水筒", "癸": "ミネラルウォーター",
}


def calculate(user_data: dict) -> dict:
    """四柱推命を実行し、共通スキーマの dict を返す。"""
    year = user_data["birth_year"]
    month = user_data["birth_month"]
    day = user_data["birth_day"]
    hour = user_data.get("birth_hour")
    today = user_data["today"]
    gender = user_data.get("gender", "unknown")

    # 四柱を立てる
    year_index = utils.four_pillar_year_index(year, month, day)
    month_index = utils.four_pillar_month_index(year, month, day)
    day_index = utils.sexagenary_index_of_date(utils.birth_date(user_data))
    hour_index = utils.four_pillar_hour_index(day_index, hour)

    pillars = {
        "年柱": utils.sexagenary_name(year_index),
        "月柱": utils.sexagenary_name(month_index),
        "日柱": utils.sexagenary_name(day_index),
        "時柱": utils.sexagenary_name(hour_index),
    }
    nisshu = utils.stem_of(day_index)  # 日主
    month_stem = utils.stem_of(month_index)
    year_branch = utils.branch_of(year_index)

    # 五行バランス（四柱の天干・地支の五行出現数）
    balance = {e: 0 for e in utils.ELEMENTS}
    for idx in (year_index, month_index, day_index, hour_index):
        balance[utils.STEM_ELEMENT[utils.stem_of(idx)]] += 1
        balance[utils.BRANCH_ELEMENT[utils.branch_of(idx)]] += 1
    strongest = max(utils.ELEMENTS, key=lambda e: (balance[e], -utils.ELEMENTS.index(e)))
    weakest = min(utils.ELEMENTS, key=lambda e: (balance[e], utils.ELEMENTS.index(e)))

    # 今日の日柱との関係でスコアを算出
    today_index = utils.sexagenary_index_of_date(today)
    today_stem = utils.stem_of(today_index)
    today_branch = utils.branch_of(today_index)
    star = tsuuhensei(nisshu, today_stem)
    branch_score = utils.branch_affinity_score(utils.branch_of(day_index), today_branch)
    score = utils.clamp_score(utils.expand_score(
        TSUUHENSEI_SCORE[star] * 0.65 + branch_score * 0.35,
        utils.daily_seed(user_data, 3)))

    nisshu_element = utils.STEM_ELEMENT[nisshu]
    lucky_color = utils.ELEMENT_COLOR[nisshu_element]
    lucky_item = ITEM_BY_MONTH_STEM[month_stem]
    lucky_dir = utils.BRANCH_DIRECTION[year_branch]

    gender_note = {
        "male": "陽の立場から積極的に動くほど命式が整いやすい傾向",
        "female": "陰の立場で受けて返す形にすると命式が整いやすい傾向",
        "unknown": "陰陽どちらの動き方でも整えられる中庸の立ち位置",
    }[gender]

    summary = "日主%s。今日の日柱%sは「%s」の巡りです。" % (
        nisshu, utils.sexagenary_name(today_index), star)

    detail = (
        "あなたの命式は年柱%s・月柱%s・日柱%s・時柱%sです。"
        "中心となる日主は%sで、%sを本質として持っています。"
        "五行のバランスは木%d・火%d・土%d・金%d・水%dとなり、%s（%s）が最も強く、"
        "%sがやや不足しています。%sを補う行動を意識すると命式全体が安定します。"
        "本日の日柱は%sで、日主%sから見ると「%s」にあたります。%s。"
        "地支の関係は%s点の相性で、%s。"
        "性別による立ち位置としては、%sが出ています。"
        "%s色を身に着け、%sの方角を意識すると、今日の巡りをうまく味方につけられます。"
    ) % (
        pillars["年柱"], pillars["月柱"], pillars["日柱"], pillars["時柱"],
        nisshu, NISSHU_NATURE[nisshu],
        balance["木"], balance["火"], balance["土"], balance["金"], balance["水"],
        strongest, BALANCE_COMMENT[strongest], weakest, weakest,
        utils.sexagenary_name(today_index), nisshu, star, TSUUHENSEI_ADVICE[star],
        branch_score,
        "対人面はスムーズに進みます" if branch_score >= 70 else "対人面は一呼吸置いて対応するのが無難です",
        gender_note, lucky_color, lucky_dir,
    )

    keywords = [star, nisshu_element + "の日主", strongest + "旺", "日柱" + pillars["日柱"]]

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
            "pillars": pillars,
            "nisshu": nisshu,
            "nisshu_element": nisshu_element,
            "balance": balance,
            "today_pillar": utils.sexagenary_name(today_index),
            "tsuuhensei": star,
            "hour_known": hour is not None,
        },
    }
