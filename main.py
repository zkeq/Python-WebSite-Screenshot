# coding:utf-8
import uvicorn
from fastapi import FastAPI
from worker import get_screenshot
from fastapi.responses import StreamingResponse, RedirectResponse
from urllib.parse import urlparse
import time
import os
from baijiahao import updateImage

app = FastAPI()


@app.get("/")
async def main(url=None, save: bool = False, upload: bool = False, json: bool = False, width=1920, height=1080):
    """
    url 为必填参数\n
    其他选填\n
    :param url:\n
    :param save:\n
    :param upload:\n
    :param json:\n
    :param width:\n
    :param height:\n
    :return:\n
    """
    print("开始记录日志")
    if not url:
        return {"docs": "http://127.0.0.1:62/docs"}
    print("开始获取截图")
    # 读取png格式的图片
    content = await get_screenshot(url, width, height)
    if upload:
        print("开始上传图片")
        json_content = updateImage(content)
        if json:
            return json_content
        print("图片上传成功")
        bos_url = json_content["ret"]["bos_url"]
        return RedirectResponse(bos_url)
    if save:
        print("开始保存图片")
        print(urlparse(url))
        host = urlparse(url).netloc
        host_dir = os.path.join("save", host)
        path = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        path_dir = os.path.join("save", host, path + ".png", )
        # 如果文件夹不存在就创建
        if not os.path.exists(host_dir):
            os.mkdir(host_dir)
        # 保存图片到path
        with open(path_dir, "wb") as f:
            f.write(content.getvalue())
        true_url = "http://127.0.0.1:62/get_save?file=" + path_dir
        print("图片保存成功")
        if json:
            return {"msg": "成功截图！", "url": true_url}
        return RedirectResponse(true_url)
    print("直接返回文件")
    return StreamingResponse(content, media_type="image/png")


@app.get("/get_save")
def main(file):
    # 读取png格式的图片
    file_like = open(file, mode="rb")
    print("开始返回文件")
    if not file_like:
        return {"msg": "图片不存在！"}
    print(file_like)
    return StreamingResponse(file_like, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=62, log_level="info")
