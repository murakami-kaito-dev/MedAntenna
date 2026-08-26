/* MedAntenna service worker
 * 方針: ネットワーク優先・キャッシュフォールバック。
 * コンテンツは毎朝更新されるため、オンライン時は常に最新を取り、
 * オフライン時のみ最後に受信したものを見せる。シェル更新時にこのファイルの
 * 変更は不要(キャッシュはリクエスト単位で上書きされる)。
 */
const CACHE = "medantenna-v1";

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) =>
      c.addAll(["./", "index.html", "css/style.css", "js/app.js", "manifest.webmanifest"])
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    fetch(e.request)
      .then((res) => {
        if (res.ok && new URL(e.request.url).origin === location.origin) {
          const clone = res.clone();
          caches.open(CACHE).then((c) => c.put(e.request, clone));
        }
        return res;
      })
      .catch(() => caches.match(e.request, { ignoreSearch: true }))
  );
});
