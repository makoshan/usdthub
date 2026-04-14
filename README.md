# USDT 新手手册

一个给新手看的公开手册。尽量把买、存、转、用这几件事讲清楚，少一点黑话，少一点过度营销，多一点能真正照着做的内容。

在线阅读（GitHub Pages）
- https://makoshan.github.io/usdthub/
- 当前项目已经迁移为真正的 Jekyll 站点，Jekyll 源文件在仓库根目录，构建输出到 `docs/`。

## 当前技术状态

已完成
- Jekyll 配置：`_config.yml`
- Layout：`_layouts/default.html`、`_layouts/bare.html`
- Include：`_includes/nav.html`
- 样式：`assets/css/style.css`
- 页面源文件：根目录各 `.html` 页面（带 front matter）
- 发布目录：`docs/`
- SEO 支持文件：`robots.txt`、`sitemap.xml`
- 校验脚本：`scripts/check_site.py`

一句话：
- 现在不是“纯静态 HTML 散文件”，而是“Jekyll 源文件 -> 构建输出到 docs/ -> GitHub Pages 发布”的标准流程。

## 本地开发

1. 安装依赖
```bash
bundle install
```

2. 本地构建
```bash
bundle exec jekyll build
```

3. 本地预览
```bash
bundle exec jekyll serve
```

默认地址：
- `http://127.0.0.1:4000/usdthub/`

如果只是想临时查看已构建结果，也可以：
```bash
cd docs
python3 -m http.server 8765
```
然后打开：
- `http://127.0.0.1:8765/index.html`

## 校验

构建后运行：
```bash
python3 scripts/check_site.py
```

它会检查：
- `docs/` 下所有 HTML 的内部链接是否存在
- 每个 HTML 是否有 `<title>`
- 每个 HTML 是否有 `meta description`
- `robots.txt` 与 `sitemap.xml` 是否存在

## 从哪里开始

1. [USDT 是什么](./what-is-usdt.html)
2. [如何购买 Tether USDt（USDT）](./how-to-buy-usdt.html)
3. [人在中国怎么买 USDT / BTC](./china-buy-crypto-notes.html)
4. [怎么选钱包](./how-to-choose-a-wallet.html)
5. [怎么发送 USDT](./how-to-send-usdt.html)
6. [TRC20、ERC20、BEP20 有什么区别](./usdt-networks-explained.html)

## 中国用户专题

1. [人在中国怎么买 USDT / BTC](./china-buy-crypto-notes.html)
2. [在中国买币最容易踩的 7 个坑](./china-7-common-mistakes.html)
3. [C2C / OTC 到底在怕什么](./china-c2c-otc-risks.html)
4. [第一次别碰的事](./china-first-time-donts.html)

## TRON / TRC20

1. [TRON 能量指南](./tron-energy-guide.html)
2. [为什么转 TRC20 USDT 要准备 TRX](./why-you-need-trx-to-send-usdt.html)
3. [TRON 带宽和能量是什么](./tron-bandwidth-and-energy.html)
4. [TRON 能量怎么获得](./how-to-get-tron-energy.html)
5. [TRC20 USDT 手续费怎么省](./how-to-reduce-trc20-usdt-fees.html)

## Use Cases

1. [USDT 可以拿来做什么](./what-can-you-do-with-usdt.html)
2. [如何用 USDT 订阅 AI](./use-usdt-for-ai.html)
3. [如何用 USDT 买 eSIM 和 VPN](./use-usdt-for-esim-and-vpn.html)
4. [出国旅游时，USDT 有哪些实际用途](./use-usdt-for-travel.html)
5. [用 USDT 做跨境小额结算前要先确认什么](./use-usdt-for-cross-border-payments.html)

## Trust

1. [How We Review Wallets and Apps](./how-we-review-wallets-and-apps.html)
2. [Editorial Policy / Disclosure](./editorial-policy.html)
3. [Changelog](./changelog.html)

## 说明

- 这不是交易平台，也不是投资建议。
- 这里优先解释问题，再推荐工具。
- imToken 在手册里的角色是 beginner-friendly option，不是站点品牌本身。
- 中国用户相关内容，重点写支付风控、问题资金、错误网络、错误路径，而不是只讲理论。
