# -*- coding: utf-8 -*-
"""★ 統合エンジン：11種の占術結果から「今日の総合鑑定」を生成する

各占術モジュールの calculate() の戻り値（共通スキーマ）を受け取り、
重み付き平均のスコア・ランク・多数決によるラッキー要素・
決定論的テンプレート選択による総合メッセージを生成する。

【重要】random は一切使用しない。同一入力＋同一日付なら必ず同一結果になる。
"""
from __future__ import annotations

from . import utils

# ---------------------------------------------------------------------------
# STEP1：重み付き平均のための重み
# ---------------------------------------------------------------------------
MODULE_WEIGHTS = {
    "姓名判断": 1.0,
    "西洋占星術": 1.0,
    "四柱推命": 1.5,
    "紫微斗数": 1.0,
    "九星気学": 1.0,
    "算命学": 1.0,
    "数秘術": 1.0,
    "インド占星術": 0.5,
    "宿曜占星術": 1.0,
    "マヤ暦占い": 0.5,
    "チベット占星術": 0.5,
}
DEFAULT_WEIGHT = 1.0

# ---------------------------------------------------------------------------
# STEP3：多数決が同数だった場合の優先モジュール
# ---------------------------------------------------------------------------
PRIORITY = {
    "lucky_color": ["四柱推命", "九星気学", "西洋占星術"],
    "lucky_item": ["四柱推命", "宿曜占星術", "姓名判断"],
    "lucky_dir": ["九星気学", "四柱推命", "算命学"],
}

# ---------------------------------------------------------------------------
# STEP6：カテゴリ別運勢の構成モジュール
# ---------------------------------------------------------------------------
CATEGORY_MODULES = {
    "love": ["西洋占星術", "四柱推命", "宿曜占星術", "数秘術"],
    "work": ["四柱推命", "算命学", "西洋占星術", "数秘術"],
    "money": ["四柱推命", "九星気学", "算命学", "チベット占星術"],
    "health": ["チベット占星術", "四柱推命", "算命学"],
}
CATEGORY_LABEL = {"love": "恋愛運", "work": "仕事運", "money": "金運", "health": "健康運"}


# ---------------------------------------------------------------------------
# STEP2：運勢ランク
# ---------------------------------------------------------------------------
def score_rank(total_score: int) -> str:
    """総合スコアから運勢ランクを返す。"""
    if total_score >= 81:
        return "大吉"
    if total_score >= 61:
        return "中吉"
    if total_score >= 41:
        return "小吉"
    if total_score >= 21:
        return "末吉"
    return "凶"


# ---------------------------------------------------------------------------
# STEP7：ランク帯ごとのメッセージテンプレート（各10パターン）
# ---------------------------------------------------------------------------
MESSAGE_TEMPLATES = {
    "大吉": [
        "本日のあなたは、11の占術がそろって上向きを示す稀な一日を迎えています。とりわけ「{kw1}」の気配が強く、"
        "普段なら二の足を踏む場面でも、迷わず前に出たほうが結果につながります。",
        "今日は流れがあなたに味方する日です。「{kw1}」と「{kw2}」がひとつに重なり、"
        "動いた分だけ確実に返ってくる構造ができています。遠慮は最大の損になります。",
        "複数の暦が同時に吉を示す、密度の高い一日です。「{kw1}」を軸に据えて動けば、"
        "長らく止まっていた案件がひとつ前へ進みます。連絡は今日のうちに入れてください。",
        "今日のあなたには、周囲を巻き込む力が宿っています。「{kw1}」の勢いに乗って、"
        "自分から声をかけた相手が、そのまま今後のキーパーソンになる可能性があります。",
        "運の器が大きく開いている日です。「{kw1}」「{kw2}」という二つの流れが後押しし、"
        "普段の一歩が二歩分の距離になります。大きめの目標をあえて口に出してみてください。",
        "本日は「決める」ことに最適な日です。「{kw1}」の巡りが判断を明快にしてくれるため、"
        "保留にしてきた選択肢を、今日のうちにひとつ手放すか進めるか決めましょう。",
        "今日は人からの評価が返ってくる日です。「{kw1}」が示すとおり、"
        "これまで見えないところで積み上げてきたものが、思わぬ形で認められます。素直に受け取ってください。",
        "強い追い風の一日です。「{kw1}」と「{kw2}」が同じ方向を向いているため、"
        "多少の無理は通ります。ただし、通った後の丁寧なお礼だけは忘れないでください。",
        "本日は「始まり」に恵まれた日です。「{kw1}」の気が新しい縁を運んできます。"
        "初めての場所、初めての人、初めての方法——そのどれを選んでも当たりが出ます。",
        "今日のあなたは、自分でも驚くほど言葉が通ります。「{kw1}」の巡りが説得力を与えるため、"
        "交渉・面談・プレゼンなど、伝えることが目的の予定を優先してください。",
    ],
    "中吉": [
        "本日は安定した良い流れの中にあります。「{kw1}」が今日のテーマで、"
        "背伸びをせず自分のペースを守ることが、結果的にいちばん遠くまで進む道になります。",
        "堅実に成果が出る一日です。「{kw1}」と「{kw2}」が支えとなり、"
        "地味な作業ほど後で効いてきます。派手さを求めず、目の前の一件を丁寧に終わらせましょう。",
        "今日は「続けてきたこと」が報われる日です。「{kw1}」の巡りが後押しするので、"
        "新しく手を広げるより、すでに始めているものを一段深めるほうが得策です。",
        "穏やかながら確かな追い風があります。「{kw1}」に沿って行動すれば、"
        "人間関係のちょっとした摩擦も、今日のうちに自然と解けていきます。",
        "本日は準備と実行のバランスが良い日です。「{kw1}」「{kw2}」の気配を感じ取り、"
        "午前に段取り、午後に実行と分けると、想像以上に多くのことが片づきます。",
        "今日は相談ごとに向いた日です。「{kw1}」の流れが人の言葉を届きやすくするので、"
        "ひとりで抱えている案件を、思い切って誰かに話してみてください。",
        "手応えのある一日になります。「{kw1}」が示すとおり、"
        "完璧を目指すより「八割で出す」ことを意識したほうが、評価も速度も上がります。",
        "本日は縁が静かに広がる日です。「{kw1}」の気を受けて、"
        "以前会ったきりの人から連絡が来たり、こちらから送った一言が思わぬ展開を呼びます。",
        "落ち着いて力を発揮できる日です。「{kw1}」と「{kw2}」が心の余裕を作ってくれるため、"
        "普段なら苛立つ場面でも、一呼吸置いて対応できます。その差が信用になります。",
        "今日は「整える」ことで運が伸びる日です。「{kw1}」の巡りに従い、"
        "机の上、予定表、頭の中——どれかひとつを片づけると、その分だけ次が入ってきます。",
    ],
    "小吉": [
        "本日は可もなく不可もない、静かな一日です。「{kw1}」がテーマとなり、"
        "大きく動くより、今あるものを確認し直すことに時間を使うと、後で効いてきます。",
        "今日は様子見が正解の日です。「{kw1}」と「{kw2}」がやや拮抗しているため、"
        "判断を急がず、情報をもう一つ集めてから決めるほうが確実です。",
        "平常運転の一日です。「{kw1}」の流れは穏やかで、"
        "特別なことをしなくても損はしません。いつもの手順を丁寧になぞってください。",
        "本日は小さな達成を積む日です。「{kw1}」の気配に合わせて、"
        "五分で終わる用事を三つ片づけるだけで、一日の印象が変わります。",
        "今日は人の話を聞く側に回ると得をします。「{kw1}」が示すとおり、"
        "自分の主張を通すより、相手の言い分を先に受け取ったほうが最終的に有利になります。",
        "穏やかですが、油断すると流されやすい日です。「{kw1}」「{kw2}」を意識して、"
        "「今日これだけはやる」という一点を朝のうちに決めておいてください。",
        "本日は準備に向いた日です。「{kw1}」の巡りは実行より仕込みを支持しています。"
        "明日以降に効く段取りを、今日のうちに済ませておきましょう。",
        "今日は感情の起伏がやや出やすい日です。「{kw1}」の流れを踏まえ、"
        "返信を書いたらすぐ送らず、一度読み返す習慣をつけると失点を防げます。",
        "現状維持が最も賢い選択になる日です。「{kw1}」と「{kw2}」が"
        "「まだその時ではない」と告げています。焦らず、機が熟すのを待ちましょう。",
        "本日は足元を見直す日です。「{kw1}」の気に従い、"
        "体調・持ち物・お金の残高——普段確認しないものをひとつ点検しておくと安心です。",
    ],
    "末吉": [
        "本日はやや向かい風のある日です。「{kw1}」が課題として浮かび上がりますが、"
        "これは失敗ではなく調整の合図です。予定を詰め込まず、余白を作ってください。",
        "今日は無理が利かない日です。「{kw1}」と「{kw2}」が消耗を示しているため、"
        "重要な決断は明日以降に回し、今日は守りに徹するのが正解です。",
        "流れが停滞しやすい一日です。「{kw1}」の巡りに逆らわず、"
        "進まないものは進まないと割り切って、別の作業に切り替えたほうが消耗しません。",
        "本日は言葉が誤解されやすい日です。「{kw1}」が示すとおり、"
        "口頭で済ませようとせず、要点を文字に残しておくと後のトラブルを防げます。",
        "小さなつまずきが重なりやすい日です。「{kw1}」「{kw2}」の気配を踏まえ、"
        "移動は十分早めに、持ち物は前夜のうちに確認しておいてください。",
        "今日は人との距離感に注意が必要です。「{kw1}」の流れの中では、"
        "親しい相手ほど言葉が刺さりやすくなります。一歩引いた丁寧さを心がけましょう。",
        "本日はお金の出入りに注意が向く日です。「{kw1}」の巡りに従い、"
        "衝動的な購入や、その場のノリでの出費は、いったん翌日まで保留にしてください。",
        "気力が上がりにくい一日です。「{kw1}」と「{kw2}」が休息を求めています。"
        "頑張りどころは今日ではありません。早めに切り上げる勇気を持ってください。",
        "今日は過去の宿題が顔を出す日です。「{kw1}」が示すのは、"
        "先送りにしてきた一件と向き合う機会です。逃げずに一歩だけ触れておくと後が楽になります。",
        "本日は判断が鈍りやすい日です。「{kw1}」の流れを踏まえ、"
        "重要な返答を求められたら「明日お返事します」と伝えて構いません。それが最善手です。",
    ],
    "凶": [
        "本日は暦のほとんどが「動くな」と告げています。「{kw1}」が強い課題として現れているため、"
        "新規の決断・契約・大きな買い物は、日を改めることを強くおすすめします。",
        "今日は守りに徹する日です。「{kw1}」と「{kw2}」が同時に警告を出しており、"
        "無理に押し切ろうとすると、後始末に何倍もの時間がかかります。",
        "流れが大きく滞る一日です。「{kw1}」の巡りに逆らわず、"
        "今日は「何もしないこと」を積極的に選んでください。それ自体が最良の対処になります。",
        "本日は感情が波立ちやすい日です。「{kw1}」が示すとおり、"
        "言い返したくなる場面が来ても、その場では飲み込んでください。明日には状況が変わります。",
        "消耗が大きい一日です。「{kw1}」「{kw2}」がともに休息を求めています。"
        "予定を削れるだけ削り、体を休めることを最優先にしてください。",
        "今日は人間関係で誤解が生まれやすい日です。「{kw1}」の流れの中では、"
        "説明を尽くしても伝わりにくくなります。重要な話し合いは日を改めましょう。",
        "本日は足元が不安定です。「{kw1}」の巡りが示すとおり、"
        "移動・体調・貴重品の管理に、いつもの倍の注意を払ってください。",
        "運の器が閉じている日です。「{kw1}」と「{kw2}」が回復を促しています。"
        "今日の停滞は、次の上昇のための溜めだと考えてください。必ず抜けます。",
        "今日は手を広げないことが最善です。「{kw1}」が警告しているのは「欲」です。"
        "今ある一つを守ることに集中すれば、損失は最小限に抑えられます。",
        "本日は静けさが薬になる日です。「{kw1}」の気配に従い、"
        "人と会う予定を減らし、ひとりで過ごす時間を確保してください。それが最も早い回復の道です。",
    ],
}

# 200字に満たない場合に追記する補助文（決定論的に選択する）
FILLER_SENTENCES = [
    "焦って結論を出す必要はありません。今日の一手は、明日の自分が受け取る贈り物になります。",
    "小さな習慣ほど、こういう日にこそ効いてきます。いつもの一杯、いつもの散歩を大切にしてください。",
    "誰かに感謝を伝えることは、どの暦でも運を押し上げる行為とされています。一言でも構いません。",
    "夜寝る前に、今日できたことを三つ書き出してみてください。運の流れが可視化されます。",
    "占いは背中を押すための道具です。最後に決めるのは、いつでもあなた自身であることを忘れずに。",
]


# ---------------------------------------------------------------------------
# 内部ヘルパ
# ---------------------------------------------------------------------------
def _safe_get(result: dict, key: str, fallback):
    """結果 dict から安全に値を取り出す。"""
    value = result.get(key)
    if value is None or (isinstance(value, str) and not value.strip()):
        return fallback
    return value


def normalize_result(result, module_name: str) -> dict:
    """モジュールの戻り値を共通スキーマに正規化する（欠損はデフォルト補完）。"""
    base = utils.default_result(module_name)
    if not isinstance(result, dict):
        return base
    normalized = {
        "name": _safe_get(result, "name", module_name),
        "summary": _safe_get(result, "summary", base["summary"]),
        "detail": _safe_get(result, "detail", base["detail"]),
        "lucky_color": _safe_get(result, "lucky_color", base["lucky_color"]),
        "lucky_item": _safe_get(result, "lucky_item", base["lucky_item"]),
        "lucky_dir": _safe_get(result, "lucky_dir", base["lucky_dir"]),
        "score": base["score"],
        "keywords": list(_safe_get(result, "keywords", base["keywords"])),
        "raw": result.get("raw") if isinstance(result.get("raw"), dict) else {},
    }
    try:
        normalized["score"] = utils.clamp_score(int(result.get("score", 50)))
    except (TypeError, ValueError):
        normalized["score"] = 50
    return normalized


def safe_calculate(module, module_name: str, user_data: dict) -> dict:
    """占術モジュールを安全に実行する。

    例外が発生した場合は score=50・lucky_color="白" 等のデフォルト値で補完し、
    アプリ全体がクラッシュしないようにする。
    """
    try:
        result = module.calculate(user_data)
        return normalize_result(result, module_name)
    except Exception:
        return utils.default_result(module_name)


def _majority_vote(results: list, key: str) -> str:
    """指定キーの値を多数決で決定する（同数時は優先モジュール→Unicode順）。"""
    counts = {}
    for r in results:
        value = r.get(key)
        if not value:
            continue
        counts[value] = counts.get(value, 0) + 1
    if not counts:
        return "白"

    max_count = max(counts.values())
    candidates = [v for v, c in counts.items() if c == max_count]
    if len(candidates) == 1:
        return candidates[0]

    # 同数の場合は優先モジュールの値を採用する
    by_module = {r.get("name"): r.get(key) for r in results}
    for module_name in PRIORITY.get(key, []):
        value = by_module.get(module_name)
        if value in candidates:
            return value

    # 最終フォールバック：Unicode 順で最初の値
    return sorted(candidates)[0]


def _merge_keywords(results: list, limit: int = 5) -> list:
    """全モジュールのキーワードを統合し、出現頻度上位を返す。"""
    counts = {}
    order = {}
    for r in results:
        for kw in r.get("keywords") or []:
            kw = str(kw).strip()
            if not kw:
                continue
            counts[kw] = counts.get(kw, 0) + 1
            order.setdefault(kw, len(order))
    # 頻度降順 → 初出順（完全に決定論的な並び）
    ranked = sorted(counts.keys(), key=lambda k: (-counts[k], order[k]))
    return ranked[:limit]


def _category_scores(results: list) -> dict:
    """カテゴリ別運勢を算出する。"""
    by_name = {r.get("name"): r.get("score", 50) for r in results}
    scores = {}
    for category, modules in CATEGORY_MODULES.items():
        values = [by_name[m] for m in modules if m in by_name]
        if not values:
            scores[category] = 50
        else:
            scores[category] = utils.clamp_score(sum(values) / len(values))
    return scores


def _build_message(rank: str, message_key: int, context: dict) -> str:
    """決定論的にテンプレートを選び、総合メッセージを組み立てる。"""
    templates = MESSAGE_TEMPLATES[rank]
    template = templates[message_key % len(templates)]
    body = template.format(**context)

    # ラッキー要素を必ず本文に織り込む
    body += (
        "本日のラッキーカラーは「%s」、ラッキーアイテムは「%s」、"
        "ラッキー方位は「%s」、ラッキーナンバーは%dです。"
        "%s色を身に着けるか視界に入る場所に置き、%sを持ち歩いてください。"
        "外出や打ち合わせの際は%sの方角を意識すると、今日の運の流れに乗りやすくなります。"
    ) % (
        context["color"], context["item"], context["dir"], context["number"],
        context["color"], context["item"], context["dir"],
    )

    # 200字に満たない場合は補助文を決定論的に追記する
    filler_index = message_key
    while len(body) < 200:
        body += FILLER_SENTENCES[filler_index % len(FILLER_SENTENCES)]
        filler_index += 1
    return body


# ---------------------------------------------------------------------------
# メイン：統合処理
# ---------------------------------------------------------------------------
def aggregate(all_results: list, user_data: dict) -> dict:
    """11種の占術結果を統合し、「今日の総合鑑定」を生成する。"""
    # 念のためここでも正規化しておく（不正な結果でも落ちないように）
    results = [normalize_result(r, r.get("name", "占術") if isinstance(r, dict) else "占術")
               for r in all_results]

    # STEP1：重み付き平均
    weight_sum = 0.0
    weighted = 0.0
    for r in results:
        w = MODULE_WEIGHTS.get(r["name"], DEFAULT_WEIGHT)
        weighted += w * r["score"]
        weight_sum += w
    total_score = utils.clamp_score(weighted / weight_sum if weight_sum else 50)

    # STEP2：ランク
    rank = score_rank(total_score)

    # STEP3：ラッキーカラー／アイテム／方位（多数決）
    lucky_color = _majority_vote(results, "lucky_color")
    lucky_item = _majority_vote(results, "lucky_item")
    lucky_dir = _majority_vote(results, "lucky_dir")

    # STEP4：ラッキーナンバー（数秘術のパーソナルデーナンバーを採用）
    lucky_number = None
    for r in results:
        if r["name"] == "数秘術":
            value = (r.get("raw") or {}).get("personal_day_number")
            if isinstance(value, int):
                lucky_number = value
            break
    if lucky_number is None:
        # 数秘術が失敗した場合も決定論的に代替値を作る
        lucky_number = utils.reduce_number(
            total_score + user_data["today"].month + user_data["today"].day)

    # STEP5：キーワード統合
    today_keywords = _merge_keywords(results, 5)

    # STEP6：カテゴリ別運勢
    category_scores = _category_scores(results)

    # STEP7：総合メッセージ（random は使わない決定論的テンプレート選択）
    pattern_count = len(MESSAGE_TEMPLATES[rank])
    message_key = (
        user_data["today"].timetuple().tm_yday
        + total_score
        + user_data["birth_year"]
        + user_data["birth_month"]
        + user_data["birth_day"]
    ) % pattern_count

    kw_padded = list(today_keywords) + ["今日の巡り", "落ち着き", "丁寧さ"]
    context = {
        "kw1": kw_padded[0],
        "kw2": kw_padded[1],
        "kw3": kw_padded[2],
        "color": lucky_color,
        "item": lucky_item,
        "dir": lucky_dir,
        "number": lucky_number,
        "score": total_score,
        "rank": rank,
    }
    overall_message = _build_message(rank, message_key, context)

    # STEP8：戻り値
    return {
        "total_score": total_score,
        "score_rank": rank,
        "lucky_color": lucky_color,
        "lucky_color_hex": utils.color_hex(lucky_color),
        "lucky_item": lucky_item,
        "lucky_dir": lucky_dir,
        "lucky_number": lucky_number,
        "today_keywords": today_keywords,
        "category_scores": category_scores,
        "overall_message": overall_message,
        "score_breakdown": {r["name"]: r["score"] for r in results},
        "detail_results": results,
    }
