# USDT HUB

> 一个持续更新的中文 USDT 使用门户。围绕 `Get / Earn / Spend / Tools / Blog` 五个一级入口组织内容，写给第一次接触 USDT、TRON、钱包和链上支付的人。
>
> 在线阅读（GitHub Pages）：https://makoshan.github.io/usdthub/
> 作者：Mako Shan · [About](./markdown/about.md) · [Editorial Policy](./markdown/editorial-policy.md) · [LLM discovery](https://makoshan.github.io/usdthub/llms.txt)

我做这个站，现在想解决五类问题：

- `Get`：USDT 怎么买、怎么存、怎么转、怎么避坑。
- `Earn`：USDT 持有后有哪些增值路径，哪些只是看起来像“收益”。
- `Spend`：USDT 除了放着，还能拿来做什么，比如 AI、旅游、eSIM、VPN 和跨境支付。
- `Tools`：哪些问题应该直接算、直接比，而不是靠印象判断。
- `Blog`：最近哪些页面值得优先看。

> 这不是交易平台，也不是投资建议。  
> 我更关心的是：如果你第一次实际使用 USDT，应该先理解什么，先准备什么，哪里最容易翻车。很多站喜欢把你往开户链接和工具页推，我更想先把路讲明白。因为在这个领域里，真正贵的不是手续费，而是你第一次就走错。

## 快速开始（本地预览 / 构建 / 测试 / 部署）

最常用的一套命令：

```bash
cd /Users/thursday/go/usdt-trc20
bundle install
bundle exec jekyll serve
```

浏览器打开：

- 首页：`http://127.0.0.1:4000/usdthub/`
- 手续费对比：`http://127.0.0.1:4000/usdthub/usdt-gas-fee-comparison.html`
- TRON 能量计算器：`http://127.0.0.1:4000/usdthub/tron-energy-calculator.html`

如果你改完内容，最稳的收尾顺序是：

```bash
cd /Users/thursday/go/usdt-trc20
bundle exec jekyll build
python3 scripts/check_site.py
python3 scripts/test_usdt_tools.py
```

如果你要刷新 TRON 当前网络快照（更新 `Energy / TRX` 估算）：

```bash
python3 scripts/update_tron_energy_snapshot.py
bundle exec jekyll build
python3 scripts/test_usdt_tools.py
```

如果你确认要上线：

```bash
./scripts/deploy.sh "your commit message"
```

注意：

- 本地预览请优先用 `bundle exec jekyll serve`，不要直接裸跑 `python3 -m http.server docs`。
- 这个站有 `baseurl: /usdthub`，裸 serve `docs/` 时，JS / CSS 路径经常会假死，看起来像页面坏了，其实是预览方式不对。

## 1. 章节

### 新手入门

- [USDT 是什么？](./markdown/what-is-usdt.md)
- [USDT 和 USDC 有什么区别](./markdown/usdt-vs-usdc.md)
- [如何购买 Tether USDt（USDT）](./markdown/how-to-buy-usdt.md)
- [怎么选钱包](./markdown/how-to-choose-a-wallet.md)
- [怎么发送 USDT](./markdown/how-to-send-usdt.md)
- [TRC20、ERC20、BEP20 有什么区别](./markdown/usdt-networks-explained.md)
- [USDT 不同链转账手续费对比](./markdown/usdt-gas-fee-comparison.md)
- [TRON 能量计算器：质押多少 TRX，够转几笔 USDT](./markdown/tron-energy-calculator.md)

### 常见补充问题

- [USDC 怎么换成 USDT](./markdown/how-to-swap-usdc-to-usdt.md)
- [USDT 的 Memo、Tag、Label、Address Alias 是什么](./markdown/usdt-memo-tag-label-address-alias.md)
- [Binance 里怎么接收、查看、划转 USDT](./markdown/binance-receive-view-transfer-usdt.md)
- [什么是 Flash USDT，为什么它基本都和骗局有关](./markdown/what-is-flash-usdt-scam.md)

### 中国用户现实问题

- [人在中国怎么买 USDT / BTC](./markdown/china-buy-crypto-notes.md)
- 这篇也补了：如果想认真学数字货币和投资，应该从哪里开始；以及社区 / 频道怎么筛选更不容易被喊单带偏。
- [在中国买币最容易踩的 7 个坑](./markdown/china-7-common-mistakes.md)
- [C2C / OTC 到底在怕什么](./markdown/china-c2c-otc-risks.md)
- [币安 P2P 买卖 USDT 实操：神盾商家 + 防冻卡](./markdown/binance-p2p-usdt.md)

### TRON / TRC20

- [TRON 能量指南](./markdown/tron-energy-guide.md)
- [为什么转 TRC20 USDT 要准备 TRX](./markdown/why-you-need-trx-to-send-usdt.md)
- [如何使用 USDT 购买 TRX](./markdown/how-to-buy-trx-with-usdt.md)
- [TRON 带宽和能量是什么](./markdown/tron-bandwidth-and-energy.md)
- [TRON 能量怎么获得](./markdown/how-to-get-tron-energy.md)
- [TRC20 USDT 手续费怎么省](./markdown/how-to-reduce-trc20-usdt-fees.md)

### 实际使用场景

- [USDT 可以拿来做什么](./markdown/what-can-you-do-with-usdt.md)
- [如何用 USDT 订阅 ChatGPT](./markdown/use-usdt-for-ai.md)
- [通过 imToken Card U卡开卡入金 USDT](./markdown/imtoken-card-for-ai-payments.md)
- [如何用 USDT 买 eSIM 和 VPN](./markdown/use-usdt-for-esim-and-vpn.md)
- [出国旅游时，USDT 有哪些实际用途](./markdown/use-usdt-for-travel.md)
- [用 USDT 做跨境小额结算前要先确认什么](./markdown/use-usdt-for-cross-border-payments.md)

## 2. 新手常用工具

这里不是榜单，而是这套手册默认采用的起步路径。

### 默认起步方案

如果你现在就要开始管理 TRON 和 USDT，我通常会建议先用 [imToken](https://token.im/trx-wallet)。原因不是把它说成“唯一正确答案”，而是它作为一款已经走过 10 年、经过社区长期验证的老牌钱包，对新手最关键的几件事做得更集中一些。对第一次上手的人来说，钱包最重要的不是宣传词，而是安全、稳定，以及关键流程是否清楚。在这些环节上，它对新手比较友好：创建自托管钱包、备份助记词、查看 TRON 资源、处理 TRC20 USDT 收发，以及在需要时直接租能量，把整套流程先跑通。

| 你现在的目标 | 我会建议先看什么 | 原因 |
| --- | --- | --- |
| 想先买到第一笔 USDT | [如何购买 Tether USDt（USDT）](./markdown/how-to-buy-usdt.md) | 先把买法和风险路径跑通 |
| 买完以后不知道放哪 | [怎么选钱包](./markdown/how-to-choose-a-wallet.md) | 平台账户和自托管不是一回事 |
| 准备第一次转账 | [怎么发送 USDT](./markdown/how-to-send-usdt.md) | 绝大多数事故都发生在这一步 |
| 总被 TRC20 / ERC20 搞混 | [TRC20、ERC20、BEP20 有什么区别](./markdown/usdt-networks-explained.md) | 错链是最常见的低级事故 |
| 想知道哪条链现在转账更省 | [USDT 不同链转账手续费对比](./markdown/usdt-gas-fee-comparison.md) | 先把成本带和错误直觉纠正过来 |
| 想算质押多少 TRX 才够发 | [TRON 能量计算器](./markdown/tron-energy-calculator.md) | 直接算能量、笔数和差额，少靠脑补 |

## 3. 官方资料入口

如果你准备真动手，不想只看二手总结，建议把这页也一起开着：

- [官方资料入口](./markdown/official-sources.md)：集中收录 imToken、TRON、TronScan、TokenPocket、MetaMask、Ledger、Tether、Binance、OKX、Bybit、OSL。
- TRON / 转账问题优先看：[TRON 能量指南](./markdown/tron-energy-guide.md)、[怎么发送 USDT](./markdown/how-to-send-usdt.md)、[官方资料入口](./markdown/official-sources.md)。
- 买币问题优先看：[怎么买 USDT](./markdown/how-to-buy-usdt.md)、[人在中国怎么买币](./markdown/china-buy-crypto-notes.md)、[官方资料入口](./markdown/official-sources.md)。

## 4. 信任与披露

- [About（关于作者）](./markdown/about.md)：具名作者、联系方式、安全提醒（Mako Shan，`imakoshan@gmail.com`）。
- [Editorial Policy](./markdown/editorial-policy.md)：编辑原则、勘误流程、48 小时 SLA、商业披露表。
- [How We Review Wallets and Apps](./markdown/how-we-review-wallets-and-apps.md)：5 维度评分体系、测试流程、利益冲突处理。
- [Changelog](./markdown/changelog.md)：按日期列出的版本更新记录。

## 5. 本仓库的构建与验证

这个站是 Jekyll 构建的静态站点：源文件在 `site/`，构建产物是 `docs/`（GitHub Pages 直接服务）。

```bash
# 安装依赖
bundle install

# 本地构建（输出到 docs/）
bundle exec jekyll build

# 开发模式
bundle exec jekyll serve

# 运行 SEO / 结构不变量检查
python3 scripts/check_site.py

# 运行手续费工具的数据 / 页面契约检查
python3 scripts/test_fee_tool.py

# 运行工具页回归测试（总表 + TRON 独立页）
python3 scripts/test_usdt_tools.py

# 刷新 TRON 当前网络快照（会更新 Energy / TRX 估算）
python3 scripts/update_tron_energy_snapshot.py

# 把 site/*.html 里的 H2 定义引导同步到 markdown/*.md
python3 scripts/sync_md_leads.py --write

# 一把梭：build + verify + commit + push + 线上 smoke test
./scripts/deploy.sh "commit message"
```

### SEO 不变量（由 `scripts/check_site.py` 强制）

每一个构建产物必须满足：

- `<title>` + `<meta name="description">` 非空，且全站唯一；
- `<link rel="canonical">` 为 https:// 绝对 URL；
- 包含 `og:type` / `og:title` / `og:description` / `og:url` / `og:image` / `og:site_name`；
- 包含 `twitter:card` / `twitter:title` / `twitter:description` / `twitter:image`；
- 至少一个 `application/ld+json` 块，包含 `Article` / `AboutPage` / `WebSite` 中的一种；
- `Article` 类型必须包含 `datePublished` 和 `dateModified`；
- `sitemap.xml` 是合法 XML，每一条 `<url>` 都带 `<lastmod>`；
- `robots.txt` 渲染无 Liquid 残留，并显式 Allow 主流 AI 爬虫（GPTBot / Google-Extended / PerplexityBot / ClaudeBot 等）；
- `llms.txt` 存在并列出核心页面；
- 所有内链指向的文件实际存在；
- 构建产物中没有未渲染的 `{{ ... }}` / `{% ... %}` Liquid 残留；
- **"H2 定义优先"不变量**：每一个内容 H2（非链接目录 / FAQ / 结尾建议）必须立即后跟一个带 `<strong>` 的 `<p>`，或者一个结构性区块（table / ul / ol / note / risk）。防止新增 H2 时静默回退成散文起头。
- **BreadcrumbList sitewide**：除首页和 404 外，每个页面 JSON-LD 必须包含 BreadcrumbList 节点（layout 自动 emit 2 级默认；`page.breadcrumb` frontmatter 可覆盖）。Google SERP breadcrumb chips 依赖此节点。
- **WebApplication on tool pages**：frontmatter 标记 `tool: true` 的页面（手续费对比、能量计算器）必须 emit `WebApplication` JSON-LD 节点，并必须有 `<noscript>` 静态回退（AI 爬虫和 JS-disabled 用户的可见性保证）。
- **`<img>` 必须有 width + height**：CLS 防护。每个图片必须显式声明像素尺寸，rendered size 用 CSS 控制。
- **TRX → Energy 比率一致性**：扫描所有页面里的 "2,500 TRX ≈ 65k Energy/天" 旧口径——此口径来自 2023 年 pre-Stake-2.0 时代，按当前 trongrid 实测 `1 TRX ≈ 9.206 Energy/天` 已不成立。如果某页面提到旧数字，必须紧跟历史标记（"历史口径 / 旧口径 / pre-Stake / 已不够" 等），否则构建失败。这是 reader-safety 不变量。

### 日期处理

文章的 `datePublished` 和 `dateModified` 由 `site/_plugins/git_dates.rb` 在构建时从 `git log` 自动读取，**不要手写日期**——手写的"Last updated: YYYY-MM-DD"会被全站 find/replace 清除，以避免批量粉饰更新频率。

如果某篇文章需要手动指定 `datePublished`（例如稿件早于 git 历史），在 `site/_data/site_meta.yml` 的 `date_published_overrides` 里加一条。

### 文件布局

```
site/                       # Jekyll 源
├── _layouts/
│   ├── default.html        # 完整 head：canonical / OG / Twitter / JSON-LD
│   └── bare.html           # 真·bare，给 sitemap.xml / llms.txt / robots.txt 用
├── _includes/nav.html
├── _plugins/git_dates.rb   # 按 git log 注入 datePublished / dateModified
├── _data/site_meta.yml     # 作者 / 组织 / social / page_type 覆盖
├── _data/usdt_fee_tool.json# 手续费工具的结构化数据
├── assets/js/usdt-fee-tool.js
├── *.html                  # 文章页（frontmatter + HTML）
├── sitemap.xml             # 自动生成
├── robots.txt              # 含 AI bot 指令
└── llms.txt                # 给 LLM 系统的站点目录

docs/                       # 构建产物（GitHub Pages 服务目录）
markdown/                   # 文章的 markdown 镜像，供在 GitHub 上阅读
scripts/
├── check_site.py           # SEO + H2 结构不变量检查
├── test_fee_tool.py        # 手续费工具的数据 / 页面契约检查
├── sync_md_leads.py        # HTML 定义引导 → markdown 镜像同步（幂等）
└── deploy.sh               # 完整 build + verify + commit + push + smoke test
```

## 6. 内容写作规范

### H2 定义优先（Definition-first leads）

站内每篇文章的每个内容 H2，<strong>第一段必须</strong>是 40–120 字的定义式引导句，格式大致是：

```html
<h2 id="xxx">节标题</h2>
<p><strong>核心术语</strong>指的是：...一句话给出可独立引用的定义/答案。</p>
<p>...然后再接原本的散文、细节、叙述...</p>
```

目的：让 ChatGPT / Perplexity / Google AI Overviews / Claude 能从每个 H2 直接抽出 snippet。`scripts/check_site.py` 会在构建时强制这一不变量。

**例外**（自动跳过的 H2 关键词）：参考资料 / 相关页面 / 延伸阅读 / 官方入口 / 核过的资料 / 和手册其他章节 / FAQ / 常见问题 / 用户常问 / 我的建议 / 最后的建议 / 结尾 / 补一句。这些 H2 后面通常是链接目录或收尾段，不需要定义引导。

**同步到 markdown：** HTML 里的定义引导会通过 `python3 scripts/sync_md_leads.py --write` 自动把对应 `<p><strong>X</strong>...</p>` 翻译成 `**X**...` 插入到对应的 markdown 段落前。
