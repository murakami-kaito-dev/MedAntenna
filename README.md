# MedAntenna — 医療・放射線のいまを受信する

放射線技師を目指す学生・若手技師のための医療・放射線ニュースキュレーション。
毎朝6時(JST)に自動更新。Cloudflare Workers で配信(git push = 自動デプロイ)。

- 構成: 静的シェル(index.html / js / css) + `content/*.json`(データ) + 最小Worker(`/api/health`)
- ニュース生成: Claude Code のスケジュール済みクラウドエージェント(毎朝の無人実行)
- 姉妹アプリ: iOS「MRIの勉強ドリル」/ 姉妹サイト: ANTENNA(AIニュース)

内部ドキュメントは `.claude/docs/`(配信除外)。リリース記録は `docs/release-log.md`。
