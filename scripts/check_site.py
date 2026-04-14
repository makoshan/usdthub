#!/usr/bin/env python3
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / 'docs'
HOME_FILE = SITE_DIR / 'index.html'

REQUIRED_HOME_SNIPPETS = [
    '1. 章节',
    '2. 新手常用工具',
    '3. 官方资料入口',
    '4. 最近更新',
]

FORBIDDEN_HOME_SNIPPETS = [
    'reading-path.svg',
    '<strong>目录</strong>',
    '1. 从哪里开始',
    '2. 我为什么这样写',
    '6. 下一步读什么',
]

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.title_found = False
        self.meta_description_found = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        elif tag == 'title':
            self.title_found = True
        elif tag == 'meta' and attrs.get('name', '').lower() == 'description' and attrs.get('content', '').strip():
            self.meta_description_found = True


def main():
    if not SITE_DIR.exists():
        print(f'missing site directory: {SITE_DIR}')
        return 1

    html_files = sorted(SITE_DIR.glob('*.html'))
    if not html_files:
        print('no HTML files found in docs/')
        return 1

    missing_links = []
    missing_meta = []
    homepage_issues = []

    for file_path in html_files:
        parser = Parser()
        parser.feed(file_path.read_text(encoding='utf-8'))

        if not parser.title_found or not parser.meta_description_found:
            missing_meta.append({
                'file': file_path.name,
                'missing_title': not parser.title_found,
                'missing_meta_description': not parser.meta_description_found,
            })

        for href in parser.links:
            if href.startswith('http://') or href.startswith('https://') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
            if href.startswith('#'):
                continue
            target = href.split('#', 1)[0]
            if not target:
                continue
            if target.startswith('./'):
                target = target[2:]
            if target.startswith('/'):
                target = target[1:]
                if target.startswith('usdthub/'):
                    target = target[len('usdthub/'):]
            target_path = SITE_DIR / target
            if not target_path.exists():
                missing_links.append({'file': file_path.name, 'missing': href})

    extra_files = ['robots.txt', 'sitemap.xml']
    missing_extra = [name for name in extra_files if not (SITE_DIR / name).exists()]

    if HOME_FILE.exists():
        home_html = HOME_FILE.read_text(encoding='utf-8')
        for snippet in REQUIRED_HOME_SNIPPETS:
            if snippet not in home_html:
                homepage_issues.append(f'missing required homepage snippet: {snippet}')
        for snippet in FORBIDDEN_HOME_SNIPPETS:
            if snippet in home_html:
                homepage_issues.append(f'found forbidden homepage snippet: {snippet}')
    else:
        homepage_issues.append(f'missing homepage file: {HOME_FILE.name}')

    if missing_links or missing_meta or missing_extra or homepage_issues:
        if missing_links:
            print('Missing internal links:')
            for item in missing_links:
                print(f"- {item['file']} -> {item['missing']}")
        if missing_meta:
            print('Missing metadata:')
            for item in missing_meta:
                print(f"- {item['file']} | missing_title={item['missing_title']} | missing_meta_description={item['missing_meta_description']}")
        if missing_extra:
            print('Missing support files:')
            for name in missing_extra:
                print(f'- {name}')
        if homepage_issues:
            print('Homepage content checks failed:')
            for issue in homepage_issues:
                print(f'- {issue}')
        return 1

    print(f'OK: checked {len(html_files)} HTML files in docs/, no missing internal links, all files have title and meta description, robots.txt and sitemap.xml exist, homepage structure matches expectations.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
