import requests
import configparser
import os
import glob
import hashlib

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

def is_uploaded_file(filename):
    basename = os.path.splitext(filename)[0]
    if len(basename) >= 32 and '_' in basename:
        parts = basename.split('_')
        if len(parts) >= 2 and all(c.isalnum() or c in '-_' for c in basename):
            return True
    return False

image_files = [f for f in image_files if not is_uploaded_file(os.path.basename(f))]

def get_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def detect_image_type(file_path):
    try:
        with open(file_path, 'rb') as f:
            header = f.read(16)
        
        if len(header) < 4:
            return None
        
        if header[0:2] == b'\xff\xd8':
            return 'jpeg'
        elif header[0:8] == b'\x89PNG\r\n\x1a\n':
            return 'png'
        elif header[0:6] in (b'GIF87a', b'GIF89a'):
            return 'gif'
        elif header[0:2] == b'BM':
            return 'bmp'
        elif header[0:4] == b'RIFF' and header[8:12] == b'WEBP':
            return 'webp'
        elif header[0:3] == b'II\x2a\x00':
            return 'tiff'
        elif header[0:4] == b'MM\x00\x2a':
            return 'tiff'
        
        return None
    except Exception:
        return None

valid_images = []
invalid_files = []
seen_hashes = set()

for image_path in image_files:
    img_type = detect_image_type(image_path)
    if img_type:
        try:
            file_hash = get_file_hash(image_path)
            if file_hash in seen_hashes:
                print(f"⚠ 检测到重复文件: {os.path.basename(image_path)}")
                print(f"  已跳过重复文件\n")
                continue
            seen_hashes.add(file_hash)
        except Exception as e:
            print(f"⚠ 计算文件 hash 失败: {os.path.basename(image_path)}, {e}")
            continue
            
        current_ext = os.path.splitext(image_path)[1].lower().lstrip('.')
        if current_ext != img_type:
            print(f"⚠ 发现扩展名不匹配: {os.path.basename(image_path)}")
            print(f"  实际格式: {img_type}, 扩展名: {current_ext}")
            print(f"  将按实际格式处理\n")
        valid_images.append((image_path, img_type))
    else:
        invalid_files.append(image_path)
        print(f"✗ 非图片文件，已排除: {os.path.basename(image_path)}")

image_files = valid_images

if not image_files:
    print(f"\n未找到有效的图片文件（共排除 {len(invalid_files)} 个非图片文件）: {tmp_pic_dir}")
    exit(0)

print(f"\n找到 {len(image_files)} 个有效图片文件（共排除 {len(invalid_files)} 个非图片文件）\n")

url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"

for image_info in sorted(image_files):
    image_path, img_type = image_info
    
    if not os.path.exists(image_path):
        print(f"⚠ 文件不存在，已跳过: {os.path.basename(image_path)}\n")
        continue
    
    print(f"上传图片: {os.path.basename(image_path)}")
    
    with open(image_path, 'rb') as f:
        files = {'media': f}
        resp = requests.post(url, files=files)
    
    result = resp.json()
    
    if 'media_id' in result:
        media_id = result['media_id']
        new_ext = f'.{img_type}'
        new_path = os.path.join(tmp_pic_dir, media_id + new_ext)
        
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
print(f"\n总计:")
print(f"  - 排除非图片文件: {len(invalid_files)} 个")
