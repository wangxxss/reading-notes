"""
核对两篇 Markdown 的文字是否完全一致（忽略排版标记）

用于"排版标注"这一步：给原文加 ## 标题、==高亮==、提示框、列表等标记后，
确认没有增删改任何一个字（标点也算）。

用法：python check_text.py 原文.md 排版后.md
一致时退出码 0；不一致时列出每一处差异，退出码 1。
"""
import difflib
import re
import sys

from md2wechat import split_frontmatter


def plain(md):
    """去掉 frontmatter 和所有排版标记，只留文字。"""
    _, body = split_frontmatter(md)
    body = re.sub(r'^\s*/\d+/\s*$', '', body, flags=re.M)           # /01/ 这类分节符
    body = re.sub(r'^\s*(-{3,}|\*{3,}|_{3,})\s*$', '', body, flags=re.M)  # 分隔线
    body = re.sub(r'^\s*```.*$', '', body, flags=re.M)               # 代码块围栏
    body = re.sub(r'^\s*#{1,6}\s+', '', body, flags=re.M)            # 标题
    body = re.sub(r'^\s*>\s?', '', body, flags=re.M)                 # 引用
    body = re.sub(r'\[!\w+\]', '', body)                             # 提示框类型
    body = re.sub(r'^\s*([-*+]|\d+[.)])\s+', '', body, flags=re.M)   # 列表符号
    body = re.sub(r'\*\*|==|~~|`|(?<![*\w])\*|\*(?![*\w])', '', body)  # 加粗、高亮、删除线、代码、斜体
    return re.sub(r'\s+', '', body)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    a, b = (plain(open(p, encoding='utf-8').read()) for p in sys.argv[1:])
    if a == b:
        print(f"文字完全一致（{len(a)} 字）")
        return
    diffs = [op for op in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if op[0] != 'equal']
    print(f"有 {len(diffs)} 处文字不一致：")
    for tag, i1, i2, j1, j2 in diffs:
        ctx = a[max(0, i1 - 12):i1]
        print(f"  …{ctx}【原文：{a[i1:i2] or '（无）'} → 现在：{b[j1:j2] or '（无）'}】")
    sys.exit(1)


if __name__ == '__main__':
    main()
