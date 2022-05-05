# coding:utf-8
import time

from selenium import webdriver


def get_screenshot(url, width, height, timeout, real_time_out):
    print("正在初始化浏览器")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options, executable_path="chromedriver")
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
