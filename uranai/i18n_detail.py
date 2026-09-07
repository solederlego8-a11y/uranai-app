# -*- coding: utf-8 -*-
"""英語版：11種の個別鑑定「詳しい文章」（detail）の英語版を生成する層。

方針:
  - 計算そのもの（uranai/*.py の calculate()）には一切手を触れない。
    各モジュールが返す raw（構造化データ）だけを材料にして、日本語の
    detail 文字列とは独立に、英語ネイティブの文章を新規に組み立てる。
  - 語彙（十干・十二支・五行・通変星・二十七宿・二十八宿・ナクシャトラ・
    紋章 など）はすべてこのファイル内の辞書で英訳する。未知語は
    .get(x, x) で素通しし、欠損があってもアプリを壊さない。
  - どうしても構築できない場合は build_detail_en() が None を返し、
    呼び出し側（i18n.py）は「日本語版のみ」の従来メッセージにフォールバックする。
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# 共通語彙
# ---------------------------------------------------------------------------
STEM_EN = {
    "甲": "Jia (Yang Wood)", "乙": "Yi (Yin Wood)",
    "丙": "Bing (Yang Fire)", "丁": "Ding (Yin Fire)",
    "戊": "Wu (Yang Earth)", "己": "Ji (Yin Earth)",
    "庚": "Geng (Yang Metal)", "辛": "Xin (Yin Metal)",
    "壬": "Ren (Yang Water)", "癸": "Gui (Yin Water)",
}

# 十二支 -> 英語の干支動物（そのまま西洋十二支動物名として使う）
BRANCH_EN = {
    "子": "Rat", "丑": "Ox", "寅": "Tiger", "卯": "Rabbit",
    "辰": "Dragon", "巳": "Snake", "午": "Horse", "未": "Goat",
    "申": "Monkey", "酉": "Rooster", "戌": "Dog", "亥": "Pig",
}

# 漢字の動物名（utils.BRANCH_ANIMAL の値）-> 英語
ANIMAL_KANJI_EN = {
    "鼠": "Rat", "牛": "Ox", "虎": "Tiger", "兎": "Rabbit",
    "龍": "Dragon", "蛇": "Snake", "馬": "Horse", "羊": "Goat",
    "猿": "Monkey", "鶏": "Rooster", "犬": "Dog", "猪": "Pig",
}

ELEMENT_EN = {"木": "Wood", "火": "Fire", "土": "Earth", "金": "Metal", "水": "Water"}
WESTERN_ELEMENT_EN = {"火": "Fire", "地": "Earth", "風": "Air", "水": "Water"}

DIR_EN = {
    "北": "North", "北東": "Northeast", "東": "East", "南東": "Southeast",
    "南": "South", "南西": "Southwest", "西": "West", "北西": "Northwest",
    "中央": "the Center",
}


def _dir(d):
    return DIR_EN.get(d, d)


def _el(e):
    return ELEMENT_EN.get(e, e)


def _ordinal_suffix(n):
    """1, 2, 3, 4, 11, 21, 22, 23... に対応する序数の接尾辞を返す。"""
    if 10 <= n % 100 <= 20:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def sexagenary_en(name):
    """「甲子」形式の2文字を英語表記にする（例: "Jia Tiger (Yang Wood)"）。"""
    if not name or len(name) < 2:
        return name
    stem_full = STEM_EN.get(name[0], name[0])  # e.g. "Jia (Yang Wood)"
    stem_short = stem_full.split(" (")[0]
    element_part = stem_full[stem_full.find("(") + 1: stem_full.find(")")] if "(" in stem_full else ""
    branch_animal = BRANCH_EN.get(name[1], name[1])
    return "%s %s (%s)" % (stem_short, branch_animal, element_part)


# ---------------------------------------------------------------------------
# ① 姓名判断
# ---------------------------------------------------------------------------
KAKU_LABEL_EN = {
    "天格": "Heaven Grid", "人格": "Personality Grid", "地格": "Earth Grid",
    "外格": "Outer Grid", "総格": "Total Grid",
}
FORTUNE4_EN = {
    "大吉": "Great Fortune", "吉": "Fortune", "凶": "Misfortune", "大凶": "Great Misfortune",
}


def detail_en_seimei(raw, score, gender):
    kaku = raw.get("kaku", {})
    fortunes = raw.get("fortunes", {})
    element = _el(raw.get("element", ""))

    def g(key):
        return "%d (%s)" % (kaku.get(key, 0), FORTUNE4_EN.get(fortunes.get(key), fortunes.get(key, "")))

    return (
        "In the Kumazaki method of Japanese name analysis, your name's kanji strokes are "
        "split into five grids: Heaven %s, Personality %s, Earth %s, Outer %s and Total %s. "
        "The Personality Grid is the one that shows most clearly in face-to-face situations, "
        "the Earth Grid reflects traits formed in childhood, the Outer Grid is the impression "
        "others form of you, and the Total Grid sums up your life as a whole. "
        "Your name's overall element is %s, which pairs with your lucky colour below. "
        "Today's resonance between your Total Grid and the calendar works out to a score of "
        "%d out of 100 for this tradition — wear a touch of your lucky colour to help the "
        "name's natural strength come through more easily today."
    ) % (g("天格"), g("人格"), g("地格"), g("外格"), g("総格"), element, score)


# ---------------------------------------------------------------------------
# ② 西洋占星術
# ---------------------------------------------------------------------------
ZODIAC_EN = {
    "牡羊座": "Aries", "牡牛座": "Taurus", "双子座": "Gemini", "蟹座": "Cancer",
    "獅子座": "Leo", "乙女座": "Virgo", "天秤座": "Libra", "蠍座": "Scorpio",
    "射手座": "Sagittarius", "山羊座": "Capricorn", "水瓶座": "Aquarius", "魚座": "Pisces",
}
ASPECT_EN = {
    "コンジャンクション（合）": "a Conjunction",
    "セミセクスタイル": "a Semisextile",
    "セクスタイル（60度）": "a Sextile (60°)",
    "スクエア（90度）": "a Square (90°)",
    "トライン（120度）": "a Trine (120°)",
    "クインカンクス": "a Quincunx",
    "オポジション（180度）": "an Opposition (180°)",
}


def detail_en_seiyo(raw, score, gender):
    sun = ZODIAC_EN.get(raw.get("sun_sign"), raw.get("sun_sign"))
    moon = ZODIAC_EN.get(raw.get("moon_sign"), raw.get("moon_sign"))
    asc = ZODIAC_EN.get(raw.get("ascendant"), raw.get("ascendant"))
    transit = ZODIAC_EN.get(raw.get("transit_sun"), raw.get("transit_sun"))
    aspect = ASPECT_EN.get(raw.get("aspect"), raw.get("aspect"))
    element = WESTERN_ELEMENT_EN.get(raw.get("element"), raw.get("element"))
    return (
        "Your natal chart places the Sun in %s, the Moon in %s, and your Ascendant in %s. "
        "The Sun shows the direction you're aiming for in life, the Moon your unguarded "
        "emotional nature, and the Ascendant the impression you make on people who are "
        "meeting you for the first time. Today the transiting Sun is passing through %s, "
        "forming %s with your natal Sun — %s "
        "Your Ascendant's element is %s, which is why today's lucky direction points that way; "
        "a score of %d out of 100 for Western Astrology reflects how favourably this "
        "configuration is working out for you today."
    ) % (
        sun, moon, asc, transit, aspect,
        "this is a configuration that rewards taking the initiative yourself."
        if score >= 65 else
        "this is a configuration better suited to watching how things unfold before acting.",
        element, score,
    )


# ---------------------------------------------------------------------------
# ③ 四柱推命
# ---------------------------------------------------------------------------
TSUUHENSEI_EN = {
    "比肩": "Companion", "劫財": "Rob Wealth", "食神": "Eating God",
    "傷官": "Hurting Officer", "偏財": "Indirect Wealth", "正財": "Direct Wealth",
    "偏官": "Seven Killings", "正官": "Direct Officer", "偏印": "Indirect Resource",
    "印綬": "Direct Resource",
}
PILLAR_LABEL_EN = {"年柱": "Year Pillar", "月柱": "Month Pillar",
                    "日柱": "Day Pillar", "時柱": "Hour Pillar"}


def detail_en_shichu(raw, score, gender):
    pillars = raw.get("pillars", {})
    nisshu = STEM_EN.get(raw.get("nisshu"), raw.get("nisshu"))
    balance = raw.get("balance", {})
    balance_str = ", ".join(
        "%s %d" % (_el(k), v) for k, v in balance.items()
    ) if balance else ""
    strongest = _el(raw.get("strongest_element", ""))
    weakest = _el(raw.get("weakest_element", ""))
    star = TSUUHENSEI_EN.get(raw.get("tsuuhensei"), raw.get("tsuuhensei"))
    branch_score = raw.get("branch_score", 0)
    hour_known = raw.get("hour_known", True)

    return (
        "Your Four Pillars (BaZi) are Year %s, Month %s, Day %s and Hour %s%s. "
        "Your Day Master — the stem of your Day Pillar — is %s, which forms the core of "
        "your chart's personality. Across the Five Elements your chart reads %s, with %s "
        "the strongest and %s running a little low; consciously bringing in more %s helps "
        "balance the whole chart. Today's Day Pillar is %s, and seen from your Day Master "
        "this relationship is classified as your '%s' — %s "
        "The branch compatibility between today and your Day Pillar scores %d out of 100, "
        "meaning %s. Today's reading for Four Pillars of Destiny comes to %d out of 100."
    ) % (
        sexagenary_en(pillars.get("年柱", "")), sexagenary_en(pillars.get("月柱", "")),
        sexagenary_en(pillars.get("日柱", "")), sexagenary_en(pillars.get("時柱", "")),
        "" if hour_known else " (estimated, since your birth time was not given)",
        nisshu, balance_str, strongest, weakest, weakest,
        sexagenary_en(raw.get("today_pillar", "")), star,
        "this is a day that favours action and follow-through." if score >= 65
        else "this is a day better spent consolidating rather than starting anything new.",
        branch_score,
        "interpersonal matters should go smoothly" if branch_score >= 70
        else "it's worth taking a beat before responding to people today",
        score,
    )


# ---------------------------------------------------------------------------
# ④ 紫微斗数
# ---------------------------------------------------------------------------
SHIBI_STAR_EN = {
    "紫微": "Emperor Star (Zi Wei)", "天機": "Wisdom Star (Tian Ji)",
    "太陽": "Sun Star (Tai Yang)", "武曲": "Military Talent Star (Wu Qu)",
    "天同": "Harmony Star (Tian Tong)", "廉貞": "Chastity Star (Lian Zhen)",
    "天府": "Treasury Star (Tian Fu)", "太陰": "Moon Star (Tai Yin)",
    "貪狼": "Greedy Wolf Star (Tan Lang)", "巨門": "Great Gate Star (Ju Men)",
    "天相": "Minister Star (Tian Xiang)", "天梁": "Elder Star (Tian Liang)",
    "七殺": "Seven Killings Star (Qi Sha)", "破軍": "Army Breaker Star (Po Jun)",
}
PALACE_EN = {
    "命宮": "Life Palace", "兄弟宮": "Siblings Palace", "夫妻宮": "Spouse Palace",
    "子女宮": "Children Palace", "財帛宮": "Wealth Palace", "疾厄宮": "Health Palace",
    "遷移宮": "Travel Palace", "奴僕宮": "Friends Palace", "官禄宮": "Career Palace",
    "田宅宮": "Property Palace", "福徳宮": "Fortune Palace", "父母宮": "Parents Palace",
}


def detail_en_shibi(raw, score, gender):
    branch = raw.get("meikyuu_branch", "")
    animal = BRANCH_EN.get(branch, branch)
    main_star = SHIBI_STAR_EN.get(raw.get("main_star"), raw.get("main_star"))
    sub_star = SHIBI_STAR_EN.get(raw.get("sub_star"), raw.get("sub_star"))
    body_star = SHIBI_STAR_EN.get(raw.get("body_star"), raw.get("body_star"))
    element = _el(raw.get("element", ""))
    today_palace = PALACE_EN.get(raw.get("today_palace"), raw.get("today_palace"))
    yin_yang = "Yang" if raw.get("yin_yang") == "陽" else "Yin"
    forward = raw.get("forward", True)
    ly, lm, ld = raw.get("lunar_year"), raw.get("lunar_month"), raw.get("lunar_day")
    lunar_str = ("On the lunar calendar this is %04d-%02d-%02d, and " % (ly, lm, ld)) if ly else ""

    return (
        "%syour Life Palace falls in the %s branch, ruled by the element %s. "
        "The %s occupies your Life Palace, with the %s alongside it, while your Fortune "
        "Palace (governing peace of mind and enjoyment) holds the %s. "
        "Your chart runs on %s energy, and reads as moving %s this year — meaning %s "
        "Today's transiting palace is your %s, %s. "
        "Zi Wei Dou Shu gives today a score of %d out of 100; your lucky colour and "
        "direction below are drawn from your Life Palace's ruling element."
    ) % (
        lunar_str, animal, element, main_star, sub_star, body_star,
        yin_yang, "forward" if forward else "in reverse",
        "acting on your own initiative tends to align you with the flow this year."
        if forward else
        "waiting to be asked before acting tends to bring better results this year.",
        today_palace,
        "which puts today's focus on outward-facing matters that are likely to be "
        "noticed and rewarded" if score >= 65 else
        "which suggests today's energy is better spent quietly getting your own "
        "situation in order",
        score,
    )


# ---------------------------------------------------------------------------
# ⑤ 九星気学
# ---------------------------------------------------------------------------
KYUSEI_STAR_EN = {
    "一白水星": "One White Water Star", "二黒土星": "Two Black Earth Star",
    "三碧木星": "Three Jade Wood Star", "四緑木星": "Four Green Wood Star",
    "五黄土星": "Five Yellow Earth Star", "六白金星": "Six White Metal Star",
    "七赤金星": "Seven Red Metal Star", "八白土星": "Eight White Earth Star",
    "九紫火星": "Nine Purple Fire Star",
}


def detail_en_kyusei(raw, score, gender):
    honmei = KYUSEI_STAR_EN.get(raw.get("honmei"), raw.get("honmei"))
    getsumei = KYUSEI_STAR_EN.get(raw.get("getsumei"), raw.get("getsumei"))
    y = KYUSEI_STAR_EN.get(raw.get("today_year_star"), raw.get("today_year_star"))
    m = KYUSEI_STAR_EN.get(raw.get("today_month_star"), raw.get("today_month_star"))
    d = KYUSEI_STAR_EN.get(raw.get("today_day_star"), raw.get("today_day_star"))
    seat = _dir(raw.get("seat", ""))
    directions = raw.get("lucky_directions_list") or []
    dir_list = ", ".join(
        "%s (%s)" % (_dir(dd), KYUSEI_STAR_EN.get(ss, ss)) for dd, ss in directions
    )
    return (
        "Your Birth Star (Honmei-sei) is the %s, and your Month Star (Getsumei-sei) is the "
        "%s — the Birth Star sets your basic lifelong nature, while the Month Star reflects "
        "tendencies formed in early childhood. Today's chart carries the %s as the year's "
        "central star, the %s for the month, and the %s for the day. Your Birth Star is "
        "currently seated in the %s direction on today's chart. Based on this month's chart, "
        "today's most favourable directions are: %s. Nine Star Ki scores today at %d out of "
        "100 — %s"
    ) % (
        honmei, getsumei, y, m, d, seat, dir_list, score,
        "moving around and meeting people tends to open doors today."
        if score >= 65 else
        "it may be wiser to hold off on travel or negotiation and tidy up what's in front of you.",
    )


# ---------------------------------------------------------------------------
# ⑥ 算命学
# ---------------------------------------------------------------------------
SANMEI_STAR_EN = {
    "貫索星": "Star of Independence", "石門星": "Star of Cooperation",
    "鳳閣星": "Star of Ease", "調舒星": "Star of Sensitivity",
    "禄存星": "Star of Service", "司禄星": "Star of Accumulation",
    "車騎星": "Star of Speed", "牽牛星": "Star of Honour",
    "龍高星": "Star of Exploration", "玉堂星": "Star of Scholarship",
}
TENCHUSATSU_EN = {
    "戌亥天中殺": "Dog-Pig Void", "申酉天中殺": "Monkey-Rooster Void",
    "午未天中殺": "Horse-Goat Void", "辰巳天中殺": "Dragon-Snake Void",
    "寅卯天中殺": "Tiger-Rabbit Void", "子丑天中殺": "Rat-Ox Void",
}
JINTAI_POSITION_EN = {
    "中央（胸）": "Chest (Centre)", "北（頭）": "Head (North)",
    "南（腹）": "Abdomen (South)", "東（右手）": "Right Hand (East)",
    "西（左手）": "Left Hand (West)",
}


def detail_en_sanmei(raw, score, gender):
    day_pillar = raw.get("day_pillar", "")
    tenchusatsu = TENCHUSATSU_EN.get(raw.get("tenchusatsu"), raw.get("tenchusatsu"))
    is_void = raw.get("is_tenchusatsu_today")
    jintai = raw.get("jintai_zu", {})
    jintai_str = ", ".join(
        "%s: %s" % (JINTAI_POSITION_EN.get(pos, pos), SANMEI_STAR_EN.get(star, star))
        for pos, star in jintai.items()
    )
    today_star = SANMEI_STAR_EN.get(raw.get("today_star"), raw.get("today_star"))
    branch_score = raw.get("branch_score", 0)
    return (
        "Your Day Pillar is %s, and your Sanmei-gaku chart maps five stars onto your body: "
        "%s. Your Tenchusatsu (Void) period is the %s — this marks the two branch-years "
        "when the everyday rules of cause and effect loosen, and matters of spirituality, "
        "friendship, family, or your own foundations (depending on which Void you carry) "
        "come under review instead. %s "
        "Today's star, seen from your Day Master, is the %s, and today's branch "
        "compatibility with your Day Pillar scores %d out of 100. Sanmei-gaku puts today's "
        "reading at %d out of 100."
    ) % (
        sexagenary_en(day_pillar), jintai_str, tenchusatsu,
        "Today happens to fall inside your Void period, so it's wise to postpone new "
        "contracts, moving house, or any big decision." if is_void else
        "Today falls outside your Void period, so there's no need to hold back from "
        "acting as usual.",
        today_star, branch_score, score,
    )


# ---------------------------------------------------------------------------
# ⑦ 数秘術
# ---------------------------------------------------------------------------
LIFE_PATH_MEANING_EN = {
    1: "The Pioneer — your role is to blaze a trail others will follow",
    2: "The Mediator — you shine by standing between people and holding them together",
    3: "The Performer — you bring luck by entertaining and creating",
    4: "The Builder — you excel at laying foundations and building solid systems",
    5: "The Adventurer — your abilities bloom in change and freedom",
    6: "The Nurturer — you find deep fulfilment in protecting and raising others",
    7: "The Seeker — quiet, solitary reflection is where your answers come from",
    8: "The Achiever — you turn practical, real-world power into major results",
    9: "The Humanitarian — you feel fulfilled working for the good of everyone",
    11: "The Intuitive Messenger — a finely tuned sensitivity that guides others",
    22: "The Master Builder — a rare ability to turn grand visions into reality",
    33: "The Embodiment of Selfless Love — a role centred on healing others",
}
PERSONAL_DAY_MEANING_EN = {
    1: "a day to start something new — simply beginning has value in itself",
    2: "a day to wait — listening to others will change the flow in your favour",
    3: "a day to enjoy yourself — self-expression, conversation and play bring luck",
    4: "a day to get organised — plain, careful work and tidying pay off later",
    5: "a day to move — it's worth changing your plans just to get outside",
    6: "a day to support others — caring for someone else fulfils you too",
    7: "a day to think — make sure you get some time alone",
    8: "a day to earn — facing numbers and negotiations brings results",
    9: "a day to let go — finishing things and clearing clutter makes room for what's next",
    11: "a day of flashes of insight — trust your intuition over your logic",
    22: "a day for big plans — an excellent day to write out a large-scale plan",
    33: "a day to give — acting without expecting anything back invites good luck",
}


def detail_en_suuhi(raw, score, gender):
    lp = raw.get("life_path_number")
    dn = raw.get("destiny_number")
    pd = raw.get("personal_day_number")
    romaji = raw.get("romaji", "")
    return (
        "Your Life Path Number is %d: %s. Romanising your name using the Hepburn system "
        "gives \"%s\"; converting each letter to a number and reducing it produces a "
        "Destiny Number of %d, which reflects how your innate talents are best put to use "
        "in the world. Today's Personal Day Number — your Life Path plus today's month and "
        "day, reduced — comes to %d: %s. This is today's theme in a single number. Numerology "
        "gives today a score of %d out of 100."
    ) % (
        lp, LIFE_PATH_MEANING_EN.get(lp, ""), romaji, dn, pd,
        PERSONAL_DAY_MEANING_EN.get(pd, ""), score,
    )


# ---------------------------------------------------------------------------
# ⑧ インド占星術
# ---------------------------------------------------------------------------
RASHI_EN = {
    "メーシャ（牡羊）": "Mesha (Aries)", "ヴリシャバ（牡牛）": "Vrishabha (Taurus)",
    "ミトゥナ（双子）": "Mithuna (Gemini)", "カルカ（蟹）": "Karka (Cancer)",
    "シンハ（獅子）": "Simha (Leo)", "カニヤー（乙女）": "Kanya (Virgo)",
    "トゥラー（天秤）": "Tula (Libra)", "ヴリシュチカ（蠍）": "Vrishchika (Scorpio)",
    "ダヌ（射手）": "Dhanu (Sagittarius)", "マカラ（山羊）": "Makara (Capricorn)",
    "クンバ（水瓶）": "Kumbha (Aquarius)", "ミーナ（魚）": "Meena (Pisces)",
}
PLANET_EN = {
    "火星": "Mars", "金星": "Venus", "水星": "Mercury", "月": "the Moon",
    "太陽": "the Sun", "木星": "Jupiter", "土星": "Saturn",
}
NAKSHATRA_EN = {
    "アシュヴィニー": "Ashwini", "バラニー": "Bharani", "クリッティカー": "Krittika",
    "ローヒニー": "Rohini", "ムリガシラー": "Mrigashira", "アールドラー": "Ardra",
    "プナルヴァス": "Punarvasu", "プシュヤ": "Pushya", "アーシュレーシャー": "Ashlesha",
    "マガー": "Magha", "プールヴァ・パールグニー": "Purva Phalguni",
    "ウッタラ・パールグニー": "Uttara Phalguni", "ハスタ": "Hasta", "チトラー": "Chitra",
    "スヴァーティー": "Swati", "ヴィシャーカー": "Vishakha", "アヌラーダー": "Anuradha",
    "ジェーシュター": "Jyeshtha", "ムーラ": "Mula",
    "プールヴァ・アーシャーダー": "Purva Ashadha", "ウッタラ・アーシャーダー": "Uttara Ashadha",
    "シュラヴァナ": "Shravana", "ダニシュター": "Dhanishta", "シャタビシャー": "Shatabhisha",
    "プールヴァ・バードラパダー": "Purva Bhadrapada",
    "ウッタラ・バードラパダー": "Uttara Bhadrapada", "レーヴァティー": "Revati",
}
TARA_EN = {
    "ジャンマ（誕生）": "Janma (Birth)", "サンパット（財）": "Sampat (Wealth)",
    "ヴィパット（災）": "Vipat (Danger)", "クシェーマ（安泰）": "Kshema (Well-being)",
    "プラティヤク（障害）": "Pratyak (Obstacle)", "サーダカ（成就）": "Sadhaka (Accomplishment)",
    "ヴァダ（危険）": "Vadha (Destruction)", "ミトラ（友好）": "Mitra (Friendship)",
    "アティミトラ（親友）": "Ati-Mitra (Best Friend)",
}


def detail_en_india(raw, score, gender):
    rashi = RASHI_EN.get(raw.get("rashi"), raw.get("rashi"))
    lord = PLANET_EN.get(raw.get("rashi_lord"), raw.get("rashi_lord"))
    nak = NAKSHATRA_EN.get(raw.get("nakshatra"), raw.get("nakshatra"))
    nak_num = raw.get("nakshatra_number")
    lagna = RASHI_EN.get(raw.get("lagna"), raw.get("lagna"))
    today_nak = NAKSHATRA_EN.get(raw.get("today_nakshatra"), raw.get("today_nakshatra"))
    tara = TARA_EN.get(raw.get("tara"), raw.get("tara"))
    ayanamsa = raw.get("ayanamsa", 23.85)
    return (
        "Vedic astrology uses the sidereal zodiac, subtracting the ayanamsa (precession "
        "correction, about %.2f°) from the tropical positions used in Western astrology. "
        "Your sidereal Sun sign (Rashi) is %s, ruled by %s. Your birth-month Nakshatra "
        "(lunar mansion) is the %d%s house, %s. Your Lagna (rising sign) works out to %s. "
        "Today the Moon is transiting %s, and counting from your birth Nakshatra this "
        "puts today's Tarabala (lunar strength) at %s — %s "
        "Vedic Astrology gives today a score of %d out of 100."
    ) % (
        ayanamsa, rashi, lord, nak_num, _ordinal_suffix(nak_num),
        nak, lagna, today_nak, tara,
        "a configuration that favours decisive action today." if score >= 65 else
        "a configuration that favours playing it safe and holding off on major decisions today.",
        score,
    )


# ---------------------------------------------------------------------------
# ⑨ 宿曜占星術
# ---------------------------------------------------------------------------
SHUKU_EN = {
    "昴宿": "Pleiades Mansion", "畢宿": "Net Mansion", "觜宿": "Turtle Beak Mansion",
    "参宿": "Three Stars Mansion", "井宿": "Well Mansion", "鬼宿": "Ghost Mansion",
    "柳宿": "Willow Mansion", "星宿": "Star Mansion", "張宿": "Extended Net Mansion",
    "翼宿": "Wings Mansion", "軫宿": "Chariot Mansion", "角宿": "Horn Mansion",
    "亢宿": "Neck Mansion", "氐宿": "Root Mansion", "房宿": "Room Mansion",
    "心宿": "Heart Mansion", "尾宿": "Tail Mansion", "箕宿": "Winnowing Basket Mansion",
    "斗宿": "Dipper Mansion", "女宿": "Girl Mansion", "虚宿": "Emptiness Mansion",
    "危宿": "Rooftop Mansion", "室宿": "Encampment Mansion", "壁宿": "Wall Mansion",
    "奎宿": "Legs Mansion", "婁宿": "Bond Mansion", "胃宿": "Stomach Mansion",
}
SHUKU_RELATION_EN = {
    "命": "Destiny", "栄": "Prosperity", "親": "Affinity", "友": "Friendship",
    "壊": "Collapse", "成": "Success", "危": "Danger", "安": "Peace",
    "業": "Karma", "胎": "Gestation",
}
SHUKU_RELATION_MEANING_EN = {
    "命": "a day to face yourself — going back to basics brings the answer",
    "栄": "your most prosperous day — recognition, income and results tend to gather",
    "親": "a day of growing closeness — relationships deepen and support arrives",
    "友": "a day for teamwork — working with others beats going it alone",
    "壊": "a day of disruption — avoid new commitments or big purchases",
    "成": "a day of completion — well suited to finishing what's already underway",
    "危": "a precarious day — take care with travel, wording and your health",
    "安": "a restful day — rest and tidying up now pays off in your fortune later",
    "業": "a day when unresolved issues surface — facing them now makes things easier later",
    "胎": "a day for planting seeds — no quick results, but ideal for laying groundwork",
}


def detail_en_shukuyo(raw, score, gender):
    natal = SHUKU_EN.get(raw.get("natal_shuku"), raw.get("natal_shuku"))
    today_shuku = SHUKU_EN.get(raw.get("today_shuku"), raw.get("today_shuku"))
    relation = raw.get("relation")
    relation_en = SHUKU_RELATION_EN.get(relation, relation)
    meaning = SHUKU_RELATION_MEANING_EN.get(relation, "")
    distance = raw.get("distance", 0)
    ly, lm, ld = raw.get("lunar_year"), raw.get("lunar_month"), raw.get("lunar_day")
    lunar_str = ("Converted to the lunar calendar, you were born on %04d-%02d-%02d, and " % (ly, lm, ld)) if ly else ""
    return (
        "%syour birth mansion (Honmyou-shuku) is the %s. Sukuyo astrology reads the "
        "quality of a day from the distance between your birth mansion and today's "
        "mansion. Today's mansion is the %s, which sits %d places on from your birth "
        "mansion, putting today's relationship at '%s' — %s. "
        "Sukuyo Astrology scores today at %d out of 100."
    ) % (lunar_str, natal, today_shuku, distance, relation_en, meaning, score)


# ---------------------------------------------------------------------------
# ⑩ マヤ暦占い
# ---------------------------------------------------------------------------
GLYPH_EN = {
    "赤い龍": "Red Dragon", "白い風": "White Wind", "青い夜": "Blue Night",
    "黄色い種": "Yellow Seed", "赤い蛇": "Red Serpent",
    "白い世界の橋渡し": "White Worldbridger", "青い手": "Blue Hand",
    "黄色い星": "Yellow Star", "赤い月": "Red Moon", "白い犬": "White Dog",
    "青い猿": "Blue Monkey", "黄色い人": "Yellow Human",
    "赤い空歩く人": "Red Skywalker", "白い魔法使い": "White Wizard",
    "青い鷲": "Blue Eagle", "黄色い戦士": "Yellow Warrior",
    "赤い地球": "Red Earth", "白い鏡": "White Mirror", "青い嵐": "Blue Storm",
    "黄色い太陽": "Yellow Sun",
}
TONE_EN = {
    "磁気": "Magnetic", "月": "Lunar", "電気": "Electric", "自己存在": "Self-Existing",
    "倍音": "Overtone", "律動": "Rhythmic", "共振": "Resonant", "銀河": "Galactic",
    "太陽": "Solar", "惑星": "Planetary", "スペクトル": "Spectral", "水晶": "Crystal",
    "宇宙": "Cosmic",
}


def detail_en_maya(raw, score, gender):
    kin = raw.get("kin")
    glyph = GLYPH_EN.get(raw.get("glyph"), raw.get("glyph"))
    tone = raw.get("tone")
    tone_name = TONE_EN.get(raw.get("tone_name"), raw.get("tone_name"))
    today_kin = raw.get("today_kin")
    today_glyph = GLYPH_EN.get(raw.get("today_glyph"), raw.get("today_glyph"))
    return (
        "In the Mayan Tzolk'in — a 260-day sacred calendar — your birth is marked by "
        "KIN %d: the %s glyph carrying the %s galactic tone (tone %d). The glyph shows "
        "the direction of your innate gifts, and the tone shows your habitual way of "
        "approaching things. Today is KIN %d, the %s glyph. The Mayan Calendar gives "
        "today a score of %d out of 100 — %s"
    ) % (
        kin, glyph, tone_name, tone, today_kin, today_glyph, score,
        "you're likely to feel especially in sync with your own natural rhythm today."
        if score >= 65 else
        "today calls for a little more conscious effort to stay in your own rhythm.",
    )


# ---------------------------------------------------------------------------
# ⑪ チベット占星術
# ---------------------------------------------------------------------------
TIBET_ANIMAL_EN = {
    "ネズミ": "Rat", "ウシ": "Ox", "トラ": "Tiger", "ウサギ": "Rabbit",
    "龍": "Dragon", "ヘビ": "Snake", "ウマ": "Horse", "ヒツジ": "Goat",
    "サル": "Monkey", "トリ": "Bird", "イヌ": "Dog", "ブタ": "Pig",
}
PARKHA_EN = {
    "リ（離）": "Li (Fire)", "クン（坤）": "Kun (Earth)", "ダ（兌）": "Da (Lake)",
    "ケン（乾）": "Ken (Heaven)", "カン（坎）": "Kan (Water)", "ゴン（艮）": "Gon (Mountain)",
    "シン（震）": "Shin (Thunder)", "ソン（巽）": "Son (Wind)",
}
MEWA_MEANING_EN = {
    1: "White Mewa — purity and a fresh start",
    2: "Black Mewa — strength grows through overcoming obstacles",
    3: "Blue Mewa — blessed with vitality and drive",
    4: "Green Mewa — blessed with harmony and good relationships",
    5: "Yellow Mewa — you stand at the centre with real influence",
    6: "White Mewa — under a protective, authoritative influence",
    7: "Red Mewa — blessed with passion and social connection",
    8: "White Mewa — accumulation and stability come your way",
    9: "Red Mewa — a symbol of honour and advancement",
}


def detail_en_tibet(raw, score, gender):
    animal = TIBET_ANIMAL_EN.get(raw.get("animal"), raw.get("animal"))
    element = _el(raw.get("element", ""))
    mewa = raw.get("mewa")
    parkha = PARKHA_EN.get(raw.get("parkha"), raw.get("parkha"))
    today_animal = ANIMAL_KANJI_EN.get(raw.get("today_animal"), raw.get("today_animal"))
    affinity = raw.get("affinity", 0)
    return (
        "Tibetan astrology reads your fate from four factors together: your animal year, "
        "your element, your Mewa (magic-square number), and your Parkha (trigram). You were "
        "born in the Year of the %s, with the element %s. Your Mewa is %d: %s. Your Parkha "
        "works out to %s. Today is a %s day, and your animal-year compatibility with today "
        "scores %d out of 100 — %s Tibetan Astrology gives today an overall score of "
        "%d out of 100."
    ) % (
        animal, element, mewa, MEWA_MEANING_EN.get(mewa, ""), parkha, today_animal, affinity,
        "relationships are working in your favour today." if affinity >= 70 else
        "it's best to keep a little distance rather than force any contact today.",
        score,
    )


# ---------------------------------------------------------------------------
# ディスパッチ
# ---------------------------------------------------------------------------
_BUILDERS = {
    "姓名判断": detail_en_seimei,
    "西洋占星術": detail_en_seiyo,
    "四柱推命": detail_en_shichu,
    "紫微斗数": detail_en_shibi,
    "九星気学": detail_en_kyusei,
    "算命学": detail_en_sanmei,
    "数秘術": detail_en_suuhi,
    "インド占星術": detail_en_india,
    "宿曜占星術": detail_en_shukuyo,
    "マヤ暦占い": detail_en_maya,
    "チベット占星術": detail_en_tibet,
}


def build_detail_en(name_ja, raw, score, gender="unknown"):
    """モジュール名（日本語）と raw データから英語の詳しい文章を組み立てる。

    未対応のモジュール、または想定外のデータ欠損で組み立てに失敗した場合は
    None を返す。呼び出し側はこれを「日本語版のみ」の案内にフォールバックする。
    """
    builder = _BUILDERS.get(name_ja)
    if builder is None:
        return None
    try:
        text = builder(raw or {}, score, gender)
    except Exception:
        return None
    return text
