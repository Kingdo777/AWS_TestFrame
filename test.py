import random
import subprocess
import time
from threading import Thread
import iperf3
from utils import *


def make_zip_file(zip_filename):
    """
    生成上传到AWS的压缩文件
    :return:
    """
    with ZipFile(zip_filename, 'w') as myzip:
        for root, dirs, files in os.walk("code"):
            for file in files:
                abs_path = os.path.join(root, file)[5:]
                myzip.write(abs_path)  # 第一个参数是绝对路径，第二个参数是命名再压缩文件中的命名，也就是砍掉多余的路径
    return os.path.join(os.getcwd(), zip_filename)


make_zip_file("tmp.zip")
