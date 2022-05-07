# coding:utf-8
import os
import json
import time
from urllib.parse import urlparse
import os
import time

from selenium import webdriver

def get_screenshot(url, width, height, timeout, real_time_out):
    print("正在初始化浏览器")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('lang=zh_CN.UTF-8')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chromedriver = "/usr/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(options=chrome_options, executable_path=chromedriver)
    print("正在尝试初始化窗口大小：", url)
    driver.set_window_size(width, height)
    print("正在获取网页")
    driver.get(url)
    print("正在等待网页加载完成")
    driver.implicitly_wait(timeout)
    time.sleep(real_time_out)
    print("获取网页成功，正在截图")
    pic_file = driver.get_screenshot_as_png()
    print("截图成功")
    driver.quit()
    return pic_file


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
