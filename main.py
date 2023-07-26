import os
import json
import time
from urllib.parse import urlparse
import os
import time
from PIL import Image
import base64

from selenium import webdriver
import hashlib

def get_dict_md5(d):
    h = hashlib.md5()
    for key, value in d.items():
        h.update(str(key).encode('utf-8'))
        h.update(str(value).encode('utf-8'))
    return h.hexdigest()



def get_screenshot(url, width, height, timeout, real_time_out, host_dir, full_page, i_hash):
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

    now_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    final_pic_file = os.path.join(host_dir, now_time + ".png")
    final_hash_file = os.path.join(host_dir, i_hash + ".png")

    # 获取页面总高度
    total_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight)")
    

    if full_page != 0:
        if full_page == 3:
            print("｜！！！！！｜采用设备模拟截图模式")
            # 直接开启设备模拟，不要再手动开devtools了，否则截图截的是devtools的界面！
            driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {'mobile': False, 'width': width, 'height': total_height, 'deviceScaleFactor': 1})
            # 执行截图
            res = driver.execute_cdp_cmd('Page.captureScreenshot', { 'fromSurface': True})
            # 返回的base64内容写入PNG文件
            with open(final_pic_file, 'wb') as f:
                img = base64.b64decode(res['data'])
                f.write(img)
            with open(final_hash_file, 'wb') as f:
                img = base64.b64decode(res['data'])
                f.write(img)
            driver.quit()
            return final_pic_file, final_hash_file

        if full_page == 1:
            print("｜！！！！！｜采用拉高视窗截图模式")
            driver.set_window_size(width, total_height)
            # 滚动到底部
            driver.execute_script(f"window.scrollTo(0, {total_height});")
        else:
            print("｜！！！！！｜不进行任何操作，直接截图")
        # 截图
        driver.save_screenshot(final_pic_file)
        driver.save_screenshot(final_hash_file)
        driver.quit()
        return final_pic_file, final_hash_file


    print("｜！！！！！｜采用滚动截图模式")    
    scrolled_height = 0
    next_scrolled_height = 0
    print("页面总高度：", total_height)
    now_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    image_path_list = []
    page = 1
    # 滚动页面
    while next_scrolled_height < total_height:
        driver.execute_script(f"window.scrollTo(0, {next_scrolled_height});")
        next_scrolled_height += height
        if total_height - scrolled_height < height:
            next_scrolled_height = total_height
        print("正在截图：", scrolled_height, next_scrolled_height)
        driver.implicitly_wait(timeout)
        time.sleep(real_time_out)
        pic_file = os.path.join(host_dir, now_time + "|" + str(scrolled_height) + "_"+ str(next_scrolled_height) + ".png")
        scrolled_height += height
        image_path_list.append(pic_file)
        driver.save_screenshot(pic_file)
        page += 1
 
    _temp = []
    for i in image_path_list:
        _temp.append(Image.open(i))
    # 裁剪图片
    for i in range(len(_temp)):
        if i == range(len(_temp))[-1]:
            _temp[i] = _temp[i].crop((0, height - (int(image_path_list[-1].split("|")[-1].split(".")[0].split("_")[-1]) - int(image_path_list[-1].split("|")[-1].split(".")[0].split("_")[0])), _temp[i].width, height  ))
        else:
            _temp[i] = _temp[i].crop((0, 0, _temp[i].width, height))
     # 创建新图像
    new_img = Image.new("RGB", (_temp[0].width, total_height))
    # 粘贴图片
    for i in range(len(_temp)):
        new_img.paste(_temp[i], (0, i*height))
        
    # 保存图片
    new_img.save(final_pic_file)
    new_img.save(final_hash_file)
    print("截图成功")
    driver.quit()
    return final_pic_file, final_hash_file


# 读取list.json文件
with open("list.json", "r") as f:
    data = json.load(f)

for i in data:
    # 算出 i 的 md5 值
    i_hash = get_dict_md5(i)
    # 获取url
    url = i["url"]
    timeout = i["timeout"]
    # 获取宽度和高度
    width = i["width"]
    height = i["height"]
    real_time_out = i["real_time_out"]
    full_page = i["full_page"]
    # 写入文件
    host = urlparse(url).netloc
    host_dir = os.path.join("save", host)
    if not os.path.exists(host_dir):
        os.mkdir(host_dir)
    final_pic_file, final_hash_file = get_screenshot(url, width, height, timeout, real_time_out, host_dir, full_page, i_hash)

    result_file = os.path.join("save", 'result.json')

    # 检查文件是否存在
    try:
        with open(result_file, 'r') as f:
            # 如果存在，读取数据
            result = json.load(f)
    except FileNotFoundError:
        # 如果不存在，创建文件并写入数据
        result = {}

    if host not in result["sites"]:
        result["data"].append({
            "site": host,
            "data":[],
            "rules": [],
            "lasted": "",
            "raw_lasted": "",
        })
        result["sites"].append(host)
    else:
        # 找到对应的 host 是第几个索引
        index = result["sites"].index(host)
    result["data"][index]["lasted"] = final_hash_file
    result["data"][index]["raw_lasted"] = final_pic_file

    if i_hash not in result["data"][index]["rules"]:
        result["data"][index]["data"].append({
            "data": [final_pic_file],
            "lasted": final_hash_file,
            "details": i,
            "rule": i_hash,
        })
        result["data"][index]["rules"].append(i_hash)
    else:
        _index = result["data"][index]["rules"].index(i_hash)
        result["data"][index]["data"][_index]["data"].append(final_pic_file)
        result["data"][index]["data"][_index]["lasted"] = final_hash_file

    # 将更新后的 result 写入文件
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=4)