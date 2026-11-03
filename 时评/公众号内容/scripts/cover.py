"""
生成公众号封面图 images/cover.png（900x383，2 倍清晰度）

公众号封面在消息列表里按 2.35:1 显示，转发给好友、分享到朋友圈时只取中间的 1:1 正方形，
所以主文字只放在中间 383x383 的区域里，两侧放装饰和品牌名。

用法：python cover.py <文章目录>
读取 03-终稿.md（没有则读 02-初稿.md）开头的 frontmatter：
  cover_text: 封面大字，10 个字以内，可用 | 手动换行（不写则用标题）
  cover_tag: 右上角小标签，如「AI 时评」（可选）
  cover_style: dark 或 light（默认 dark）
"""
import html
import os
import subprocess
import sys
import tempfile

from md2wechat import ACCENT, split_frontmatter

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
BRAND = '哀的代码实验室'

THEMES = {
    'dark': {
        'bg': f'radial-gradient(circle at 50% 55%, {ACCENT}55 0%, transparent 45%), #0e1526',
        'grid': 'rgba(255,255,255,0.05)',
        'text': '#ffffff',
        'sub': 'rgba(255,255,255,0.55)',
    },
    'light': {
        'bg': f'radial-gradient(circle at 50% 55%, {ACCENT}22 0%, transparent 45%), #f6f4ef',
        'grid': 'rgba(0,0,0,0.045)',
        'text': '#1f2329',
        'sub': 'rgba(0,0,0,0.45)',
    },
}


def cover_html(text, tag, style):
    t = THEMES[style]
    lines = text.split('|') if '|' in text else ([text] if len(text) <= 5 else [text[:(len(text) + 1) // 2], text[(len(text) + 1) // 2:]])
    size = 64 if max(len(l) for l in lines) <= 4 else 54 if max(len(l) for l in lines) <= 5 else 44
    body = '<br>'.join(html.escape(l.strip()) for l in lines)
    tag_html = f'<div class="tag">{html.escape(tag)}</div>' if tag else ''
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:900px;height:383px;overflow:hidden}}
body{{background:{t['bg']};font-family:'PingFang SC','Hiragino Sans GB',sans-serif;position:relative}}
.grid{{position:absolute;inset:0;background-image:linear-gradient({t['grid']} 1px,transparent 1px),
  linear-gradient(90deg,{t['grid']} 1px,transparent 1px);background-size:32px 32px}}
.brand{{position:absolute;left:36px;top:30px;font-size:15px;color:{t['sub']};letter-spacing:3px}}
.brand::before{{content:'';display:inline-block;width:8px;height:8px;border-radius:50%;background:{ACCENT};
  margin-right:10px;vertical-align:2px}}
.tag{{position:absolute;right:36px;top:26px;font-size:14px;color:{ACCENT};border:1.5px solid {ACCENT};
  padding:3px 12px;border-radius:14px;letter-spacing:2px}}
.main{{position:absolute;left:258px;width:384px;top:0;height:383px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;text-align:center}}
.text{{font-size:{size}px;font-weight:800;color:{t['text']};line-height:1.25;letter-spacing:3px}}
.bar{{width:44px;height:5px;background:{ACCENT};border-radius:3px;margin-top:22px}}
.corner{{position:absolute;right:36px;bottom:28px;font-size:12px;color:{t['sub']};letter-spacing:4px;
  font-family:Menlo,monospace}}
</style></head><body><div class="grid"></div><div class="brand">{BRAND}</div>{tag_html}
<div class="main"><div class="text">{body}</div><div class="bar"></div></div>
<div class="corner">// AI CODE LAB</div></body></html>"""


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    article_dir = os.path.abspath(sys.argv[1])
    for name in ('03-终稿.md', '02-初稿.md'):
        md_path = os.path.join(article_dir, name)
        if os.path.exists(md_path):
            break
    else:
        sys.exit(f"{article_dir} 下没有 03-终稿.md 或 02-初稿.md")
    with open(md_path, encoding='utf-8') as f:
        meta, _ = split_frontmatter(f.read())

    text = meta.get('cover_text') or meta.get('title')
    if not text:
        sys.exit("frontmatter 里需要 cover_text 或 title")
    if len(text.replace('|', '')) > 10:
        print(f"提示：封面字「{text}」超过 10 个字，分享卡片里会显得挤，建议写个短的 cover_text")
    style = meta.get('cover_style', 'dark')
    if style not in THEMES:
        sys.exit(f"cover_style 只能是 {' / '.join(THEMES)}")

    out = os.path.join(article_dir, 'images', 'cover.png')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(cover_html(text, meta.get('cover_tag', ''), style))
        page = f.name
    try:
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        '--force-device-scale-factor=2', '--window-size=900,383',
                        f'--screenshot={out}', f'file://{page}'],
                       check=True, capture_output=True)
    finally:
        os.unlink(page)
    print(f"封面已生成: {out}")


if __name__ == '__main__':
    main()
