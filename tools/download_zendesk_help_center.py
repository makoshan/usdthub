#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import re
import sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests


USER_AGENT = "Mozilla/5.0 (compatible; ZendeskHelpCenterDownloader/1.0)"
TIMEOUT = 30


class ImgSrcParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images: List[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "img":
            return
        attrs = dict(attrs)
        src = attrs.get("src")
        if src:
            self.images.append(src)


TAG_RE = re.compile(r"<[^>]+>")
SECTION_RE = re.compile(r"/sections/(\d+)")
ARTICLE_RE = re.compile(r"/articles/(\d+)")


def slugify(text: str) -> str:
    text = unescape(text).strip().lower()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^a-z0-9\-\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "article"


def strip_tags(html: str) -> str:
    text = TAG_RE.sub(" ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return unescape(text)


def safe_filename_from_url(url: str) -> str:
    parsed = urlparse(url)
    name = os.path.basename(parsed.path) or "asset"
    name = re.sub(r"[^a-zA-Z0-9._-]", "_", name)
    return name


def ensure_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def fetch_json(session: requests.Session, url: str) -> Dict:
    r = session.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def section_api_url(section_url: str) -> str:
    m = SECTION_RE.search(section_url)
    if not m:
        raise ValueError(f"Cannot find section id in URL: {section_url}")
    parsed = urlparse(section_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    return f"{base}/api/v2/help_center/sections/{m.group(1)}/articles.json"


def article_api_url(article_url: str) -> str:
    m = ARTICLE_RE.search(article_url)
    if not m:
        raise ValueError(f"Cannot find article id in URL: {article_url}")
    parsed = urlparse(article_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    lang_match = re.search(r"/hc/([^/]+)/articles/", article_url)
    if lang_match:
        lang = lang_match.group(1)
        return f"{base}/api/v2/help_center/{lang}/articles/{m.group(1)}.json"
    return f"{base}/api/v2/help_center/articles/{m.group(1)}.json"


def list_articles_from_section(session: requests.Session, section_url: str) -> List[Dict]:
    api = section_api_url(section_url)
    data = fetch_json(session, api)
    return data.get("articles", [])


def get_article(session: requests.Session, article_url: str) -> Dict:
    api = article_api_url(article_url)
    data = fetch_json(session, api)
    return data.get("article", data)


def download_file(session: requests.Session, url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with session.get(url, timeout=TIMEOUT, stream=True) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
    return dest


def localize_images(session: requests.Session, article_html: str, base_url: str, image_dir: Path) -> Dict:
    parser = ImgSrcParser()
    parser.feed(article_html)
    mapping = {}
    for src in parser.images:
        absolute = urljoin(base_url, src)
        filename = safe_filename_from_url(absolute)
        unique = hashlib.sha1(absolute.encode("utf-8")).hexdigest()[:8]
        final_name = f"{unique}-{filename}"
        local_path = image_dir / final_name
        try:
            download_file(session, absolute, local_path)
            mapping[src] = f"images/{final_name}"
            if absolute != src:
                mapping[absolute] = f"images/{final_name}"
        except Exception as e:
            mapping[src] = None
            if absolute != src:
                mapping[absolute] = None
            print(f"WARN: failed to download image {absolute}: {e}", file=sys.stderr)
    localized_html = article_html
    for old, new in mapping.items():
        if new:
            localized_html = localized_html.replace(old, new)
    return {
        "html": localized_html,
        "images": [
            {"source": src, "local": local}
            for src, local in mapping.items()
            if local and src == next(iter([src]))
        ],
        "mapping": mapping,
    }


def save_article(article: Dict, out_dir: Path, session: requests.Session) -> Dict:
    title = article.get("title") or f"article-{article.get('id')}"
    slug = slugify(title)
    article_dir = out_dir / slug
    images_dir = article_dir / "images"
    article_dir.mkdir(parents=True, exist_ok=True)

    body = article.get("body") or ""
    html_url = article.get("html_url") or ""
    localized = localize_images(session, body, html_url, images_dir)
    clean_text = strip_tags(body)

    meta = {
        "id": article.get("id"),
        "title": title,
        "html_url": html_url,
        "api_url": article.get("url"),
        "author_id": article.get("author_id"),
        "created_at": article.get("created_at"),
        "updated_at": article.get("updated_at"),
        "draft": article.get("draft"),
        "promoted": article.get("promoted"),
        "position": article.get("position"),
        "label_names": article.get("label_names") or [],
        "images_downloaded": [item for item in localized["mapping"].values() if item],
    }

    (article_dir / "article.html").write_text(localized["html"], encoding="utf-8")
    (article_dir / "article.txt").write_text(clean_text + "\n", encoding="utf-8")
    (article_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "slug": slug,
        "title": title,
        "article_dir": str(article_dir),
        "html_url": html_url,
        "images": meta["images_downloaded"],
    }


def build_markdown_index(section_title: str, items: List[Dict], out_dir: Path):
    lines = [
        f"# {section_title}",
        "",
        "这个目录由 Zendesk Help Center 导出生成。",
        "",
        "## 文章",
        "",
    ]
    for item in items:
        slug = item["slug"]
        lines.append(f"- [{item['title']}](./{slug}/meta.json)")
        lines.append(f"  - HTML: `./{slug}/article.html`")
        lines.append(f"  - Text: `./{slug}/article.txt`")
        if item["images"]:
            lines.append(f"  - Images: `{len(item['images'])}` files")
    lines.append("")
    (out_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Download Zendesk Help Center section/article content and images")
    parser.add_argument("url", help="Zendesk section URL or article URL")
    parser.add_argument("--output", default="vendor/zendesk-download", help="Output directory relative to current working directory")
    parser.add_argument("--section-title", default="Zendesk Export", help="Title for generated README index")
    args = parser.parse_args()

    session = ensure_session()
    out_dir = Path(args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []
    if "/sections/" in args.url:
        articles = list_articles_from_section(session, args.url)
        for summary in articles:
            full = get_article(session, summary.get("html_url") or summary.get("url"))
            results.append(save_article(full, out_dir, session))
    elif "/articles/" in args.url:
        article = get_article(session, args.url)
        results.append(save_article(article, out_dir, session))
    else:
        raise SystemExit("URL must be a Zendesk section or article URL")

    manifest = {
        "source_url": args.url,
        "count": len(results),
        "items": results,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    build_markdown_index(args.section_title, results, out_dir)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
