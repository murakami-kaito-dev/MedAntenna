#!/usr/bin/env python3
"""ANTENNA コンテンツ検証 — push前に必ず実行する(update-runbook.md 参照)。
検査: JSON構文 / site.json⇔pages対応 / [[glossary:]]・[[page:]]リンク整合 / demo id実在
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
DEMOS = {"next-token", "attention", "training", "tokenize", "temperature", "neural-params"}
LINK_RE = re.compile(r"\[\[(glossary|page):([a-z0-9/-]+)\|([^\]]+)\]\]")
errors = []


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"JSON構文エラー: {path.relative_to(ROOT)}: {e}")
        return None


def walk_text(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_text(v)
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from walk_text(v)


site = load(CONTENT / "site.json")
glossary = load(CONTENT / "glossary.json")
trends = load(CONTENT / "trends.json")
if site is None or glossary is None or trends is None:
    print("\n".join(errors)); sys.exit(1)

slugs = {t.get("slug") for t in glossary["terms"]}
if None in slugs or "" in slugs:
    errors.append("glossary: slug のないエントリがある")

page_refs = set()
nav_titles = {}
for s in site["sections"]:
    for p in s.get("pages", []):
        page_refs.add(f"{s['id']}/{p['slug']}")
        nav_titles[f"{s['id']}/{p['slug']}"] = p.get("title")
        f = CONTENT / "pages" / s["id"] / f"{p['slug']}.json"
        if not f.exists():
            errors.append(f"site.json に載っているが実体がない: {f.relative_to(ROOT)}")

for f in sorted((CONTENT / "pages").rglob("*.json")):
    rel = f"{f.parent.name}/{f.stem}"
    if rel not in page_refs:
        errors.append(f"実体はあるが site.json に載っていない: {f.relative_to(ROOT)}")
    data = load(f)
    if data is None:
        continue
    for key in ("title", "lede", "updated", "blocks"):
        if key not in data:
            errors.append(f"{f.relative_to(ROOT)}: 必須キー {key} がない")
    # ナビ(site.json)のタイトルとページ本体のタイトルの不一致を検出
    nav_title = nav_titles.get(rel)
    if nav_title is not None and data.get("title") and nav_title != data["title"]:
        errors.append(
            f"{f.relative_to(ROOT)}: site.json のタイトルと不一致 "
            f"(nav='{nav_title}' / page='{data['title']}')")
    for b in data.get("blocks", []):
        if b.get("type") == "demo" and b.get("id") not in DEMOS:
            errors.append(f"{f.relative_to(ROOT)}: 不明な demo id {b.get('id')}")
        # リンク記法が展開されない場所にリンクを書いていないか
        # (h2/title はシェルが素のテキストとして描画するため、記法がそのまま画面に出てしまう)
        if b.get("type") == "h2" and LINK_RE.search(b.get("text", "")):
            errors.append(
                f"{f.relative_to(ROOT)}: h2見出しにリンク記法は使えない(画面にそのまま出る)。"
                f"見出しはプレーンにし、本文でリンクすること: {b['text'][:40]}")
        if b.get("type") == "flow":
            for row in b.get("rows", []):
                for st in row.get("steps", []):
                    txt = st if isinstance(st, str) else st.get("text", "")
                    if LINK_RE.search(txt):
                        errors.append(
                            f"{f.relative_to(ROOT)}: flowのstepsにリンク記法は使えない。"
                            f"exampleに書くこと: {txt[:40]}")
    if LINK_RE.search(data.get("title", "")):
        errors.append(f"{f.relative_to(ROOT)}: title にリンク記法は使えない")
    for text in walk_text(data):
        for kind, target, _label in LINK_RE.findall(text):
            if kind == "glossary" and target not in slugs:
                errors.append(f"{f.relative_to(ROOT)}: 存在しない用語リンク [[glossary:{target}]]")
            if kind == "page" and target not in page_refs:
                errors.append(f"{f.relative_to(ROOT)}: 存在しないページリンク [[page:{target}]]")

for t in glossary["terms"]:
    for r in t.get("related", []):
        if r not in slugs:
            errors.append(f"glossary[{t.get('slug')}]: related に存在しないslug {r}")
    for kind, target, _ in LINK_RE.findall(t.get("definition", "") + t.get("context", "")):
        if kind == "glossary" and target not in slugs:
            errors.append(f"glossary[{t.get('slug')}]: 存在しない用語リンク [[glossary:{target}]]")
        if kind == "page" and target not in page_refs:
            errors.append(f"glossary[{t.get('slug')}]: 存在しないページリンク [[page:{target}]]")

versions = [i["version"] for i in trends["issues"]]
if len(versions) != len(set(versions)):
    errors.append("trends: version が重複している")
for i in trends["issues"]:
    for item in i["items"]:
        for key in ("title", "category", "lead", "explanation", "source"):
            if key not in item:
                errors.append(f"trends[{i['version']}]: 記事に {key} がない: {item.get('title', '?')[:20]}")
        if "briefing" in item and not isinstance(item["briefing"], list):
            errors.append(f"trends[{i['version']}]: briefing は配列であること: {item.get('title','?')[:20]}")

if errors:
    print(f"NG: {len(errors)}件")
    print("\n".join(" - " + e for e in errors))
    sys.exit(1)
n_pages = len(list((CONTENT / 'pages').rglob('*.json')))
print(f"OK: pages={n_pages} terms={len(slugs)} issues={len(versions)}")
