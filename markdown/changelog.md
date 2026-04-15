---
title: "Changelog | USDT 新手手册"
source_html: "changelog.html"
---

# Changelog

> 按日期列出的版本更新记录。细粒度 diff 请看 [GitHub commit 历史](https://github.com/makoshan/usdthub/commits/main)。

读法：`added` = 新增章节 / 页面；`rewrite` = 整页重写；`fix` = 事实或表述勘误；`infra` = 构建 / SEO / 模板层变化，不影响内容。

## 2026-04-15 · GEO 全量铺开

- `rewrite` 把"定义优先"段落模板**铺到全站 32 篇文章**——每个内容 H2 下都先有一段 40–120 字的定义式引导句（`**术语**指的是：...`），再接原有散文。目的是让 Google AI Overviews / ChatGPT / Perplexity / Claude 能从每个小节直接抽出可独立引用的 snippet。总计约 170 个定义引导。
- `infra` 新增 `scripts/sync_md_leads.py`：把 HTML 源里的 H2 定义引导自动同步到 `markdown/` 镜像，保证 GitHub 读者看到的和 AI 爬虫看到的一致。幂等，可反复运行。
- `infra` `scripts/check_site.py` 新增**"H2 定义优先"结构不变量**：每个内容 H2 要么后跟带 `<strong>` 的 `<p>`，要么后跟结构性区块（table / ul / ol / note / risk），否则构建失败。防止后续新增 H2 时这个模式静默回退。
- `infra` `scripts/sync_md_leads.py` 和 `scripts/check_site.py` 共享相同的"跳过"H2 词表（参考资料 / 相关页面 / FAQ / 用户常问 / 结尾建议 等），避免误伤链接目录和收尾建议段。
- `fix` 修正 `use-usdt-for-ai.html` 里一个预存的 `</p></div>` 标签不配对 bug。
- `infra` `docs/llms.txt` 新增"示例引用 / Sample answers"段——3 组 Q&A 直接演示给 LLM 看本站适合回答的查询形态，并附 canonical URL。

## 2026-04-15 · SEO & Trust 大版本

- `infra` 构建模板加入 canonical、Open Graph、Twitter Card、JSON-LD (Article / Organization / WebSite / Person) 结构化数据，全站 34 个页面统一注入。
- `infra` 新增 Jekyll 插件 `site/_plugins/git_dates.rb`：每个页面的 `dateModified` 和 `datePublished` 由 git log 自动生成，取代之前全站手写的同一个日期。
- `infra` 修复 `sitemap.xml`（之前被默认 layout 包成了 HTML）。加入 `lastmod` / `changefreq` / `priority`。
- `infra` 修复 `robots.txt`（之前 `{{ absolute_url }}` 模板没渲染）。显式 Allow GPTBot / Google-Extended / PerplexityBot / ClaudeBot / CCBot 等 16 个 AI 爬虫。
- `infra` `scripts/check_site.py` 扩展为 SEO 不变量检查器：canonical、OG、Twitter、JSON-LD、sitemap lastmod、robots、llms.txt、Liquid 残留都会检测。
- `added` 新增 [About](./about.md) 页：作者具名（Mako Shan）、联系方式、安全提醒。
- `added` 新增 `/llms.txt`：给 LLM 系统的站点目录，附引用准则。
- `rewrite` 重写 [Editorial Policy](./editorial-policy.md)：加入具名负责人、勘误 SLA、商业披露表、利益冲突处理、YMYL 风险声明——从 2.2 KB 扩展到 ~6 KB。
- `rewrite` 重写 [How We Review](./how-we-review-wallets-and-apps.md)：加入 5 维度评分体系 + 权重、完整测试流程、季度复审节奏——从 2.4 KB 扩展到 ~5 KB。
- `fix` [冷钱包文章](./cold-wallet-for-usdt-china.md)：去掉"基于一支中文视频整理"的模糊出处，改为作者自用经验 + 厂商官方文档 + 中文社区反馈综合。标题从 58 字缩到 27 字避免 SERP 截断。
- `fix` 全站移除所有手写的 `Last updated: YYYY-MM-DD` 字符串（34 个页面批量替换）。真实的更新时间由 layout 从 git log 读取，避免批量粉饰更新频率。
- `rewrite` 重写 5 个页面的段落引导以便于 LLM 片段提取（每个 H2 下加一段定义式首段）：[C2C / OTC 风险](./china-c2c-otc-risks.md)、[中国买币 7 个坑](./china-7-common-mistakes.md)、[USDT 是什么](./what-is-usdt.md)、[TRON 带宽与能量](./tron-bandwidth-and-energy.md)、[为什么需要 TRX](./why-you-need-trx-to-send-usdt.md)。

## 2026-04-14 · 内容重写

- `rewrite` 首页改为 handbook / README 风格，去掉 hero CTA。
- `added` [Start Here](./start-here.md) 入口。
- `rewrite` 基础章节：[怎么买 USDT](./how-to-buy-usdt.md)、[怎么选钱包](./how-to-choose-a-wallet.md)、[怎么发送 USDT](./how-to-send-usdt.md)、[TRON 能量指南](./tron-energy-guide.md)。
- `added` Use cases：[USDT 可以拿来做什么](./what-can-you-do-with-usdt.md)、[用 USDT 订阅 ChatGPT](./use-usdt-for-ai.md)、[用 USDT 买 eSIM 和 VPN](./use-usdt-for-esim-and-vpn.md)。
- `added` 中国大陆用户专题：[人在中国怎么买 USDT / BTC](./china-buy-crypto-notes.md)、[7 个常见坑](./china-7-common-mistakes.md)、[C2C / OTC 风险](./china-c2c-otc-risks.md)。
- `added` Trust pages：[How We Review Wallets and Apps](./how-we-review-wallets-and-apps.md)、[Editorial Policy / Disclosure](./editorial-policy.md)。
- `added` `QA-CHECKLIST.md`。
