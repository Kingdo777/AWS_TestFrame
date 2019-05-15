# -*- coding: utf-8 -*-
import json
import os
import socket
import time
from urllib.request import urlopen
from zipfile import ZipFile

from utils import *

# 准备工作
func_prex = "start"
aws_id, aws_key, region, roles = get_config_basic()
role = roles[0]
zipped_code_path = make_zip_file('tmp.zip')
func_handler = "index.handler"
runtime = "python3.7"
mem_size = 512
# func_name = "start14693170"
# fp = FuncOp(aws_id, aws_key, region, role, runtime, mem_size, func_name)
for rId in range(1):
    func_name = func_prex + str(int(time.time() * 1000))[-8:]
    fp = FuncOp(aws_id, aws_key, region, role, runtime, mem_size, func_name)
    # 创建函数
    fp.create_function(zipped_code_path, func_handler)
    # 调用函数
    send_request(fp, 1, sync=True, rId=rId)
    # time.sleep((rId + 21) * 60)
    # 删除函数
    fp.delete_function()
