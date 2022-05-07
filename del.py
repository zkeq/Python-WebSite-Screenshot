# coding:utf-8
import json
from urllib.parse import urlparse
import os

def get_json():
    with open('list.json', 'r') as f:
        data = json.load(f)
    return data

data = get_json()
for i in data:
    work_dir = urlparse(i['url']).netloc
    print("del ing:", work_dir)
    daydel = i["daydel"]
    os.system("sh del.sh " + work_dir + " " + str(daydel))
    print("del done:", work_dir)
