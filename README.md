# USDT 新手手册

> 写给第一次接触 USDT 的人。
>
> 在线阅读（GitHub Pages）：https://makoshan.github.io/usdthub/

如果你现在脑子里同时有这些问题：

- USDT 到底是什么？
- 为什么同样都叫 USDT，还分 ERC20、TRC20？
- 为什么别人说转 TRC20 USDT 还要准备 TRX？
- 钱包到底是选交易所、软件钱包，还是别的？

那你来对地方了。

我做这个手册，不是为了喊口号，也不是为了把你直接推去某个工具页。我更关心的是：如果你第一次实际使用 USDT，应该先理解什么，先准备什么，哪里最容易翻车。因为在这个领域里，真正贵的不是手续费，而是你第一次就走错。

## 先记住三件事

- USDT 只是名字一样，不同网络不是自动互通。
- 自托管钱包意味着控制权在你手里，也意味着备份责任在你手里。
- 区块链转账通常不可撤回，所以第一次一定小额测试。

## 我建议你按这个顺序读

1. [USDT 是什么](./markdown/what-is-usdt.md)
2. [如何购买 Tether USDt（USDT）](./markdown/how-to-buy-usdt.md)
3. [人在中国怎么买 USDT / BTC](./markdown/china-buy-crypto-notes.md)
4. [怎么选钱包](./markdown/how-to-choose-a-wallet.md)
5. [怎么发送 USDT](./markdown/how-to-send-usdt.md)
6. [TRC20、ERC20、BEP20 有什么区别](./markdown/usdt-networks-explained.md)
7. [TRON 能量指南](./markdown/tron-energy-guide.md)
8. [如何用 USDT 订阅 AI](./markdown/use-usdt-for-ai.md)

## 这份手册不做什么

- 不代客买币
- 不提供投资建议
- 不承诺哪个钱包适合所有人
- 不把 affiliate 排名伪装成客观结论

## 如果你只打算先读一篇

那就先读这篇：

- [USDT 是什么](./markdown/what-is-usdt.md)

它会先把最基础、但也最容易被误解的那层东西讲明白。很多新手不是输在不会操作，而是输在还没搞清楚 USDT 在整个流程里到底扮演什么角色。

## 下一篇

读完这一页，建议直接接下一篇：

➡ [USDT 是什么](./markdown/what-is-usdt.md)

---

<details>
<summary>展开看完整目录</summary>

### 中国用户专题
- [人在中国怎么买 USDT / BTC](./markdown/china-buy-crypto-notes.md)
- [在中国买币最容易踩的 7 个坑](./markdown/china-7-common-mistakes.md)
- [C2C / OTC 到底在怕什么](./markdown/china-c2c-otc-risks.md)
- [第一次别碰的事](./markdown/china-first-time-donts.md)

### TRON / TRC20
- [TRON 能量指南](./markdown/tron-energy-guide.md)
- [为什么转 TRC20 USDT 要准备 TRX](./markdown/why-you-need-trx-to-send-usdt.md)
- [TRON 带宽和能量是什么](./markdown/tron-bandwidth-and-energy.md)
- [TRON 能量怎么获得](./markdown/how-to-get-tron-energy.md)
- [TRC20 USDT 手续费怎么省](./markdown/how-to-reduce-trc20-usdt-fees.md)

### Use Cases
- [USDT 可以拿来做什么](./markdown/what-can-you-do-with-usdt.md)
- [如何用 USDT 订阅 AI](./markdown/use-usdt-for-ai.md)
- [如何用 USDT 买 eSIM 和 VPN](./markdown/use-usdt-for-esim-and-vpn.md)
- [出国旅游时，USDT 有哪些实际用途](./markdown/use-usdt-for-travel.md)
- [用 USDT 做跨境小额结算前要先确认什么](./markdown/use-usdt-for-cross-border-payments.md)

### Trust
- [How We Review Wallets and Apps](./markdown/how-we-review-wallets-and-apps.md)
- [Editorial Policy / Disclosure](./markdown/editorial-policy.md)
- [Changelog](./markdown/changelog.md)

</details>

---

## 本地开发与发布

站点是 Jekyll 项目，源文件在 `site/`，构建产物在 `docs/`，GitHub Pages 直接把 `docs/` 当静态文件发布。

**首次安装依赖**

```bash
bundle install
```

**本地预览**

```bash
bundle exec jekyll serve --port 4000 --host 127.0.0.1
# 打开 http://127.0.0.1:4000/usdthub/（baseurl 是 /usdthub，不能漏）
```

**发布到线上**

```bash
./scripts/deploy.sh                       # 默认 commit message: "Rebuild site"
./scripts/deploy.sh "update wallet guide" # 自定义 message
```

`deploy.sh` 会做完整流程：拒绝在 `jekyll serve` 还在跑时部署（避免 localhost URL 污染）→ 用 `JEKYLL_ENV=production` 重新 build → 跑 `scripts/check_site.py` 校验链接和 meta → 检查每个页面都引用了线上 CSS、没有 localhost 泄漏 → 提交 `docs/` 并 push → 轮询 https://makoshan.github.io/usdthub/ 直到新版本上线。任何一步失败都会中止并报错。
