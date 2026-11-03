"""
一条命令：Markdown 终稿 -> 排版 -> 上传图片 -> 推送到公众号草稿箱

用法：
  python wx_publish.py <文章目录或 .md 文件>           只生成本地预览，不推送
  python wx_publish.py <文章目录或 .md 文件> --push    生成预览并推送到草稿箱

传入文章目录时读取其中的 03-终稿.md。文章开头的 frontmatter：
  ---
  title: 文章标题
  digest: 摘要（也会显示在正文开头的引导框里）
  cover: images/cover.png       # 封面图，默认就是这个路径（scripts/cover.py 生成）；不存在则用 config.properties 里的 thumb_media_id
  author: 作者（可选）
  ---

AppID/AppSecret 优先读环境变量 WX_APPID / WX_SECRET，其次读根目录的 config.properties，
没有的话沿用 ../publish/config.properties（原来那份）。
已上传过的图片记在文章目录的 .wx-uploaded.json 里，重复推送不会重复上传。
"""
import configparser
import hashlib
import json
import os
import re
import subprocess
import sys

import requests

from md2wechat import convert, preview_page

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
config = configparser.ConfigParser()
for candidate in (os.path.join(project_dir, 'config.properties'),
                  os.path.join(project_dir, '..', 'publish', 'config.properties')):
    if config.read(candidate, encoding='utf-8'):
        break


def get_token():
    appid = os.environ.get('WX_APPID') or config['weixin']['appid']
    secret = os.environ.get('WX_SECRET') or config['weixin']['secret']
    resp = requests.get('https://api.weixin.qq.com/cgi-bin/token',
                        params={'grant_type': 'client_credential', 'appid': appid, 'secret': secret}).json()
    if 'access_token' not in resp:
        sys.exit(f"获取token失败: {resp}\n（40164 表示当前 IP 不在公众号后台的 IP 白名单里）")
    return resp['access_token']


def file_hash(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def fit_for_upload(path, limit=1024 * 1024):
    """正文图片超过 1MB 或不是 jpg/png 时，用 macOS 自带的 sips 转成 jpg 并逐步压缩，返回可上传的文件路径。"""
    if os.path.getsize(path) <= limit and path.lower().endswith(('.jpg', '.jpeg', '.png')):
        return path
    out = os.path.join(project_dir, 'tmp', hashlib.md5(path.encode()).hexdigest() + '.jpg')
    for quality, width in ((85, 1600), (75, 1280), (65, 1080)):
        subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', str(quality),
                        '--resampleWidth', str(width), path, '--out', out], check=True, capture_output=True)
        if os.path.getsize(out) <= limit:
            print(f"  {os.path.basename(path)} 超过 1MB，已压缩为 {os.path.getsize(out) // 1024}KB 的 jpg")
            return out
    sys.exit(f"{os.path.basename(path)} 压缩后仍超过 1MB，请换一张小一点的图")


class Uploader:
    def __init__(self, token, article_dir):
        self.token = token
        self.cache_path = os.path.join(article_dir, '.wx-uploaded.json')
        self.cache = {}
        if os.path.exists(self.cache_path):
            with open(self.cache_path, encoding='utf-8') as f:
                self.cache = json.load(f)

    def _save(self):
        with open(self.cache_path, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def _post(self, url, path):
        with open(path, 'rb') as f:
            result = requests.post(url, files={'media': f}).json()
        if 'errcode' in result and result['errcode'] != 0:
            sys.exit(f"上传失败 {os.path.basename(path)}: {result}")
        return result

    def content_image(self, path):
        """正文图片：uploadimg 接口，返回微信图片地址。仅支持 jpg/png，1MB 以内。"""
        key = 'img:' + file_hash(path)
        if key not in self.cache:
            print(f"  上传正文图片: {os.path.basename(path)}")
            url = f'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={self.token}'
            self.cache[key] = self._post(url, fit_for_upload(path))['url']
            self._save()
        return self.cache[key]

    def cover(self, path):
        """封面：永久素材接口，返回 media_id。"""
        key = 'cover:' + file_hash(path)
        if key not in self.cache:
            print(f"  上传封面: {os.path.basename(path)}")
            url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={self.token}&type=image'
            self.cache[key] = self._post(url, path)['media_id']
            self._save()
        return self.cache[key]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    push = '--push' in sys.argv
    if not args:
        sys.exit(__doc__)

    target = os.path.abspath(args[0])
    md_path = os.path.join(target, '03-终稿.md') if os.path.isdir(target) else target
    article_dir = os.path.dirname(md_path)
    with open(md_path, encoding='utf-8') as f:
        meta, content = convert(f.read(), article_dir)

    title, digest = meta.get('title'), meta.get('digest', '')
    if not title:
        sys.exit("frontmatter 里缺少 title")
    leftover = re.findall(r'【补充[^】]*】', content)
    if leftover:
        sys.exit(f"还有 {len(leftover)} 处【补充】没填，先补完再发布：\n" + '\n'.join(leftover))

    preview = os.path.join(project_dir, 'tmp', os.path.basename(article_dir) + '.html')
    with open(preview, 'w', encoding='utf-8') as f:
        f.write(preview_page(meta, content, article_dir))
    print(f"预览已生成: {preview}")
    print(f"标题: {title}（{len(title)} 字）\n摘要: {digest}（{len(digest)} 字）")
    if not push:
        print("\n确认预览没问题后，加 --push 推送到草稿箱")
        return

    token = get_token()
    up = Uploader(token, article_dir)

    def replace_img(m):
        src = m.group(1)
        if src.startswith('http'):
            return m.group(0)
        return m.group(0).replace(src, up.content_image(os.path.join(article_dir, src)))

    content = re.sub(r'<img src="([^"]+)"', replace_img, content)

    cover = os.path.join(article_dir, meta.get('cover', 'images/cover.png'))
    if os.path.exists(cover):
        thumb = up.cover(cover)
    else:
        thumb = config['publish']['thumb_media_id']
        print("  未指定封面，沿用 config.properties 里的 thumb_media_id")

    draft = {'articles': [{
        'title': title,
        'author': meta.get('author', ''),
        'digest': digest,
        'content': content,
        'thumb_media_id': thumb,
        'need_open_comment': 1,
        'only_fans_can_comment': 1,
    }]}
    # ensure_ascii=False 很关键：否则中文会被转成 \uXXXX，微信按转义后的长度算，标题很快就超限
    body = json.dumps(draft, ensure_ascii=False).encode('utf-8')
    result = requests.post(f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}', data=body,
                           headers={'Content-Type': 'application/json; charset=utf-8'}).json()
    if 'media_id' in result:
        print(f"\n已推送到草稿箱 media_id: {result['media_id']}\n去手机「公众号助手」里检查后发布。")
    else:
        sys.exit(f"\n推送失败: {result}")


if __name__ == '__main__':
    main()
