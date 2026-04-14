# USDT 新手手册

一个面向新手的公开手册仓库。

目标不是做“返佣导航站”，而是做成一个能顺着读完并真正完成买、存、转、用的公开笔记库。

一句话定位：
- 中文：USDT 新手手册：教你买、存、转、用
- English: A beginner-friendly guide to buying, storing, sending, and using USDT

## 两种阅读方式

### 1. GitHub Pages / HTML 版本
适合：像网站一样连续阅读。

主要入口：
- `index.html`
- `start-here.html`
- `how-to-buy-usdt.html`
- `china-buy-crypto-notes.html`

如果启用 GitHub Pages，默认首页就是：
- `index.html`

### 2. GitHub 仓库 / Markdown 版本
适合：直接在 GitHub 里看内容，像看 handbook / notes 仓库。

Markdown 镜像目录：
- `markdown/README.md`
- `markdown/index.md`
- `markdown/how-to-buy-usdt.md`
- `markdown/china-buy-crypto-notes.md`

说明：
- HTML 版本用于 Pages / 本地预览
- Markdown 版本用于 GitHub 仓库内直接阅读
- Markdown 镜像由脚本自动从 HTML 导出，避免手工维护两套正文

## 主要页面

### 首页与入口
- `index.html` — 手册首页
- `start-here.html` — 从哪里开始
- `changelog.html` — 更新记录

### 基础章节
- `what-is-usdt.html` — USDT 是什么
- `how-to-buy-usdt.html` — 如何购买 Tether USDt（USDT）
- `how-to-choose-a-wallet.html` — 怎么选钱包
- `how-to-send-usdt.html` — 怎么发送 USDT
- `usdt-networks-explained.html` — TRC20、ERC20、BEP20 有什么区别

### 中国用户专题
- `china-buy-crypto-notes.html` — 人在中国怎么买 USDT / BTC
- `china-7-common-mistakes.html` — 在中国买币最容易踩的 7 个坑
- `china-c2c-otc-risks.html` — C2C / OTC 到底在怕什么
- `china-first-time-donts.html` — 第一次别碰的事

### TRON / TRC20
- `tron-energy-guide.html` — TRON 能量指南
- `why-you-need-trx-to-send-usdt.html` — 为什么转 TRC20 USDT 要准备 TRX
- `tron-bandwidth-and-energy.html` — TRON 带宽和能量是什么
- `how-to-get-tron-energy.html` — TRON 能量怎么获得
- `how-to-reduce-trc20-usdt-fees.html` — TRC20 USDT 手续费怎么省

### Use Cases
- `what-can-you-do-with-usdt.html` — USDT 可以拿来做什么
- `use-usdt-for-ai.html` — 如何用 USDT 订阅 AI
- `use-usdt-for-esim-and-vpn.html` — 如何用 USDT 买 eSIM 和 VPN
- `use-usdt-for-travel.html` — 出国旅游时，USDT 有哪些实际用途
- `use-usdt-for-cross-border-payments.html` — 用 USDT 做跨境小额结算前要先确认什么

### Trust
- `how-we-review-wallets-and-apps.html` — 钱包与应用评测原则
- `editorial-policy.html` — 编辑原则与披露

## GitHub Pages 相关文件
- `_config.yml` — GitHub Pages 基础配置
- `index.html` — Pages 首页

## Markdown 镜像与导出
- `markdown/` — 仓库阅读用 Markdown 镜像
- `scripts/export_markdown_mirrors.py` — 从 HTML 导出 Markdown 镜像

导出命令：
- `python3 scripts/export_markdown_mirrors.py`

## 本地预览
- `python3 -m http.server 8008`
- 然后访问 `http://127.0.0.1:8008/index.html`

## 基础校验
- 站点检查文档：`QA-CHECKLIST.md`
- 链接检查脚本：`scripts/check_site.py`

## 内容原则
- 先解释问题，再推荐工具
- 第一人称，但不过度表演“亲历感”
- 先风险提醒，再给默认路径
- 具体平台名要有，但不能写成硬广
- 中国用户语境下，重点写支付风控、问题资金、错误网络、错误路径
- 推荐工具用：`beginner-friendly option` / `editor’s pick`
- 避免：“最强”“闭眼冲”“稳赚”

## 当前状态
- HTML 版本：已可本地预览
- Markdown 镜像：已生成，可直接在 GitHub 中阅读
- 本地内部链接：已做检查，无缺失本地链接
- 第一版：已经可作为完整公开草案使用
