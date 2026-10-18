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

## 待你确认 / 补全

| 项 | 当前值 | 说明 |
|---|---|---|
| `Education.dept` | 空 | 专业名称未知，未填 |
| `Education.date` | `2026` | 只知道已毕业；建议改成 `2023 – 2026` 这类区间 |
| `Education.name` | Fudan University | 如果硕士不是复旦，务必改 |
| 首页 About 两段 | 我按仓库内容写的 | **必须按自己语气改写** |
| News 第 1 条日期 | `Sep 01` | 论文接收月份无依据，请核准 |
| 论文封面 | 模板自动生成的彩色气泡图 | `sc-save` 仓库里没有任何图片，想放真图需你提供方法图 |
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
