import requests
import configparser
import os
import glob

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
print("Token OK\n")

tmp_pic_dir = os.path.join(project_dir, 'tmpPic')

image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
image_files = []
for ext in image_extensions:
    pattern = os.path.join(tmp_pic_dir, f'*{ext}')
    image_files.extend(glob.glob(pattern))
    pattern = os.path.join(tmp_pic_dir, f'*{ext.upper()}')
    image_files.extend(glob.glob(pattern))

image_files = [f for f in image_files if not os.path.basename(f).startswith('.')]

if not image_files:
    print(f"未找到图片文件: {tmp_pic_dir}")
    exit(0)

print(f"找到 {len(image_files)} 个图片文件\n")

url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"

for image_path in sorted(image_files):
    print(f"上传图片: {os.path.basename(image_path)}")
    
    with open(image_path, 'rb') as f:
        files = {'media': f}
        resp = requests.post(url, files=files)
    
    result = resp.json()
    
    if 'media_id' in result:
        media_id = result['media_id']
        file_ext = os.path.splitext(image_path)[1]
        new_path = os.path.join(tmp_pic_dir, media_id + file_ext)
        
        try:
            os.rename(image_path, new_path)
            print(f"  ✓ SUCCESS! media_id: {media_id}")
            print(f"  文件已重命名: {os.path.basename(new_path)}\n")
        except Exception as e:
            print(f"  ✓ SUCCESS! media_id: {media_id}")
            print(f"  ✗ 重命名失败: {e}\n")
    else:
        print(f"  ✗ FAILED: {result}\n")

print("全部完成！")
