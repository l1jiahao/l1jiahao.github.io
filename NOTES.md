# luost26/academic-homepage 版本

基于 [luost26/academic-homepage](https://github.com/luost26/academic-homepage)（MIT）定制，
目标仓库 `l1jiahao/l1jiahao.github.io`，构建方式为 **GitHub Pages 原生 Jekyll 构建**（无需 Actions）。

## 数据在哪

| 想改什么 | 改哪个文件 |
|---|---|
| 姓名 / 邮箱 / 职位 / 社交链接 | `_data/profile.yml` |
| 个人简介段落 | `_data/profile.yml` → `short_bio` |
| 首页显示哪些区块 | `_data/display.yml` |
| 顶部导航 | `_data/navigation.yml` |
| 作者加粗 / 主页链接 | `_data/authors.yml` |
| 新增论文 | `_publications/<年份>/<日期>-<slug>.md` |
| 新增动态 | `_news/<日期>-<slug>.md` |

## 需要你替换 / 确认

| 项 | 当前值 | 说明 |
|---|---|---|
| `positions` | `Fudan University` / `Shanghai, China` | 没有写具体头衔（PhD student 等），**请补** |
| `short_bio` | 我根据你的仓库写的两段 | 必须按自己语气改写 |
| 论文 `date` | `2026-09-01` | 只用于排序；实际接收月份请改成准确值 |
| News 第 1 条日期 | `2026-09-01` | 同上 |
| `gscholar` | 注释状态 | 填入 Scholar ID 后侧栏会出现图标 |
| `orcid` / `cv_link` | 注释状态 | 有就填 |
| `education` / `awards` | **未启用** | 见下 |

### 为什么 education 没开

`_data/display.yml` 里 `show_experience: false`。原因：

1. 我不确定你的具体身份（博士/硕士/研究员）和入学年份
2. 模板的 education 条目**必须有 logo 图片**，否则显示裂图

要启用：在 `_data/profile.yml` 补 `education:` 段落（`name` / `logo` / `position` / `date`），
把 logo 图片放进 `assets/images/badges/`，再把 `show_experience` 改成 `true`。

## 关于 CDN（重要）

这个模板从以下海外 CDN 加载资源：

```
cdnjs.cloudflare.com      Bootstrap / FontAwesome / academicons / jQuery
fonts.googleapis.com      Lato / Fira Sans / Source Code Pro
cdn.jsdelivr.net          KaTeX
unpkg.com                masonry / imagesloaded
```

**国内访问 cdnjs 和 unpkg 经常很慢甚至超时**，首屏可能要几秒。如果在意，
可以后续把 `_layouts/default.html` 里的这些 `<link>`/`<script>` 换成本地文件（约 1.2MB），
代价是仓库变大、但加载稳定。要我做就说。

## 部署

```bash
cd ~/Code/github_manager/site-luost26
git init -b main && git add -A
git commit -m "academic homepage"
gh repo create l1jiahao/l1jiahao.github.io --public --source . --push
```

然后 Settings → Pages → Source 选 `Deploy from a branch` → `main` / `/`。

> `_config.yml` 里 `baseurl` 必须是空字符串（用户站点在根路径）；
> 如果是项目站点（`username.github.io/repo`），则要设成 `/repo`。

## 构建失败的排查顺序

1. 仓库 Settings → Pages 看报错
2. Actions 标签页里 `pages-build-deployment` 的日志
3. 常见原因：`_config.yml` 出现**不在 GitHub Pages 白名单**里的插件（本模板用的
   `jekyll-email-protect` 实测可用；`jekyll-scholar` 之类不行）
