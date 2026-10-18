# luost26/academic-homepage 版本

基于 [luost26/academic-homepage](https://github.com/luost26/academic-homepage)（MIT）定制，
仓库 `l1jiahao/l1jiahao.github.io`，**GitHub Pages 原生 Jekyll 构建**（无需 Actions）。

已上线：https://l1jiahao.github.io

## 数据在哪

| 想改什么 | 改哪个文件 |
|---|---|
| 姓名 / 邮箱 / 职位 / 社交链接 | `_data/profile.yml` |
| 个人简介段落 | `_data/profile.yml` → `short_bio` |
| 学历 / 经历 / 获奖 | `_data/profile.yml` → `education` / `experience` / `awards` |
| 首页显示哪些区块 | `_data/display.yml` |
| 顶部导航 | `_data/navigation.yml` |
| 作者加粗 / 主页链接 | `_data/authors.yml` |
| 新增论文 | `_publications/<年份>/<日期>-<slug>.md` |
| 新增动态 | `_news/<日期>-<slug>.md` |

## 相对原模板的改动

| 改动 | 原因 |
|---|---|
| 所有 CSS/JS/字体本地化到 `assets/lib/` | 原模板依赖 10 个海外 CDN，国内首屏慢 |
| 目录名 `assets/vendor` → `assets/lib` | **模板 `.gitignore` 里有 `vendor/`（给 Bundler 用的），会把 `assets/vendor/` 整个忽略，文件根本不会进仓库** |
| 移除 KaTeX | 页面没有 `$...$` 数学公式，省约 1MB |
| 移除 academicons / github-buttons | 没有任何组件实际使用 |
| 字体只保留 Lato + Source Code Pro 的 latin 子集 | 原来白加载 Fira Sans + 各语言子集（28 个 `@font-face` 砍到 9 个） |
| 删除 `jekyll-email-protect` | 不在 GitHub Pages 白名单，未知 filter 被**静默跳过**，构建成功但加密失效 |
| 新增 `assets/js/email.js` | 邮箱拆成 `data-email-user` / `data-email-domain`，页面加载后拼装 |
| 新增 SEO 标签 | 原模板无 `description` / `og:*` / `canonical` |
| 新增 `jekyll-sitemap` + `robots.txt` | 学术主页最需要被搜到 |
| 删除 blog / showcase / 示例内容 | 不用，且会带来额外 CDN 引用 |

## 论文库（7 篇）

| 年份 | 会议/期刊 | 标题 | 本人位次 | 首页精选 |
|---|---|---|---|---|
| 2026 | ICLR | SAVE: A Generalizable Framework for Multi-Condition Single-Cell Generation with Gene Block Attention | 一作 | ✅ |
| 2025 | IJCAI | Conditional causal representation learning for heterogeneous single-cell RNA data integration and prediction | 二作 | ✅ |
| 2025 | BIBM | scDiformer: A Difference-Aware Transformer for Time-Series Single-Cell Gene Expression Forecasting | 三作 | — |
| 2024 | IEEE/ACM TCBB | Deep learning in gene regulatory network inference: a survey | 二作 | ✅ |
| 2024 | Briefings in Bioinformatics | stDiff: a diffusion model for imputing spatial transcriptomics through single-cell transcriptomics | 二作 | ✅ |
| 2022 | Sensors | Fruchterman–Reingold hexagon empowered node deployment in wireless sensor network application | 一作 | ✅ |
| 2022 | Space Weather | The short-time prediction of the energetic electron flux in the planetary radiation belt based on stacking ensemble-learning algorithm | 三作 | — |

改「是否上首页」只需改对应 md 里的 `selected: true/false`。

## 新增的论文字段

模板原生只有 `title/pub/pub_date/authors/links`。我扩了 `publication_item.html`，支持：

```yaml
volume: "21"
number: "6"
pages: "2089–2101"      # 真正的页码范围
pub_post: ", Art. no. 5179"   # 文章编号，不是页码时用这个
publisher: "IEEE"
```

渲染成：*期刊*, vol. 21, no. 6, pp. 2089–2101, 2024 · IEEE

> `Sensors` 与 `Briefings in Bioinformatics` 的两篇给的 `bbae171` / `5179` 是**文章编号**，
> 不是页码范围，所以用 `pub_post: ", Art. no. ..."` 而不是 `pages`。

## 封面图

`assets/images/covers/` 下 7 个 SVG，每个 1.2KB。

- 按会议/期刊生成：色块渐变 + 同心环 + 期刊名 + 年份，全站统一视觉
- 颜色按会议固定（ICLR 深蓝、IJCAI 青绿、BIBM 紫、BIB 酒红……）
- 同心环圆心按文件名的 SHA-256 分散，所以每张图都不一样

**为什么不放出版商原图**：Elsevier/IEEE/Wiley 的封面有版权，热链或转载都不合适。
如果你有论文里自己画的**方法图**，直接换成 `cover: /assets/images/covers/你的图.png` 效果最好。

## 待你确认 / 补全

| 项 | 当前值 | 说明 |
|---|---|---|
| `Education.dept` | 空 | 专业名称未知，未填 |
| `Education.date` | `2026` | 只知道已毕业；建议改成 `2023 – 2026` 这类区间 |
| `Education.name` | Fudan University | 如果硕士不是复旦，务必改 |
| 首页 About 两段 | 我按仓库内容写的 | **必须按自己语气改写** |
| News 第 1 条日期 | `Sep 01` | 论文接收月份无依据，请核准 |
| 论文封面 | 生成的矢量图 | 想换成真实方法图随时给图 |
| 论文链接 | 只有 SAVE 有 Paper/Code | 其余 6 篇没有 DOI，我没有编造 |
| `gscholar` / `orcid` / `cv_link` | 注释状态 | 有就填，侧栏会多出对应图标 |

## 本地调试（重要）

本机 Ruby 是 2.6，`ffi` 要求 ≥3.0，**本地 `bundle exec jekyll serve` 跑不起来**。三个选择：

1. 直接推到 GitHub，等 Pages 构建（约 40–60 秒），改完刷新页面
2. `brew install ruby` 后在仓库内 `bundle install && bundle exec jekyll serve`
3. 启动 Docker，用 `jekyll/jekyll` 镜像

## 换主题 / 加功能时的注意

- 新增的 `_includes`、`_layouts` 里不要再写 CDN 链接，统一放 `assets/lib/` 并用
  `{{ '/assets/lib/...' | relative_url }}`
- `_config.yml` 的 `plugins` 只能是 GitHub Pages 白名单内的（`jekyll-sitemap`、
  `jekyll-seo-tag`、`jekyll-feed` 等安全；`jekyll-scholar`、`jekyll-email-protect` 不行）
- `_config.yml` 里 `baseurl` 必须为空（用户站点在根路径）；将来搬去做项目站点才改成 `/repo`
