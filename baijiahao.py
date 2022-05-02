import requests


# 上传图片
def updateImage(content):
    # 百家号图床链接不开源（:
    _upload_url = ""
    files = {'media': content}
    upload_res = requests.post(_upload_url, files=files)
    print('正在上传')
    return upload_res.json()
