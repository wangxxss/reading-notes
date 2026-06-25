# 写文档还在折腾 Docusaurus？这个零配置工具，一行命令就出活

> 如果你也被「搭个文档站」折磨过——装一堆依赖、改一堆配置、跑起来还卡——这篇值得花 5 分钟看看。

---

## 先说结论

最近发现一个挺香的开源工具：**docmd**。

一句话介绍它：**把一堆 Markdown 文件，一行命令变成生产级文档网站。零配置。**

```bash
npx @docmd/core dev
```

就这一行，浏览器打开 `http://localhost:3000`，你的文档站就跑起来了。不用建配置文件，不用写导航菜单——它会自动扫描你的 Markdown，按文件夹结构生成侧边栏。

是不是有点东西？继续往下看。

- 官网：https://docmd.io/zh/
- GitHub：https://github.com/docmd-io/docmd

---

## 它到底强在哪

市面上文档工具不少：Docusaurus、VitePress、MkDocs……docmd 凭什么值得你换？

三个字：**轻、快、新**。

**轻** —— 运行时 JavaScript 只有约 **18KB**。什么概念？比同类小一大截。产物是纯静态 HTML，SEO 友好，但翻页又有单页应用那种丝滑感。

**快** —— 改完文档保存，**亚 200 毫秒**就重新构建完。基本是「保存即所见」。

**新** —— 这是它最大的差异点：**为 AI 时代而生**。它能自动生成喂给大模型的上下文文件，内置 MCP server，还能让 AI agent 直接读你的文档。这个后面单独讲。

---

## 五分钟，从零搭一个文档站

### ① 准备环境

只需要 **Node.js 18+**。

### ② 初始化项目

```bash
npm install -D @docmd/core
npx docmd init
```

### ③ 写文档

在 `docs/` 文件夹里随便建个 `index.md`：

```markdown
# 欢迎来到我的文档

直接写 Markdown 就行，
连配置都不用碰。
```

目录长这样，导航会**自动**按这个结构生成：

```text
my-docs/
├── docs/
│   ├── index.md
│   └── guides/
│       └── advanced.md
├── assets/          ← 图片放这
└── package.json
```

### ④ 跑起来

```bash
npx docmd dev
```

打开 `http://localhost:3000`，搞定。是不是比想象中简单太多？

---

## 不止 Markdown：好看的排版也能一行搞定

写技术文档总免不了要「提示框」「选项卡」「步骤条」这些花活。一般工具要么写 HTML，要么记一堆组件。

docmd 用一套统一的「容器」语法，**不写一行 HTML** 就能做出来：

```text
::: callout info
这是一个信息提示框，支持 **加粗** 等所有 Markdown 语法。
:::
```

它内置了一整套常用块：

- 📌 **callout** —— 提示 / 警告 / 提醒
- 🗂 **tabs** —— 多平台说明切换面板
- 🃏 **card** —— 功能卡片网格
- 🪜 **steps** —— How-to 教程的步骤时间线
- ▸ **collapsible** —— FAQ 折叠手风琴
- 🔘 **button** —— 突出的行动按钮
- 🏷 **tag** —— 版本 / 状态彩色标签

而且容器能**任意嵌套**，卡片里套提示框、提示框里再套按钮都行。

贴心的是，它还兼容 VitePress / Docusaurus 的写法（比如 `:::tip`、`:::warning`），老用户几乎零迁移成本。

---

## 真正的杀手锏：AI 原生

这才是 docmd 最「2025」的地方。

它把「让 AI 读懂你的文档」做成了开箱即用的能力：

- 🤖 **自动生成 `llms.txt`** —— 构建时自动产出结构化上下文，方便大模型抓取理解你的整套文档。
- 🔌 **内置 MCP server** —— 一行 `docmd mcp`，就能把你的文档作为「工具」暴露给 AI agent，让 Claude、Cursor 这类 agent 直接查阅。
- 🧩 **Agent skills** —— 给 IDE 里的 AI 助手提供模块化技能。
- 📋 **一键复制到 AI** —— 文档页面上直接有按钮，把内容塞进 AI 对话框。

简单说：你写的文档，不只是给人看的，也是给 AI 看的。这在 AI 编程越来越普及的今天，价值会越来越大。

---

## 还有这些「企业级」能力

别看它上手简单，该有的一个不少：

- 🔍 **离线全文搜索** —— 内置模糊搜索，100% 离线，不依赖任何外部 API
- 🌍 **多语言 i18n** —— 原生支持，连搜索索引都是多语言的
- 🕐 **多版本文档** —— v1 / v2 文档分版本管理
- 🎨 **明暗主题 + 自定义 CSS** —— 不锁定 React/Vue，纯静态
- 📦 **monorepo 支持** + 插件体系（数学公式、Mermaid 图表、OpenAPI、PWA 等）

---

## 已经在用别的工具？一行命令搬家

最怕的就是迁移成本。docmd 直接给你兜底:

```bash
docmd migrate
```

支持从 **Docusaurus / VitePress / MkDocs / Starlight** 一键导入。

写完要上线也简单:

```bash
docmd build      # 构建静态站点
docmd deploy     # 自动生成 Docker/NGINX/Vercel/Netlify 等部署配置
```

产物能丢到任何静态托管：Vercel、Netlify、Cloudflare Pages、GitHub Pages，或你自己的服务器。

---

## 一张图记住整个流程

```bash
npm install -D @docmd/core   # 1. 安装
npx docmd init               # 2. 初始化
npx docmd dev                # 3. 写文档 + 实时预览
npx docmd build              # 4. 构建
npx docmd deploy             # 5. 部署
```

五步，从零到上线。

---

## 写在最后

如果你正打算：

- 给开源项目搭个文档站
- 整理团队内部知识库
- 写 API 文档 / 技术教程

那 docmd 真的值得试一试。**零配置上手、产物超轻、还为 AI 时代做了准备**——花 5 分钟，可能就帮你省下未来几天的折腾。

感兴趣的话，去官网逛逛 👇

🔗 **官网**：https://docmd.io/zh/
⭐ **GitHub**（觉得不错就给个 Star）：https://github.com/docmd-io/docmd

---

*觉得有用，欢迎点赞、在看、转发给需要的朋友。我们下期见 👋*
