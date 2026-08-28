# -*- coding: utf-8 -*-
"""共通ユーティリティモジュール

干支・五行・方位・色・都道府県経緯度・旧暦変換など、
11種の占術モジュールが共通で利用する定数と関数をまとめる。

【重要】このアプリは完全に決定論的である。random モジュールは一切使用しない。
日替わりの変化はすべて「生年月日 + 氏名 + 今日の日付」からの剰余演算で表現する。
"""
from __future__ import annotations

from datetime import date

# ---------------------------------------------------------------------------
# 十干・十二支・六十干支
# ---------------------------------------------------------------------------
STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

STEM_ELEMENT = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
}
STEM_YINYANG = {
    "甲": "陽", "乙": "陰", "丙": "陽", "丁": "陰", "戊": "陽",
    "己": "陰", "庚": "陽", "辛": "陰", "壬": "陽", "癸": "陰",
}
BRANCH_ELEMENT = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
    "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水",
}
BRANCH_DIRECTION = {
    "子": "北", "丑": "北東", "寅": "北東", "卯": "東", "辰": "南東", "巳": "南東",
    "午": "南", "未": "南西", "申": "南西", "酉": "西", "戌": "北西", "亥": "北西",
}
BRANCH_ANIMAL = {
    "子": "鼠", "丑": "牛", "寅": "虎", "卯": "兎", "辰": "龍", "巳": "蛇",
    "午": "馬", "未": "羊", "申": "猿", "酉": "鶏", "戌": "犬", "亥": "猪",
}
BRANCH_HOUR_LABEL = {
    "子": "23-01時", "丑": "01-03時", "寅": "03-05時", "卯": "05-07時",
    "辰": "07-09時", "巳": "09-11時", "午": "11-13時", "未": "13-15時",
    "申": "15-17時", "酉": "17-19時", "戌": "19-21時", "亥": "21-23時",
}

# ---------------------------------------------------------------------------
# 五行
# ---------------------------------------------------------------------------
ELEMENTS = ["木", "火", "土", "金", "水"]
ELEMENT_COLOR = {"木": "緑", "火": "赤", "土": "黄", "金": "白", "水": "黒"}
ELEMENT_GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
ELEMENT_CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
ELEMENT_DIRECTION = {"木": "東", "火": "南", "土": "南西", "金": "西", "水": "北"}
ELEMENT_ITEM = {
    "木": "観葉植物", "火": "アロマキャンドル", "土": "陶器のマグカップ",
    "金": "シルバーアクセサリー", "水": "ガラスのボトル",
}

# ---------------------------------------------------------------------------
# 方位
# ---------------------------------------------------------------------------
DIRECTIONS = ["北", "北東", "東", "南東", "南", "南西", "西", "北西"]
OPPOSITE_DIRECTION = {
    "北": "南", "北東": "南西", "東": "西", "南東": "北西",
    "南": "北", "南西": "北東", "西": "東", "北西": "南東",
}

# ---------------------------------------------------------------------------
# 色名 -> HEX コード
# ---------------------------------------------------------------------------
COLOR_HEX = {
    "白": "#F3F1EC", "黒": "#26282E", "赤": "#C8102E", "青": "#1B4F9C",
    "緑": "#2E8B57", "黄": "#E5B31B", "紫": "#7B4EA8", "茶": "#8B5A2B",
    "金": "#C9A227", "銀": "#A8AEB5", "橙": "#E8762C", "桃": "#E890A8",
    "藍": "#2A4B7C", "灰": "#8A8F98", "紺": "#1F2A5A", "水色": "#6FC3DF",
    "空色": "#7EC8E3", "青緑": "#17796B", "深緑": "#14532D", "若草色": "#9BCB5A",
    "朱色": "#D94E2B", "山吹色": "#E5A20C", "黄土色": "#B58B3C", "臙脂": "#9E1B32",
    "生成り": "#EDE6D6", "真珠色": "#EFEAE0", "群青": "#2B4C9B", "翡翠色": "#2FA98C",
    "藤色": "#A79FD6", "紅": "#C93756", "灰青": "#6E7F92", "琥珀色": "#C68A28",
}


def color_hex(color_name: str) -> str:
    """色名から HEX コードを返す。未知の色名は決定論的に生成する。"""
    if color_name in COLOR_HEX:
        return COLOR_HEX[color_name]
    seed = sum(ord(ch) * (i + 3) for i, ch in enumerate(color_name)) or 7
    r = 90 + (seed * 13) % 140
    g = 80 + (seed * 29) % 140
    b = 80 + (seed * 47) % 140
    return "#%02X%02X%02X" % (r, g, b)


# ---------------------------------------------------------------------------
# 都道府県 -> 代表地点の経緯度
# ---------------------------------------------------------------------------
PREFECTURES = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県",
]

PREFECTURE_GEO = {
    "北海道": (141.35, 43.06), "青森県": (140.74, 40.82), "岩手県": (141.15, 39.70),
    "宮城県": (140.87, 38.27), "秋田県": (140.10, 39.72), "山形県": (140.36, 38.24),
    "福島県": (140.47, 37.75), "茨城県": (140.45, 36.34), "栃木県": (139.88, 36.57),
    "群馬県": (139.06, 36.39), "埼玉県": (139.65, 35.86), "千葉県": (140.12, 35.61),
    "東京都": (139.69, 35.69), "神奈川県": (139.64, 35.45), "新潟県": (139.02, 37.90),
    "富山県": (137.21, 36.70), "石川県": (136.63, 36.59), "福井県": (136.22, 36.07),
    "山梨県": (138.57, 35.66), "長野県": (138.18, 36.65), "岐阜県": (136.72, 35.39),
    "静岡県": (138.38, 34.98), "愛知県": (136.91, 35.18), "三重県": (136.51, 34.73),
    "滋賀県": (135.87, 35.00), "京都府": (135.76, 35.02), "大阪府": (135.52, 34.69),
    "兵庫県": (135.18, 34.69), "奈良県": (135.83, 34.69), "和歌山県": (135.17, 34.23),
    "鳥取県": (134.24, 35.50), "島根県": (133.05, 35.47), "岡山県": (133.93, 34.66),
    "広島県": (132.46, 34.40), "山口県": (131.47, 34.19), "徳島県": (134.56, 34.07),
    "香川県": (134.04, 34.34), "愛媛県": (132.77, 33.84), "高知県": (133.53, 33.56),
    "福岡県": (130.42, 33.61), "佐賀県": (130.30, 33.25), "長崎県": (129.87, 32.74),
    "熊本県": (130.74, 32.79), "大分県": (131.61, 33.24), "宮崎県": (131.42, 31.91),
    "鹿児島県": (130.56, 31.56), "沖縄県": (127.68, 26.21),
}
DEFAULT_GEO = (139.69, 35.69)  # 出生地不明時は東京で代替


def get_geo(prefecture: str) -> tuple:
    """都道府県名から (経度, 緯度) を返す。不明時は東京。"""
    return PREFECTURE_GEO.get(prefecture, DEFAULT_GEO)


# ---------------------------------------------------------------------------
# 干支計算
# ---------------------------------------------------------------------------
SEXAGENARY_BASE_DATE = date(1924, 1, 1)  # 甲子日を基準とする


def sexagenary_index_of_date(target: date) -> int:
    """指定日の日柱干支番号（0=甲子 〜 59=癸亥）を返す。"""
    return (target - SEXAGENARY_BASE_DATE).days % 60


def sexagenary_index_of_year(year: int) -> int:
    """指定年の年柱干支番号（1924年=甲子）を返す。"""
    return (year - 1924) % 60


def sexagenary_name(index: int) -> str:
    """干支番号から「甲子」形式の文字列を返す。"""
    i = index % 60
    return STEMS[i % 10] + BRANCHES[i % 12]


def stem_of(index: int) -> str:
    """干支番号から十干を返す。"""
    return STEMS[index % 60 % 10]


def branch_of(index: int) -> str:
    """干支番号から十二支を返す。"""
    return BRANCHES[index % 60 % 12]


# 節入り日の近似テーブル（暦月 -> その月の節入り日）
SETSUIRI_DAY = {
    1: 6, 2: 4, 3: 6, 4: 5, 5: 6, 6: 6,
    7: 7, 8: 8, 9: 8, 10: 8, 11: 7, 12: 7,
}


def solar_term_month(year: int, month: int, day: int) -> tuple:
    """節入りを考慮した (年, 暦月) を返す。"""
    if day < SETSUIRI_DAY[month]:
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    return year, month


def sexagenary_pair_to_index(stem_index: int, branch_index: int) -> int:
    """十干・十二支の組み合わせから六十干支番号を求める。"""
    for i in range(60):
        if i % 10 == stem_index % 10 and i % 12 == branch_index % 12:
            return i
    return 0


def four_pillar_year_index(year: int, month: int, day: int) -> int:
    """立春を基準にした年柱干支番号を返す。"""
    y = year
    if month < 2 or (month == 2 and day < SETSUIRI_DAY[2]):
        y -= 1
    return sexagenary_index_of_year(y)


def four_pillar_month_index(year: int, month: int, day: int) -> int:
    """五虎遁を用いた月柱干支番号を返す。"""
    _, calc_month = solar_term_month(year, month, day)
    branch_index = calc_month % 12  # 1月=丑, 2月=寅 ... 12月=子
    year_stem_index = four_pillar_year_index(year, month, day) % 10
    # 甲己年は丙寅月から起こる（五虎遁）
    stem_index = ((year_stem_index % 5) * 2 + 2 + (branch_index - 2)) % 10
    return sexagenary_pair_to_index(stem_index, branch_index)


def hour_branch_index(hour: int) -> int:
    """時刻（0〜23）から時支のインデックスを返す（23時台は子）。"""
    return ((hour + 1) // 2) % 12


def four_pillar_hour_index(day_index: int, hour) -> int:
    """日柱干支番号と出生時刻から時柱干支番号を返す。"""
    if hour is None:
        b = day_index % 12  # 時刻不明時は日柱の十二支を代用
    else:
        b = hour_branch_index(int(hour))
    stem_index = ((day_index % 10) % 5 * 2 + b) % 10
    return sexagenary_pair_to_index(stem_index, b)


# ---------------------------------------------------------------------------
# 五行・十二支の相性スコア
# ---------------------------------------------------------------------------
def element_relation(a: str, b: str) -> str:
    """五行 a から見た b の関係名を返す。"""
    if a == b:
        return "比和"
    if ELEMENT_GENERATES.get(a) == b:
        return "相生（与える）"
    if ELEMENT_GENERATES.get(b) == a:
        return "相生（受ける）"
    if ELEMENT_CONTROLS.get(a) == b:
        return "相剋（剋す）"
    if ELEMENT_CONTROLS.get(b) == a:
        return "相剋（剋される）"
    return "無関係"


ELEMENT_RELATION_SCORE = {
    "比和": 72,
    "相生（与える）": 80,
    "相生（受ける）": 88,
    "相剋（剋す）": 46,
    "相剋（剋される）": 34,
    "無関係": 55,
}


def element_relation_score(a: str, b: str) -> int:
    """五行 a と b の相性を 1〜100 の基礎点で返す。"""
    return ELEMENT_RELATION_SCORE[element_relation(a, b)]


BRANCH_SANGOU = [
    {"申", "子", "辰"}, {"亥", "卯", "未"},
    {"寅", "午", "戌"}, {"巳", "酉", "丑"},
]
BRANCH_SHIGOU = [
    {"子", "丑"}, {"寅", "亥"}, {"卯", "戌"}, {"辰", "酉"},
    {"巳", "申"}, {"午", "未"},
]


def branch_affinity_score(a: str, b: str) -> int:
    """十二支同士の相性を 1〜100 の基礎点で返す。"""
    if a == b:
        return 70
    pair = {a, b}
    for s in BRANCH_SHIGOU:
        if s == pair:
            return 90
    for group in BRANCH_SANGOU:
        if a in group and b in group:
            return 86
    if (BRANCHES.index(a) - BRANCHES.index(b)) % 12 == 6:
        return 32  # 冲
    return element_relation_score(BRANCH_ELEMENT[a], BRANCH_ELEMENT[b])


# ---------------------------------------------------------------------------
# 汎用ヘルパ
# ---------------------------------------------------------------------------
def clamp_score(value) -> int:
    """スコアを 1〜100 の整数に丸める。"""
    v = int(round(value))
    return max(1, min(100, v))


# 各占術の基礎点が集まりやすい中心値と、総合スコアの目標中心値
BASE_CENTER = 66.0
TARGET_CENTER = 63.0
# 両端の圧縮を始めるしきい値と圧縮率（1・100 への張り付きを防ぐ）
SOFT_HIGH = 86.0
SOFT_LOW = 22.0
SOFT_RATIO = 0.32


def expand_score(value, seed: int, gain: float = 2.2, swing: int = 11) -> float:
    """スコアのコントラストを広げる。

    各占術の基礎点は 30〜92 の狭い帯に収まり、しかも中心が 66 付近に偏るため、
    そのまま平均すると総合スコアが常に「中吉」へ収束してしまう。
    そこで BASE_CENTER からの偏差を gain 倍に拡大したうえで TARGET_CENTER へ
    平行移動し、さらに seed から決定論的に求めた振れ幅（±swing）を加えることで、
    大吉から凶までの帯域が実際に出現するようにする。
    拡大した結果が両端に張り付かないよう、SOFT_HIGH 以上・SOFT_LOW 以下は
    SOFT_RATIO で圧縮する。random は一切使用しない。
    """
    deviation = value - BASE_CENTER
    wobble = (seed % (2 * swing + 1)) - swing
    result = TARGET_CENTER + deviation * gain + wobble
    if result > SOFT_HIGH:
        result = SOFT_HIGH + (result - SOFT_HIGH) * SOFT_RATIO
    elif result < SOFT_LOW:
        result = SOFT_LOW - (SOFT_LOW - result) * SOFT_RATIO
    return result


def name_seed(user_data: dict) -> int:
    """氏名から決定論的な整数シードを作る。"""
    full = (user_data.get("last_name") or "") + (user_data.get("first_name") or "")
    return sum(ord(ch) * (i + 1) for i, ch in enumerate(full))


def daily_seed(user_data: dict, salt: int = 0) -> int:
    """「本人の出生データ + 今日の日付 + 塩」から決定論的シードを作る。"""
    today = user_data["today"]
    hour = user_data.get("birth_hour")
    hour = 12 if hour is None else int(hour)
    return (
        today.toordinal() * 7
        + user_data["birth_year"] * 13
        + user_data["birth_month"] * 29
        + user_data["birth_day"] * 17
        + hour * 3
        + name_seed(user_data)
        + salt * 101
    )


def pick(seq, index: int):
    """シーケンスから決定論的に 1 要素を選ぶ。"""
    if not seq:
        return None
    return seq[index % len(seq)]


def digit_sum(n: int) -> int:
    """整数の各桁の和を返す。"""
    return sum(int(c) for c in str(abs(n)))


def reduce_number(n: int, keep_master: bool = True) -> int:
    """数秘術の還元。マスターナンバー（11/22/33）は保持する。"""
    while n > 9:
        if keep_master and n in (11, 22, 33):
            return n
        n = digit_sum(n)
    return n


def to_lunar(target: date):
    """新暦 date を旧暦 (年, 月, 日) に変換する。失敗時は近似で代替。"""
    try:
        from lunardate import LunarDate

        ld = LunarDate.fromSolarDate(target.year, target.month, target.day)
        return (ld.year, ld.month, ld.day)
    except Exception:
        # lunardate の対応範囲外などの場合は約 354 日周期の近似で代替する
        base = date(target.year, 1, 1).toordinal()
        offset = (target.toordinal() - base + 21) % 354
        lmonth = min(offset // 30 + 1, 12)
        lday = offset % 30 + 1
        return (target.year, lmonth, lday)


def safe_hour(user_data: dict) -> int:
    """出生時刻を返す。不明時は正午（12時）で補完する。"""
    h = user_data.get("birth_hour")
    return 12 if h is None else int(h)


def birth_date(user_data: dict) -> date:
    """生年月日を date 型で返す。"""
    return date(user_data["birth_year"], user_data["birth_month"], user_data["birth_day"])


def default_result(name: str) -> dict:
    """占術モジュールが例外を投げた場合のフォールバック結果。"""
    return {
        "name": name,
        "summary": "本日は暦の巡りが読み取りにくい日です。基本に立ち返りましょう。",
        "detail": (
            "この占術では本日、明確な吉凶の傾き（強い偏り）が観測できませんでした。"
            "こうした日は、突飛な決断を避け、いつもの手順を丁寧になぞることが最良の戦略になります。"
            "朝のうちに今日やることを三つだけ書き出し、その三つを終えることに集中してください。"
            "判断に迷う場面が来たら、損得ではなく「後から説明できるかどうか」を基準に選ぶと後悔がありません。"
            "人との連絡はいつもより一言だけ丁寧に添えると、思わぬ好意が返ってきます。"
        ),
        "lucky_color": "白",
        "lucky_item": "白いハンカチ",
        "lucky_dir": "東",
        "score": 50,
        "keywords": ["平常心", "基本", "丁寧さ"],
        "raw": {},
    }
