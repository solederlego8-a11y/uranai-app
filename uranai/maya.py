# -*- coding: utf-8 -*-
"""⑩ マヤ暦占い（ツォルキン）

1900-01-01 をキン1として、260 日周期のキン番号・20 の紋章・13 のトーンを算出する。
本日のキン番号との差分から本日の運勢を導く。
"""
from __future__ import annotations

from datetime import date

from . import utils

MODULE_NAME = "マヤ暦占い"

TZOLKIN_BASE = date(1900, 1, 1)  # この日をキン1とする

# 20 の紋章
GLYPHS = [
    "赤い龍", "白い風", "青い夜", "黄色い種", "赤い蛇",
    "白い世界の橋渡し", "青い手", "黄色い星", "赤い月", "白い犬",
    "青い猿", "黄色い人", "赤い空歩く人", "白い魔法使い", "青い鷲",
    "黄色い戦士", "赤い地球", "白い鏡", "青い嵐", "黄色い太陽",
]
GLYPH_MEANING = [
    "誕生と母性。すべてを受け止め、育てる力",
    "伝達と精神。言葉で人の心を動かす力",
    "豊かさと直感。内なる声が現実を作る力",
    "開花と気づき。可能性の種を蒔く力",
    "生命力と本能。身体感覚で真実を掴む力",
    "架け橋と機会。人と人をつなぐ力",
    "実践と癒やし。手を動かして解決する力",
    "調和と芸術。美しく整える力",
    "浄化と流れ。感情を洗い流す力",
    "誠実と愛情。忠実であることで結ばれる力",
    "遊びと魔術。楽しむことで奇跡を起こす力",
    "自由意志と智慧。自分で選び取る力",
    "空間と探索。飛び出して視野を広げる力",
    "受容と魅了。受け入れることで相手を変える力",
    "ビジョンと大局。高い視点から見通す力",
    "知性と挑戦。問いを立てて突破する力",
    "共時性と信頼。流れに乗る力",
    "秩序と真実。ありのままを映す力",
    "変容と加速。嵐のように状況を変える力",
    "生命と統合。すべてを照らし、まとめる力",
]
GLYPH_COLOR = ["赤", "白", "青", "黄"]  # 紋章の系統色（4色循環）
GLYPH_DIR = ["東", "北", "西", "南"]    # マヤの四方位（赤=東、白=北、青=西、黄=南）

# 13 のトーン（銀河の音）
TONES = [
    "磁気", "月", "電気", "自己存在", "倍音", "律動", "共振",
    "銀河", "太陽", "惑星", "スペクトル", "水晶", "宇宙",
]
TONE_MEANING = [
    "目的を定める音。何を望むのかを決めるところから始まります",
    "挑戦の音。障害を知ることで進む方向が見えます",
    "奉仕の音。動き出すことでエネルギーが生まれます",
    "形の音。枠組みを決めると力が集中します",
    "輝きの音。自分の力を惜しまず出すときです",
    "組織の音。バランスを取り、整えるときです",
    "調律の音。本質に立ち返り、流れに合わせるときです",
    "統合の音。関わる人と足並みを揃えるときです",
    "意図の音。実現に向けて明確に宣言するときです",
    "現れの音。形として結果が出てくるときです",
    "解放の音。手放すことで次のスペースが空きます",
    "協力の音。分かち合うことで大きくなります",
    "存在の音。すべてを超えて在るがままでいるときです",
]
TONE_ITEM = [
    "新しいノート", "二色のペン", "小さなスピーカー", "四角いポーチ",
    "星形のチャーム", "手帳のリフィル", "音楽プレイリスト",
    "みんなで分けられるお菓子", "宣言を書いた付箋", "小さな鉢植え",
    "捨てる予定の物を入れる袋", "誰かと使えるおそろいの小物",
    "何も入れない空のポケット",
]


def kin_number(target: date) -> int:
    """指定日のキン番号（1〜260）を返す。"""
    days = (target - TZOLKIN_BASE).days
    return (days % 260) + 1


def glyph_index(kin: int) -> int:
    """キン番号から紋章のインデックス（0〜19）を返す。"""
    return kin % 20


def tone_number(kin: int) -> int:
    """キン番号からトーン（1〜13）を返す。"""
    return (kin - 1) % 13 + 1


def calculate(user_data: dict) -> dict:
    """マヤ暦占いを実行し、共通スキーマの dict を返す。"""
    today = user_data["today"]
    birth = utils.birth_date(user_data)

    kin = kin_number(birth)
    g_idx = glyph_index(kin)
    tone = tone_number(kin)

    today_kin = kin_number(today)
    today_g = glyph_index(today_kin)
    today_tone = tone_number(today_kin)

    # 本人のキンと今日のキンの差分（% 13）で本日の質を判定する
    diff = (today_kin - kin) % 13
    diff_score = [70, 84, 76, 60, 88, 52, 66, 66, 90, 58, 74, 82, 46][diff]
    # 紋章の系統色（4色）が一致すると共鳴が強まる
    same_family = (g_idx % 4) == (today_g % 4)
    score = utils.clamp_score(utils.expand_score(
        diff_score + (8 if same_family else -4), utils.daily_seed(user_data, 10)))

    lucky_color = GLYPH_COLOR[g_idx % 4]
    lucky_item = TONE_ITEM[tone - 1]
    lucky_dir = GLYPH_DIR[g_idx % 4]

    summary = "KIN%d %s・%sの音%d。今日はKIN%dです。" % (
        kin, GLYPHS[g_idx], TONES[tone - 1], tone, today_kin)

    detail = (
        "マヤの神聖暦ツォルキンでは、260 日で一巡する暦の中のどの位置に生まれたかで本質を読みます。"
        "あなたのキンナンバーはKIN%dで、紋章は「%s」、銀河の音は%d（%s）です。"
        "紋章%sが示すのは「%s」で、これがあなたの生まれ持った才能の方向です。"
        "音%dは「%s」を意味し、物事への取り組み方の癖を表します。"
        "本日はKIN%dで、紋章は%s、音は%d（%s）が巡っています。"
        "あなたのキンとの差は%d（13日周期上の位置）で、%s。"
        "紋章の系統色は%sで、本日の%sと%s。"
        "今日は%sの方角に意識を向け、%sを持ち歩くと、あなた本来のリズムに戻りやすくなります。"
    ) % (
        kin, GLYPHS[g_idx], tone, TONES[tone - 1],
        GLYPHS[g_idx], GLYPH_MEANING[g_idx],
        tone, TONE_MEANING[tone - 1],
        today_kin, GLYPHS[today_g], today_tone, TONES[today_tone - 1],
        diff,
        "自然体でいるほど流れに乗れる位置です" if diff_score >= 74
        else "普段より意識的に整えることが必要な位置です",
        lucky_color, GLYPH_COLOR[today_g % 4],
        "共鳴しています" if same_family else "系統が異なるため、意識して切り替えると楽になります",
        lucky_dir, lucky_item,
    )

    keywords = [
        GLYPHS[g_idx], TONES[tone - 1] + "の音",
        "KIN%d" % kin, GLYPH_MEANING[g_idx].split("。")[0],
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
            "kin": kin,
            "glyph": GLYPHS[g_idx],
            "tone": tone,
            "tone_name": TONES[tone - 1],
            "today_kin": today_kin,
            "today_glyph": GLYPHS[today_g],
        },
    }
