# USDT 新手手册

一个给新手看的公开手册。尽量把买、存、转、用这几件事讲清楚，少一点黑话，少一点过度营销，多一点能真正照着做的内容。

在线阅读（GitHub Pages）
- https://makoshan.github.io/usdthub/

仓库现在的组织方式
- `README.md`：仓库首页说明，直接展示给 GitHub 访客
- `site/`：Jekyll 源文件（页面、layouts、includes、assets、robots、sitemap）
- `docs/`：Jekyll 构建输出，作为 GitHub Pages 发布目录
- `scripts/check_site.py`：构建后校验脚本

一句话：
- 现在仓库首页是 README，源码 HTML 不再摊在根目录，已经收进 `site/` 里了。

## 本地开发

安装依赖
```bash
bundle install
```

本地构建
```bash
bundle exec jekyll build
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

## 从哪里开始

1. [USDT 是什么](https://makoshan.github.io/usdthub/what-is-usdt.html)
2. [如何购买 Tether USDt（USDT）](https://makoshan.github.io/usdthub/how-to-buy-usdt.html)
3. [人在中国怎么买 USDT / BTC](https://makoshan.github.io/usdthub/china-buy-crypto-notes.html)
4. [怎么选钱包](https://makoshan.github.io/usdthub/how-to-choose-a-wallet.html)
5. [怎么发送 USDT](https://makoshan.github.io/usdthub/how-to-send-usdt.html)
6. [TRC20、ERC20、BEP20 有什么区别](https://makoshan.github.io/usdthub/usdt-networks-explained.html)

## 中国用户专题

1. [人在中国怎么买 USDT / BTC](https://makoshan.github.io/usdthub/china-buy-crypto-notes.html)
2. [在中国买币最容易踩的 7 个坑](https://makoshan.github.io/usdthub/china-7-common-mistakes.html)
3. [C2C / OTC 到底在怕什么](https://makoshan.github.io/usdthub/china-c2c-otc-risks.html)
4. [第一次别碰的事](https://makoshan.github.io/usdthub/china-first-time-donts.html)

## TRON / TRC20

1. [TRON 能量指南](https://makoshan.github.io/usdthub/tron-energy-guide.html)
2. [为什么转 TRC20 USDT 要准备 TRX](https://makoshan.github.io/usdthub/why-you-need-trx-to-send-usdt.html)
3. [TRON 带宽和能量是什么](https://makoshan.github.io/usdthub/tron-bandwidth-and-energy.html)
4. [TRON 能量怎么获得](https://makoshan.github.io/usdthub/how-to-get-tron-energy.html)
5. [TRC20 USDT 手续费怎么省](https://makoshan.github.io/usdthub/how-to-reduce-trc20-usdt-fees.html)

## Use Cases

1. [USDT 可以拿来做什么](https://makoshan.github.io/usdthub/what-can-you-do-with-usdt.html)
2. [如何用 USDT 订阅 AI](https://makoshan.github.io/usdthub/use-usdt-for-ai.html)
3. [如何用 USDT 买 eSIM 和 VPN](https://makoshan.github.io/usdthub/use-usdt-for-esim-and-vpn.html)
4. [出国旅游时，USDT 有哪些实际用途](https://makoshan.github.io/usdthub/use-usdt-for-travel.html)
5. [用 USDT 做跨境小额结算前要先确认什么](https://makoshan.github.io/usdthub/use-usdt-for-cross-border-payments.html)

## Trust

1. [How We Review Wallets and Apps](https://makoshan.github.io/usdthub/how-we-review-wallets-and-apps.html)
2. [Editorial Policy / Disclosure](https://makoshan.github.io/usdthub/editorial-policy.html)
3. [Changelog](https://makoshan.github.io/usdthub/changelog.html)

## 说明

- 这不是交易平台，也不是投资建议。
- 这里优先解释问题，再推荐工具。
- imToken 在手册里的角色是 beginner-friendly option，不是站点品牌本身。
- 中国用户相关内容，重点写支付风控、问题资金、错误网络、错误路径，而不是只讲理论。
