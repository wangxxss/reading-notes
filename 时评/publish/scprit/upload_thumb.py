import requests
import configparser
import os
import sys

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

if len(sys.argv) < 2:
    print("用法: python upload_thumb.py <图片路径>")
    print("示例: python upload_thumb.py ../images/thumb.jpg")
    exit(1)

image_path = os.path.join(project_dir, sys.argv[1])

if not os.path.exists(image_path):
    print(f"图片文件不存在: {image_path}")
    exit(1)

print(f"上传图片: {image_path}")

url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"

with open(image_path, 'rb') as f:
    files = {'media': f}
    resp = requests.post(url, files=files)

result = resp.json()

if 'media_id' in result:
    print(f"\nSUCCESS!")
    print(f"thumb_media_id: {result['media_id']}")
    print(f"URL: {result.get('url', 'N/A')}")
else:
    print(f"\nFAILED: {result}")
