# coding:utf-8
import os
import json
import time
from urllib.parse import urlparse

from worker_ import get_screenshot

# 读取list.json文件
with open("list.json", "r") as f:
    data = json.load(f)

for i in data:
    # 获取url
    url = i["url"]
    timeout = i["timeout"]
    # 获取宽度和高度
    width = i["width"]
    height = i["height"]
    real_time_out = i["real_time_out"]
    pic = get_screenshot(url, width, height, timeout, real_time_out)
    # 写入文件
    host = urlparse(url).netloc
    host_dir = os.path.join("save", host)
    path = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    path_dir = os.path.join("save", host, path + ".png")
    if not os.path.exists(host_dir):
        os.mkdir(host_dir)
    with open(path_dir, "wb") as f:
        f.write(pic)
