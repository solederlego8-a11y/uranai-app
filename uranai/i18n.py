# -*- coding: utf-8 -*-
"""英語版（グローバル向け）の翻訳テーブルと変換ロジック。

内部の計算（uranai.aggregator / 各占術モジュール）はすべて日本語のまま
決定論的に動作させ、この層で「表示直前」に日本語の語彙（色・方位・
アイテム・ランク・モジュール名など）を英語へ変換する。

方針（v1のスコープ）:
  - 数値（スコア・ラッキーナンバー）、色見本のHEXコードはそのまま使う。
  - ラッキーカラー／アイテム／方位、ランク、モジュール名、カテゴリ名は
    辞書引きで英訳する（未知語は素通しし、日本語のまま表示されても
    アプリが壊れないようにする＝安全側のフォールバック）。
  - 「今日の総合アドバイス」は、日本語版のキーワード差し込み文とは別に、
    英語専用のテンプレート集を新規に用意する（キーワード自体の翻訳網羅は
    v1のスコープ外のため）。
  - 11種の個別鑑定の長文（detail）は日本語のみ。英語版では要約行として
    「モジュール名 (EN) ＋ スコア」と、翻訳済みのラッキー色/アイテム/方位を
    表示し、「詳しい文章は日本語のみ」であることを明記する。
"""
from __future__ import annotations

from . import i18n_detail

# ---------------------------------------------------------------------------
# 語彙辞書
# ---------------------------------------------------------------------------
COLOR_EN = {
    "白": "White", "黒": "Black", "赤": "Red", "青": "Blue", "緑": "Green",
    "黄": "Yellow", "紫": "Purple", "茶": "Brown", "金": "Gold", "銀": "Silver",
    "橙": "Orange", "桃": "Pink", "藍": "Indigo", "灰": "Grey", "紺": "Navy",
    "水色": "Light Blue", "空色": "Sky Blue", "青緑": "Teal", "深緑": "Dark Green",
    "若草色": "Fresh Green", "朱色": "Vermilion", "山吹色": "Amber",
    "黄土色": "Ochre", "臙脂": "Deep Crimson", "生成り": "Ivory",
    "真珠色": "Pearl", "群青": "Ultramarine", "翡翠色": "Jade Green",
    "藤色": "Wisteria", "紅": "Crimson", "灰青": "Slate Blue",
    "琥珀色": "Amber Brown",
}

DIR_EN = {
    "北": "North", "北東": "Northeast", "東": "East", "南東": "Southeast",
    "南": "South", "南西": "Southwest", "西": "West", "北西": "Northwest",
}

ITEM_EN = {
    "お気に入りのお菓子": "your favorite snack",
    "お気に入りの本": "your favorite book",
    "お気に入りの飲み物": "your favorite drink",
    "きちんとした上着": "a smart jacket",
    "みんなで分けられるお菓子": "snacks to share with others",
    "アロマオイル": "aromatic oil",
    "アロマキャンドル": "an aroma candle",
    "イヤホン": "earphones",
    "エコバッグ": "an eco bag",
    "エメラルドグリーンの小物": "an emerald-green accessory",
    "オレンジのタオル": "an orange towel",
    "カラフルな付箋": "colorful sticky notes",
    "クリスタルのアクセサリー": "a crystal accessory",
    "サングラス": "sunglasses",
    "シルバーのアクセサリー": "a silver accessory",
    "スポーツシューズ": "sports shoes",
    "ノイズキャンセリングイヤホン": "noise-cancelling earphones",
    "ハンドクリーム": "hand cream",
    "パールのアクセサリー": "a pearl accessory",
    "ペアのマグカップ": "a pair of matching mugs",
    "ボイスメモの使えるスマホ": "your phone (for a voice memo)",
    "ミネラルウォーター": "mineral water",
    "ラベンダーのアロマ": "lavender aroma",
    "リップまたはミント": "lip balm or mints",
    "リップクリーム": "lip balm",
    "ワイヤレスイヤホン": "wireless earphones",
    "万年筆": "a fountain pen",
    "上質な名刺入れ": "a quality business card holder",
    "二色のペン": "a two-colour pen",
    "人数分のお菓子": "snacks for everyone",
    "何も入れない空のポケット": "an empty pocket",
    "使い込んだ愛用品": "a well-worn favourite item",
    "写真立て": "a photo frame",
    "刺繍入りのハンカチ": "an embroidered handkerchief",
    "印鑑またはスタンプ": "a seal or stamp",
    "名刺入れ": "a business card holder",
    "四角いポーチ": "a square pouch",
    "土の器": "an earthenware vessel",
    "土色の器": "an earth-toned vessel",
    "定規またはスケジュール帳": "a ruler or planner",
    "宣言を書いた付箋": "a sticky note with your intention written on it",
    "家計簿アプリの入ったスマホ": "your phone (with a budgeting app)",
    "小さなスピーカー": "a small speaker",
    "小さなプレゼント": "a small gift",
    "小さなメモ帳": "a small notepad",
    "小さな手鏡": "a small hand mirror",
    "小さな植木鉢": "a small potted plant",
    "小さな石のお守り": "a small stone charm",
    "小さな観葉植物": "a small houseplant",
    "小さな鈴": "a small bell",
    "小さな鉢植え": "a small potted plant",
    "山の写真または石": "a photo of mountains, or a stone",
    "山吹色のバッグチャーム": "an amber-coloured bag charm",
    "布製のトートバッグ": "a cloth tote bag",
    "布製のポーチ": "a cloth pouch",
    "扇子またはハンカチ": "a folding fan or handkerchief",
    "手作りのお弁当": "a homemade lunch box",
    "手帳とペン": "a notebook and pen",
    "手帳のリフィル": "notebook refills",
    "捨てる予定の物を入れる袋": "a bag for things you plan to throw away",
    "文庫本": "a paperback novel",
    "新しいノート": "a new notebook",
    "新しい文房具": "new stationery",
    "旅の写真": "a photo from a trip",
    "旅の切符やICカード": "a travel ticket or transit card",
    "旅の地図やガイドブック": "a travel map or guidebook",
    "星形のチャーム": "a star-shaped charm",
    "木製のブレスレット": "a wooden bracelet",
    "木製のボールペン": "a wooden ballpoint pen",
    "木製の櫛": "a wooden comb",
    "桃色のリップ": "a pink lip colour",
    "桜のモチーフ": "a cherry-blossom motif item",
    "歩きやすい靴": "comfortable walking shoes",
    "水を入れた小瓶": "a small bottle of water",
    "水筒": "a water bottle",
    "深緑のブックカバー": "a dark-green book cover",
    "灰色のポーチ": "a grey pouch",
    "白いシャツ": "a white shirt",
    "白い封筒": "a white envelope",
    "白い扇子": "a white folding fan",
    "白い花": "a white flower",
    "白木の箸": "plain wooden chopsticks",
    "白檀の香": "sandalwood incense",
    "紙の書籍": "a paper book",
    "紫のペン": "a purple pen",
    "紺のハンカチ": "a navy handkerchief",
    "紺色のノート": "a navy notebook",
    "緑色のノート": "a green notebook",
    "腕時計": "a wristwatch",
    "花の一輪挿し": "a single-stem flower vase",
    "藍染めの布": "indigo-dyed cloth",
    "藍色のハンカチ": "an indigo handkerchief",
    "設計図のようなメモ帳": "a notepad for sketching plans",
    "読みかけの本": "the book you're currently reading",
    "誰かと使えるおそろいの小物": "a matching item to share with someone",
    "誰かへの小さな贈り物": "a small gift for someone",
    "貯金箱": "a piggy bank",
    "赤いお守り": "a red charm",
    "赤いペン": "a red pen",
    "赤いミサンガ": "a red friendship bracelet",
    "赤いリップ": "a red lip colour",
    "赤い房のお守り": "a red tasselled charm",
    "赤い手帳": "a red notebook",
    "赤い石のお守り": "a red stone charm",
    "赤い糸のブレスレット": "a red-thread bracelet",
    "金属のペンダント": "a metal pendant",
    "金属製のキーホルダー": "a metal keychain",
    "金色のアクセサリー": "a gold-coloured accessory",
    "金色のクリップ": "a gold-coloured clip",
    "金色のペン": "a gold-coloured pen",
    "銀のリング": "a silver ring",
    "銀色の小物": "a silver-coloured item",
    "鏡": "a mirror",
    "長財布": "a long wallet",
    "陶器のマグカップ": "a ceramic mug",
    "陶器の湯呑み": "a ceramic teacup",
    "青いしおり": "a blue bookmark",
    "革のキーケース": "a leather key case",
    "革のコインケース": "a leather coin case",
    "革のベルト": "a leather belt",
    "音楽プレイヤー": "a music player",
    "音楽プレイリスト": "a music playlist",
    "風を通す薄いスカーフ": "a light, breathable scarf",
    "香りのよいハンドクリーム": "a nicely scented hand cream",
    "香りのよい石鹸": "a nicely scented soap",
    "香り付きのハンカチ": "a scented handkerchief",
    "香水": "perfume",
    "黄色い付箋": "yellow sticky notes",
    "黄色のスカーフ": "a yellow scarf",
    "黄色の紐": "yellow string",
    "黒いキーケース": "a black key case",
    "黒い手帳": "a black notebook",
    "黒い革の小物": "a small black leather item",
}

RANK_EN = {
    "大吉": "Excellent Fortune",
    "中吉": "Good Fortune",
    "小吉": "Modest Fortune",
    "末吉": "Waning Fortune",
    "凶": "Caution",
}

MODULE_NAME_EN = {
    "姓名判断": "Name Analysis (Kumazaki Method)",
    "西洋占星術": "Western Astrology",
    "四柱推命": "Four Pillars of Destiny (BaZi)",
    "紫微斗数": "Zi Wei Dou Shu",
    "九星気学": "Nine Star Ki",
    "算命学": "Sanmei-gaku",
    "数秘術": "Numerology",
    "インド占星術": "Vedic Astrology",
    "宿曜占星術": "Sukuyo Astrology",
    "マヤ暦占い": "Mayan Calendar (Tzolk'in)",
    "チベット占星術": "Tibetan Astrology",
}

CATEGORY_LABEL_EN = {
    "love": "Love", "work": "Work", "money": "Money", "health": "Health",
}

GENDER_EN = {"male": "Male", "female": "Female", "unknown": "Prefer not to say"}

PREFECTURE_EN = {
    "北海道": "Hokkaido", "青森県": "Aomori", "岩手県": "Iwate", "宮城県": "Miyagi",
    "秋田県": "Akita", "山形県": "Yamagata", "福島県": "Fukushima",
    "茨城県": "Ibaraki", "栃木県": "Tochigi", "群馬県": "Gunma",
    "埼玉県": "Saitama", "千葉県": "Chiba", "東京都": "Tokyo",
    "神奈川県": "Kanagawa", "新潟県": "Niigata", "富山県": "Toyama",
    "石川県": "Ishikawa", "福井県": "Fukui", "山梨県": "Yamanashi",
    "長野県": "Nagano", "岐阜県": "Gifu", "静岡県": "Shizuoka",
    "愛知県": "Aichi", "三重県": "Mie", "滋賀県": "Shiga", "京都府": "Kyoto",
    "大阪府": "Osaka", "兵庫県": "Hyogo", "奈良県": "Nara",
    "和歌山県": "Wakayama", "鳥取県": "Tottori", "島根県": "Shimane",
    "岡山県": "Okayama", "広島県": "Hiroshima", "山口県": "Yamaguchi",
    "徳島県": "Tokushima", "香川県": "Kagawa", "愛媛県": "Ehime",
    "高知県": "Kochi", "福岡県": "Fukuoka", "佐賀県": "Saga",
    "長崎県": "Nagasaki", "熊本県": "Kumamoto", "大分県": "Oita",
    "宮崎県": "Miyazaki", "鹿児島県": "Kagoshima", "沖縄県": "Okinawa",
}


def color_en(name: str) -> str:
    """色名を英訳する。未知語はそのまま返す（安全側フォールバック）。"""
    return COLOR_EN.get(name, name)


def dir_en(name: str) -> str:
    """方位名を英訳する。"""
    return DIR_EN.get(name, name)


def item_en(name: str) -> str:
    """アイテム名を英訳する。"""
    return ITEM_EN.get(name, name)


def rank_en(name: str) -> str:
    """運勢ランクを英訳する。"""
    return RANK_EN.get(name, name)


def module_name_en(name: str) -> str:
    """占術モジュール名を英訳する。"""
    return MODULE_NAME_EN.get(name, name)


def prefecture_en(name: str) -> str:
    """都道府県名を英訳する。"""
    return PREFECTURE_EN.get(name, name)


# ---------------------------------------------------------------------------
# 英語版「今日の総合アドバイス」テンプレート
#
# 日本語版はキーワード（各占術のkeywords）を差し込む方式だが、キーワードの
# 語彙は数百種類にのぼり網羅翻訳はv1のスコープ外とする。英語版では、既に
# 翻訳済みの要素（色・アイテム・方位・ランク・スコア）だけを使って、
# 自然に読める文章を組み立てる。ランクごとに10パターン、
# 生年月日＋氏名＋今日の日付から決定論的に選ぶ点は日本語版と同じ。
# ---------------------------------------------------------------------------
EN_MESSAGE_TEMPLATES = {
    "Excellent Fortune": [
        "Today brings a rare alignment across all eleven readings in your favour. "
        "This is a day to step forward rather than hold back — the momentum is genuinely with you.",
        "The flow is working in your favour today. Whatever you commit to now is likely "
        "to come back to you multiplied, so hesitation would be the real cost.",
        "A high-energy day where several of your readings point the same direction at once. "
        "Long-stalled plans have a real chance of moving forward if you reach out today.",
        "You carry an unusual pull on the people around you today. A conversation you start "
        "yourself could turn into an important relationship going forward.",
        "Your capacity for opportunity is wide open today. A small step can carry you twice "
        "as far as usual — it's worth naming a bigger goal out loud.",
        "This is a day suited to decisions. The readings are unusually clear, so use the "
        "clarity to finally settle something you've been putting off.",
        "Recognition tends to arrive today. Work you've quietly built up may be noticed in "
        "an unexpected way — accept it graciously when it comes.",
        "A strong tailwind runs through today. You can push a little further than usual, "
        "but remember to follow through with a proper thank-you afterwards.",
        "New beginnings are favoured today. A new place, a new person, or a new method — "
        "whichever you choose, the odds are with you.",
        "Your words carry unusual persuasive weight today. Prioritise anything involving "
        "negotiation, presenting, or simply telling someone how you feel.",
    ],
    "Good Fortune": [
        "A steady, dependable day. Keeping to your own pace rather than overreaching "
        "will, in the end, take you the furthest.",
        "Solid results are likely today. Unglamorous, careful work pays off later, "
        "so there's no need to force anything flashy.",
        "Things you've kept at for a while are due some reward today. It's better to "
        "go one level deeper on something already underway than to start something new.",
        "A gentle tailwind is present. Small frictions in relationships are likely "
        "to resolve naturally if you follow this flow.",
        "A well-balanced day for planning and doing. Splitting your day into "
        "preparation first, execution second, will get more done than you'd expect.",
        "A good day for asking for advice. If you've been carrying something alone, "
        "today is a good day to finally say it out loud to someone.",
        "A day with real traction. Aiming for a solid eighty percent will serve you "
        "better than chasing perfection.",
        "Connections quietly widen today. An old contact may reach out, or a small "
        "message you send could lead somewhere unexpected.",
        "A calm, composed day. Situations that would normally irritate you are easier "
        "to handle with a breath first — and that composure builds trust.",
        "A good day for tidying up. Clearing your desk, your schedule, or your own "
        "thoughts creates room for what comes next.",
    ],
    "Modest Fortune": [
        "An unremarkable, quiet day. Rather than making a big move, spend it "
        "checking over what you already have — it pays off later.",
        "A day for watching rather than acting. Gathering one more piece of "
        "information before deciding is the safer choice today.",
        "Business as usual. Nothing special is required — simply following your "
        "normal routine carefully is enough.",
        "A day for small wins. Clearing three five-minute tasks changes the shape "
        "of the whole day.",
        "You'll do well listening more than speaking today. Hearing someone out "
        "before making your case tends to work in your favour in the end.",
        "Steady, but easy to drift through. Decide one thing you will get done "
        "today, first thing in the morning.",
        "A day suited to preparation rather than action. Today's groundwork "
        "is what makes tomorrow easier.",
        "Emotions may run a little closer to the surface today. Read a reply back "
        "before sending it — that habit will save you a misstep.",
        "Staying the course is the wisest move today. Both readings agree that "
        "the time isn't quite right yet — patience will be rewarded.",
        "A day to check the basics. Health, belongings, finances — pick one you "
        "don't normally check and give it a look.",
    ],
    "Waning Fortune": [
        "A slight headwind today. This isn't failure — it's a signal to adjust. "
        "Leave some space in your schedule rather than filling every hour.",
        "Not a day for forcing things. Postpone major decisions where you can "
        "and focus on holding steady.",
        "Progress may stall today. Don't fight it — switch to something else "
        "rather than burning energy on what won't move.",
        "Words are easily misread today. Put anything important in writing "
        "rather than relying on a spoken exchange.",
        "Small setbacks may cluster together. Leave early for anything, and "
        "check your belongings the night before.",
        "Be mindful of tone with people close to you today — words tend to land "
        "harder than intended. A little extra courtesy goes a long way.",
        "Money matters need a closer look today. Hold off on impulse purchases "
        "until at least tomorrow.",
        "Energy runs low today. This isn't the day to push through — an early "
        "finish is the better call.",
        "Old unfinished business may resurface today. Facing it, even briefly, "
        "makes it easier to carry going forward.",
        "Judgement may be a little clouded today. It's fine to say \"let me get "
        "back to you tomorrow\" if pressed for an answer.",
    ],
    "Caution": [
        "Most of today's readings are urging caution. Postpone new contracts, "
        "big purchases, or major decisions if you possibly can.",
        "A day to stay defensive. Pushing through today's resistance tends to "
        "cost far more time to undo later.",
        "Momentum is largely stalled today. Choosing to do nothing is, in "
        "itself, the wisest move available.",
        "Emotions may run high today. If you feel the urge to snap back at "
        "someone, holding it in for now is the better choice.",
        "A draining day. Cut what you can from your schedule and prioritise rest.",
        "Misunderstandings are more likely in conversation today. Save important "
        "discussions for another day if you can.",
        "Footing feels unstable today — take extra care with travel, health, "
        "and your belongings.",
        "The door feels closed today, but treat it as a pause before the next "
        "rise rather than a dead end.",
        "Restraint is the theme today. Protecting what you already have matters "
        "more than reaching for anything new.",
        "A quiet day suits you best. Clear your schedule where you can and "
        "spend time alone — it's the fastest route back to balance.",
    ],
}

FILLER_EN = [
    "There's no need to rush to a conclusion — today's small choice is a gift "
    "your future self will be glad to receive.",
    "Small habits matter most on days like this. Your usual cup of coffee, "
    "your usual walk — keep them.",
    "Saying thank you to someone is considered lucky in almost every tradition. "
    "Even a single word counts.",
    "Before bed tonight, try writing down three things that went well today. "
    "It makes the flow of luck easier to see.",
    "A reading like this is meant to nudge you forward, not decide for you. "
    "The final call is always yours.",
]


def build_message_en(rank_en_label: str, message_key: int, color: str,
                     item: str, direction: str, number: int) -> str:
    """英語版の「今日の総合アドバイス」を決定論的に組み立てる。"""
    templates = EN_MESSAGE_TEMPLATES[rank_en_label]
    body = templates[message_key % len(templates)]
    body += (
        " Today's lucky colour is %s, your lucky item is %s, your lucky "
        "direction is %s, and your lucky number is %d. Keep %s somewhere "
        "visible, carry %s with you, and let %s guide the direction you head "
        "in today." % (color, item, direction, number, color, item, direction)
    )
    filler_index = message_key
    while len(body) < 400:
        body += " " + FILLER_EN[filler_index % len(FILLER_EN)]
        filler_index += 1
    return body


def translate_report(report: dict, user_data: dict) -> dict:
    """build_report() の戻り値に、英語表示用のキーを追加して返す。

    元の日本語のキー（lucky_color 等）はそのまま残し、
    lucky_color_en のように "_en" サフィックスを付けたキーを新設する。
    detail_results の各要素にも同様に "_en" キーを追加する。
    """
    en = dict(report)
    en["score_rank_en"] = rank_en(report["score_rank"])
    en["lucky_color_en"] = color_en(report["lucky_color"])
    en["lucky_item_en"] = item_en(report["lucky_item"])
    en["lucky_dir_en"] = dir_en(report["lucky_dir"])

    message_key = (
        user_data["today"].timetuple().tm_yday
        + report["total_score"]
        + user_data["birth_year"]
        + user_data["birth_month"]
        + user_data["birth_day"]
    )
    en["overall_message_en"] = build_message_en(
        en["score_rank_en"], message_key,
        en["lucky_color_en"], en["lucky_item_en"], en["lucky_dir_en"],
        report["lucky_number"],
    )

    en["category_scores_en"] = {
        CATEGORY_LABEL_EN[k]: v for k, v in report["category_scores"].items()
    }

    en["score_breakdown_en"] = {
        module_name_en(k): v for k, v in report["score_breakdown"].items()
    }

    gender = user_data.get("gender", "unknown")
    detail_en = []
    for item_result in report["detail_results"]:
        d = dict(item_result)
        d["name_en"] = module_name_en(item_result["name"])
        d["lucky_color_en"] = color_en(item_result["lucky_color"])
        d["lucky_item_en"] = item_en(item_result["lucky_item"])
        d["lucky_dir_en"] = dir_en(item_result["lucky_dir"])
        d["detail_en"] = i18n_detail.build_detail_en(
            item_result["name"], item_result.get("raw"), item_result["score"], gender,
        )
        detail_en.append(d)
    en["detail_results_en"] = detail_en

    return en
