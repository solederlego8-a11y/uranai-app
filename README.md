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
