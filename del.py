# coding:utf-8
import json
from urllib.parse import urlparse
import os
import time
import oss_uploader as oss

def get_json():
    with open('list.json', 'r') as f:
        data = json.load(f)
    return data


data = get_json()
for i in data:
    work_dir = urlparse(i['url']).netloc
    print("del ing:", work_dir)
    day_del = i["daydel"]
    # 打印现在的时间戳
    time_now = time.time()
    # 找出文件名在8天前的文件
    for root, dirs, files in os.walk(os.path.join("save", work_dir)):
        for file in files:
            file_path = os.path.join(root, file)
            print("find file:", file_path)
            # 2022-05-16_06-53-54.png 转换为 时间戳
            try:
                file_time = time.mktime(time.strptime(file.split("|")[0].split(".")[0], "%Y-%m-%d_%H-%M-%S"))
            except:
                continue
            print("file time:", file_time)
            # 86400 = 1天
            lived_time = time_now - 86400 * day_del
            print("lived time:", lived_time)
            if file_time < lived_time:
                print("文件过期，正在上传阿里云：", oss.uploader(file_path))
                os.remove(file_path)    # 删除文件
                print("del:", file_path)

            # 删除 temp 缓存
            if "|" in file:
                print("del temp:", file_path)
                os.remove(file_path)