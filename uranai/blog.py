# -*- coding: utf-8 -*-
"""ブログ記事（購入・申込み前の疑問に答えるロングテール記事）と PR 商材データ。

Flask 版（app.py の /blog/<slug>・/picks）と静的版（scripts/build_blog.py が
docs/blog/<slug>.html・docs/picks.html を生成）の共通データ源。

本文は uranai/blog_content/<slug>.html に置き、サイト内リンクと商材リンクは
プレースホルダーで書く（Flask と静的版で URL の形が違うため）:
    {{home}}  {{blog_index}}  {{picks}}
    {{guide:<slug>}}  {{post:<slug>}}
    {{cta:<商材キー>}}               … PR 商材ボックス
    {{link:<商材キー>|リンク文字列}}   … 本文中の PR テキストリンク

アフィリエイトリンクは growth_plan/affiliate/a8-links-2026-10-02.json・a8-links-2026-10-09.json（site=005）と
楽天2件のみ。ここに無いリンクを作らない・推測しない。成果報酬額は書かない。
"""
from __future__ import annotations

import html as _html
import os
import re

CONTENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blog_content")

CHECKED_ON = "2026年10月3日〜20日"

# ---------------------------------------------------------------------------
# PR 商材（A8: websiteId 005 / 楽天）
#   facts は公式・販売ページで確認できた事実のみ（確認日 CHECKED_ON）。
#   enabled=False の商材は picks ページ・本文のどちらにも出さない。
# ---------------------------------------------------------------------------
PRODUCTS = {
    "coconala_uranai": {
        "name": "ココナラ占い（メール・チャット・電話）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BC36N+CFQ2S2+2PEO+1BO6EQ",
        "pixel": "https://www14.a8.net/0.gif?a8mat=4BC36N+CFQ2S2+2PEO+1BO6EQ",
        "button": "ココナラ占いの出品一覧を見る",
        "lead": "個人の占い師が鑑定を出品しているスキルマーケット「ココナラ」の占いカテゴリです。",
        "facts": [
            "相談の形式は「メッセージ・チャット占い」と「電話占い」",
            "メッセージ型は出品者ごとに価格が異なり、数百円台から数万円以上まで幅がある",
            "タロット・四柱推命・西洋占星術・手相など20以上の占術から選べる",
        ],
        "enabled": True,
    },
    "coconala": {
        "name": "ココナラ（スキルマーケット）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BC8NA+8ZAHCI+2PEO+OAHHE",
        "pixel": "https://www18.a8.net/0.gif?a8mat=4BC8NA+8ZAHCI+2PEO+OAHHE",
        "button": "ココナラのトップページを見る",
        "lead": "個人の知識・スキルを売り買いできるマーケットです。占い以外にも、文章の添削や悩み相談などさまざまな出品があります。",
        "facts": [
            "出品者が内容と価格を決めて出品し、購入者が選んで依頼する仕組み",
            "出品の有無・価格は時期によって変わるため、依頼前に出品ページで内容を確認する",
        ],
        "enabled": True,
    },
    "saifu": {
        "name": "あなたを幸せにする開運の財布（財布屋）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BE70R+10BJRM+UHI+64JTE",
        "pixel": "https://www17.a8.net/0.gif?a8mat=4BE70R+10BJRM+UHI+64JTE",
        "button": "財布屋の公式サイトを見る",
        "lead": "「開運の財布」を屋号に掲げる財布の専門店です。商品名・コンセプトの「開運」は広告主の表記です。",
        "facts": [
            "公式サイト掲載の価格は550円〜22,000円（最上位の「極上モデル」が22,000円）",
            "サイト内に寅の日・天赦日などの開運日カレンダーを掲載",
            "電話（フリーダイヤル）での問い合わせ窓口あり",
        ],
        "enabled": True,
    },
    "pappy": {
        # 2026-10-03 掲載保留: App Store の説明が「成功した男性と魅力的な女性を繋ぐ」で、
        # 報酬型交際（Sugar dating）を禁じる Google パブリッシャー ポリシー
        # （Compensated sexual acts）に抵触するおそれがある。Render 版が AdSense 審査中のため
        # naoさん判断まで enabled=False。スマホ専用案件（PCではQRコード画面になる）。
        "name": "Pappy（マッチングアプリ）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BCDBL+DUXCSY+22QA+NTRMQ",
        "pixel": "https://www17.a8.net/0.gif?a8mat=4BCDBL+DUXCSY+22QA+NTRMQ",
        "button": "Pappyを見る（スマートフォン専用）",
        "lead": "iPhone向けのマッチングアプリです（18歳以上）。",
        "facts": ["スマートフォンからのみ申し込めます"],
        "enabled": False,
    },
    "photojoy": {
        "name": "Photojoy（マッチングアプリ用プロフィール写真撮影）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BE70R+BBCCY+4HMW+5YJRM",
        "pixel": "https://www15.a8.net/0.gif?a8mat=4BE70R+BBCCY+4HMW+5YJRM",
        "button": "Photojoyの公式サイトを見る",
        "lead": "マッチングアプリのプロフィール写真に特化した出張撮影サービスです。",
        "facts": [
            "定番プラン（一眼×スマホ）16,500円・45分以内・データ35枚",
            "47都道府県で撮影可能（公式表記）",
            "Web予約 → メールで日時調整 → 撮影 → 3営業日以内にメール納品",
        ],
        "enabled": True,
    },
    "otophee": {
        "name": "オトフィー（マッチングアプリ写真撮影）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BE70R+DP2S2+515E+5YRHE",
        "pixel": "https://www12.a8.net/0.gif?a8mat=4BE70R+DP2S2+515E+5YRHE",
        "button": "オトフィーの公式サイトを見る",
        "lead": "マッチングアプリのプロフィール写真撮影サービスです。撮影のほか、アプリの使い方や服装のアドバイスも行うと案内されています。",
        "facts": [
            "写真だけのプラン 9,800円（15分以内）＋カフェ代、定番プラン 16,500円（45分以内）＋カフェ代",
            "一眼レフとスマートフォンで撮影し、全データを納品（最短翌日）",
        ],
        "enabled": True,
    },
    "tsutaekata": {
        "name": "伝え方コミュニケーション検定（初級・中級）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BCDBL+FGOEHE+4K7E+5YJRM",
        "pixel": "https://www17.a8.net/0.gif?a8mat=4BCDBL+FGOEHE+4K7E+5YJRM",
        "button": "伝え方コミュニケーション検定の公式サイトを見る",
        "lead": "一般社団法人 日本ライフコミュニケーション協会のオンライン講座と検定です。",
        "facts": [
            "動画講座170分（15分割）＋Web試験（選択式15問・約15分）",
            "受講料33,000円（税込）、受講期間6か月、分割払いあり",
            "修了すると「JLCA認定・伝え方コミュニケーション検定 中級」の合格証書が郵送される",
        ],
        "enabled": True,
    },
    "totonoe": {
        "name": "光目覚まし時計 トトノエライト プレーン",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BCDBL+G5OLW2+2HEW+5YCH7M",
        "pixel": "https://www17.a8.net/0.gif?a8mat=4BCDBL+G5OLW2+2HEW+5YCH7M",
        "button": "トトノエライトの公式サイトを見る",
        "lead": "株式会社ムーンムーンが販売する、光で起こすタイプの目覚まし時計です。",
        "facts": [
            "公式サイト掲載価格 19,800円",
            "朝は朝日と同等の明るさの光で起こし、夜は赤い光で過ごす使い方を案内（広告主表記）",
        ],
        "enabled": True,
    },
    "tarot": {
        "name": "タロットカード ライダー版（日本語解説書付き）",
        "asp": "rakuten",
        "href": "https://a.r10.to/h8i4uX",
        "pixel": "",
        "button": "楽天市場で商品ページを見る",
        "lead": "初心者向けとして多くの入門書が採用しているウェイト版（ライダー版）のスタンダードデッキです。",
        "facts": [
            "60ページ版または90ページ版の日本語解説書付き（購入時に選択）",
            "収納用ポーチ付き",
            "楽天市場 mitake shop の商品（閲覧時の表示価格 3,080円〜）",
        ],
        "enabled": True,
    },
    "koyomi": {
        "name": "令和九年 高島易断本暦",
        "asp": "rakuten",
        "href": "https://a.r10.to/hHIVX6",
        "pixel": "",
        "button": "楽天ブックスで商品ページを見る",
        "lead": "高島易断協同組合 著・編、ディスカヴァー・トゥエンティワン刊の暦です。",
        "facts": [
            "2026年7月24日発売、1,980円（税込）",
            "シリーズで最も情報量の多い完全版。2027年1〜12月に加え2028年1〜3月も掲載",
            "九星別の運勢、方位盤、吉日の選び方、六輝・十二直・二十八宿などを収録（目次より）",
        ],
        "enabled": True,
    },
    # ---- 2026-10-09 追加（a8-links-2026-10-09.json の site=005）。Morning Booster は広告主の実体を確認できず見送り→KKday で代替 ----
    "coconala_denwa": {
        "name": "ココナラ電話占い",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BC36N+CM9UFM+2PEO+C3BAQ",
        "pixel": "https://www10.a8.net/0.gif?a8mat=4BC36N+CM9UFM+2PEO+C3BAQ",
        "button": "ココナラ電話占いのページを見る",
        "lead": "ココナラが提供する電話占いです。占い師の料金・口コミ・予約可否は占い師ごとの詳細ページで確認できます。",
        "facts": [
            "鑑定料は1分100円（税込）から。占い師ごとに設定（ココナラ公式マガジン 2026年9月28日付）",
            "アプリからの通話は無料。電話からかける場合は1分20円のシステム利用料がかかる",
            "支払いは後払いのみ。クレジットカードは「すぐに電話」と予約の両方で利用可",
            "新規登録向けの3,000円分クーポン（有効期限1週間）は、電話占いページの専用バナーから登録した場合のみ付与（公式マガジンの記載。現行条件は移動先で確認）",
        ],
        "enabled": True,
    },
    "sara_school": {
        "name": "SARAスクール（占い師・スピリチュアル講座）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=3T4RCE+23M5OY+4N6C+787AA",
        "pixel": "https://www19.a8.net/0.gif?a8mat=3T4RCE+23M5OY+4N6C+787AA",
        "button": "SARAスクールの公式サイトを見る",
        "lead": "自宅で学ぶ通信講座のスクールです。公式サイトには占い師・スピリチュアル分野の講座が掲載されています。",
        "facts": [
            "公式サイトの占い師・スピリチュアル講座は22講座（タロット、手相、西洋占星術、風水師、四柱推命、九星気学、姓名判断など）",
            "基本コースは修了後に各資格試験を別途受験、プラチナコースは試験が免除され課題提出で資格授与（公式の案内）",
            "受講料以外の追加料金はなし。ただし資格カード・認定証は資格協会から別途購入（公式FAQ）",
            "受講料・期間・返金条件は講座ごとに異なるため、資料請求・申込み画面で確認する",
        ],
        "enabled": True,
    },
    "ryo_sekkei": {
        "name": "諒設計アーキテクトラーニング（風水セラピスト講座ほか）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=3T4RCE+247LAQ+4N6C+C8VWY",
        "pixel": "https://www16.a8.net/0.gif?a8mat=3T4RCE+247LAQ+4N6C+C8VWY",
        "button": "諒設計アーキテクトラーニングの公式サイトを見る",
        "lead": "通信講座の学校です。公式サイトの「占い師・スピリチュアル」カテゴリに風水関連の講座が掲載されています。",
        "facts": [
            "公式サイトに「風水セラピスト」のほか、タロットカード士、数秘術鑑定士、四柱推命占術士などの講座を掲載",
            "風水に関する資格は国家資格ではなく民間資格",
            "受講料・コース・最短期間は講座ごとに異なるため、公式の講座ページ・資料で確認する",
        ],
        "enabled": True,
    },
    "hana_no_kai": {
        "name": "華の会メール",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BE70R+5YFWY+1T5K+25ES2Q",
        "pixel": "https://www18.a8.net/0.gif?a8mat=4BE70R+5YFWY+1T5K+25ES2Q",
        "button": "華の会メールの公式サイトを見る",
        "lead": "30代以上の恋活・婚活向けの出会いサイトです。広告主は中高年向けのサイトとして案内しています。",
        "facts": [
            "女性は無料と公式に記載。男性の料金は公式ページで確認する",
            "年齢確認として公的な身分証の提示が必要と案内。30歳未満は利用できない旨の注記あり（登録年齢の表記は公式で確認）",
            "公式サイトにインターネット異性紹介事業の届出表示あり",
        ],
        "enabled": True,
    },
    "tasuhana": {
        "name": "タスハナ（+hana・花の定期便）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BCDBM+FKUFPU+4XOY+5YJRM",
        "pixel": "https://www14.a8.net/0.gif?a8mat=4BCDBM+FKUFPU+4XOY+5YJRM",
        "button": "タスハナの公式サイトを見る",
        "lead": "暮らしに花を足すことをコンセプトにした、花の定期便です。",
        "facts": [
            "料金・送料・配送頻度・対象エリア・解約条件はプランや時期で変わるため、申込み前に公式サイトで確認する",
            "比較記事では、解約に最低の配送回数が必要と紹介される例がある（公式の最新条件を確認）",
        ],
        "enabled": True,
    },
    "hugravi": {
        "name": "ハグラビ（ウェイトブランケット）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BE70R+4EYUDU+5XHK+BWVTE",
        "pixel": "https://www17.a8.net/0.gif?a8mat=4BE70R+4EYUDU+5XHK+BWVTE",
        "button": "ハグラビの公式サイトを見る",
        "lead": "重みで体を包む「重いふとん」タイプのウェイトブランケットです。",
        "facts": [
            "販売店の掲載では、Sサイズ（122×198cm）が約6.8kg、Mサイズ（152×203cm）が約9.0kg",
            "重さは体重に合わせて選ぶ商品。サイズ・価格・返品条件・洗濯方法は公式サイトで確認する",
            "睡眠の質の改善や健康への効果を保証するものではありません",
        ],
        "enabled": True,
    },
    "motton": {
        "name": "高反発まくら モットン",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=3T4QKD+9DKVV6+3606+NYHDU",
        "pixel": "https://www15.a8.net/0.gif?a8mat=3T4QKD+9DKVV6+3606+NYHDU",
        "button": "モットンの公式サイトを見る",
        "lead": "高反発素材を使い、中のシートで高さを調整するタイプの枕です。",
        "facts": [
            "高さの調整はシートの抜き差しで行う方式（比較記事の説明。調整幅は公式で確認）",
            "返金保証は公式サイトでの購入が対象と紹介する記事が多い。期間・条件の数え方は公式で確認する",
            "肩こりや睡眠への効果を保証するものではありません",
        ],
        "enabled": True,
    },
    "jalan": {
        "name": "じゃらんnet（国内宿泊予約）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=3T4QKD+AJ987M+14CS+67JUA",
        "pixel": "https://www17.a8.net/0.gif?a8mat=3T4QKD+AJ987M+14CS+67JUA",
        "button": "じゃらんnetで宿を探す",
        "lead": "国内の宿をインターネットで予約できる宿泊予約サイトです。",
        "facts": [
            "宿ごとにプラン・料金・キャンセル規定が異なる",
            "宿泊日の直前はキャンセル料がかかる宿もあるため、予約前にプランごとの規定を確認する",
        ],
        "enabled": True,
    },
    "asoview": {
        "name": "アソビュー（レジャー・体験予約）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=3T4QKD+B9GATU+455G+67C4I",
        "pixel": "https://www12.a8.net/0.gif?a8mat=3T4QKD+B9GATU+455G+67C4I",
        "button": "アソビュー！で体験を探す",
        "lead": "レジャー施設や体験アクティビティを予約できるサイトです。「日本最大級」は広告主の表記です。",
        "facts": [
            "体験やチケットごとに料金・開催日・キャンセル規定が異なる",
            "天候や開催状況による中止・変更の扱いは、各商品ページで確認する",
        ],
        "enabled": True,
    },
    "kkday": {
        "name": "KKday（海外・国内の現地ツアー・体験予約）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=3T4S4T+7K37BM+52F8+5YJRM",
        "pixel": "https://www17.a8.net/0.gif?a8mat=3T4S4T+7K37BM+52F8+5YJRM",
        "button": "KKdayで現地ツアーを探す",
        "lead": "旅行先の現地ツアーや体験、チケットを予約できるサイトです。海外の寺院・聖地めぐりのツアーを探すときの選択肢になります。",
        "facts": [
            "ツアーごとに催行会社・料金・集合場所・キャンセル規定が異なる",
            "最少催行人数に満たない場合の中止や、返金の扱いは各商品ページで確認する",
        ],
        "enabled": True,
    },
    # ---- 2026-10-13 追加（a8-links-2026-10-13.json の site=005）。hanamel・なつみかん・ソルトウェディングは公式情報を確認できず見送り ----
    "jtrip": {
        "name": "J-TRIP（ジェイトリップ・JALで行く国内ツアー）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BCDBM+FG2YVM+40T2+6DRLU",
        "pixel": "https://www17.a8.net/0.gif?a8mat=4BCDBM+FG2YVM+40T2+6DRLU",
        "button": "J-TRIPの公式サイトを見る",
        "lead": "JALの航空便とホテルを組み合わせた国内パッケージツアーを扱うサービスです。",
        "facts": [
            "公式サイトによると、北海道から沖縄までの各地が対象。出発地は東京・大阪・中部・四国・九州・北海道から選べ、2〜5日間",
            "「予約当日23時まで無料キープ＆キャンセル無料」の案内あり（対象と条件は申し込み画面で確認）",
            "取消料の金額は旅行条件書で確認する",
        ],
        "enabled": True,
    },
    "airtrip_tour": {
        "name": "エアトリ国内ツアー",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BCDBM+F4RQDU+AD2+2HB8GI",
        "pixel": "https://www10.a8.net/0.gif?a8mat=4BCDBM+F4RQDU+AD2+2HB8GI",
        "button": "エアトリの国内ツアーを見る",
        "lead": "航空券などを扱う旅行予約サービス「エアトリ」の国内ツアーです。「格安」は広告主の表記です。",
        "facts": [
            "ツアーごとに旅行会社・料金・含まれる内容が異なる",
            "取消料は商品ごとの旅行条件書で確認する（国内航空券のキャンセル案内とは別の規定が適用される場合がある）",
        ],
        "enabled": True,
    },
    "needs_tour": {
        "name": "ニーズツアー（国内旅行・沖縄旅行）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BCDBM+F46AS2+AD2+2BD44I",
        "pixel": "https://www16.a8.net/0.gif?a8mat=4BCDBM+F46AS2+AD2+2BD44I",
        "button": "ニーズツアーを見る",
        "lead": "沖縄・北海道などの国内旅行を扱う旅行会社です。",
        "facts": [
            "旅行比較サイトの掲載情報では、運営は株式会社かんざし。ツアーによって適用される旅行条件書が異なる場合がある",
            "取消料は申し込むツアーの旅行条件書で確認する（広告文の記載と一致するかも確認）",
        ],
        "enabled": True,
    },
    "kobe_cruise": {
        "name": "THE KOBE CRUISE（神戸のレストランクルーズ）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BCDBM+FM1AXE+59HO+5YRHE",
        "pixel": "https://www12.a8.net/0.gif?a8mat=4BCDBM+FM1AXE+59HO+5YRHE",
        "button": "THE KOBE CRUISEの公式サイトを見る",
        "lead": "神戸港のレストランクルーズです。",
        "facts": [
            "公式ページ（確認日2026年10月13日）では、コンチェルトが毎日運航。ルミナス神戸2は「チャーターのみ運航」と案内",
            "時間帯はランチ・ティー・トワイライト・ナイト。所要は約1時間30分〜1時間45分",
            "予約はWebまたは電話（078-360-5600、10:00〜19:00）。キャンセル規定は予約時に確認",
        ],
        "enabled": True,
    },
    "nenga_kazoku": {
        "name": "年賀家族2027（写真入り年賀状）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BE70R+5FVPW2+2ZQM+NTJWY",
        "pixel": "https://www14.a8.net/0.gif?a8mat=4BE70R+5FVPW2+2ZQM+NTJWY",
        "button": "年賀家族2027の公式サイトを見る",
        "lead": "写真入りのデザイナーズ年賀状を注文できるサービスです。",
        "facts": [
            "確認日2026年10月13日時点で、超早期割引は基本料金13,000円が6,760円（48%OFF）、期限は10月27日16:00と案内",
            "年賀はがきを含む注文は予約販売で、11月2日以降に順次出荷",
            "宛名印刷・投函代行は無料と案内。仕上がりが気になる場合の再印刷保障あり",
        ],
        "enabled": True,
    },
    "hyacca": {
        "name": "HYACCA（結婚祝い・内祝いのギフトショップ）",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BE70R+17GR0Y+5VGS+5YJRM",
        "pixel": "https://www13.a8.net/0.gif?a8mat=4BE70R+17GR0Y+5VGS+5YJRM",
        "button": "HYACCAの公式サイトを見る",
        "lead": "結婚・出産のお祝いや内祝いなどのギフトを扱うオンラインギフトショップです。",
        "facts": [
            "公式ページ（確認日2026年10月13日）掲載の価格は、結婚祝いが税込4,400円〜14,979円、結婚内祝いが税込2,754円〜約10,278円",
            "のし対応は商品による。メッセージカードは注文前にプレビューで確認できると案内",
            "ギフトボックスは送料無料（最短翌日発送）。返品・交換の条件は公式ページで確認",
        ],
        "enabled": True,
    },
    "tsutaekata_shokyu": {
        "name": "伝え方コミュニケーション検定・初級",
        "asp": "a8",
        "href": "https://px.a8.net/svt/ejp?a8mat=4BCDBM+EDDSK2+4K7E+C4LLE",
        "pixel": "https://www10.a8.net/0.gif?a8mat=4BCDBM+EDDSK2+4K7E+C4LLE",
        "button": "伝え方コミュニケーション検定・初級の公式サイトを見る",
        "lead": "日本ライフコミュニケーション協会のオンライン講座と検定の初級です。「ウェブ3時間で資格取得」は広告主の表記です。",
        "facts": [
            "受講料・内容・試験方法は初級のページで確認する（中級とは異なる）",
            "民間資格であり、取得による効果を保証するものではありません",
        ],
        "enabled": True,
    },
}

# ---------------------------------------------------------------------------
# ブログ記事のメタ情報（新しい順）
# ---------------------------------------------------------------------------
POSTS = [
    {
        "slug": "coconala-uranai-shiharai-card-meisai",
        "tag": "有料占いの選び方",
        "title": "ココナラ占いの支払い方法は？クレジットカード明細の表記と購入後に確認できること",
        "description": "ココナラ占いで使える支払い方法を公式のお支払いガイドで整理し、クレジットカード明細の表記は公式で確認できなかった点を明記。条件別の判断表と、購入後に確認できること・領収書の発行条件を出典つきで紹介します。",
        "keyword": "ココナラ 占い 支払い方法 クレジットカード 明細",
        "published": "2026-10-22",
    },
    {
        "slug": "tarot-kaisetsusho-nihongo-dore",
        "tag": "タロットの選び方",
        "title": "タロットカードの日本語解説書はどれ？付属本で確認する4点と比較表",
        "description": "タロットの日本語解説書を選ぶときに確認する4点（扱う札の範囲・ページ数・スプレッド・絵柄の系統）と、販売ページや出版情報で確認できた商品の枚数・解説書・価格の一覧を、確認できなかった項目も含めて整理します。",
        "keyword": "タロットカード 解説書 日本語 どれ",
        "published": "2026-10-21",
    },
    {
        "slug": "coconala-uranai-henshin-konai-nannichi",
        "tag": "有料占いの選び方",
        "title": "ココナラ占いの返信が来ないとき何日待つ？キャンセルできる条件と手順",
        "description": "ココナラ占いの出品者から返信が来ないとき、運営のお知らせで確認できた条件（購入から48時間、出品者の最後の連絡から4日以上、リクエスト後24時間）を出典つきで整理。先にすること、返金の考え方、依頼前の確認点を紹介します。",
        "keyword": "ココナラ 占い 返信 来ない 何日待つ キャンセル",
        "published": "2026-10-20",
    },
    {
        "slug": "tarot-22mai-78mai-shoshinsha-dochira",
        "tag": "タロットの選び方",
        "title": "タロットカード初心者は22枚と78枚どっち？買う前の確認点と選び方",
        "description": "タロットの枚数構成（大アルカナ22枚＋小アルカナ56枚）を出典つきで整理し、22枚セットと78枚フルデッキの違い、状況別の選び方、購入前に商品ページで確認する枚数表示と解説書の範囲を紹介します。",
        "keyword": "タロットカード 22枚 78枚 初心者 どっち",
        "published": "2026-10-20",
    },
    {
        "slug": "muryo-uranai-kanteishi-message-yamerarenai",
        "tag": "有料占いの選び方",
        "title": "無料占いの鑑定士からのメッセージが止まらない時は？やめ方と相談先",
        "description": "国民生活センターの公表資料で確認できた、無料占いから有料に誘導される5つの手口と公表事例、メッセージが止まらないときの対応、消費者ホットライン188などの相談先、有料占いを選ぶ前の確認点を整理します。",
        "keyword": "無料占い 鑑定士 メッセージ 止まらない やめたい",
        "published": "2026-10-20",
    },
    {
        "slug": "coconala-uranai-tokumei-kojin-joho",
        "tag": "有料占いの選び方",
        "title": "ココナラ占いは匿名で相談できる？生年月日や本名を伝える前の確認点",
        "description": "ココナラ公式の購入ガイドで確認できた、匿名相談・やり取りの非公開・代金預かりの仕組みを出典つきで整理。生年月日や本名が必要になる占術の目安と、依頼前に出品者へ確認するチェックリストを紹介します。",
        "keyword": "ココナラ 占い 匿名 生年月日 本名",
        "published": "2026-10-16",
    },
    {
        "slug": "takashima-ekidan-koyomi-kindle-kami-dochira",
        "tag": "暦の選び方",
        "title": "高島易断の暦はKindleと紙どっち？令和九年版の選び方と確認点",
        "description": "令和九年版の高島易断シリーズ4種はすべてKindle版あり。出版社の発表資料で確認できた事実をもとに、紙とKindleの向き不向き、購入前に販売ページで確認したい4点を整理します。",
        "keyword": "高島易断 暦 Kindle 紙 どっち",
        "published": "2026-10-16",
    },
    {
        "slug": "tarot-rider-waite-han-chigai-namae",
        "tag": "タロットの選び方",
        "title": "ライダー版とウェイト版のタロットは違う？名前の由来と選び方",
        "description": "タロットカードの「ライダー版」「ウェイト版」「ライダー・ウェイト・スミス版」の呼び名の由来を英語圏の資料で整理。同じ系統でも版で異なる点と、初心者が購入前に確認したい項目を紹介します。",
        "keyword": "タロット ライダー版 ウェイト版 違い",
        "published": "2026-10-16",
    },
    {
        "slug": "coconala-uranai-cancel-henkin-atanaranai",
        "tag": "有料占いの選び方",
        "title": "ココナラ占いのキャンセル・返金は？当たらない・違うと感じたときの確認点",
        "description": "ココナラ公式の購入ガイドとお知らせで確認できた、キャンセルと返金の仕組みを出典つきで整理。「当たらなかった」場合の扱い、差し戻し、電話占いの注意点と、申し込み前の確認チェックリストを紹介します。",
        "keyword": "ココナラ 占い キャンセル 返金 当たらない",
        "published": "2026-10-16",
    },
    {
        "slug": "takashima-ekidan-koyomi-itsu-doko-iranai",
        "tag": "暦の選び方",
        "title": "高島易断の暦はいつ買う？どこで買う？令和九年版がいらない人の判断基準",
        "description": "令和九年版の高島易断の暦について、発売時期、紙と電子の購入先、必要な人・いらない人の判断基準を、出版社の発表資料と楽天ブックスの情報で整理。買う前に手元で確認できる3点も紹介します。",
        "keyword": "高島易断 暦 いつ買う どこで買う いらない",
        "published": "2026-10-16",
    },
    {
        "slug": "uranai-kekka-kodo-erabikata-hub",
        "tag": "選び方まとめ",
        "title": "占いのあとにお金を使う前に｜目的別の選び方と判断フロー表",
        "description": "占いの結果を見たあとの「次の一手」を、相談・学び・旅行・記念日・年賀状・お祝い・道具・出会いの状況別に整理。申し込み前に確認する総額・期間・解約条件の3点と、無料でできることを紹介します。",
        "keyword": "占い 結果 行動 選び方 申し込み前 確認",
        "published": "2026-10-13",
    },
    {
        "slug": "kokunai-tour-kojin-tehai-dochira",
        "tag": "旅と開運",
        "title": "国内旅行はツアーか個人手配か｜判断基準と取消料の確認点",
        "description": "国内旅行のパッケージツアーと個人手配の違いを、費用・自由度・キャンセルで比較。J-TRIP・エアトリ国内ツアー・ニーズツアーを申し込む前に旅行条件書で確認する点と、方位や吉日で日程を決める人の注意をまとめました。",
        "keyword": "国内旅行 ツアー 個人手配 どっち 取消料",
        "published": "2026-10-13",
    },
    {
        "slug": "nengajo-2027-shashin-hayawari-kazoku",
        "tag": "暮らしと暦",
        "title": "写真入り年賀状2027は早割で頼むべき？注文前の判断基準5つ",
        "description": "2027年（未年）の写真入り年賀状を「年賀家族2027」で注文する前の判断基準を整理。公式ページで確認できた早割の期限、出荷時期、宛名印刷・投函代行、再印刷保障と、総額の計算方法を紹介します。",
        "keyword": "年賀状 2027 写真入り 早割 注文",
        "published": "2026-10-13",
    },
    {
        "slug": "kobe-dinner-cruise-kinenbi-yoyaku-mae",
        "tag": "旅と開運",
        "title": "神戸のレストランクルーズは記念日向き？予約前の確認点5つ",
        "description": "THE KOBE CRUISEの公式ページで確認できた運航状況・時間帯・料金の見方・予約方法をもとに、記念日のクルーズ予約前に確認したい5つの点と、キャンセル規定・天候への備えを整理しました。",
        "keyword": "神戸 レストランクルーズ 記念日 予約 キャンセル",
        "published": "2026-10-13",
    },
    {
        "slug": "kekkon-iwai-uchiiwai-yosan-noshi",
        "tag": "暮らしと暦",
        "title": "結婚祝いと内祝いの予算はいくら？のし・配送の確認点",
        "description": "結婚祝いと結婚内祝いの違い、予算の決め方、のし・メッセージカードの確認点を整理。HYACCAの公式ページで確認できた価格帯・送料・返品交換の案内とあわせて、注文前のチェックリストを紹介します。",
        "keyword": "結婚祝い 内祝い 予算 のし 選び方",
        "published": "2026-10-13",
    },
    {
        "slug": "power-spot-ryokou-yado-taiken-yoyaku",
        "tag": "旅と開運",
        "title": "パワースポット旅行は宿と体験をどう予約する？日帰り・一泊の段取りとキャンセル規定の確認点",
        "description": "神社めぐりなどのパワースポット旅行で、宿と体験をどの順番で予約するか、日帰りと一泊の違い、じゃらんnet・アソビュー！で予約する前に確認したいキャンセル規定や天候の扱いを整理しました。",
        "keyword": "パワースポット 旅行 宿 予約 体験",
        "published": "2026-10-09",
    },
    {
        "slug": "shinshitsu-fusui-makura-weighted-blanket-hana",
        "tag": "暮らしと風水",
        "title": "寝室の風水は何から整える？枕・ウェイトブランケット・花の定期便の選び方と申し込み前の確認点",
        "description": "風水の寝室づくりの基本（掃除・換気・整理整頓・枕の向き）を整理し、高さ調整できる枕、ウェイトブランケットの重さの目安、花の定期便の解約条件など、購入前に確認したい点をまとめました。",
        "keyword": "寝室 風水 枕 ウェイトブランケット 花 定期便",
        "published": "2026-10-09",
    },
    {
        "slug": "hana-no-kai-mail-touroku-mae-kakunin",
        "tag": "恋愛占いのあとに",
        "title": "華の会メールに登録する前に確認したいこと：年齢条件・女性無料・年齢確認と詐欺への注意",
        "description": "30代以上向けの出会いサイト「華の会メール」について、公式サイトで確認できた年齢条件・料金の仕組み・年齢確認と、ロマンス詐欺・投資詐欺を避けるための基本、占いの結果を行動に生かす方法を整理しました。",
        "keyword": "華の会メール 登録前 年齢確認 女性無料",
        "published": "2026-10-09",
    },
    {
        "slug": "fusui-shikaku-tsushin-kouza-hikaku",
        "tag": "占いを学ぶ",
        "title": "風水の資格は通信講座で取れる？SARAスクールと諒設計アーキテクトラーニングの選び方と申し込み前の確認点",
        "description": "風水や占術の資格は民間資格です。公式サイトで講座が確認できるSARAスクールと諒設計アーキテクトラーニングを例に、基本コースとプラチナコースの違い、追加費用、返金条件など申し込み前の比較項目を整理しました。",
        "keyword": "風水 資格 通信講座 比較",
        "published": "2026-10-09",
    },
    {
        "slug": "coconala-denwa-uranai-hatsukai-coupon-nanpun",
        "tag": "有料占いの選び方",
        "title": "ココナラ電話占いの初回クーポンは何分使える？専用バナーの条件・通話料・後払いの注意点",
        "description": "ココナラ公式マガジンの記載をもとに、電話占いの初回3,000円分クーポンで話せる時間の計算、付与されない登録経路、有効期限1週間の段取り、料金が膨らまないためのルールを整理しました。",
        "keyword": "電話占い 初回 クーポン 何分",
        "published": "2026-10-09",
    },
    {
        "slug": "mail-uranai-denwa-uranai-dochira",
        "tag": "有料占いの選び方",
        "title": "メール占いと電話占いはどっちがいい？相談内容別の選び方と料金の考え方",
        "description": "メール占いと電話占いの違いを、料金のかかり方・向いている相談・申し込み前の確認点から整理。ココナラでの選び方と、人間関係の悩みで占い以外に取れる手段も紹介します。",
        "keyword": "メール占い 電話占い どっちがいい",
        "published": "2026-10-03",
    },
    {
        "slug": "tarot-card-shoshinsha-erabikata",
        "tag": "道具の選び方",
        "title": "タロットカード初心者はどれを買う？1組目はライダー版78枚が無難な理由",
        "description": "タロットカード初心者はどれを買うか迷ったら、ライダー版の78枚フルデッキで日本語解説書付きが無難です。マルセイユ版との違い、78枚と22枚、サイズなど購入前の確認点を整理しました。",
        "keyword": "タロットカード 初心者 ライダー版 解説書付き",
        "published": "2026-10-03",
    },
    {
        "slug": "takashima-ekidan-hongoyomi-chigai",
        "tag": "暦の選び方",
        "title": "高島易断の本暦・開運本暦・運勢本暦の違いは？令和九年版の選び方",
        "description": "令和九年版の高島易断シリーズ4種（本暦・開運本暦・運勢本暦・吉運本暦）の違いを収録範囲とページ数で比較し、使い方別にどれを選ぶかを整理しました。",
        "keyword": "高島易断 本暦 運勢暦 違い",
        "published": "2026-10-03",
    },
    {
        "slug": "saifu-shinchou-hi-koyomi-erabikata",
        "tag": "暦の使い方",
        "title": "財布を新調する日は暦でどう選ぶ？寅の日・一粒万倍日・天赦日の調べ方",
        "description": "財布の買い替え・使い始めの日を暦で選ぶときの考え方を整理。寅の日・一粒万倍日・天赦日などの暦注の意味、自分で調べる手順、購入前に確認したい点をまとめました。",
        "keyword": "財布 新調 日 暦 選び方",
        "published": "2026-10-03",
    },
    {
        "slug": "matching-app-shashin-satsuei-hikaku",
        "tag": "恋愛占いのあとに",
        "title": "マッチングアプリの写真撮影サービスは使うべき？料金とプランの比較と申し込み前の確認点",
        "description": "恋愛占いのあとに出会いの行動を始める人向けに、マッチングアプリのプロフィール写真撮影サービス（Photojoy・オトフィー）の料金とプラン、申し込み前の確認点を整理しました。",
        "keyword": "マッチングアプリ 写真撮影 料金 比較",
        "published": "2026-10-03",
    },
]

# 既存の占術ガイドから関連ブログ記事へ張る内部リンク（ガイド slug → 記事 slug）
GUIDE_RELATED_POSTS = {
    "kyusei-kigaku": ["kokunai-tour-kojin-tehai-dochira", "nengajo-2027-shashin-hayawari-kazoku", "takashima-ekidan-hongoyomi-chigai", "saifu-shinchou-hi-koyomi-erabikata",
                      "power-spot-ryokou-yado-taiken-yoyaku", "shinshitsu-fusui-makura-weighted-blanket-hana"],
    "shukuyo": ["saifu-shinchou-hi-koyomi-erabikata", "hana-no-kai-mail-touroku-mae-kakunin"],
    "seiyo-uranai": ["tarot-card-shoshinsha-erabikata", "tarot-22mai-78mai-shoshinsha-dochira", "tarot-kaisetsusho-nihongo-dore", "mail-uranai-denwa-uranai-dochira",
                     "fusui-shikaku-tsushin-kouza-hikaku"],
    "suuhi": ["mail-uranai-denwa-uranai-dochira", "coconala-denwa-uranai-hatsukai-coupon-nanpun"],
    "sanmei": ["takashima-ekidan-hongoyomi-chigai", "fusui-shikaku-tsushin-kouza-hikaku"],
    "seimei": ["uranai-kekka-kodo-erabikata-hub", "matching-app-shashin-satsuei-hikaku", "hana-no-kai-mail-touroku-mae-kakunin"],
    "shichu-suimei": ["fusui-shikaku-tsushin-kouza-hikaku", "coconala-denwa-uranai-hatsukai-coupon-nanpun"],
}


def get_post(slug: str):
    for p in POSTS:
        if p["slug"] == slug:
            return p
    return None


def related_posts(slug: str, n: int = 3) -> list:
    others = [p for p in POSTS if p["slug"] != slug]
    return others[:n]


def posts_for_guide(guide_slug: str) -> list:
    return [get_post(s) for s in GUIDE_RELATED_POSTS.get(guide_slug, []) if get_post(s)]


def enabled_products() -> list:
    return [(k, v) for k, v in PRODUCTS.items() if v.get("enabled")]


# ---------------------------------------------------------------------------
# HTML 生成
# ---------------------------------------------------------------------------
def _esc(s) -> str:
    return _html.escape(str(s), quote=True)


def _pixel(p: dict) -> str:
    if not p.get("pixel"):
        return ""
    return '<img border="0" width="1" height="1" src="%s" alt="">' % _esc(p["pixel"])


def cta_box(key: str) -> str:
    p = PRODUCTS[key]
    if not p.get("enabled"):
        return ""
    facts = "".join("<li>%s</li>" % _esc(f) for f in p["facts"])
    return (
        '<aside class="aff-box">\n'
        '  <p class="consult-label">【PR】</p>\n'
        '  <p class="aff-title">%(name)s</p>\n'
        '  <p class="aff-lead">%(lead)s</p>\n'
        '  <ul class="aff-facts">%(facts)s</ul>\n'
        '  <a class="submit-button link-button consult-button" href="%(href)s" '
        'rel="nofollow sponsored noopener" target="_blank">%(button)s【PR】</a>%(pixel)s\n'
        '  <p class="consult-note">※外部サイトに移動します。価格・内容は%(date)s時点の公式・販売ページの表示です。'
        '最新の条件は移動先でご確認ください。</p>\n'
        '</aside>\n'
    ) % {"name": _esc(p["name"]), "lead": _esc(p["lead"]), "facts": facts,
         "href": _esc(p["href"]), "button": _esc(p["button"]), "pixel": _pixel(p),
         "date": CHECKED_ON}


def inline_link(key: str, text: str) -> str:
    p = PRODUCTS[key]
    if not p.get("enabled"):
        return _esc(text)
    return ('<a class="aff-inline" href="%s" rel="nofollow sponsored noopener" target="_blank">%s【PR】</a>%s'
            % (_esc(p["href"]), text, _pixel(p)))


_PH = re.compile(r"\{\{(home|blog_index|picks|guide:[a-z0-9-]+|post:[a-z0-9-]+|cta:[a-z_]+|link:[a-z_]+\|[^}]+)\}\}")


def render_body(raw: str, urls) -> str:
    """プレースホルダーを解決する。urls(kind, arg) -> URL を呼び出し側が渡す。"""
    def rep(m):
        tok = m.group(1)
        if tok in ("home", "blog_index", "picks"):
            return urls(tok, None)
        kind, _, arg = tok.partition(":")
        if kind in ("guide", "post"):
            return urls(kind, arg)
        if kind == "cta":
            return cta_box(arg)
        if kind == "link":
            key, _, text = arg.partition("|")
            return inline_link(key, text)
        return m.group(0)
    out = _PH.sub(rep, raw)
    if "{{" in out:
        raise ValueError("未解決のプレースホルダーがあります: %s" % out[out.index("{{"):][:60])
    return out


def load_body(slug: str) -> str:
    with open(os.path.join(CONTENT_DIR, "%s.html" % slug), encoding="utf-8") as f:
        return f.read()


def toc_of(body_html: str) -> list:
    """本文の <h2 class="guide-heading" id="..."> から目次を作る。"""
    return re.findall(r'<h2 class="guide-heading" id="([^"]+)">(.*?)</h2>', body_html)


def picks_body() -> str:
    """商材一覧ページの本文（プレースホルダーなしの完成HTML。記事リンクは呼び出し側で付ける）。"""
    return "".join(cta_box(k) for k, _ in enabled_products())


# 商材ごとの「紹介している記事」（picks ページから記事へ戻す導線）
def posts_mentioning(key: str) -> list:
    out = []
    for p in POSTS:
        try:
            raw = load_body(p["slug"])
        except OSError:
            continue
        if ("{{cta:%s}}" % key) in raw or ("{{link:%s|" % key) in raw:
            out.append(p)
    return out


# ---------------------------------------------------------------------------
# 構造化データ（FAQPage / BlogPosting）と記事の外枠（Flask・静的版で共通）
# ---------------------------------------------------------------------------
def _clean(t: str) -> str:
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", t))).strip()


def faq_of(body_html: str) -> list:
    m = re.search(r'<h2 class="guide-heading" id="faq">よくある質問</h2>(.*?)</section>', body_html, re.S)
    if not m:
        return []
    return [(_clean(q), _clean(a)) for q, a in re.findall(
        r'<h3 class="guide-subheading">(.*?)</h3>\s*<p class="guide-paragraph">(.*?)</p>',
        m.group(1), re.S)]


def jsonld(post: dict, url: str, body_html: str) -> str:
    import json
    blocks = []
    faq = faq_of(body_html)
    if faq:
        blocks.append({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": [{"@type": "Question", "name": q,
                                       "acceptedAnswer": {"@type": "Answer", "text": a}}
                                      for q, a in faq]})
    blocks.append({"@context": "https://schema.org", "@type": "BlogPosting",
                   "headline": post["title"], "description": post["description"],
                   "datePublished": post["published"],
                   "dateModified": post.get("modified", post["published"]),
                   "mainEntityOfPage": url, "inLanguage": "ja",
                   "author": {"@type": "Organization", "name": "今日の総合鑑定 編集部"},
                   "publisher": {"@type": "Organization", "name": "今日の総合鑑定"}})
    return "".join('<script type="application/ld+json">\n%s\n</script>\n'
                   % json.dumps(b, ensure_ascii=False) for b in blocks)


PR_NOTICE = ("【PR】この記事にはアフィリエイト広告（A8.net・楽天アフィリエイト）を利用したリンクを含みます。"
             "紹介する商品・サービスの価格や条件は、公式・販売ページで確認できた範囲のみを記載しています。"
             "占いの結果や商品の効果を保証するものではありません。")


def _related_li(url: str, label: str, title: str) -> str:
    return ('    <li>\n      <a href="%s">\n        <strong>%s</strong>\n        <span>%s</span>\n'
            '      </a>\n    </li>\n' % (url, _esc(label), _esc(title)))


def article_html(post: dict, body: str, urls) -> str:
    """記事ページの <main> 内 HTML。body は render_body 済み、urls は同じ解決関数。"""
    toc = "".join('      <li><a href="#%s">%s</a></li>\n' % (i, h) for i, h in toc_of(body))
    rel = "".join(_related_li(urls("post", r["slug"]), r["tag"], r["title"])
                  for r in related_posts(post["slug"]))
    return (
        '<nav class="breadcrumb" aria-label="パンくずリスト">\n'
        '  <a href="%(home)s">トップ</a>\n'
        '  <span aria-hidden="true">›</span>\n'
        '  <a href="%(blog)s">ブログ・占術ガイド</a>\n'
        '  <span aria-hidden="true">›</span>\n'
        '  <span>%(tag)s</span>\n'
        '</nav>\n\n'
        '<article class="card guide-article">\n'
        '  <p class="guide-tag">%(tag)s</p>\n'
        '  <h1 class="guide-title">%(title)s</h1>\n'
        '  <p class="blog-meta">公開日 <time datetime="%(pub)s">%(pub)s</time>　文：今日の総合鑑定 編集部</p>\n'
        '  <p class="pr-notice">%(pr)s</p>\n\n'
        '  <nav class="guide-toc" aria-label="目次">\n'
        '    <p class="guide-toc-title">目次</p>\n'
        '    <ol>\n%(toc)s    </ol>\n'
        '  </nav>\n\n'
        '%(body)s\n'
        '  <p class="guide-disclaimer">\n'
        '    ※本記事は占いや暦の考え方、商品・サービスの選び方を紹介するものであり、占いの結果や開運などの効果を保証するものではありません。\n'
        '    鑑定結果はエンターテインメントとしてお楽しみください。\n'
        '  </p>\n'
        '</article>\n\n'
        '<section class="card">\n'
        '  <h2 class="card-title">まずは無料で今日の総合鑑定を見る</h2>\n'
        '  <p>\n'
        '    当サイトでは、お名前と生年月日など5項目を入力するだけで、11種の占術をまとめて計算した今日の総合鑑定を無料で表示します。\n'
        '    有料の相談や道具を検討する前に、まず自分の結果を確かめてみてください。\n'
        '  </p>\n'
        '  <a class="submit-button link-button" href="%(home)s">今日の総合鑑定を見る</a>\n'
        '</section>\n\n'
        '<section class="card">\n'
        '  <h2 class="card-title">あわせて読みたい記事</h2>\n'
        '  <ul class="guide-related">\n%(rel)s  </ul>\n'
        '  <a class="guide-card-link" href="%(picks)s">記事で紹介しているサービス・アイテムの一覧【PR】</a>\n'
        '</section>\n'
    ) % {"home": urls("home", None), "blog": urls("blog_index", None), "picks": urls("picks", None),
         "tag": _esc(post["tag"]), "title": _esc(post["title"]), "pub": post["published"],
         "pr": _esc(PR_NOTICE), "toc": toc, "body": body, "rel": rel}


PICKS_TITLE = "記事で紹介しているサービス・アイテム一覧【PR】"
PICKS_DESC = ("今日の総合鑑定のブログ記事で紹介している占い相談サービス・通信講座・タロットカード・暦・財布・"
              "寝具・旅行予約・年賀状・ギフト・写真撮影サービスなどを、公式ページで確認できた価格・内容とあわせて一覧にしました。")


def picks_html(urls) -> str:
    items = ""
    for k, _ in enabled_products():
        items += cta_box(k)
        posts = posts_mentioning(k)
        if posts:
            items += ('  <p class="guide-paragraph">この商品・サービスを紹介している記事：%s</p>\n'
                      % "、".join('<a href="%s">%s</a>' % (urls("post", p["slug"]), _esc(p["title"]))
                                 for p in posts))
    return (
        '<nav class="breadcrumb" aria-label="パンくずリスト">\n'
        '  <a href="%(home)s">トップ</a>\n'
        '  <span aria-hidden="true">›</span>\n'
        '  <a href="%(blog)s">ブログ・占術ガイド</a>\n'
        '  <span aria-hidden="true">›</span>\n'
        '  <span>紹介しているサービス・アイテム</span>\n'
        '</nav>\n\n'
        '<article class="card guide-article">\n'
        '  <p class="guide-tag">PR</p>\n'
        '  <h1 class="guide-title">記事で紹介しているサービス・アイテム一覧</h1>\n'
        '  <p class="pr-notice">%(pr)s</p>\n'
        '  <p class="guide-lead">当サイトのブログ記事で紹介している有料の相談サービスや道具を、一か所にまとめました。'
        'どれも「占いの結果を見たあと、自分で次の行動を選ぶ」ための選択肢のひとつで、利用しなければならないものではありません。'
        '価格・内容は%(date)s時点で公式・販売ページに表示されていたものです。</p>\n'
        '%(items)s'
        '  <p class="guide-disclaimer">※占いの結果や、商品・サービスによる開運などの効果を保証するものではありません。'
        '申し込み・購入の前に、移動先のページで最新の価格・条件・解約方法をご確認ください。</p>\n'
        '</article>\n\n'
        '<section class="card">\n'
        '  <h2 class="card-title">まずは無料で今日の総合鑑定を見る</h2>\n'
        '  <p>5項目の入力で、11種の占術をまとめた今日の総合鑑定を無料で表示します。</p>\n'
        '  <a class="submit-button link-button" href="%(home)s">今日の総合鑑定を見る</a>\n'
        '</section>\n'
    ) % {"home": urls("home", None), "blog": urls("blog_index", None),
         "pr": _esc(PR_NOTICE), "date": CHECKED_ON, "items": items}


def blog_index_section(urls) -> str:
    """一覧ページ（ブログ・占術ガイド）に差し込むブログ記事カード群。"""
    cards = ""
    for p in POSTS:
        cards += (
            '  <article class="guide-card">\n'
            '    <p class="guide-card-tag">%(tag)s</p>\n'
            '    <h2 class="guide-card-title">\n'
            '      <a href="%(url)s">%(title)s</a>\n'
            '    </h2>\n'
            '    <p class="guide-card-desc">%(desc)s</p>\n'
            '    <a class="guide-card-link" href="%(url)s">\n'
            '      この記事を読む\n'
            '    </a>\n'
            '  </article>\n'
        ) % {"tag": _esc(p["tag"]), "url": urls("post", p["slug"]),
             "title": _esc(p["title"]), "desc": _esc(p["description"])}
    return (
        '<!-- blog-index:start -->\n'
        '<section class="card" id="blog">\n'
        '  <h2 class="card-title">ブログ：申し込み・購入の前に読む記事</h2>\n'
        '  <p>有料の占い相談や占いの道具、暦を使った日取りなど、申し込みや購入の前に迷いやすい点を整理した記事です。'
        '一部の記事はアフィリエイト広告（PR）を含みます。'
        '<a href="%(picks)s">紹介しているサービス・アイテムの一覧【PR】</a></p>\n'
        '</section>\n'
        '<section class="guide-index">\n%(cards)s</section>\n'
        '<!-- blog-index:end -->\n'
    ) % {"picks": urls("picks", None), "cards": cards}


def guide_related_section(guide_slug: str, urls) -> str:
    """占術ガイド記事の末尾に差し込む「関連するブログ記事」カード。"""
    posts = posts_for_guide(guide_slug)
    if not posts:
        return ""
    lis = "".join(_related_li(urls("post", p["slug"]), p["tag"], p["title"]) for p in posts)
    return ('<!-- guide-blog:start -->\n'
            '<section class="card">\n'
            '  <h2 class="card-title">関連するブログ記事</h2>\n'
            '  <ul class="guide-related">\n%s  </ul>\n'
            '</section>\n'
            '<!-- guide-blog:end -->\n' % lis)
