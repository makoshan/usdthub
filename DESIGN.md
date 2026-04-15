# DESIGN.md — USDT HUB设计系统

这是一份写给自己和未来协作者的设计系统说明。目标：在新增文章或改模板时，不要引入与现有语言冲突的元件。

## 核心原则

1. **极简优先。** 没有装饰元素。没有 hero SVG，没有 icon-in-circle，没有渐变背景，没有 emoji 作为设计元素。
2. **链接是 first-class 公民。** 整本手册靠相互跳转活，链接必须明显可识别。
3. **中文长读优化。** 760px 单栏、1.65 行高、-apple-system + PingFang SC 字体栈。
4. **内容密度高于视觉节奏。** 不追求发布会式的 Hero + 留白，追求 Wikipedia / Gwern 式的信息密度。
5. **减法默认。** 每次改动问一句「能不能不加」。

## 参考

- 字体和字重参考了 [openai.com](https://openai.com) 的排版（H1/H2/H3 统一 500 字重，紧凑字距）。只借 typographic token，不借他们的结构和 Hero 逻辑。
- 链接体感参考 NYTimes / Stripe（默认浅色下划线，hover 变实色）。
- 内容密度参考 Wikipedia / Gwern.net。

## Token

### 颜色
| Token | 值 | 用途 |
|---|---|---|
| `--bg` | `#fff` | 页面背景 |
| `--text` | `#000` | 正文 + 标题（纯黑，不带蓝调）|
| `--muted` | `#6b7280` | 元信息、kicker、TOC 标题、footer |
| `--line` | `#e5e7eb` | 分隔线、边框、h2 顶边 |
| `--link` | `#2563eb` | 所有 inline 链接 |
| `--link-soft` | `#bfdbfe` | 链接默认下划线颜色（浅蓝）|
| `--soft` | `#f9fafb` | `.note`、`.toc`、表头背景 |
| `--warn-bg` | `#fff7ed` | `.risk` 卡片背景 |
| `--warn-line` | `#fed7aa` | `.risk` 边框 |

**永远不要引入**：紫色 / 洋红 / 渐变色 / 霓虹色。出现装饰色是系统失败信号。

### 字体
```css
font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text",
  "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
  "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
```
零下载。中英文都靠系统字体最高质量 fallback。**不要引入自托管字体**（中文字库太重，性价比负）。

### 字号 / 行高 / 字重
- 正文：17px / 1.65 / 400 / tracking -0.005em
- H1：`clamp(28px, 5vw, 40px)` / 1.15 / **500** / tracking -0.03em
- H2：`clamp(22px, 3vw, 28px)` / 1.25 / **500** / tracking -0.02em
- H3：18px / 1.3 / **500** / tracking -0.02em
- `.meta` / `.kicker` / `.toc-title`：13-14px / muted 色 / 500 字重 / uppercase 0.06em tracking

**所有标题字重统一 500**（不是 700/bold）。这是 OpenAI 同款的「克制高级感」——大字号本身就足够显眼，字重再重就变成广告。

### 间距
没有统一的 8/16/24 阶系。现状是按元件手工调（p 14、h2 上 40、table 16、note 16）。**不要发明间距 token**，读者感知不到那么细的差别，维护成本高。

### 容器
- `--max: 760px` 单栏。
- `.wrap { width: min(var(--max), calc(100% - 32px)); margin: 0 auto; }` 自动留 16px 安全边距。
- **不要引入多列 grid 布局用于正文**。760px 是中文长读的舒适上限。

## 元件

### 语义卡片（只有两个）
- `.note` — 中性补充，灰底边框。用于「提示 / 小结 / 默认起步方案」。
- `.risk` — 警告，橙底边框。用于「不要做 X / 合规风险 / 购买渠道硬规矩」。

**不要再发明第三种卡片。** 需要强调的信息要么进 `.note`，要么进 `.risk`，要么就是正文里的 `<strong>`。

### TOC
- `.toc` 块，灰底，圆角 8px。
- 出现在「超过 5 个 H2」的长文顶部。每个 H2 需要对应 id。
- **手写 TOC，不跑 JS**。维护成本换简单性。

### 目录列表
- `.chapter-list` — 首页和 Start Here 的章节导航。
- 每条一行 `display: block`。

### 按钮 / CTA
- **不做。** 这个手册的所有行动都是「跳到另一篇文章」，靠蓝色 inline 链接就够。
- 曾经尝试过 OpenAI 同款的 `.primary-link` pill 做「Start Here →」入口，最终撤掉了——手册不需要 hero CTA，nav 里已经有 Start Here 入口。加任何 pill / 按钮都会往 SaaS 感滑。

### 链接
- 默认：蓝色 `#2563eb` + 浅蓝下划线（`text-decoration-color: #bfdbfe`）+ 3px offset。
- Hover：下划线变实蓝色。
- **永远不要 `text-decoration: none`**。链接必须可扫到。

### 表格
- 全边框，左对齐，表头灰底。用来装「品牌对比 / 场景对照 / 历史事故 / 按金额分档」。
- 不要用表格做布局。

### .steps 有序列表
- 用于「收到硬件后要做的 6 件事」「评价维度」这类强顺序的操作清单。
- 每个 `<li>` 首个 `<strong>` 自动加粗，作为视觉锚。

### .source-grid / .source-card
- 出现在文章末尾的「参考资料」section。
- 自适应网格（`minmax(240px, 1fr)`），手机自动单列。
- 卡片内三件套：`.card-kicker`（小标签）/ `.card-title`（标题，蓝色）/ `.card-copy`（一句说明）。
- 只用于「外部资源引用」，不要用来做卡片化导航。

## 文末手写「相关章节」链接

每篇长文末尾放一个 `<h2>和手册其他章节的关系</h2>` + 3-5 条链接列表，说明这篇跟哪些上下游文章有关系，每条一句话。

这比机械的 Prev/Next 按钮好——读者能看出「为什么要跳过去」。cold-wallet 文末的「八、和手册其他章节的关系」是范本。

## AI Slop 黑名单（永不引入）

以下 10 个模式**在本手册任何页面出现就是 bug**：

1. 紫 / 洋红 / 蓝紫渐变背景或配色
2. 3 列对称 feature grid（icon + 粗标题 + 两行说明）
3. 彩色圆圈里放 icon 当装饰
4. 标题 / 正文全居中
5. 所有元素统一大圆角
6. 装饰性 blob、波浪分割线、浮动圆圈
7. Emoji 作为设计元素（emoji 在正文里作功能性标记 ✅❌ OK，但不作为装饰）
8. 左侧色边框的 card（`border-left: 3px solid <accent>`）
9. Hero 文案「Welcome to X / Unlock the power of...」
10. Hero → 3 features → 测评 → 价格 → CTA 同质节奏

## 流程约定

- 新文章一律用 `site/_layouts/default.html` 布局，不要写自定义 HTML 壳。
- 如需新 CSS 类，**先在 `site/assets/css/style.css` 里定义**，再在文章里用。规则：如果写 HTML 时引用了一个类，它必须已经在 CSS 里存在。
- `site/assets/css/style.css` 是 master，`docs/assets/css/style.css` 由 Jekyll build 生成或手动同步。
- 超过 5 个 H2 的长文**必须**在顶部加 `.toc`，并为每个 H2 添加 id（kebab-case 英文 slug）。
