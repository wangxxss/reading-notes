# docmd 完全指南：介绍与入门

> 一个零配置、AI 原生的静态文档站点生成器。一条命令，把一堆 Markdown 变成生产级文档网站。
>
> - 官网：https://docmd.io/zh/
> - 仓库：https://github.com/docmd-io/docmd
> - 文档：https://docs.docmd.io/zh/

---

## 一、docmd 是什么

docmd 是一个**开源、零配置**的文档引擎，专门把 Markdown 文件转换成生产就绪的文档站点。它的定位类似 Docusaurus、VitePress、MkDocs，但核心理念是「更轻、更快、更省心，并且为 AI 时代而生」。

它的三个关键差异点：

1. **零配置起步** —— 不需要写任何配置文件就能跑起来，导航直接根据**文件夹结构**自动生成。
2. **极致轻量** —— 运行时 JS 大约只有 **18 KB**，产物是 SEO 友好的静态 HTML，但导航有单页应用（SPA）级别的速度。
3. **AI 原生** —— 内置 MCP server、自动生成 `llms.txt` 与结构化上下文文件、给 IDE agent 用的 skill 集，还有页面上一键「复制内容到 AI 对话」的按钮。

### 它适合谁

- 开源项目的 README / 文档站
- 企业内部知识库
- API 参考文档（内置 OpenAPI 渲染）
- 技术指南、教程、变更日志（changelog）

---

## 二、核心特性一览

| 类别 | 能力 |
|------|------|
| **上手** | 零配置；自动从目录结构生成导航；无需 frontmatter |
| **性能** | 运行时 ~18KB；静态 HTML + SPA 导航；保存后亚 200ms 增量重建 |
| **搜索** | 内置全文模糊搜索，**100% 离线**，无需任何外部 API |
| **国际化** | 原生多语言（i18n）与多语言搜索索引 |
| **版本** | 多版本文档管理（versioning） |
| **主题** | 明暗主题切换、自定义 CSS、无框架锁定（不依赖 React/Vue） |
| **AI** | MCP server、`llms.txt` 上下文生成、agent skill、一键复制到 AI |
| **企业** | monorepo workspace、插件架构 |
| **迁移** | 一键从 Docusaurus / VitePress / MkDocs / Starlight 导入 |
| **部署** | 自动生成 Docker / NGINX / Caddy / Vercel / Netlify 配置 |

### 技术栈
- 语言：TypeScript（主）+ JavaScript + CSS + EJS 模板
- 运行环境：**Node.js 18+**，也支持 Docker
- 产物：优化过的静态站点（含 sitemap、canonical URL）

---

## 三、快速开始（5 分钟）

### 1. 环境要求
- Node.js **18 或更高版本**（本地构建需要）

### 2. 最快体验（无需安装）

```bash
npx @docmd/core dev
```

引擎会自动扫描项目里的 Markdown 文件（依次查找 `docs/`、`src/docs/`、`documentation/`、`content/`，或根目录下任意 `.md`），然后在 `http://localhost:3000` 启动开发服务器。如果 3000 端口被占用，会自动切换到下一个可用端口。

### 3. 推荐：本地安装并初始化（适合长期项目）

```bash
# 作为开发依赖安装
npm install -D @docmd/core

# 初始化项目（生成示例结构）
npx docmd init
```

> 也支持 pnpm / yarn / bun，例如 `pnpm add -g @docmd/core`、`bunx @docmd/core dev`。

### 4. 全局安装（任意目录可用）

```bash
npm install -g @docmd/core
# 之后可在任何项目里直接用：
docmd dev
docmd build
```

### 5. Docker 方式

```bash
docker run -p 3000:3000 ghcr.io/docmd-io/docmd:0.8.7
```

---

## 四、项目结构

最简结构如下，**导航根据文件树自动生成，无需手写菜单**：

```text
my-docs/
├── docs/                ← Markdown 文档放这里
│   ├── index.md
│   ├── getting-started.md
│   └── guides/
│       └── advanced.md
├── assets/              ← 图片和静态资源
├── docmd.config.json    ← 可选配置文件
└── package.json
```

约定：
- **侧边栏导航**：按文件夹与文件的层级自动嵌套生成。
- **页面标题**：自动从每个页面的第一个 `# H1` 提取。
- **首页**：`docs/index.md`。

---

## 五、写第一篇文档

新建 `docs/index.md`，最简单的写法连 frontmatter 都不需要：

```markdown
# 欢迎使用我的文档

这是首页内容，直接写 **Markdown** 即可。
```

如需更精细控制，可加 frontmatter（YAML 头部）：

```markdown
---
title: 快速开始
description: 5 分钟搭好你的文档站
---

# 快速开始

正文内容……
```

---

## 六、增强内容：容器（Containers）语法

docmd 在标准 Markdown 之上提供了一套统一的「容器」语法，用来做提示框、选项卡、卡片、步骤等**富布局，且无需写 HTML**。

### 统一语法结构

```text
::: 类型 "可选标题"
这里是内容，支持 **Markdown**、图片，以及深层嵌套。
:::
```

### 常用容器类型

| 容器 | 关键字 | 用途 |
|------|--------|------|
| 标注框 | `callout` | 提示、警告、提醒等语义化高亮 |
| 卡片 | `card` | 功能网格、有边框的结构块 |
| 网格 | `grids` | 自动多列布局 |
| 选项卡 | `tabs` | 多平台说明的可切换面板 |
| 步骤 | `steps` | How-to 指南的数字时间线 |
| 折叠块 | `collapsible` | FAQ、可折叠的手风琴 |
| 按钮 | `button` | 突出的行动号召（CTA）导航链接 |
| 标签 | `tag` | 版本/状态彩色标签 |
| 英雄区 | `hero` | 落地页大标题区块 |
| 嵌入 | `embed` | 安全嵌入视频、社交、交互内容 |
| 变更日志 | `changelog` | 基于时间线的发布说明 |

### 示例：标注框

```text
::: callout info
这是一条信息提示，支持 **加粗** 等 Markdown。
:::
```

> 提示：docmd 兼容 VitePress / Docusaurus 的语法别名，例如 `:::tip`、`:::warning`，也支持无空格写法 `:::tabs`。

### 示例：嵌套组合

容器支持「无限嵌套」，可自由组合：

```text
::: card "架构概览"
    ::: callout info
        此模块使用异步 I/O 流水线。
    :::
    ::: button "深入核心引擎" /advanced/developer-guide
:::
```

---

## 七、配置文件（可选）

零配置即可起步。需要自定义时，在项目根目录创建 `docmd.config.json`（也支持 `.ts` / `.js`，后两者可写动态逻辑）：

```json
{
  "title": "My Project",
  "url": "https://docs.myproject.com",
  "src": "./docs",
  "out": "./site"
}
```

常用字段：

- `title`：站点标题
- `url`：站点正式地址（用于 SEO / canonical / sitemap）
- `src`：Markdown 源目录（默认自动探测 `docs/` 等）
- `out`：构建输出目录（默认 `./site`）

> `.ts` / `.js` 配置可以使用动态值（例如读环境变量、按条件启用插件）。

使用编程式 API（Node.js，支持 CommonJS 与 ESM）：

```javascript
import { build } from '@docmd/core';

await build('./docmd.config.json', { isDev: false });
```

---

## 八、插件系统

### 核心插件（默认包含）

| 插件 | 作用 |
|------|------|
| `search` | 离线全文搜索 |
| `seo` | SEO 元数据 |
| `sitemap` | 生成 XML sitemap |
| `git` | 提交历史 / 最后更新时间 |
| `analytics` | 接入统计分析 |
| `llms` | 生成 AI 上下文（`llms.txt`） |
| `mermaid` | Mermaid 图表 |
| `openapi` | 渲染 OpenAPI 规范 |

### 可选插件（按需安装）

| 插件 | 作用 |
|------|------|
| `pwa` | PWA 离线支持 |
| `threads` | 讨论 / 评论线程 |
| `math` | KaTeX / LaTeX 数学公式 |

安装可选插件：

```bash
docmd add <plugin-name>
# 例如
docmd add math
```

---

## 九、AI 原生能力（docmd 的招牌）

docmd 把「文档喂给 AI」做成了一等公民：

- **`llms.txt` 与结构化上下文**：构建时自动生成，方便 LLM 抓取你的文档。
- **MCP server**：把文档作为工具暴露给 AI agent。

  ```bash
  docmd mcp   # 通过 stdio 以 MCP server 运行
  ```

- **Agent skills**：为 IDE agent 提供模块化技能集。
- **一键复制到 AI**：页面上提供按钮，把内容直接复制进 AI 对话窗口。

---

## 十、CLI 命令速查

| 命令 | 作用 |
|------|------|
| `docmd dev` | 启动本地开发服务器（热更新） |
| `docmd build` | 构建优化后的静态站点用于部署 |
| `docmd live` | 打开浏览器版「在线编辑器」 |
| `docmd init` | 初始化项目结构 |
| `docmd migrate` | 从 Docusaurus / VitePress / MkDocs / Starlight 导入 |
| `docmd deploy` | 生成部署配置（Docker / NGINX / Caddy / Vercel / Netlify） |
| `docmd validate` | 检查所有站内链接是否有效 |
| `docmd add <name>` | 安装插件或模板 |
| `docmd mcp` | 以 MCP server 运行（stdio） |

---

## 十一、构建与部署

### 1. 本地构建

```bash
npx @docmd/core build
```

产物是高度优化的静态站点（默认输出到 `./site/`，可用 `out` 字段修改），可部署到任意静态托管：Vercel、Cloudflare Pages、Netlify、GitHub Pages，或自有服务器。

### 2. 生成部署配置

```bash
docmd deploy
```

可一键生成 Docker / NGINX / Caddy / Vercel / Netlify 的配置文件。

### 3. 部署前自检

```bash
docmd validate   # 校验所有内部链接，避免死链
```

---

## 十二、从其他工具迁移

如果你已经在用 Docusaurus、VitePress、MkDocs 或 Starlight，可一键导入：

```bash
docmd migrate
```

---

## 十三、典型工作流小结

```bash
# 1. 初始化
npm install -D @docmd/core
npx docmd init

# 2. 写文档（在 docs/ 下增删 .md，导航自动更新）
npx docmd dev          # 浏览器打开 http://localhost:3000 实时预览

# 3. 校验 + 构建
npx docmd validate
npx docmd build        # 输出到 ./site/

# 4. 部署
npx docmd deploy       # 生成所需平台的部署配置
```

---

## 参考链接

- 官网（中文）：https://docmd.io/zh/
- 文档（中文）：https://docs.docmd.io/zh/
- GitHub：https://github.com/docmd-io/docmd
- 容器语法：https://docs.docmd.io/zh/content/containers/
- 插件用法：https://docs.docmd.io/zh/plugins/usage/
- CLI 命令：https://docs.docmd.io/zh/api/cli-commands/
- MCP server：https://docs.docmd.io/zh/api/mcp-server/

> 注：docmd 仍在快速迭代（示例镜像版本 `0.8.7`），个别命令默认值或字段可能随版本调整，最终以官方文档为准。
