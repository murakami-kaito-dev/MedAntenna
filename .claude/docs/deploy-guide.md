# デプロイ手順(ユーザー向け)

ホスティング: **Cloudflare Workers(静的アセット配信・無料・サーバーレス関数あり)**。
リポジトリは GitHub(`murakami-kaito-dev/MedAntenna`・public)。**git push = 自動デプロイ**。

## 【確定した設定】(2026-08-27 初回デプロイ完了・確認済み)

| 項目 | 値 |
|---|---|
| 作成フロー | 統合フロー(Workers Builds) |
| Project name | `medantenna` |
| 公開URL | **https://medantenna.km-solo-developer.workers.dev** |
| Build command | (空欄) |
| Deploy command | `npx wrangler deploy` |
| API token | 「Create new token」で自動生成(CF側保持) |
| Variables | なし |
| 配信構成 | `wrangler.jsonc` + `worker/index.js`(静的アセット + `/api/health`) |
| 公開除外 | `.assetsignore`(`.claude/` `docs/` `tools/` `worker/` 等) |
| 計測 | **Web Analytics beacon は入れない**(iOSアプリの App Privacy「データ収集なし」維持のため) |

## 2回目以降のデプロイ

不要。`main` に push するだけで自動反映(毎朝の定期更新エージェントがこれを行う)。

## 動作確認

- サイト表示: https://medantenna.km-solo-developer.workers.dev
- ヘルスチェック: `/api/health` が `{"status":"ok","service":"MedAntenna",...}` を返せばOK
