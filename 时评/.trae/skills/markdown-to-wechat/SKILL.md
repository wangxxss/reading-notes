---
name: "markdown-to-wechat"
description: "Converts markdown articles to WeChat public account HTML format with beautiful styling and left-aligned layout. Invoke when user asks to convert markdown to WeChat HTML or wants to create a WeChat article from a markdown file."
---

# Markdown to WeChat Article HTML

This skill converts markdown articles into HTML format suitable for WeChat public account publishing, following the official HTML support specifications.

## When to Use

- User asks to convert a markdown article to WeChat HTML format
- User wants to create a WeChat article with beautiful styling
- User asks to transform an article for WeChat public account
- User mentions "微信公众号" and "HTML" together

## Input Requirements

1. **Source Markdown File**: Path to the markdown article to convert
2. **HTML Specification Document**: `publish/微信公众号HTML支持说明.md` - Contains WeChat HTML rules and limitations
3. **Output Directory**: `publish/tmp/`

## Key WeChat HTML Rules

### Supported Elements
- `<section>`, `<p>`, `<span>`, `<h1>`-`<h6>`, `<ul>`, `<ol>`, `<li>`
- `<img>` (with inline style only)
- `<a>` (links must be to approved domains)
- `<strong>`, `<b>`, `<em>`, `<i>`
- `<blockquote>`, `<table>`, `<hr>`

### CSS Restrictions
- **ONLY inline styles** (`style="..."` attribute)
- NO `<style>` tags (will be deleted)
- NO JavaScript (`<script>` tags)
- NO `display: flex` or `display: grid`
- NO `position: absolute/fixed/relative`
- NO `float`, `transform`, `animation`, `transition`
- NO `background-image` or gradients
- YES `display: block`, `display: inline-block`
- YES `border-radius`, `border`, `margin`, `padding`
- YES `background-color` (solid colors only)

### Layout Requirements
- Left-aligned by default
- No left margin/padding on body
- Use `margin: 0; padding: 0` on body
- Use `text-align: left` on content sections

## Output Structure

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

        <!-- H1 title -->
        <h1 style="...">文章标题</h1>

        <!-- Introduction/Lead -->
        <p style="...">引言内容</p>

        <!-- H2 section headers with left border -->
        <h2 style="padding-left: 12px; border-left: 4px solid #07c160; ...">小节标题</h2>

        <!-- Content sections (cards/boxes) -->
        <section style="background-color: #f0f4ff; padding: 15px; border-radius: 8px; ...">
            <p>内容</p>
        </section>

        <!-- Lists -->
        <ul style="margin-left: 20px; ...">
            <li style="margin-bottom: 8px;">列表项</li>
        </ul>

        <!-- Divider -->
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;" />

        <!-- Conclusion -->
        <p style="...">结尾内容</p>

    </section>
</body>
</html>
```

## Styling Recommendations

### Color Palette
- Primary accent: `#07c160` (WeChat green)
- Secondary accent: `#667eea` (purple for highlights)
- Title dark: `#1a1a2e`
- Body text: `#333` or `#2c3e50`
- Muted text: `#666` or `#888`
- Background: `#f5f5f5` (light gray)
- Card backgrounds: `#fff`, `#f0f4ff`

### Typography
- Font size: 16px (body), 14px (intro), 17-20px (headers)
- Line height: 1.8 for readability
- H1 title: centered, bold, larger font

### Visual Elements
- H2 headers: left border accent (4px solid color)
- Important sections: card style with background color
- Strategy items: white cards with subtle border
- Separators: thin horizontal lines

## Execution Steps

1. Read the source markdown article
2. Read the HTML specification document (`publish/微信公众号HTML支持说明.md`)
3. Parse markdown structure (headers, paragraphs, lists, quotes)
4. Convert to HTML with inline styles following the rules
5. Apply beautiful styling consistent with WeChat aesthetics
6. Ensure left-aligned layout with no left margin
7. Save to `publish/tmp/` directory with `.html` extension
8. Report success to user

## File Naming

Output file should have the same name as the source markdown, just with `.html` extension.

Example:
- Input: `专注力保卫战：如何从被打断的恶性循环中脱身.md`
- Output: `publish/tmp/专注力保卫战.html`