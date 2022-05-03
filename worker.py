# coding:utf-8
from pyppeteer import launch
from io import BytesIO


async def get_screenshot(url, width, height):
    print("正在初始化浏览器")
    browser = await launch()
    print("正在打开浏览器")
    page = await browser.newPage()
    print("正在设置页面大小%s*%s" % (width, height))
    await page.setViewport({"width": width, "height": height})
    print("正在打开页面: %s" % url)
    await page.goto(url)
    print("正在截图")
    content = await page.screenshot()
    print("正在转换截图类型")
    content = BytesIO(content)
    print("正在关闭浏览器")
    await browser.close()
    return content
