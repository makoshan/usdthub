#!/usr/bin/env python3
"""Propagate H2 definition-first lead paragraphs from site/*.html to markdown/*.md.

Why: the Markdown mirrors in `markdown/` are what GitHub readers see. The
definition-first leads live in the HTML source. Without this sync, GitHub readers
see the older prose-first content while AI crawlers see the new leads.

Strategy:
  1. For each site/*.html with a corresponding markdown/*.md:
     a. Parse every <h2 id="..."> + its immediately-following <p><strong>term</strong>...</p>.
     b. Find the matching `## ...` heading in the markdown file by visible-text match
        (tolerant of small wording differences — matches on prefix).
     c. If the paragraph after the ## heading doesn't already start with a **strong**
        term, insert the HTML-derived lead as `**term**: body.` with external links
        preserved.
  2. Never delete existing markdown content — only PREPEND the lead after the heading.
  3. Idempotent: running twice is a no-op.

Usage:
    python3 scripts/sync_md_leads.py           # dry run; prints what would change
    python3 scripts/sync_md_leads.py --write   # actually write
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
MD = ROOT / "markdown"

# <h2 ...>visible text</h2> followed (within whitespace) by <p>...<strong>term</strong>...</p>
H2_LEAD_RE = re.compile(
    r'<h2\b[^>]*>(?P<h2>.*?)</h2>\s*'
    r'<p\b[^>]*>(?P<p>[^<]*<strong>(?P<term>[^<]+)</strong>.*?)</p>',
    re.IGNORECASE | re.DOTALL,
)
TAG_STRIP_RE = re.compile(r"<[^>]+>")
LINK_RE = re.compile(r'<a\b[^>]*\shref="([^"]+)"[^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)
STRONG_RE = re.compile(r'<strong>(.*?)</strong>', re.IGNORECASE | re.DOTALL)
BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)


def html_fragment_to_md(html: str) -> str:
    """Convert a small HTML fragment (inside a <p>) to Markdown."""
    s = html
    s = LINK_RE.sub(lambda m: f"[{TAG_STRIP_RE.sub('', m.group(2))}]({m.group(1)})", s)
    s = STRONG_RE.sub(lambda m: f"**{TAG_STRIP_RE.sub('', m.group(1))}**", s)
    s = BR_RE.sub(" ", s)
    s = TAG_STRIP_RE.sub("", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def h2_text(html: str) -> str:
    return TAG_STRIP_RE.sub("", html).strip()


def extract_leads(html_path: Path) -> list[tuple[str, str]]:
    """Return list of (h2_text, markdown_lead) pairs."""
    raw = html_path.read_text(encoding="utf-8")
    out = []
    for m in H2_LEAD_RE.finditer(raw):
        h2 = h2_text(m.group("h2"))
        md = html_fragment_to_md(m.group("p"))
        if h2 and md:
            out.append((h2, md))
    return out


MD_HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$", re.MULTILINE)


def h2_keys(text: str) -> list[str]:
    """Tokens to try matching a Markdown heading against an HTML H2."""
    t = text.strip()
    keys = [t]
    # Strip leading number + dot + space (e.g. "1. 交易对手风险" -> "交易对手风险")
    m = re.match(r"^\d+\.?\s*[、.：:]?\s*(.+)", t)
    if m:
        keys.append(m.group(1))
    # Strip leading 一/二/三...
    m = re.match(r"^[一二三四五六七八九十]+[、.：:]?\s*(.+)", t)
    if m:
        keys.append(m.group(1))
    # Strip "用户常问：" prefix
    keys.append(re.sub(r"^用户常问[：:]\s*", "", t))
    return [k for k in keys if k]


def strong_term(md_lead: str) -> str:
    m = re.search(r"\*\*([^*]+)\*\*", md_lead)
    return m.group(1) if m else ""


# H2 headings whose sections are link directories / FAQ / closing advice.
# Mirrors check_site.H2_SKIP_PATTERNS; keep the two lists in sync when editing.
SKIP_H2_SUBSTRINGS = (
    "参考资料", "相关页面", "延伸阅读", "官方入口", "官方参考",
    "核过的资料", "我核过的", "和手册其他章节", "上一篇", "下一篇",
    "返回", "下一步", "更新记录", "changelog", "faq", "常见问题",
    "用户常问",  # FAQ-style H2s in this repo
    "我的建议", "我的下一步", "一句更现实的建议", "一句总结",
    "最后的建议", "结尾", "补一句",
)


def should_skip(h2_text: str) -> bool:
    low = h2_text.lower()
    return any(p in low for p in SKIP_H2_SUBSTRINGS)


def sync_one(html_path: Path, md_path: Path, write: bool) -> int:
    """Return number of leads inserted."""
    if not md_path.exists():
        return 0
    md = md_path.read_text(encoding="utf-8")
    leads = extract_leads(html_path)
    if not leads:
        return 0

    # Build a map from H2 text → lead
    lead_by_key = {}
    for h2, md_lead in leads:
        for k in h2_keys(h2):
            lead_by_key.setdefault(k, md_lead)

    # Walk markdown headings
    headings = list(MD_HEADING_RE.finditer(md))
    # We'll insert from the end to keep earlier offsets valid.
    edits = []
    for idx, h in enumerate(headings):
        if h.group(1) != "##":
            continue
        md_heading_text = h.group(2).strip()
        if should_skip(md_heading_text):
            continue
        matched_lead = None
        for k in h2_keys(md_heading_text):
            if k in lead_by_key:
                matched_lead = lead_by_key[k]
                break
        if not matched_lead:
            continue
        term = strong_term(matched_lead)
        if not term:
            continue  # no reliable idempotency signal; safer to skip
        # Find the slice between this heading and the next one
        start = h.end()
        end = headings[idx + 1].start() if idx + 1 < len(headings) else len(md)
        section = md[start:end]
        # Idempotent check: if the target term is already bolded anywhere in the
        # section, assume the lead is in place and skip.
        if re.search(r"\*\*" + re.escape(term) + r"\*\*", section):
            continue
        # Insert the lead paragraph right after the heading line (leave one blank line)
        insert = f"\n\n{matched_lead}\n"
        edits.append((start, insert))

    if not edits:
        return 0

    # Apply from end to start
    new_md = md
    for offset, text in sorted(edits, key=lambda x: -x[0]):
        new_md = new_md[:offset] + text + new_md[offset:]

    if write:
        md_path.write_text(new_md, encoding="utf-8")
    return len(edits)


def main():
    write = "--write" in sys.argv
    total_files = 0
    total_inserts = 0
    for html_path in sorted(SITE.glob("*.html")):
        md_path = MD / (html_path.stem + ".md")
        n = sync_one(html_path, md_path, write)
        if n:
            print(f"{'wrote' if write else 'would insert'} {n} lead(s): {md_path.relative_to(ROOT)}")
            total_files += 1
            total_inserts += n
    mode = "wrote" if write else "dry-run"
    print(f"\n{mode}: {total_inserts} leads across {total_files} files")


if __name__ == "__main__":
    main()
