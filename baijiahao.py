import requests


# 上传图片
def updateImage(content):
    _upload_url = "https://baijiahao.baidu.com/builderinner/api/content/file/upload"
    files = {'media': content}
    upload_res = requests.post(_upload_url, files=files)
    print('正在上传')
    return upload_res.json()
