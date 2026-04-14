# USDT 新手手册

一个给新手看的公开手册。尽量把买、存、转、用这几件事讲清楚，少一点黑话，少一点过度营销，多一点能真正照着做的内容。

在线阅读（GitHub Pages）
- https://makoshan.github.io/usdthub/

仓库结构
- `README.md`：仓库首页说明
- `markdown/`：适合直接在 GitHub 阅读的 Markdown 版本
- `site/`：Jekyll 源文件
- `docs/`：Jekyll 构建输出，作为 GitHub Pages 发布目录
- `scripts/check_site.py`：构建后校验脚本

如果你是在 GitHub 里看仓库，我默认让你直接点 Markdown，不强行把你跳到 HTML 网站。

## 从哪里开始

1. [USDT 是什么](./markdown/what-is-usdt.md)
2. [如何购买 Tether USDt（USDT）](./markdown/how-to-buy-usdt.md)
3. [人在中国怎么买 USDT / BTC](./markdown/china-buy-crypto-notes.md)
4. [怎么选钱包](./markdown/how-to-choose-a-wallet.md)
5. [怎么发送 USDT](./markdown/how-to-send-usdt.md)
6. [TRC20、ERC20、BEP20 有什么区别](./markdown/usdt-networks-explained.md)

## 中国用户专题

1. [人在中国怎么买 USDT / BTC](./markdown/china-buy-crypto-notes.md)
2. [在中国买币最容易踩的 7 个坑](./markdown/china-7-common-mistakes.md)
3. [C2C / OTC 到底在怕什么](./markdown/china-c2c-otc-risks.md)
4. [第一次别碰的事](./markdown/china-first-time-donts.md)

## TRON / TRC20

1. [TRON 能量指南](./markdown/tron-energy-guide.md)
2. [为什么转 TRC20 USDT 要准备 TRX](./markdown/why-you-need-trx-to-send-usdt.md)
3. [TRON 带宽和能量是什么](./markdown/tron-bandwidth-and-energy.md)
4. [TRON 能量怎么获得](./markdown/how-to-get-tron-energy.md)
5. [TRC20 USDT 手续费怎么省](./markdown/how-to-reduce-trc20-usdt-fees.md)

## Use Cases

1. [USDT 可以拿来做什么](./markdown/what-can-you-do-with-usdt.md)
2. [如何用 USDT 订阅 AI](./markdown/use-usdt-for-ai.md)
3. [如何用 USDT 买 eSIM 和 VPN](./markdown/use-usdt-for-esim-and-vpn.md)
4. [出国旅游时，USDT 有哪些实际用途](./markdown/use-usdt-for-travel.md)
5. [用 USDT 做跨境小额结算前要先确认什么](./markdown/use-usdt-for-cross-border-payments.md)

## Trust

1. [How We Review Wallets and Apps](./markdown/how-we-review-wallets-and-apps.md)
2. [Editorial Policy / Disclosure](./markdown/editorial-policy.md)
3. [Changelog](./markdown/changelog.md)

## 本地开发

安装依赖
```bash
bundle install
```

本地构建
```bash
bundle exec jekyll build --clean
```

本地预览
```bash
bundle exec jekyll serve
```

默认地址
- `http://127.0.0.1:4000/usdthub/`

## 校验

构建后运行
```bash
python3 scripts/check_site.py
```

它会检查：
- `docs/` 下所有 HTML 的内部链接是否存在
- 每个 HTML 是否有 `<title>`
- 每个 HTML 是否有 `meta description`
- `robots.txt` 与 `sitemap.xml` 是否存在

## 说明

- 这不是交易平台，也不是投资建议。
- 这里优先解释问题，再推荐工具。
- imToken 在手册里的角色是 beginner-friendly option，不是站点品牌本身。
- 中国用户相关内容，重点写支付风控、问题资金、错误网络、错误路径，而不是只讲理论。
