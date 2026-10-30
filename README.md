# 今日の総合鑑定

生年月日・氏名など5項目の入力から、命占10種＋姓名判断＝11種の占術をすべて計算し、
「今日の総合鑑定」として1つの結論（総合評価・ラッキーカラー・アイテム・方位・ナンバー）に
まとめて提示するFlask製Webアプリケーションです。

- 完全に決定論的（`random`モジュール不使用）。同一入力＋同一日付は必ず同一結果。
- 「今日の日付」を計算に組み込むため、同じ人でも日付が変われば結果が変わる日替わり占い。
- Render.com無料プランでの動作を想定。

## デプロイ（Render.com）

下のボタンから、このリポジトリの `render.yaml` を使って新しいWeb Serviceを作成できます。

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/solederlego8-a11y/uranai-app)

このリポジトリは非公開のため、ボタンを押すとRenderのGitHub連携画面で
アクセス許可を求められます。GitHubアカウント（`solederlego8-a11y`）でログインし、
このリポジトリへのアクセスを許可してください。

### 手動でデプロイする場合

1. [Render Dashboard](https://dashboard.render.com/) → **New → Web Service**
2. GitHubを連携し、`uranai-app` リポジトリを選択
3. `render.yaml` が自動検出されるので、Plan が **Free** になっていることを確認して作成

## 環境変数（すべて任意・未設定でも動作する）

| 変数名 | 用途 | 未設定時の挙動 |
|---|---|---|
| `SITE_OPERATOR` | お問い合わせページに表示する運営者名 | 「未設定」の警告が表示される |
| `CONTACT_EMAIL` | お問い合わせページに表示する連絡先 | 「未設定」の警告が表示される |
| `ADSENSE_CLIENT_ID` | Google AdSenseのパブリッシャーID（`ca-pub-`で始まる16桁） | AdSenseタグと`/ads.txt`が無効化される |

Renderのサービス画面 → **Environment** タブから設定し、保存すると自動で再デプロイされます。

## AdSense申請前のチェックリスト

- [ ] Renderにデプロイし、公開URLを取得する
- [ ] `SITE_OPERATOR` / `CONTACT_EMAIL` を設定する
- [ ] スリープ対策：[UptimeRobot](https://uptimerobot.com/)等で `/healthz` を5分間隔で監視する（無料プランは15分放置でスリープするため）
- [ ] AdSenseに申請し、発行された `ca-pub-...` を `ADSENSE_CLIENT_ID` に設定する

## ローカルでの起動方法

```bash
pip install -r requirements.txt
python app.py
```

`http://localhost:5000` で起動します。

## ディレクトリ構成

```
app.py                  Flaskアプリ本体
uranai/
  ├─ __init__.py        11モジュール登録・build_report()
  ├─ utils.py            共通ユーティリティ（干支・五行・方位・色・旧暦変換等）
  ├─ seimei.py            ① 姓名判断
  ├─ seiyo_uranai.py       ② 西洋占星術
  ├─ shichu_suimei.py      ③ 四柱推命
  ├─ shibi_tosuu.py        ④ 紫微斗数
  ├─ kyusei_kigaku.py      ⑤ 九星気学
  ├─ sanmei.py             ⑥ 算命学
  ├─ suuhi.py              ⑦ 数秘術
  ├─ india_uranai.py       ⑧ インド占星術
  ├─ shukuyo.py            ⑨ 宿曜占星術
  ├─ maya.py               ⑩ マヤ暦占い
  ├─ tibet.py              ⑪ チベット占星術
  ├─ aggregator.py        ★11種の結果を統合し「今日の総合鑑定」を生成
  └─ guides.py             占術解説記事のコンテンツ
templates/               Jinja2テンプレート
static/                  CSS・JS
```

## 免責事項

当サイトが提供する鑑定結果は、エンターテインメントを目的としたものです。
各占術は文化的・歴史的な体系であり、その内容について科学的根拠を保証するものではありません。

<!-- article-index:start -->
## 今日の総合鑑定 公開中のページ一覧

生年月日などの入力から11種の占術をまとめて鑑定する無料占いサイト

サイト: https://solederlego8-a11y.github.io/uranai-app/

### top
- [今日の総合鑑定｜5項目の入力で11種の占術をまとめて鑑定](https://solederlego8-a11y.github.io/uranai-app/)
- [このサイトについて](https://solederlego8-a11y.github.io/uranai-app/about.html)
- [占い方の解説一覧｜11種の占術をやさしく読み解く](https://solederlego8-a11y.github.io/uranai-app/guides.html)
- [プライバシーポリシー](https://solederlego8-a11y.github.io/uranai-app/privacy.html)
- [お問い合わせ・運営者情報](https://solederlego8-a11y.github.io/uranai-app/contact.html)
- [記事で紹介しているサービス・アイテム一覧【PR】](https://solederlego8-a11y.github.io/uranai-app/picks.html)

### blog
- [メール占いと電話占いはどっちがいい？相談内容別の選び方と料金の考え方](https://solederlego8-a11y.github.io/uranai-app/blog/mail-uranai-denwa-uranai-dochira.html)
- [タロットカード初心者はどれを買う？1組目はライダー版78枚が無難な理由](https://solederlego8-a11y.github.io/uranai-app/blog/tarot-card-shoshinsha-erabikata.html)
- [高島易断の本暦・開運本暦・運勢本暦の違いは？令和九年版の選び方](https://solederlego8-a11y.github.io/uranai-app/blog/takashima-ekidan-hongoyomi-chigai.html)
- [財布を新調する日は暦でどう選ぶ？寅の日・一粒万倍日・天赦日の調べ方](https://solederlego8-a11y.github.io/uranai-app/blog/saifu-shinchou-hi-koyomi-erabikata.html)
- [マッチングアプリの写真撮影サービスは使うべき？料金とプランの比較と申し込み前の確認点](https://solederlego8-a11y.github.io/uranai-app/blog/matching-app-shashin-satsuei-hikaku.html)
- [パワースポット旅行は宿と体験をどう予約する？日帰り・一泊の段取りとキャンセル規定の確認点](https://solederlego8-a11y.github.io/uranai-app/blog/power-spot-ryokou-yado-taiken-yoyaku.html)
- [寝室の風水は何から整える？枕・ウェイトブランケット・花の定期便の選び方と申し込み前の確認点](https://solederlego8-a11y.github.io/uranai-app/blog/shinshitsu-fusui-makura-weighted-blanket-hana.html)
- [華の会メールに登録する前に確認したいこと：年齢条件・女性無料・年齢確認と詐欺への注意](https://solederlego8-a11y.github.io/uranai-app/blog/hana-no-kai-mail-touroku-mae-kakunin.html)
- [風水の資格は通信講座で取れる？SARAスクールと諒設計アーキテクトラーニングの選び方と申し込み前の確認点](https://solederlego8-a11y.github.io/uranai-app/blog/fusui-shikaku-tsushin-kouza-hikaku.html)
- [ココナラ電話占いの初回クーポンは何分使える？専用バナーの条件・通話料・後払いの注意点](https://solederlego8-a11y.github.io/uranai-app/blog/coconala-denwa-uranai-hatsukai-coupon-nanpun.html)
- [占いのあとにお金を使う前に｜目的別の選び方と判断フロー表](https://solederlego8-a11y.github.io/uranai-app/blog/uranai-kekka-kodo-erabikata-hub.html)
- [国内旅行はツアーか個人手配か｜判断基準と取消料の確認点](https://solederlego8-a11y.github.io/uranai-app/blog/kokunai-tour-kojin-tehai-dochira.html)
- [写真入り年賀状2027は早割で頼むべき？注文前の判断基準5つ](https://solederlego8-a11y.github.io/uranai-app/blog/nengajo-2027-shashin-hayawari-kazoku.html)
- [神戸のレストランクルーズは記念日向き？予約前の確認点5つ](https://solederlego8-a11y.github.io/uranai-app/blog/kobe-dinner-cruise-kinenbi-yoyaku-mae.html)
- [結婚祝いと内祝いの予算はいくら？のし・配送の確認点](https://solederlego8-a11y.github.io/uranai-app/blog/kekkon-iwai-uchiiwai-yosan-noshi.html)
- [ココナラ占いのキャンセル・返金は？当たらない・違うと感じたときの確認点](https://solederlego8-a11y.github.io/uranai-app/blog/coconala-uranai-cancel-henkin-atanaranai.html)
- [高島易断の暦はいつ買う？どこで買う？令和九年版がいらない人の判断基準](https://solederlego8-a11y.github.io/uranai-app/blog/takashima-ekidan-koyomi-itsu-doko-iranai.html)
- [ココナラ占いは匿名で相談できる？生年月日や本名を伝える前の確認点](https://solederlego8-a11y.github.io/uranai-app/blog/coconala-uranai-tokumei-kojin-joho.html)
- [高島易断の暦はKindleと紙どっち？令和九年版の選び方と確認点](https://solederlego8-a11y.github.io/uranai-app/blog/takashima-ekidan-koyomi-kindle-kami-dochira.html)
- [ライダー版とウェイト版のタロットは違う？名前の由来と選び方](https://solederlego8-a11y.github.io/uranai-app/blog/tarot-rider-waite-han-chigai-namae.html)
- [ココナラ占いの返信が来ないとき何日待つ？キャンセルできる条件と手順](https://solederlego8-a11y.github.io/uranai-app/blog/coconala-uranai-henshin-konai-nannichi.html)
- [タロットカード初心者は22枚と78枚どっち？買う前の確認点と選び方](https://solederlego8-a11y.github.io/uranai-app/blog/tarot-22mai-78mai-shoshinsha-dochira.html)
- [無料占いの鑑定士からのメッセージが止まらない時は？やめ方と相談先](https://solederlego8-a11y.github.io/uranai-app/blog/muryo-uranai-kanteishi-message-yamerarenai.html)
- [タロットカードの日本語解説書はどれ？付属本で確認する4点と比較表](https://solederlego8-a11y.github.io/uranai-app/blog/tarot-kaisetsusho-nihongo-dore.html)
- [ココナラ占いの支払い方法は？クレジットカード明細の表記と購入後に確認できること](https://solederlego8-a11y.github.io/uranai-app/blog/coconala-uranai-shiharai-card-meisai.html)
- [タロットカードの浄化は必要？新品でしない場合と傷めない方法の比較表](https://solederlego8-a11y.github.io/uranai-app/blog/tarot-card-jouka-hitsuyou-shinpin.html)
- [ココナラ占いの追加質問は追加料金がかかる？有料オプション・おひねりの確認点](https://solederlego8-a11y.github.io/uranai-app/blog/coconala-uranai-tsuika-shitsumon-ryokin.html)
- [ココナラ電話占いで電話番号は相手に伝わる？アプリ通話と電話通話の違い](https://solederlego8-a11y.github.io/uranai-app/blog/coconala-denwa-uranai-denwabango-tsutawaru.html)
- [タロットの逆位置は使わなくていい？正位置だけで読む場合の考え方と注意点](https://solederlego8-a11y.github.io/uranai-app/blog/tarot-gyakuichi-tsukawanai-seiichi-dake.html)
- [タロットで同じカードが何度も出る？引き直しの考え方を8ページで比較](https://solederlego8-a11y.github.io/uranai-app/blog/tarot-onaji-card-nandomo-deru-hikinaoshi.html)
- [ココナラ占いで評価しないとどうなる？任意か・期限10日・公開の仕組み](https://solederlego8-a11y.github.io/uranai-app/blog/coconala-uranai-hyouka-shinai-dounaru.html)

### en
- [Today's Fortune | Combine 11 Divination Systems in One Reading](https://solederlego8-a11y.github.io/uranai-app/en/)
- [About This Site | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/about.html)
- [Privacy Policy | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/privacy.html)
- [Contact / Operator Info | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/contact.html)
- [Divination Guides | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/guides.html)
- [What Is BaZi (Four Pillars of Destiny)? Reading Your Chart from Birth Data | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/guides/shichu-suimei.html)
- [Western Astrology 101: Sun Sign, Moon Sign and Ascendant | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/guides/seiyo-uranai.html)
- [The Five Grids of Japanese Name Analysis: Heaven, Personality, Earth, Outer and Total | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/guides/seimei.html)
- [Nine Star Ki: Finding Your Birth Star, from One White Water to Nine Purple Fire | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/guides/kyusei-kigaku.html)
- [What Is Zi Wei Dou Shu? Reading Your Chart Through the Life Palace and 14 Main Stars | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/guides/shibi-tosuu.html)
- [Tenchusatsu in Sanmei-gaku: Reading the Body Star Chart and the Void Periods | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/guides/sanmei.html)
- [The Life Path Number in Numerology: How It's Calculated, and What 11, 22 and 33 Mean | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/guides/suuhi.html)
- [The 27 Lunar Mansions of Sukuyo Astrology: Your Birth Mansion and Its Relationships | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/guides/shukuyo.html)
- [What Is Your KIN Number? The 20 Glyphs and 13 Galactic Tones of the Mayan Calendar | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/guides/maya.html)
- [What Is Vedic Astrology (Jyotish)? The Ayanamsa and the 27 Nakshatras | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/guides/india-uranai.html)
- [What Is Tibetan Astrology? Reading Fate Through Element, Mewa and Parkha | Today's Fortune](https://solederlego8-a11y.github.io/uranai-app/en/guides/tibet.html)

### guides
- [四柱推命とは｜生年月日時から命式を立てる東洋占術の基本](https://solederlego8-a11y.github.io/uranai-app/guides/shichu-suimei.html)
- [西洋占星術とは｜太陽星座・月星座・アセンダントの違い](https://solederlego8-a11y.github.io/uranai-app/guides/seiyo-uranai.html)
- [姓名判断の五格とは｜天格・人格・地格・外格・総格の読み方](https://solederlego8-a11y.github.io/uranai-app/guides/seimei.html)
- [九星気学の本命星とは｜一白水星から九紫火星までの調べ方](https://solederlego8-a11y.github.io/uranai-app/guides/kyusei-kigaku.html)
- [紫微斗数とは｜命宮と14主星で読む中国の占星術](https://solederlego8-a11y.github.io/uranai-app/guides/shibi-tosuu.html)
- [算命学の天中殺とは｜人体星図と空亡の読み方](https://solederlego8-a11y.github.io/uranai-app/guides/sanmei.html)
- [数秘術のライフパスナンバーとは｜計算方法と11・22・33の意味](https://solederlego8-a11y.github.io/uranai-app/guides/suuhi.html)
- [宿曜占星術の27宿とは｜本命宿と相性の読み方](https://solederlego8-a11y.github.io/uranai-app/guides/shukuyo.html)
- [マヤ暦占いのKINとは｜20の紋章と13の銀河の音](https://solederlego8-a11y.github.io/uranai-app/guides/maya.html)
- [インド占星術（ジョーティシュ）とは｜アヤナムシャと27ナクシャトラ](https://solederlego8-a11y.github.io/uranai-app/guides/india-uranai.html)
- [チベット占星術とは｜五大元素・メワ・パルカで読む運命](https://solederlego8-a11y.github.io/uranai-app/guides/tibet.html)

<!-- article-index:end -->
