#!/usr/bin/env python3
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_ROOT = os.path.join(ROOT, 'docs')

class LinkParser(HTMLParser):
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
    html_files = sorted([f for f in os.listdir(HTML_ROOT) if f.endswith('.html')])
    if not html_files:
        print('No HTML files found.')
        return 1

    missing_links = []
    missing_meta = []

    for filename in html_files:
        path = os.path.join(HTML_ROOT, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        parser = LinkParser()
        parser.feed(content)

        if not parser.title_found or not parser.meta_description_found:
            missing_meta.append({
                'file': filename,
                'missing_title': not parser.title_found,
                'missing_meta_description': not parser.meta_description_found,
            })

        for href in parser.links:
            if not href.startswith('./'):
                continue
            target = href[2:]
            if '#' in target:
                target = target.split('#', 1)[0]
            if not target:
                continue
            target_path = os.path.join(HTML_ROOT, target)
            if not os.path.exists(target_path):
                missing_links.append({'file': filename, 'missing': target})

    if missing_links or missing_meta:
        if missing_links:
            print('Missing internal links:')
            for item in missing_links:
                print(f"- {item['file']} -> {item['missing']}")
        if missing_meta:
            print('Missing metadata:')
            for item in missing_meta:
                print(
                    f"- {item['file']} | missing_title={item['missing_title']} | missing_meta_description={item['missing_meta_description']}"
                )
        return 1

    print(f'OK: checked {len(html_files)} HTML files, no missing internal links, all files have title and meta description.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
