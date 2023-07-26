import os
import json

# 读取 result.json
with open(os.path.join("save", 'result.json'), 'r') as f:
    result = json.load(f)



def find_unuse_data(result):
    # 遍历 result 中的所有域名
    for domain in result["data"]:
        for site in domain["data"]:
            for item in site["data"]:
                if not os.path.exists(item):
                    # 如果文件不存在，删除数据
                    del site["data"][site["data"].index(item)]
                    result = find_unuse_data(result)
                    return result
                else:   
                    print("该文件存在:" + item)
    return result


result = find_unuse_data(result)


# 将更新后的 result 写入文件
with open(os.path.join("save", 'result.json'), 'w') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
