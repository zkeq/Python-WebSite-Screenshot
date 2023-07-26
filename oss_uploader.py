import os
import oss2


def uploader(path):
    # 如果环境变量有AK才进行上传
    if not os.environ.get("OSS_AK"):
        return False

    # 从环境变量取
    AK = os.environ.get('AK')
    SK = os.environ.get('SK')
    ENDPOINT = os.environ.get('ENDPOINT')
    # 桶名
    BUCKET_NAME = os.environ.get('BUCKET_NAME')

    # 填写您的 AccessKey ID 和 AccessKey Secret
    access_key_id = AK
    access_key_secret = SK

    # 创建 Auth 实例
    auth = oss2.Auth(access_key_id, access_key_secret)

    # 创建 Bucket 实例
    bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)

    # 上传文件
    bucket.put_object_from_file(path, path)

    print("文件上传成功！")

    return True
