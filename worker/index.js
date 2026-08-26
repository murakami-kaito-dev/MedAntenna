// MedAntenna の Worker 本体(Cloudflare Workers 静的アセット構成)。
// 静的ファイル(HTML/CSS/JS/JSON)は Cloudflare が直接配信し、/api/* だけこの Worker が処理する。
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // 動作確認用エンドポイント
    if (url.pathname === "/api/health") {
      return Response.json({
        status: "ok",
        service: "MedAntenna",
        runtime: "cloudflare-workers",
      });
    }

    // それ以外は静的アセットにフォールバック
    return env.ASSETS.fetch(request);
  },
};
