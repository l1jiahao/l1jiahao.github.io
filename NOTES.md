# 学术主页维护

更新于 2026-11-07。基于 luost26/academic-homepage（MIT）定制。

- 线上：https://l1jiahao.github.io
- 源码：`l1jiahao/l1jiahao.github.io`，本地 `site-luost26/`。
- 部署：GitHub Pages 从 main 根目录原生构建；保留现有部署方式。
- `../site/` 是早期静态草稿，不是线上源码。

## 内容入口

| 内容 | 文件 |
|---|---|
| 身份、邮箱、简介、学历 | `_data/profile.yml` |
| 首页区块 | `_data/display.yml` |
| 导航、作者 | `_data/navigation.yml`、`_data/authors.yml` |
| 论文 | `_publications/<年份>/*.md` |
| 动态 | `_news/*.md` |

## 已完成

- 全部 CSS、JS、字体存于 `assets/lib/`，页面不依赖海外 CDN 加载这些资源。
- 邮箱由 `assets/js/email.js` 从两段属性拼接，替代 Pages 不支持的 `jekyll-email-protect`。
  这是简单混淆，不是加密；公开源码中仍有邮箱。
- description、canonical、Open Graph 标签、sitemap 和 robots.txt 已配置。
- 7 篇论文均已加入；6 篇使用 DOI，SAVE 使用 OpenReview、arXiv 和公开代码链接。
- 7 张封面均已替换为论文方法图；GRN survey 和 Space Weather 已于 10 月 18 日完成。
- 本科、硕士专业和年份已填充；本人于 11 月 7 日确认两者均为工学，使用 B.Eng. / M.Eng.。
- 学历在左侧个人信息卡中简要展示学校、学位和年份，独立 Education 卡片已关闭；About Me 不重复学历。
- SAVE 接收日及代码公开日尚未获得精确依据，动态只展示年份。
  `date_precision: year` 隐藏月日；`date: 2026-01-01` 仅用于年度分组。
  GitHub 的仓库创建时间不等于转为公开的时间。

## 论文库

| 年份 | 会议/期刊 | 简称 | 作者位次 | 首页精选 |
|---|---|---|---|---|
| 2026 | ICLR | SAVE | 一作 | 是 |
| 2025 | IJCAI | Conditional causal representation learning | 二作 | 是 |
| 2025 | BIBM | scDiformer | 三作 | 否 |
| 2024 | IEEE/ACM TCBB | Deep learning in GRN inference: a survey | 二作 | 是 |
| 2024 | Briefings in Bioinformatics | stDiff | 二作 | 是 |
| 2022 | Sensors | FR-HEX node deployment | 一作 | 是 |
| 2022 | Space Weather | Energetic electron flux prediction | 三作 | 否 |

首页选择由 `selected: true/false` 控制。`pages` 用于页码；文章编号使用
`pub_post: ", Art. no. ..."`。模板同时支持 volume、number 和 publisher。

## 封面

文件在 `assets/images/covers/`。布局为 600×400 白底、边框和底部会议信息条。
SAVE、IJCAI、stDiff、WSN、GRN survey、Space Weather 使用论文中的方法图；
scDiformer 使用此前提供图片的 panel c。

```bash
python3 -m venv /tmp/paper-cover-venv
/tmp/paper-cover-venv/bin/pip install pymupdf Pillow
/tmp/paper-cover-venv/bin/python scripts/make-cover.py paper.pdf \
  --venue ICLR --year 2026 --out assets/images/covers/cover-save.png
```

可用 `--figure 1 --page 3` 指定图；`--crop 0.34,0,1,1` 可截取 scDiformer 的 panel c。
使用图片时按论文及图像的适用许可处理；不把“方法图”视为自动免版权。

## 本地构建与预览

安装 Homebrew Ruby 3.3 后运行：

```bash
brew install ruby@3.3
./scripts/preview.sh build
./scripts/preview.sh
```

默认预览地址为 `http://127.0.0.1:4000`。脚本为当前进程选择 Ruby，不改系统 Ruby 或 shell 配置。
依赖安装到被忽略的 `vendor/bundle/`，Gemfile.lock 纳入版本控制。
Gemfile 对齐 https://pages.github.com/versions.json 中本项目使用的 Jekyll 3.10.0、
kramdown 2.4.0、kramdown-parser-gfm 1.1.0 和 jekyll-sitemap 1.4.0（2026-11-07 核对）。
预览服务使用 webrick；邮件混淆不依赖 Ruby 插件。

## 后续可选补充

Google Scholar、ORCID、CV 链接目前未填；有真实资料后再开启。精确新闻日期有可靠依据后再细化。

新增资源继续放入 `assets/lib/` 并使用 `relative_url`；用户主页的 `baseurl` 保持为空。
