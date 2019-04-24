# -*- coding: utf-8 -*-
import json
import os
import time

from utils import *

# 准备工作
func_prex = "start"
aws_id, aws_key, region, roles = get_config_basic()
role = roles[0]
zipped_code_path = os.path.join(os.getcwd(), "tmp.zip")
func_handler = "index.handler"
runtime = "python3.7"
mem_size = 128
func_name = func_prex + str(int(time.time() * 1000))[-8:]
fp = FuncOp(aws_id, aws_key, region, role, runtime, mem_size, func_name)

# 创建函数
fp.create_function(zipped_code_path, func_handler)

# 调用函数
respond = fp.invoke_function()
with open("logfile", "a+") as f:
    f.write(fp.func_name + str(respond) + "\n")

# 删除函数
# fp.delete_function()
