import time

def get_timestamp():
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())