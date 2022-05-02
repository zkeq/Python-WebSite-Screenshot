# coding:utf-8
import uvicorn
from fastapi import FastAPI
from worker import get_screenshot
from fastapi.responses import StreamingResponse, RedirectResponse
from urllib.parse import urlparse
import time
import os
from io import BytesIO
from baijiahao import updateImage

app = FastAPI()


@app.get("/")
def main(url=None, save: bool = False, upload: bool = False, json: bool = False, width=1920, height=1080):
    """
    url 为必填参数
    其他选填
    :param url:
    :param save:
    :param upload:
    :param json:
    :param width:
    :param height:
    :return:
    """
    if not url:
        return {"docs": "http://127.0.0.1:61/docs"}
    # 读取png格式的图片
    content = BytesIO(get_screenshot(url, width, height))
    if upload:
        json_content = updateImage(content)
        if json:
            return json_content
        bos_url = json_content["ret"]["bos_url"]
        return RedirectResponse(bos_url)
    if save:
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
        true_url = "http://127.0.0.1:61/get_save?file=" + path_dir
        if json:
            return {"msg": "成功截图！", "url": true_url}
        return RedirectResponse(true_url)
    print("直接返回文件")
    return StreamingResponse(content, media_type="image/png")


@app.get("/get_save")
def main(file):
    # 读取png格式的图片
    file_like = open(file, mode="rb")
    if not file_like:
        return {"msg": "图片不存在！"}
    print(file_like)
    return StreamingResponse(file_like, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=61, log_level="info")
