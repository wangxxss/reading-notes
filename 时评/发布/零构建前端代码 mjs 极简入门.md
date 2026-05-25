
# 告别 Webpack/Vite？零构建前端代码 .mjs 极简入门

> 还在为配不上 `webpack.config.js` 而熬夜秃头？还在等 `npm install` 下载半个互联网？
> 今天，我们把构建工具一脚踢开，体验一把**"零构建"**的前端极客玩法！

## 01 前端的"基建之痛"

现代前端开发，上来就是一套连招：

```bash
npm init -y
npm install webpack webpack-cli babel-loader @babel/core ...
```

写个 `Hello World`，`node_modules` 比命都长。配置文件写了三百行，业务代码写了三行。

这时候你不禁会问：**我就写个简单页面，有必要这么兴师动众吗？**

其实，现代浏览器早就进化了。从 ES6 模块（ESM）被广泛支持那一刻起，**浏览器本身就自带了"模块化构建"能力**。而 `.mjs`，就是打开这扇大门的钥匙。

## 02 什么是 .mjs？

`.mjs` 并不是什么新语言，它仅仅是 **JavaScript ES Module 的文件扩展名**。

- `.js`：默认是 CommonJS 模块（Node.js 老规矩）或普通脚本。
- `.mjs`：明确宣告天下——**我是个 ES Module，我支持 `import`/`export`**。

在 Node.js 环境中，用 `.mjs` 可以直接享受 ESM 的红利，无需在 `package.json` 里配置 `"type": "module"`。

而在浏览器端，它配合 `<script type="module">`，就能实现**原生的模块化加载**，无需任何编译！

## 03 零构建实战：3步跑通前端代码

说了这么多，直接上手！不装任何依赖，打开编辑器，3个文件搞定。

**第一步：创建入口 HTML**

新建 `index.html`，注意关键的 `type="module"`：

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <title>零构建前端实验</title>
</head>
<body>
  <h1 id="app"></h1>
  <!-- 注意这里的 type="module" -->
  <script type="module" src="./main.mjs"></script>
</body>
</html>
```

**第二步：写个工具模块**

新建 `utils.mjs`，导出一个函数：

```javascript
// utils.mjs
export const sayHello = (name) => `你好，${name}！零构建真香！`;
```

**第三步：写主逻辑**

新建 `main.mjs`，导入并使用：

```javascript
// main.mjs
import { sayHello } from './utils.mjs';

const app = document.getElementById('app');
app.textContent = sayHello('前端打工人');
```

**运行！**
直接双击打开 `index.html`？**报错！**（别慌，是 CORS 限制）
本地零构建必须起个静态服务。最快的办法，在目录下运行：

```bash
# 任意一种即可，不需要装包
npx serve .
# 或 python3 -m http.server
# 或 php -S localhost:8080
```

打开浏览器，页面完美渲染。打开 DevTools 的 Network 面板，你会发现浏览器**自动按依赖关系请求了** `main.mjs` 和 `utils.mjs`。

🎉 恭喜！你完成了第一次零构建前端开发。

## 04 进阶：用 Import Map 拥抱生态

"零构建是好，但我离不开 Lodash / Three.js / RxJS 怎么办？总不能自己手写吧？"

别担心，**Import Map**（导入映射）登场！它是浏览器原生的"模块别名解析器"，相当于极简版的 Webpack alias。

修改你的 `index.html`：

```html
<script type="importmap">
  {
    "imports": {
      "lodash": "https://cdn.jsdelivr.net/npm/lodash-es@4.17.21/lodash.js"
    }
  }
</script>
<script type="module" src="./main.mjs"></script>
```

然后在 `main.mjs` 里，你就可以**像写 Node.js 一样**直接 bare import：

```javascript
// main.mjs
import { debounce } from 'lodash';

const log = debounce(() => console.log('零构建也能用 Lodash！'), 300);
window.addEventListener('resize', log);
```

无需 `npm install`，无需打包，CDN 即你的 `node_modules`。[目前主流浏览器已全面支持 Import Map](https://caniuse.com/import-maps)。

## 05 零构建的优势与代价

任何架构选型都是权衡，零构建也不是银弹。

### ✅ 优势
- **极速启动**：无需等待打包，秒开秒改。
- **零依赖**：没有 `node_modules`，不怕依赖黑洞，代码库极其干净。
- **调试友好**：浏览器直接映射源码，报错定位精准到原始 `.mjs` 行，再无 Source Map 迷惑行为。
- **适合微前端/组件库开发**：独立模块即插即用。

### ❌ 代价
- **兼容性**：IE 肯定是不行了，不过反正 IE 也入土了。老旧国产浏览器可能需要降级方案。
- **网络性能**：小模块过多会导致大量 HTTP 请求（HTTP/2 环境下此问题大幅缓解，但仍不如单 Bundle 极致）。
- **缺乏高级语法转译**：TS、JSX、Vue SFC 等需预编译，纯零构建玩不转（除非用 `esm.sh` 等黑科技）。
- **CSS 模块化受限**：无法像 Vite 那样 `import style from './xxx.css'`，只能依赖原生 CSS 或者手写动态插入。

## 06 何时该用零构建？

| 场景 | 推荐度 |
|---|---|
| 轻量级落地页 / 活动页 | ⭐⭐⭐⭐⭐ |
| 内部小工具 / Dashboard | ⭐⭐⭐⭐ |
| 嵌入式小部件 / 浏览器插件 | ⭐⭐⭐⭐ |
| 组件库文档 / 原型验证 | ⭐⭐⭐⭐ |
| 复杂企业级 SPA / SSR 项目 | ⭐⭐（还是老实用 Vite/Nuxt/Next 吧） |

## 07 写在最后

前端圈有一句名言：**"你并不总是需要 Webpack。"**

从 Webpack 到 Vite，前端工具链的演进方向一直是**"更快、更轻"**。而零构建（`.mjs` + Import Map）代表了一种回归本源的极简哲学：**把模块化的权力还给浏览器**。

下次再遇到改个字要等 30 秒热更新的小项目，不妨试试零构建的爽感。
