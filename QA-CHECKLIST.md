# QA Checklist

Date: 2026-04-14
Project: USDT 新手手册

Checked pages
- index.html
- changelog.html
- start-here.html
- how-to-buy-usdt.html
- china-buy-crypto-notes.html
- china-7-common-mistakes.html
- china-c2c-otc-risks.html
- china-first-time-donts.html
- how-to-choose-a-wallet.html
- how-to-send-usdt.html
- tron-energy-guide.html
- what-can-you-do-with-usdt.html
- use-usdt-for-ai.html
- use-usdt-for-esim-and-vpn.html
- how-we-review-wallets-and-apps.html
- editorial-policy.html

Checks performed
- All pages return 200 locally
- Titles render correctly
- Homepage nav includes China-specific guide entry and changelog
- Homepage Basics section includes the China-specific article cluster
- Start Here links to wallet and send chapters, plus China-specific guide
- China-specific cluster internally links across the three risk pages
- Handbook voice preserved: no heavy landing-page CTA blocks on rewritten pages
- Risk disclaimers included on buying / transfer / China-specific / payment-related pages
- Changelog page exists and is linked from homepage and Start Here
- Local internal-link audit across 24 HTML files: no missing local links found
- Markdown mirrors generated for all 24 HTML pages
- Markdown mirror index exists at markdown/README.md
- Export script exists at scripts/export_markdown_mirrors.py
- GitHub Pages deployment files exist: docs/.nojekyll, docs/robots.txt, docs/sitemap.xml, docs/404.html
- HTML site files are consolidated under docs/ for GitHub Pages publishing

Current structure status
- Handbook home: complete
- Core beginner chapters: complete
- Network / TRON basics: complete
- Transfer basics: complete
- Use cases starter set: complete
- China-specific starter cluster: complete
- Trust pages: complete
- Changelog: complete
- GitHub Pages config: complete
- GitHub Pages deployment files: complete
- HTML content consolidated under docs/: complete
- Markdown mirrors: complete
- QA doc: complete

Known gaps (non-blocking for first usable release)
- No dedicated compare/review chapter yet
- No full glossary section yet

Result
- Current handbook is internally navigable, link-complete, thematically coherent, and usable as a first complete public draft.
