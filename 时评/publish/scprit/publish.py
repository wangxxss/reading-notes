import requests
import json
import configparser
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
config = configparser.ConfigParser()
config.read(os.path.join(project_dir, 'config.properties'), encoding='utf-8')

token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={config['weixin']['appid']}&secret={config['weixin']['secret']}"
token_resp = requests.get(token_url).json()

if 'access_token' not in token_resp:
    print(f"获取token失败: {token_resp}")
    exit(1)

token = token_resp['access_token']
print("Token OK")

html_path = os.path.join(project_dir, config['article']['html_file'])
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

print(f"HTML: {len(html_content)} chars")

title = config['article']['title']
digest = config['article']['digest']

print(f"Title: {title}")
print(f"Digest: {digest}")

draft_data = {
    'articles': [{
        'title': title,
        'author': '',
        'digest': digest,
        'content': html_content,
        'thumb_media_id': config['publish']['thumb_media_id'],
        'need_open_comment': 0,
        'only_fans_can_comment': 0
    }]
}

json_str = json.dumps(draft_data, ensure_ascii=False)

url = f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}'
headers = {'Content-Type': 'application/json; charset=utf-8'}

resp = requests.post(url, data=json_str.encode('utf-8'), headers=headers)
result = resp.json()

if 'media_id' in result:
    print(f"\nSUCCESS! media_id: {result['media_id']}")
else:
    print(f"\nFAILED: {result}")
