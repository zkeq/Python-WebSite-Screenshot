# coding:utf-8
from selenium import webdriver


def get_screenshot(url, width, height):
    print("正在初始化浏览器")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    print("正在尝试初始化窗口大小：", url)
    driver.set_window_size(width, height)
    print("正在获取网页")
    driver.get(url)
    print("获取网页成功，正在截图")
    pic_file = driver.get_screenshot_as_png()
    print("截图成功")
    driver.quit()
    return pic_file

