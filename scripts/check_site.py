#!/usr/bin/env python3
"""Site / SEO invariants for the built docs/ directory.

This script runs after `bundle exec jekyll build` and enforces:
  - every indexable *.html has <title>, <meta description>, <link canonical>,
    <meta og:*>, <meta twitter:card>, and an Article/AboutPage JSON-LD block
    with datePublished + dateModified;
  - no internal link points at a missing file;
  - sitemap.xml is well-formed XML with >= N <loc> entries and carries <lastmod>;
  - robots.txt renders without Liquid residue and declares the sitemap URL;
  - llms.txt exists and lists the handbook's core pages;
  - homepage carries the expected section anchors.

Exits non-zero on any violation. Run from repo root:
    python3 scripts/check_site.py
"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "docs"
HOME_FILE = SITE_DIR / "index.html"

# Pages that are intentionally lightweight on SEO (e.g. 404) and don't need
# the full JSON-LD / OG payload. Keep this list minimal and documented.
SEO_EXEMPT = {"404.html"}

REQUIRED_HOME_SNIPPETS = [
    "USDT 新手手册",
    "2. 常用外部 App 与工具",
    "4. 最近更新",
    "USDT 不同链转账手续费对比",
]

FORBIDDEN_HOME_SNIPPETS = [
    "reading-path.svg",
    "<strong>目录</strong>",
    "2. 新手常用工具",
]

# H2 headings whose sections are link directories / FAQ / navigation lists /
# closing recaps. Matched case-insensitively against the H2's visible text.
H2_SKIP_PATTERNS = (
    "参考资料", "相关页面", "延伸阅读", "官方入口", "官方参考",
    "核过的资料", "我核过的", "写这篇时我核过",
    "和手册其他章节的关系", "上一篇", "下一篇",
    "返回", "下一步", "更新记录", "changelog", "faq", "常见问题",
    "我的建议", "我的下一步", "一句更现实的建议", "一句总结",
    "最后的建议", "结尾", "补一句",
    "browse another task", "browse another",
)

# Matcher for every <h2 ...>...</h2> and what directly follows.
H2_BLOCK_RE = re.compile(
    r'<h2\b([^>]*)>(.*?)</h2>(.*?)(?=<h2\b|<footer\b|</main\b|</body\b)',
    re.IGNORECASE | re.DOTALL,
)
TAG_STRIP_RE = re.compile(r"<[^>]+>")

CANONICAL_RE = re.compile(
    r'<link\s+rel="canonical"\s+href="([^"]+)"', re.IGNORECASE
)
OG_PROP_RE = re.compile(
    r'<meta\s+property="og:([a-z_:]+)"\s+content="([^"]*)"', re.IGNORECASE
)
TWITTER_RE = re.compile(
    r'<meta\s+name="twitter:([a-z_]+)"\s+content="([^"]*)"', re.IGNORECASE
)
JSONLD_RE = re.compile(
    r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)
LIQUID_RESIDUE_RE = re.compile(r"{{\s*[^}]+}}|{%\s*[^%]+%}")


class LinksAndMetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.title_found = False
        self.meta_description_found = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        elif tag == "title":
            self.title_found = True
        elif (
            tag == "meta"
            and attrs.get("name", "").lower() == "description"
            and attrs.get("content", "").strip()
        ):
            self.meta_description_found = True


def required_og_keys():
    return {"type", "title", "description", "url", "image", "site_name"}


def required_twitter_keys():
    return {"card", "title", "description", "image"}


def check_h2_definition_leads(path: Path, raw: str, issues: list):
    """Every content H2 must open with a definition-first lead paragraph.

    Pattern: the first element after </h2> is either
      (a) <p>...<strong>...</strong>...</p>  -- the definition lead, or
      (b) a block structure that IS the answer: <table>, <ul>, <ol>, <nav>,
          <figure>, <pre>, <dl>, <div class="note">, <div class="risk"> -- where
          a lead paragraph would be redundant.

    H2s whose visible text matches H2_SKIP_PATTERNS (link directories, FAQ,
    closing advice, navigation) are exempt.
    """
    name = path.name
    for attrs, h2_inner, body in H2_BLOCK_RE.findall(raw):
        visible = TAG_STRIP_RE.sub("", h2_inner).strip().lower()
        if any(p in visible for p in H2_SKIP_PATTERNS):
            continue
        # Locate the first non-whitespace element after the H2.
        tail = body.lstrip()
        if not tail:
            issues.append(
                f"{name}: H2 '{h2_inner.strip()}' has no following content"
            )
            continue
        # Accept block structures that are self-explanatory without a lead.
        if re.match(
            r'<(?:table|ul|ol|nav|figure|pre|dl|blockquote)\b',
            tail, re.IGNORECASE,
        ):
            continue
        if re.match(
            r'<div\s+class="(?:note|risk|doc-shot|toc)\b',
            tail, re.IGNORECASE,
        ):
            continue
        # Otherwise the first element must be a <p> with a <strong> inside
        # (the definition-first lead).
        first_p = re.match(
            r'<p\b[^>]*>(.*?)</p>', tail, re.DOTALL | re.IGNORECASE,
        )
        if not first_p:
            issues.append(
                f"{name}: H2 '{h2_inner.strip()}' is not followed by a <p> "
                "or a structural block"
            )
            continue
        p_body = first_p.group(1)
        if "<strong" not in p_body.lower():
            issues.append(
                f"{name}: H2 '{h2_inner.strip()}' first <p> has no "
                "<strong> lead term (definition-first pattern missing)"
            )


def check_html_file(path: Path, issues: list):
    name = path.name
    raw = path.read_text(encoding="utf-8")

    parser = LinksAndMetaParser()
    parser.feed(raw)

    if not parser.title_found:
        issues.append(f"{name}: missing <title>")
    if not parser.meta_description_found:
        issues.append(f"{name}: missing <meta name=description>")

    if name in SEO_EXEMPT:
        return parser.links  # skip the rest

    # Canonical
    m = CANONICAL_RE.search(raw)
    if not m:
        issues.append(f"{name}: missing <link rel=canonical>")
    else:
        canonical = m.group(1)
        if not canonical.startswith("https://"):
            issues.append(f"{name}: canonical is not https ({canonical})")

    # Open Graph coverage
    og = {k: v for k, v in OG_PROP_RE.findall(raw)}
    missing_og = required_og_keys() - set(og.keys())
    if missing_og:
        issues.append(f"{name}: missing og:{{{', '.join(sorted(missing_og))}}}")

    # Twitter card coverage
    tw = {k: v for k, v in TWITTER_RE.findall(raw)}
    missing_tw = required_twitter_keys() - set(tw.keys())
    if missing_tw:
        issues.append(
            f"{name}: missing twitter:{{{', '.join(sorted(missing_tw))}}}"
        )

    # JSON-LD must exist and include datePublished + dateModified on Article/AboutPage
    jsonld_blocks = JSONLD_RE.findall(raw)
    if not jsonld_blocks:
        issues.append(f"{name}: no JSON-LD block")
    else:
        joined = "\n".join(jsonld_blocks)
        if '"@type": "Article"' in joined or '"@type":"Article"' in joined:
            for key in ("datePublished", "dateModified"):
                if key not in joined:
                    issues.append(f"{name}: Article JSON-LD missing {key}")
        # Every page should reference at least one of Article / AboutPage / WebSite
        if not any(
            kind in joined
            for kind in ('"Article"', '"AboutPage"', '"WebSite"')
        ):
            issues.append(
                f"{name}: JSON-LD has no Article/AboutPage/WebSite node"
            )

    # No unrendered Liquid in output
    if LIQUID_RESIDUE_RE.search(raw):
        issues.append(f"{name}: contains unrendered Liquid residue")

    # BreadcrumbList on every non-home Article/AboutPage (layout default catches
    # these; this invariant catches regressions if someone removes the default
    # branch or changes page_type routing).
    if name not in {"index.html", "404.html"}:
        if '"BreadcrumbList"' not in "\n".join(jsonld_blocks or []):
            issues.append(
                f"{name}: JSON-LD missing BreadcrumbList (Google SERP chip loss)"
            )

    # WebApplication schema on interactive tool pages.
    # Detected by filename convention (pages with `tool: true` frontmatter are
    # the ones named *-calculator.html / *-comparison.html AND have a
    # data-*-tool div). Keep the list explicit so typos are caught.
    TOOL_PAGES = {"usdt-gas-fee-comparison.html", "tron-energy-calculator.html"}
    if name in TOOL_PAGES:
        if '"WebApplication"' not in "\n".join(jsonld_blocks or []):
            issues.append(
                f"{name}: tool page missing WebApplication JSON-LD node"
            )
        if "<noscript" not in raw.lower():
            issues.append(
                f"{name}: tool page missing <noscript> fallback "
                "(AI crawlers + JS-disabled users see empty widgets)"
            )

    # <img> tags must carry width + height to prevent CLS.
    for m in re.finditer(r"<img\b([^>]*)>", raw, re.IGNORECASE):
        attrs_str = m.group(1).lower()
        if " width=" not in attrs_str or " height=" not in attrs_str:
            # Find a readable snippet for the error
            snippet = m.group(0)[:90].replace("\n", " ")
            issues.append(
                f"{name}: <img> missing width/height attrs (CLS risk): {snippet}..."
            )

    # H2 definition-first leads (only on content articles).
    # Skip trust / index / meta pages that use H2s structurally, not as article
    # sections requiring snippet-extractable leads.
    H2_LEAD_EXEMPT = {
        "index.html", "404.html", "about.html",
        "editorial-policy.html", "how-we-review-wallets-and-apps.html",
        "changelog.html", "official-sources.html", "start-here.html",
    }
    if name not in H2_LEAD_EXEMPT:
        check_h2_definition_leads(path, raw, issues)

    return parser.links


def resolve_internal_link(href: str) -> Optional[str]:
    if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
        return None
    target = href.split("#", 1)[0]
    if not target:
        return None
    if target.startswith("./"):
        target = target[2:]
    if target.startswith("/"):
        target = target[1:]
        if target.startswith("usdthub/"):
            target = target[len("usdthub/"):]
    return target


def check_sitemap(issues: list, expected_min: int = 25):
    path = SITE_DIR / "sitemap.xml"
    if not path.exists():
        issues.append("sitemap.xml: missing")
        return
    text = path.read_text(encoding="utf-8")
    if "<!DOCTYPE html" in text.lower():
        issues.append("sitemap.xml: HTML wrapper leaked into sitemap")
        return
    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        issues.append(f"sitemap.xml: invalid XML ({e})")
        return
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = root.findall(f"{ns}url")
    if len(urls) < expected_min:
        issues.append(
            f"sitemap.xml: only {len(urls)} <url> entries (expected >= {expected_min})"
        )
    missing_lastmod = [
        u.find(f"{ns}loc").text
        for u in urls
        if u.find(f"{ns}lastmod") is None
    ]
    if missing_lastmod:
        issues.append(
            f"sitemap.xml: {len(missing_lastmod)} URL(s) missing <lastmod>"
        )


def check_robots(issues: list):
    path = SITE_DIR / "robots.txt"
    if not path.exists():
        issues.append("robots.txt: missing")
        return
    text = path.read_text(encoding="utf-8")
    if LIQUID_RESIDUE_RE.search(text):
        issues.append("robots.txt: unrendered Liquid residue")
    if "Sitemap:" not in text:
        issues.append("robots.txt: no Sitemap: declaration")
    if "GPTBot" not in text or "Google-Extended" not in text:
        issues.append(
            "robots.txt: missing explicit AI bot directives (GPTBot, Google-Extended)"
        )


def check_energy_ratio_consistency(issues: list):
    """TRX -> Energy conversion rate must not drift between pages.

    History: a prior audit caught one page using the pre-Stake-2.0 "1 TRX ~= 26
    Energy/day" folklore (implying "2,500 TRX ~= 65,000 Energy/day") while the
    tool pages had moved to the current trongrid snapshot "1 TRX ~= 9.206
    Energy/day". Readers following the old number would under-stake by ~3x —
    real money miscalculation. This check scans for the legacy pattern and
    requires any mention to be clearly flagged as historical, not current.
    """
    legacy_pattern = re.compile(
        r"2[,，]?500\s*TRX[^\n<]{0,40}(?:65[,，]?000|6\.5\s*万|65k)\s*(?:Energy|能量)[^\n<]{0,20}(?:/\s*天|每?天)",
        re.IGNORECASE,
    )
    historical_marker = re.compile(
        r"(?:历史口径|旧口径|旧(?:的)?(?:粗)?估值|旧网络快照|"
        r"pre[- ]?Stake|Stake\s*1\.0|已不够|不再是|historical|"
        r"已经站不住|站不住|2023 年前后|"
        r"必须紧跟|必须紧随|required to be flagged)",
        re.IGNORECASE,
    )
    for path in sorted(SITE_DIR.glob("*.html")):
        raw = path.read_text(encoding="utf-8")
        for m in legacy_pattern.finditer(raw):
            # Window: 400 chars around the match (needs to mention it's historical)
            lo = max(0, m.start() - 200)
            hi = min(len(raw), m.end() + 200)
            window = raw[lo:hi]
            if not historical_marker.search(window):
                issues.append(
                    f"{path.name}: legacy '2,500 TRX ≈ 65k Energy/day' ratio "
                    "appears without 'historical / 旧口径' context — "
                    "current snapshot is 9.206 E/TRX, legacy was ~26 E/TRX"
                )


def check_llms_txt(issues: list):
    path = SITE_DIR / "llms.txt"
    if not path.exists():
        issues.append("llms.txt: missing")
        return
    text = path.read_text(encoding="utf-8")
    # Should list core pages for LLM discovery.
    required_entries = [
        "/what-is-usdt.html",
        "/how-to-buy-usdt.html",
        "/about.html",
        "/editorial-policy.html",
    ]
    for entry in required_entries:
        if entry not in text:
            issues.append(f"llms.txt: missing link to {entry}")


def check_homepage(issues: list):
    if not HOME_FILE.exists():
        issues.append(f"homepage: missing {HOME_FILE.name}")
        return
    html = HOME_FILE.read_text(encoding="utf-8")
    for snippet in REQUIRED_HOME_SNIPPETS:
        if snippet not in html:
            issues.append(f"homepage: missing required snippet: {snippet}")
    for snippet in FORBIDDEN_HOME_SNIPPETS:
        if snippet in html:
            issues.append(f"homepage: contains forbidden snippet: {snippet}")


def main() -> int:
    if not SITE_DIR.exists():
        print(f"missing site directory: {SITE_DIR}")
        return 1

    html_files = sorted(SITE_DIR.glob("*.html"))
    if not html_files:
        print("no HTML files found in docs/")
        return 1

    issues = []
    missing_links = []

    for f in html_files:
        links = check_html_file(f, issues)
        for href in links or []:
            target = resolve_internal_link(href)
            if target is None:
                continue
            if not (SITE_DIR / target).exists():
                missing_links.append(f"{f.name} -> {href}")

    check_sitemap(issues)
    check_robots(issues)
    check_llms_txt(issues)
    check_homepage(issues)
    check_energy_ratio_consistency(issues)

    if missing_links:
        print("Missing internal links:")
        for item in missing_links:
            print(f"- {item}")
    if issues:
        print("SEO / structural issues:")
        for item in issues:
            print(f"- {item}")

    if missing_links or issues:
        return 1

    print(
        f"OK: {len(html_files)} pages pass title + description + canonical + OG + "
        "Twitter + JSON-LD + internal-link checks; sitemap.xml valid with lastmod; "
        "robots.txt + llms.txt present; homepage structure matches expectations."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
