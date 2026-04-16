# 微信公众号图文消息 HTML 支持详细说明

## 一、标题与摘要限制

### 1. 标题限制
- **字符限制**：约 10 个中文字符（或等效字节长度）
- **字节限制**：约 30-40 字节（UTF-8 编码下，中文占 3 字节）
- **错误代码**：45003 "title size out of limit"
- **实测结论**：
  - ✅ 10 个中文字符 = 30 字节 → 成功
  - ✅ 含英文混合约 35 字节 → 可能成功（取决于具体字符）
  - ❌ 14 个中文字符 = 42 字节 → 失败
  - ❌ 15 个中文字符 = 45 字节 → 失败

### 2. 摘要（digest）限制
- **字符限制**：约 10-12 个中文字符
- **错误代码**：45004 "description size out of limit"
- **实测结论**：
  - ✅ 10 个中文字符 → 成功
  - ❌ 37 个中文字符（107 字节）→ 失败

---

## 二、支持的 HTML 标签

### ✅ 完全支持的标签
| 标签 | 说明 |
|------|------|
| `<p>` | 段落，最常用的文本容器 |
| `<div>` | 块级容器 |
| `<span>` | 行内容器 |
| `<section>` | 区块容器（推荐使用） |
| `<br>` | 换行 |
| `<img>` | 图片 |
| `<a>` | 链接 |
| `<strong>`, `<b>` | 加粗 |
| `<em>`, `<i>` | 斜体 |
| `<ul>`, `<ol>`, `<li>` | 列表 |
| `<blockquote>` | 引用块 |
| `<h1>` ~ `<h6>` | 标题（但样式会被重置） |
| `<table>`, `<tr>`, `<td>`, `<th>` | 表格 |

### ❌ 完全不支持（会被过滤）的标签
| 标签 | 说明 |
|------|------|
| `<style>` | CSS 样式块 → **会被完全删除** |
| `<script>` | JavaScript → **会被完全删除** |
| `<link>` | 外部CSS链接 → **会被删除** |
| `<iframe>` | 内嵌框架 → **会被删除** |
| `<form>` | 表单 → **会被删除** |
| `<input>`, `<button>` | 输入控件 → **会被删除** |
| `<video>`, `<audio>` | 媒体标签 → **需用微信专用标签** |
| `<object>`, `<embed>` | 插件 → **会被删除** |

---

## 三、CSS 样式支持

### 核心规则：只支持内联样式（style 属性）

```html
<!-- ❌ 错误：style 标签会被过滤 -->
<style>
  .title { color: red; }
</style>
<p class="title">这段文字不会变红</p>

<!-- ✅ 正确：使用内联样式 -->
<p style="color: red;">这段文字会变红</p>
```

### ✅ 支持的 CSS 属性

#### 文本样式
| 属性 | 示例 | 说明 |
|------|------|------|
| `color` | `color: #333;` | 文字颜色（支持十六进制、rgb、rgba） |
| `font-size` | `font-size: 16px;` | 字体大小（建议用 px） |
| `font-weight` | `font-weight: bold;` | 字重（normal/bold/100-900） |
| `font-style` | `font-style: italic;` | 斜体 |
| `text-align` | `text-align: center;` | 对齐（left/center/right） |
| `text-decoration` | `text-decoration: underline;` | 文字装饰 |
| `line-height` | `line-height: 1.8;` | 行高（建议用无单位数值或 px） |
| `letter-spacing` | `letter-spacing: 2px;` | 字间距 |

#### 背景
| 属性 | 示例 | 说明 |
|------|------|------|
| `background-color` | `background-color: #f5f5f5;` | 背景色（✅ 支持） |
| `background` | `background: #fff;` | 简写（✅ 纯色支持） |

#### 盒模型
| 属性 | 示例 | 说明 |
|------|------|------|
| `margin` | `margin: 10px 0;` | 外边距（✅ 支持） |
| `padding` | `padding: 15px;` | 内边距（✅ 支持） |
| `border` | `border: 1px solid #ddd;` | 边框（✅ 支持） |
| `border-radius` | `border-radius: 8px;` | 圆角（✅ 部分支持） |
| `width` | `width: 100%;` | 宽度（✅ 百分比或固定值） |
| `max-width` | `max-width: 100%;` | 最大宽度（✅ 支持） |
| `box-sizing` | `box-sizing: border-box;` | 盒模型（✅ 支持） |

#### 其他
| 属性 | 示例 | 说明 |
|------|------|------|
| `display` | `display: block;` | 显示类型（部分支持，flex 不支持） |
| `opacity` | `opacity: 0.8;` | 透明度（✅ 支持） |
| `box-shadow` | `box-shadow: 0 2px 4px rgba(0,0,0,0.1);` | 阴影（⚠️ 部分客户端支持） |

---

### ❌ 不支持的 CSS 属性

| 属性 | 说明 |
|------|------|
| `display: flex` | Flexbox 布局 → **不支持** |
| `display: grid` | Grid 布局 → **不支持** |
| `position` | 定位（absolute/fixed/relative）→ **不支持** |
| `float` | 浮动 → **不支持** |
| `transform` | 变换 → **不支持** |
| `animation` | 动画 → **不支持** |
| `transition` | 过渡 → **不支持** |
| `background-image` | 背景图片 → **不支持** |
| `background-gradient` | 渐变 → **不支持或支持有限** |
| `filter` | 滤镜 → **不支持** |
| `clip-path` | 裁剪路径 → **不支持** |

---

## 四、特殊注意事项

### 1. 样式优先级
微信会注入自己的默认样式，你的样式可能被覆盖。建议：
- 使用更具体的选择器（但 class 选择器可能不生效）
- 内联样式优先级最高

### 2. 图片处理
```html
<!-- ✅ 推荐写法 -->
<img 
  src="图片URL" 
  style="width: 100%; display: block; margin: 10px 0;" 
  alt="描述"
/>
```

注意事项：
- 图片宽度建议用 `100%` 或固定像素
- 添加 `display: block` 避免底部留白
- 大图会被自动压缩

### 3. 链接处理
```html
<!-- ✅ 推荐写法 -->
<a href="链接地址" style="color: #07c160; text-decoration: none;">点击访问</a>
```

注意事项：
- 只能跳转到微信允许的域名（需要在后台配置）
- 外部链接会弹出确认框

### 4. 表格处理
```html
<!-- ✅ 推荐写法 -->
<table style="width: 100%; border-collapse: collapse;">
  <tr>
    <td style="border: 1px solid #ddd; padding: 8px;">内容</td>
  </tr>
</table>
```

---

## 五、推荐的 HTML 模板结构

```html
<section style="padding: 20px 15px; font-size: 16px; color: #333; line-height: 1.8;">
  
  <!-- 标题 -->
  <h1 style="font-size: 20px; font-weight: bold; margin-bottom: 20px; text-align: center;">
    文章标题
  </h1>
  
  <!-- 引言/摘要 -->
  <p style="font-size: 14px; color: #888; margin-bottom: 25px; text-align: center;">
    这是一段引言文字，用于吸引读者。
  </p>
  
  <!-- 正文段落 -->
  <p style="margin-bottom: 15px;">
    这是正文内容，使用默认样式即可。
  </p>
  
  <!-- 小标题 -->
  <h2 style="font-size: 18px; font-weight: bold; margin-top: 25px; margin-bottom: 15px; padding-left: 12px; border-left: 4px solid #07c160;">
    小标题
  </h2>
  
  <!-- 重点内容框 -->
  <section style="background-color: #f5f5f5; padding: 15px; border-radius: 8px; margin: 20px 0;">
    <p style="margin: 0;">
      这是重点内容，用浅色背景突出显示。
    </p>
  </section>
  
  <!-- 列表 -->
  <ul style="margin-left: 20px; margin-bottom: 20px;">
    <li style="margin-bottom: 8px;">列表项一</li>
    <li style="margin-bottom: 8px;">列表项二</li>
    <li>列表项三</li>
  </ul>
  
  <!-- 图片 -->
  <img src="图片URL" style="width: 100%; display: block; margin: 15px 0;" alt="图片描述" />
  
  <!-- 结尾 -->
  <p style="text-align: center; font-size: 12px; color: #999; margin-top: 30px;">
    点击下方「阅读原文」查看更多
  </p>
  
</section>
```

---

## 六、调试建议

### 1. 本地预览方法
使用 Chrome 开发者工具模拟手机视图，手动添加微信的默认样式。

### 2. 实际测试方法
1. 先保存到草稿箱
2. 在手机微信上预览效果
3. 检查是否有样式丢失

### 3. 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 样式不生效 | 使用了 `<style>` 标签 | 改用内联 `style` 属性 |
| 布局错乱 | 使用了 flex/grid | 改用传统布局（margin/padding + display: block） |
| 定位失效 | 使用了 position | 移除定位，用 margin 实现 |
| 渐变不显示 | 使用了背景渐变 | 用纯色替代或用图片 |
| 动画不播放 | 使用了 animation | 移除动画，用静态样式 |

---

## 七、API 发布时的实际限制（实测数据）

| 字段 | 限制 | 超出错误码 |
|------|------|-----------|
| title | 约 10 中文字符 / 30-40 字节 | 45003 |
| digest | 约 10-12 中文字符 | 45004 |
| content | 无明确限制（但建议 < 20000 字符） | - |
| thumb_media_id | 必须是永久素材 | 40007 |

---

## 八、总结

### ✅ 推荐做法
1. **只用内联样式** - 所有样式写在 `style="..."` 属性里
2. **用 section 替代 div** - 更符合微信的渲染逻辑
3. **布局用 margin/padding** - 避免使用 flex/position
4. **颜色用十六进制** - 如 `#333`、`#07c160`
5. **宽度用百分比** - 适配不同手机屏幕
6. **标题摘要要短** - 标题 ≤ 10 字，摘要 ≤ 12 字

### ❌ 避免使用
1. `<style>` 标签和外部 CSS 文件
2. `<script>` 标签和 JavaScript
3. Flexbox 和 Grid 布局
4. position 定位
5. CSS 动画和过渡
6. 背景渐变和复杂阴影

---

## 九、本文档使用规范

### 本文档模板开发要求

根据本文档规范，开发微信公众号HTML模板时应遵循以下要求：

#### 布局相关
- ❌ 禁止使用 `display: flex`
- ❌ 禁止使用 `display: grid`
- ❌ 禁止使用 `position: absolute / fixed / relative`
- ❌ 禁止使用 `float`
- ✅ 使用默认块级布局，通过 `margin` 和 `padding` 调整间距

#### 样式相关
- ❌ 禁止使用 `@keyframes` 和 `animation`
- ❌ 禁止使用 `transition`
- ❌ 禁止使用 `transform`
- ❌ 禁止使用 `background: linear-gradient(...)`（渐变）
- ❌ 禁止使用 `box-shadow`（阴影效果）
- ✅ 只使用内联样式 `style="..."`，不使用 `<style>` 标签
- ✅ 背景色使用纯色，如 `background-color: #f5f5f5`
- ✅ 支持 `display: inline-block`（用于徽章等场景）
- ✅ 支持 `border-radius`（圆角）
- ✅ 支持 `border`（边框）

#### 文本排版
- ✅ 推荐使用 `text-align: left` 或 `text-align: center`
- ❌ 不推荐使用 `text-align: justify`（两端对齐）

#### 容器选择
- ✅ 推荐使用 `<section>` 作为外层容器
- ✅ 可使用 `<p>`、`<span>`、`<ul>`、`<li>`、`<h1>`-`<h6>`
- ❌ 不支持 `<div>` 的部分特性

#### 推荐基础模板结构
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章标题</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5;">
    <section style="padding: 20px 15px; font-size: 16px; color: #333; line-height: 1.8; text-align: left;">

        <!-- 标题 -->
        <h1 style="font-size: 22px; font-weight: bold; margin-bottom: 20px; text-align: center; color: #1a1a2e;">
            文章标题
        </h1>

        <!-- 引言 -->
        <p style="font-size: 14px; color: #888; margin-bottom: 25px; text-align: center;">
            引言文字
        </p>

        <!-- 内容区块 -->
        <section style="background-color: #fff; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #667eea;">
            <p style="font-size: 16px; color: #2c3e50; margin-bottom: 15px;">
                正文内容
            </p>
        </section>

        <!-- 带边框的内容框 -->
        <section style="background-color: #f0f4ff; padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #d0d8ff;">
            <p style="color: #667eea; font-weight: bold; margin-bottom: 0;">
                重点内容
            </p>
        </section>

        <!-- 列表 -->
        <ul style="margin-left: 20px; margin-bottom: 20px; color: #34495e;">
            <li style="margin-bottom: 8px;">列表项一</li>
            <li style="margin-bottom: 8px;">列表项二</li>
        </ul>

        <!-- 分隔线 -->
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;" />

    </section>
</body>
</html>
```
