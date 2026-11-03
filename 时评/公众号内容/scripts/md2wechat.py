"""
Markdown -> 公众号 HTML（只用内联样式）

同一篇 Markdown 每次转换结果都一样，不再依赖 AI 手写 HTML。

支持的写法：
  ## 标题 / ### 小标题         一级标题自动编号 PART 01、02...
  **加粗** ==高亮== *斜体* `代码` ~~删除线~~ [链接](url)
  > 引用
  > [!TIP] / [!WARN] / [!OK] / [!GOLD]   蓝色重点 / 红色警告 / 绿色正确 / 居中金句
  - 无序列表 / 1. 有序列表
  ```代码块```
  | 表格 |
  ![图片说明](images/a.png)     单独一行的图片，说明文字显示在图下方
  ---                            分隔线

用法：python md2wechat.py 文章.md [输出.html]
"""
import base64
import html
import mimetypes
import os
import re
import sys

BODY_FONT = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Helvetica,"
             "'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif")
MONO = "Consolas,'Courier New',monospace"

# 主色。整篇只用这一个强调色，想换风格改这里即可
ACCENT = '#2b5fd9'
ACCENT_SOFT = '#eef3fd'
TEXT = '#3a3a3a'
MUTED = '#8a8f98'

S = {
    'wrap': "max-width:680px; margin:0 auto; background:#ffffff; padding:0 4px; box-sizing:border-box;",
    'lead': f"margin:8px 0 32px; padding:14px 16px; background:{ACCENT_SOFT}; border-radius:6px;",
    'lead_p': f"margin:0; font-size:14px; color:#4b5563; line-height:1.8; letter-spacing:0.5px;",
    'h2': "margin:44px 0 22px; text-align:center; line-height:1.4;",
    'h2_no': f"display:block; font-size:12px; color:{ACCENT}; letter-spacing:3px; font-weight:400; margin-bottom:6px;",
    'h2_text': f"display:inline-block; font-size:19px; color:#1f2329; font-weight:700; padding:0 4px 8px; border-bottom:3px solid {ACCENT};",
    'h3': f"font-size:16px; color:#1f2329; font-weight:700; margin:30px 0 14px; line-height:1.5;",
    'h3_bar': f"display:inline-block; width:4px; height:15px; background:{ACCENT}; margin-right:8px; vertical-align:-2px; border-radius:2px;",
    'p': f"margin:0 0 20px; color:{TEXT}; font-size:15px; line-height:1.85; letter-spacing:0.5px; text-align:justify;",
    'strong': f"color:{ACCENT}; font-weight:700;",
    'mark': "background:#fff1a8; padding:0 2px; color:#1f2329;",
    'quote': f"margin:22px 0; padding:2px 0 2px 14px; border-left:3px solid #d4d8de;",
    'quote_p': f"margin:0 0 6px; font-size:14px; color:#6b7280; line-height:1.8; letter-spacing:0.5px;",
    'list': "margin:0 0 20px; padding:0;",
    'li': f"margin:0 0 10px; font-size:15px; color:{TEXT}; line-height:1.8; letter-spacing:0.5px;",
    'li_mark': f"color:{ACCENT}; font-weight:700; margin-right:6px;",
    'code': "background:#282c34; padding:14px 16px; margin:22px 0; border-radius:6px; overflow-x:auto;",
    'code_p': f"margin:0; font-size:12.5px; color:#d7dae0; font-family:{MONO}; line-height:1.7; white-space:pre;",
    'icode': f"background:#f3f4f6; color:#c7254e; padding:2px 5px; letter-spacing:0; border-radius:3px; font-size:13px; font-family:{MONO};",
    'link': f"color:{ACCENT};",
    'link_url': f"color:{MUTED}; font-size:12px;",
    'fig': "margin:24px 0; padding:0;",
    'img': "width:100%; display:block; border-radius:6px;",
    'cap': f"text-align:center; font-size:12px; color:{MUTED}; margin:8px 0 0;",
    'hr': f"margin:36px 0; text-align:center; color:#c4c8ce; font-size:14px; letter-spacing:12px;",
    'table_wrap': "margin:22px 0; padding:0; overflow-x:auto;",
    'table': "width:100%; min-width:300px; border-collapse:collapse; font-size:14px;",
    'th': f"border-bottom:2px solid {ACCENT}; padding:10px 8px; font-weight:700; color:#1f2329; text-align:left;",
    'td': "border-bottom:1px solid #eceef1; padding:10px 8px; color:#4b5563;",
    'end': f"margin:48px 0 12px; text-align:center; font-size:13px; color:{MUTED}; letter-spacing:4px;",
    'thanks_p': f"margin:0 0 6px; text-align:center; font-size:14px; color:#4b5563;",
    'copy': f"text-align:center; font-size:12px; color:#b0b4ba; margin:0 0 30px;",
}

# 背景色, 左边框色, 文字色
CALLOUTS = {
    'TIP':  (ACCENT_SOFT, ACCENT, '#1f3f8f'),
    'WARN': ('#fdf0ef', '#d9534f', '#8f2a26'),
    'OK':   ('#eef8f1', '#3a9d5d', '#22603a'),
    'GOLD': None,  # 金句：居中大字，不用框
}

CJK = re.compile(r'[　-鿿＀-￯]')


def split_frontmatter(text):
    """按行解析 key: value。不用 YAML，因为 "360压缩差哪了？"：…… 这类标题在 YAML 里是语法错误。"""
    if text.startswith('---\n'):
        end = text.find('\n---', 4)
        if end != -1:
            meta = {}
            for line in text[4:end].split('\n'):
                key, sep, value = line.partition(':')
                if sep and key.strip():
                    value = value.strip()
                    if len(value) > 1 and value[0] == value[-1] and value[0] in '\'"':
                        value = value[1:-1]
                    meta[key.strip()] = value
            return meta, text[end + 4:].lstrip('\n')
    return {}, text


def inline(text):
    """转换行内语法。先转义 HTML，再把行内代码抽出来，避免里面的符号被当成语法。"""
    codes = []

    def keep_code(m):
        codes.append(m.group(1))
        return f'\x00{len(codes) - 1}\x00'

    text = re.sub(r'`([^`]+)`', keep_code, text)
    text = html.escape(text, quote=False)
    text = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)',
                  lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}" style="{S["img"]}">', text)
    # 个人号外链点不开，所以把网址以灰色小字写在链接文字后面
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)',
                  lambda m: f'<span style="{S["link"]}">{m.group(1)}</span>'
                            f'<span style="{S["link_url"]}">（{m.group(2)}）</span>', text)
    text = re.sub(r'\*\*(.+?)\*\*', rf'<strong style="{S["strong"]}">\1</strong>', text)
    text = re.sub(r'(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])', r'<em>\1</em>', text)
    text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
    text = re.sub(r'==(.+?)==', rf'<span style="{S["mark"]}">\1</span>', text)
    return re.sub('\x00(\\d+)\x00',
                  lambda m: f'<code style="{S["icode"]}">{html.escape(codes[int(m.group(1))], quote=False)}</code>',
                  text)


def join_lines(lines):
    """软换行：中文之间直接拼接，英文之间补一个空格。"""
    out = ''
    for line in (l.strip() for l in lines):
        if out and not (CJK.search(out[-1]) or CJK.search(line[0])):
            out += ' '
        out += line
    return out


def render_table(rows):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    head, body = cells[0], cells[2:] if len(cells) > 1 and set(''.join(cells[1])) <= set('-: ') else cells[1:]
    out = [f'<section style="{S["table_wrap"]}"><table style="{S["table"]}">', '<tr>']
    out += [f'<td style="{S["th"]}">{inline(c)}</td>' for c in head]
    out.append('</tr>')
    for row in body:
        out.append('<tr>' + ''.join(f'<td style="{S["td"]}">{inline(c)}</td>' for c in row) + '</tr>')
    out.append('</table></section>')
    return '\n'.join(out)


def render_quote(lines):
    first = lines[0].strip()
    m = re.match(r'\[!(\w+)\]\s*(.*)', first)
    if m and m.group(1).upper() in CALLOUTS:
        kind = m.group(1).upper()
        body = paragraphs([m.group(2)] + lines[1:] if m.group(2) else lines[1:])
        if kind == 'GOLD':
            paras = ''.join(f'<p style="margin:0; font-size:17px; color:#1f2329; font-weight:700; '
                            f'line-height:1.7; letter-spacing:1px;">{inline(p)}</p>' for p in body)
            return (f'<section style="margin:32px 0; padding:22px 8px; border-top:1px solid #e3e6ea; '
                    f'border-bottom:1px solid #e3e6ea; text-align:center;">{paras}</section>')
        bg, bar, color = CALLOUTS[kind]
        paras = ''.join(f'<p style="margin:0 0 4px; font-size:14px; color:{color}; line-height:1.8; letter-spacing:0.5px;">'
                        f'{inline(p)}</p>' for p in body)
        return (f'<section style="margin:22px 0; padding:12px 14px 8px; background:{bg}; border-left:3px solid {bar}; '
                f'border-radius:0 6px 6px 0;">{paras}</section>')
    paras = [f'<p style="{S["quote_p"]}">{inline(p)}</p>' for p in paragraphs(lines)]
    return f'<blockquote style="{S["quote"]}">' + ''.join(paras) + '</blockquote>'


def paragraphs(lines):
    out, buf = [], []
    for l in lines + ['']:
        if l.strip():
            buf.append(l)
        elif buf:
            out.append(join_lines(buf))
            buf = []
    return out


def render_list(items, ordered):
    out = [f'<section style="{S["list"]}">']
    for i, (indent, text) in enumerate(items, 1):
        mark = f'{i}.' if ordered else '•'
        pad = f' padding-left:{indent * 18}px;' if indent else ''
        out.append(f'<p style="{S["li"]}{pad}"><span style="{S["li_mark"]}">{mark}</span>{inline(text)}</p>')
    out.append('</section>')
    return '\n'.join(out)


def render_body(md):
    lines = md.split('\n')
    out, i, h2_no = [], 0, 0
    para = []

    def flush():
        if para:
            out.append(f'<p style="{S["p"]}">{inline(join_lines(para))}</p>')
            para.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()

        if s.startswith('```'):
            flush()
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code.append(html.escape(lines[i], quote=False) or ' ')
                i += 1
            out.append(f'<section style="{S["code"]}"><p style="{S["code_p"]}">' + '<br>'.join(code) + '</p></section>')
        elif not s:
            flush()
        elif s.startswith('# '):
            flush()  # 一级标题即文章标题，公众号会单独显示，正文里不重复
        elif s.startswith('## '):
            flush()
            h2_no += 1
            out.append(f'<h2 style="{S["h2"]}"><span style="{S["h2_no"]}">PART {h2_no:02d}</span>'
                       f'<span style="{S["h2_text"]}">{inline(s[3:])}</span></h2>')
        elif s.startswith('### '):
            flush()
            out.append(f'<h3 style="{S["h3"]}"><span style="{S["h3_bar"]}"></span>{inline(s[4:])}</h3>')
        elif re.fullmatch(r'(-{3,}|\*{3,}|_{3,})', s):
            flush()
            out.append(f'<p style="{S["hr"]}">···</p>')
        elif s.startswith('>'):
            flush()
            block = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                block.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            out.append(render_quote(block))
            continue
        elif s.startswith('|'):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append(lines[i])
                i += 1
            out.append(render_table(rows))
            continue
        elif re.fullmatch(r'!\[([^\]]*)\]\(([^)\s]+)\)', s):
            flush()
            m = re.fullmatch(r'!\[([^\]]*)\]\(([^)\s]+)\)', s)
            cap = f'<p style="{S["cap"]}">{html.escape(m.group(1))}</p>' if m.group(1) else ''
            out.append(f'<section style="{S["fig"]}"><img src="{m.group(2)}" alt="{html.escape(m.group(1))}" '
                       f'style="{S["img"]}">{cap}</section>')
        elif re.match(r'\s*([-*+]|\d+[.)])\s+', line):
            flush()
            ordered = bool(re.match(r'\s*\d', line))
            items = []
            while i < len(lines):
                m = re.match(r'(\s*)([-*+]|\d+[.)])\s+(.*)', lines[i])
                if m and not m.group(1) and m.group(2)[0].isdigit() != ordered:
                    break  # 顶层从无序换成有序（或反过来），另起一个列表
                if m:
                    items.append((len(m.group(1)) // 2, m.group(3)))
                elif lines[i].strip() and items and lines[i].startswith(' '):
                    items[-1] = (items[-1][0], join_lines([items[-1][1], lines[i]]))
                else:
                    break
                i += 1
            out.append(render_list(items, ordered))
            continue
        else:
            para.append(line)
        i += 1
    flush()
    return '\n'.join(out)


def convert(md_text, base_dir=None):
    """返回 (meta, 正文 HTML)。正文 HTML 可直接作为草稿的 content。
    base_dir 是文章目录，用来判断封面图是否存在；封面默认放在正文最上面，cover_in_body: no 可关掉。"""
    meta, body = split_frontmatter(md_text)
    if 'title' not in meta:  # 旧文章没有 frontmatter，用第一个一级标题当标题
        m = re.search(r'^# (.+)$', body, re.M)
        if m:
            meta['title'] = m.group(1).strip()
    parts = [f'<section style="{S["wrap"]}">']
    cover = meta.get('cover', 'images/cover.png')
    if base_dir and meta.get('cover_in_body', 'yes') != 'no' and os.path.exists(os.path.join(base_dir, cover)):
        parts.append(f'<section style="margin:0 0 24px; padding:0;"><img src="{html.escape(cover)}" alt="封面" '
                     f'style="{S["img"]}"></section>')
    if meta.get('digest'):
        parts.append(f'<section style="{S["lead"]}"><p style="{S["lead_p"]}">{inline(str(meta["digest"]))}</p></section>')
    parts.append(render_body(body))
    parts.append(f'<p style="{S["end"]}">— 完 —</p>')
    parts.append(f'<p style="{S["thanks_p"]}">觉得有用，点个「在看」让更多人看到</p>')
    parts.append(f'<p style="{S["copy"]}">哀的代码实验室</p>')
    parts.append('</section>')
    return meta, explicit_align('\n'.join(parts))


def explicit_align(content):
    """给没写对齐方式的块级元素补上 text-align:left。
    否则粘贴进公众号时会被补成 text-align:start，触发「文字对齐异常」检测。"""
    def fix(m):
        style = m.group(2)
        if 'text-align' in style:
            return m.group(0)
        return f'<{m.group(1)} style="{style.rstrip("; ")}; text-align:left;"'
    return re.sub(r'<(p|h[1-6]|section|blockquote|td)\s+style="([^"]*)"', fix, content)


# 预览页的「复制正文」：直接把脚本生成的原始 HTML 放进剪贴板。
# 不能让用户自己框选复制，浏览器会把计算出来的样式（如 text-align:start）一起带上。
COPY_SCRIPT = """
<script>
function copyArticle() {
  var el = document.getElementById('wx-article');
  var onCopy = function (e) {
    e.clipboardData.setData('text/html', el.outerHTML);
    e.clipboardData.setData('text/plain', el.innerText);
    e.preventDefault();
  };
  document.addEventListener('copy', onCopy);
  var ok = document.execCommand('copy');
  document.removeEventListener('copy', onCopy);
  var btn = document.getElementById('wx-copy');
  btn.textContent = ok ? '已复制，去公众号编辑器粘贴' : '复制失败，请重试';
  setTimeout(function () { btn.textContent = '复制正文'; }, 2500);
}
</script>"""


def embed_images(content, base_dir):
    """把本地图片转成 data URI 嵌进页面，预览能看到，「复制正文」时图片也会一起带走。"""
    def to_data_uri(m):
        src = m.group(1)
        path = os.path.join(base_dir, src)
        if src.startswith(('http', 'data:')) or not os.path.exists(path):
            return m.group(0)
        mime = mimetypes.guess_type(path)[0] or 'image/png'
        with open(path, 'rb') as f:
            data = base64.b64encode(f.read()).decode()
        return f'<img src="data:{mime};base64,{data}"'
    return re.sub(r'<img src="([^"]+)"', to_data_uri, content)


def preview_page(meta, content, base_dir=None):
    title = html.escape(str(meta.get('title', '预览')))
    if base_dir:
        content = embed_images(content, base_dir)
    content = content.replace('<section ', '<section id="wx-article" ', 1)
    return (f'<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
            f'<meta name="viewport" content="width=device-width,initial-scale=1.0">\n<title>{title}</title>\n</head>\n'
            # 外层模拟公众号文章页：白底、左右 16px 边距、标题 22px
            f'<body style="margin:0; padding:0 16px 80px; background:#fff; font-family:{BODY_FONT};">\n'
            f'<h1 style="max-width:680px; margin:0 auto; font-size:22px; color:#1f2329; '
            f'padding:24px 4px 6px; line-height:1.4;">{title}</h1>\n'
            f'<p style="max-width:680px; margin:0 auto 20px; padding:0 4px; font-size:14px; color:#576b95;">哀的代码实验室</p>\n'
            f'{content}\n'
            f'<button id="wx-copy" onclick="copyArticle()" style="position:fixed; right:20px; bottom:20px; '
            f'padding:12px 20px; background:#07c160; color:#fff; border:0; border-radius:8px; font-size:15px; '
            f'cursor:pointer; box-shadow:0 4px 12px rgba(0,0,0,0.15);">复制正文</button>\n'
            f'{COPY_SCRIPT}\n</body>\n</html>\n')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    base = os.path.dirname(os.path.abspath(sys.argv[1]))
    with open(sys.argv[1], encoding='utf-8') as f:
        meta, content = convert(f.read(), base)
    page = preview_page(meta, content, base)
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'w', encoding='utf-8') as f:
            f.write(page)
    else:
        print(page)
