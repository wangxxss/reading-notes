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
3. **HTML Template File**: `publish/公众号模板.html` - The template to use for generated HTML
4. **Output Directory**: `publish/tmp/`

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

Use the `publish/公众号模板.html` as the base template. Replace the placeholder content in the template with the converted markdown content while preserving the template's styling and layout structure.

**Template Structure to Preserve:**
- Head section with meta tags and title
- Body wrapper with max-width container
- H1 title area
- Subtitle/description area
- Cover image area
- Lead/intro box
- Content sections
- H2 section headers with left border accent
- Various content blocks (cards, lists, quotes)
- Bottom attention box
- Copyright area

**Content Placement Rules:**
- Article title → `<h1>` tag
- Subtitle/date → `<p>` subtitle tag
- Lead/intro → the `#f7f8fa` background box with left border
- H2 headers → `<h2>` with `border-left: 4px solid #4e9eff`
- Body paragraphs → `<p>` with `text-indent: 2em`
- Highlight boxes → `#fff5cc` background style
- Blockquotes → `<blockquote>` with gray left border
- Lists → div with padding-left containing paragraphs
- Images → div with border-radius and img inside
- Dividers → `<div>` with height 1px gray line
- Conclusion → standard `<p>` paragraphs

## Styling Recommendations

### Color Palette (from template)
- Primary accent: `#4e9eff` (blue accent)
- Secondary accent: `#6688ff` (purple-blue)
- Title dark: `#222`
- Body text: `#333` or `#555`
- Muted text: `#999`
- Background: `#f4f4f4` (light gray)
- Card backgrounds: `#fff`, `#f7f8fa`, `#fff5cc`

### Typography (from template)
- Font size: 16px (body), 14px (subtitle/intro), 19px (h2), 17px (h3)
- Line height: 1.75
- H1 title: centered, bold, 22px
- Font family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif

### Visual Elements (from template)
- H2 headers: left border accent (4px solid #4e9eff)
- Important sections: yellow highlight box (#fff5cc)
- Lead/intro: gray background box with blue left border
- Cover images: full-width with border-radius
- Dividers: 1px gray lines, centered, 35px margin

## Execution Steps

1. Read the source markdown article
2. Read the HTML specification document (`publish/微信公众号HTML支持说明.md`)
3. Read the HTML template file (`publish/公众号模板.html`)
4. Parse markdown structure (headers, paragraphs, lists, quotes, images)
5. Map markdown elements to template structure:
   - H1 → article title (centered, bold, 22px)
   - Lead paragraph → intro box (gray background with blue left border)
   - H2 → section headers (left border accent)
   - Paragraphs → body text with text-indent
   - Emphasis → yellow highlight boxes
   - Blockquotes → gray left border quote style
   - Images → full-width image containers
   - Lists → indented paragraph lists
   - Dividers → centered gray lines
6. Fill the template with converted content, preserving all template styling
7. Ensure left-aligned layout with proper text-indent for paragraphs
8. Save to `publish/tmp/` directory with `.html` extension
9. Report success to user

## File Naming

Output file should have the same name as the source markdown, just with `.html` extension.

Example:
- Input: `专注力保卫战：如何从被打断的恶性循环中脱身.md`
- Output: `publish/tmp/专注力保卫战.html`