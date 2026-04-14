from pathlib import Path
import re
from html.parser import HTMLParser

base = Path(__file__).resolve().parent.parent
out_dir = base / 'markdown'
out_dir.mkdir(exist_ok=True)


class Extractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_main = False
        self.skip_depth = 0
        self.current = None
        self.buffer = []
        self.out = []
        self.list_stack = []
        self.in_table = False
        self.current_row = []
        self.current_cell = []
        self.table_rows = []
        self.cell_tag = None

    def flush(self):
        if self.current is None:
            return
        text = ''.join(self.buffer)
        text = re.sub(r'\s+', ' ', text).strip()
        if text:
            if self.current == 'li':
                indent = '  ' * (len(self.list_stack) - 1)
                self.out.append(f'{indent}- {text}')
            elif self.current == 'p':
                self.out.append(text)
                self.out.append('')
            elif self.current == 'h1':
                self.out.append(f'# {text}')
                self.out.append('')
            elif self.current == 'h2':
                self.out.append(f'## {text}')
                self.out.append('')
            elif self.current == 'h3':
                self.out.append(f'### {text}')
                self.out.append('')
            elif self.current in ('meta', 'note'):
                self.out.append(f'> {text}')
                self.out.append('')
        self.current = None
        self.buffer = []

    def flush_table(self):
        if not self.table_rows:
            return
        header = self.table_rows[0]
        self.out.append('| ' + ' | '.join(header) + ' |')
        self.out.append('| ' + ' | '.join(['---'] * len(header)) + ' |')
        for row in self.table_rows[1:]:
            padded = row + [''] * (len(header) - len(row))
            self.out.append('| ' + ' | '.join(padded[:len(header)]) + ' |')
        self.out.append('')
        self.table_rows = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'main':
            self.in_main = True
            return
        if not self.in_main:
            return
        if tag in ('nav', 'header', 'footer'):
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag == 'table':
            self.flush()
            self.in_table = True
            self.table_rows = []
            return
        if self.in_table:
            if tag == 'tr':
                self.current_row = []
            elif tag in ('th', 'td'):
                self.cell_tag = tag
                self.current_cell = []
            return
        if tag in ('h1', 'h2', 'h3', 'p', 'li'):
            self.flush()
            self.current = tag
        elif tag in ('ul', 'ol'):
            self.list_stack.append(tag)
        elif tag == 'div' and attrs.get('class', '') in ('meta', 'note', 'risk'):
            self.flush()
            self.current = 'meta' if attrs.get('class') == 'meta' else 'note'
        elif tag == 'br':
            self.buffer.append(' ')

    def handle_endtag(self, tag):
        if tag == 'main':
            self.flush()
            self.flush_table()
            self.in_main = False
            return
        if not self.in_main:
            return
        if self.skip_depth:
            if tag in ('nav', 'header', 'footer'):
                self.skip_depth -= 1
            return
        if self.in_table:
            if tag in ('th', 'td') and self.cell_tag == tag:
                text = re.sub(r'\s+', ' ', ''.join(self.current_cell)).strip()
                self.current_row.append(text)
                self.current_cell = []
                self.cell_tag = None
            elif tag == 'tr' and self.current_row:
                self.table_rows.append(self.current_row)
                self.current_row = []
            elif tag == 'table':
                self.flush_table()
                self.in_table = False
            return
        if tag in ('h1', 'h2', 'h3', 'p', 'li'):
            self.flush()
        elif tag in ('ul', 'ol') and self.list_stack:
            self.list_stack.pop()
            self.out.append('')

    def handle_data(self, data):
        if not self.in_main or self.skip_depth:
            return
        if self.in_table and self.cell_tag:
            self.current_cell.append(data)
            return
        if self.current is None:
            return
        self.buffer.append(data)


def convert(path: Path) -> str:
    html = path.read_text(encoding='utf-8')
    title_match = re.search(r'<title>(.*?)</title>', html, re.S)
    title = title_match.group(1).strip() if title_match else path.stem
    parser = Extractor()
    parser.feed(html)
    content = '\n'.join(line.rstrip() for line in parser.out)
    content = re.sub(r'\n{3,}', '\n\n', content).strip() + '\n'
    frontmatter = f'---\ntitle: "{title}"\nsource_html: "{path.name}"\n---\n\n'
    return frontmatter + content


html_files = sorted(base.glob('*.html'))
for html_path in html_files:
    md_path = out_dir / f'{html_path.stem}.md'
    md_path.write_text(convert(html_path), encoding='utf-8')

index_lines = [
    '# USDT 新手手册（Markdown 镜像）',
    '',
    '这个目录是 GitHub 直接阅读用的 Markdown 镜像。',
    '',
    '- HTML 版本用于 GitHub Pages / 本地预览',
    '- Markdown 版本用于 GitHub 仓库内直接阅读',
    '',
    '主要章节：',
    ''
]
for html_path in html_files:
    index_lines.append(f'- [{html_path.stem}](./{html_path.stem}.md)')
index_lines.append('')
(out_dir / 'README.md').write_text('\n'.join(index_lines), encoding='utf-8')

print(f'Exported {len(html_files)} markdown mirrors to {out_dir}')
