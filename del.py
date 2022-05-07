# coding:utf-8
import json
from urllib.parse import urlparse
import os

def get_json():
    with open('list.json', 'r') as f:
        data = json.load(f)
    return data

data = get_json()
for i in data:
    work_dir = urlparse(i['url']).netloc
    print("del ing:", work_dir)
    day_del = i["daydel"]
    # 找出文件名在8天前的文件
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            file_path = os.path.join(root, file)
            print("find file:", file_path)
            file_time = os.path.getmtime(file_path)
            print("file time:", file_time)
            # 86400
            if file_time < 10 * day_del:
                os.remove(file_path)    # 删除文件
                print("del:", file_path)
