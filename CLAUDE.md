# MedAntenna — プロジェクトルール・情報の地図

放射線技師を志す学生・若手技師(〜2,3年目)のための、医療・放射線ニュースの
キュレーションPWA。ANTENNA(~/Dev/Products/AiNewsCurator)のアーキテクチャを移植した姉妹サイト。
ホスティング: **Cloudflare Workers(静的アセット配信)**。リポジトリは GitHub(public)。
公開URL: **https://medantenna.km-solo-developer.workers.dev**

## これは何か
- 静的サイト(ビルドステップなし)+ PWA。全パス相対指定なのでホスト非依存。**git push = 自動デプロイ**。
- Cloudflare は統合フロー(Workers Builds)で Git連携。`wrangler.jsonc`(静的アセット + `main`)で配信し、
  `worker/index.js` にサーバー側処理(`/api/health` のみ)。内部ファイルは `.assetsignore` で公開除外。
- **シェル(HTML/CSS/JS)とコンテンツ(`content/` 配下のJSON)を分離**。
  定期更新ではコンテンツJSONだけを触り、シェルは原則触らない。
- 毎朝 6:00 JST にスケジュール済みクラウドエージェントが自律更新
  (リサーチ → JSON更新 → 検証 → commit/push)。
- セクション: ニュース(trends) / 用語辞典(glossary) / このサイトについて(about)。
  `content/site.json` がナビの正。
- iOSアプリ「MRIの勉強ドリル」(~/Dev/Products/mri_study)の「ニュース」タブから
  WebView で読まれる(v2.0.0 以降)。**Cloudflare Web Analytics 等の計測ビーコンを入れない**
  (アプリの App Privacy「データ収集なし」を維持するため。アクセス把握は Workers のリクエスト数で行う)。

## 読者・編集方針(不変)
- 読者は「技師1年目基準」: 放射線技師を志す学生〜2,3年目が読み切れば理解できる書き方。
- 各号の記事の**半分以上は放射線技術・放射線技師に直接関わる話題**
  (モダリティ・撮像・被ばく・技師制度・放射線系学会等)。医療一般は半分以下。
- **医療ガードレール**(content-guide.md が正): 診療助言をしない / source は一次情報源のみ /
  研究の限界(査読前・小規模等)を明記 / 誇張・断定禁止 / 未承認・適応外を推奨と読める書き方をしない /
  患者が特定される記述をしない。

## 情報の地図
- **コンテンツ様式ガイド: `.claude/docs/content-guide.md`**(スキーマ・文体・用語ルールの正)
- 定期更新の実行手順: `.claude/docs/update-runbook.md`
- デプロイ手順: `.claude/docs/deploy-guide.md` / 定期ルーチン設定の写し: `.claude/docs/routine-config.json`
- **リリースログ: `docs/release-log.md`**(`.claude/` の外。理由は「不変条件・禁忌」を参照)
- 検証スクリプト: `tools/validate.py`(JSON構文・リンク整合・category enum・source URL を一括検査)
- コンテンツ: `content/site.json`(ナビ) / `content/trends.json`(号アーカイブ) /
  `content/glossary.json`(用語辞典) / `content/pages/about/*.json`(about・免責)

## 不変条件・禁忌(ANTENNAの運用事故から継承)
- コンテンツ更新時にシェルの構造(ルート、JSONスキーマ)を壊さない。demo ブロックは使わない。
- **専門用語の全数ルール**: 専門用語は説明か `[[glossary:slug|表示]]` リンクなしに登場させない。
- ニュース記事には必ず解説(`explanation`)を添える。日本語のみ。
- サイトの文言に開発経緯・運用都合のメタ表現を書かない。
- push 前に `python3 tools/validate.py` を必ず通す。
- 定期更新の commit/push はユーザーから事前承認済み。それ以外は指示があったときのみ。
- 更新のたび `docs/release-log.md` に記録する。
- **`docs/release-log.md` を `.claude/` 配下に戻さない。** `.claude/**` への書き込みは
  センシティブファイル判定で承認プロンプトが出るため、無人の定期実行が承認待ちで停止する
  (ANTENNAで2026-08-25に実際に発生)。同じ理由で、
  **配信(content の commit/push)を release-log の記録より先に完了させる**(update-runbook §4)。
- `docs/` `tools/` `worker/` `.claude/` `CLAUDE.md` `wrangler.jsonc` は
  **`.assetsignore` に必ず載せる**(載せ忘れると内部メモが公開される)。
