# -*- coding: utf-8 -*-
import decimal
import json
import os
import time
from threading import Thread
from zipfile import ZipFile

import boto3 as boto3

from conf import CONGIF


def get_config_basic():
    """
    Get the credentials and basic setting from the config file
    """
    aws_id = CONGIF["creds"]["aws_id"]
    aws_key = CONGIF["creds"]["aws_key"]
    region = CONGIF["func"]["region"]
    roles = [CONGIF["func"]["role_1"], CONGIF["func"]["role_2"]]

    return aws_id, aws_key, region, roles


def fstr(f):
    """
    Convert a float number to string
    """

    ctx = decimal.Context()
    ctx.prec = 20
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')


def fix_str_len(string, length):
    """
    限定字符串的长度，不足则补全空格，超过则裁剪
    :param string: 要操作的字符串
    :param length: 要固定的字符串的长度
    :return: 返回限定好长度的字符串
    """
    string_len = len(string)
    if string_len < length:
        string += " " * (length - string_len)
    else:
        string = string[0:length]
    return string


def make_zip_file(zip_filename):
    """
    生成上传到AWS的压缩文件
    :return:
    """
    with ZipFile(zip_filename, 'w') as myzip:
        for root, dirs, files in os.walk("code"):
            for file in files:
                abs_path = os.path.join(root, file)
                file = abs_path[5:]
                myzip.write(abs_path, file)  # 第一个参数是绝对路径，第二个参数是命名再压缩文件中的命名，也就是砍掉多余的路径
    return os.path.join(os.getcwd(), zip_filename)


def send_request(fp, task_num, sync, rId):
    """
    发起调用请求
    :param
        task_num: 并发度
        fp: FuncOp对象
        sync:是否同步发起调用请求
        rId:roundId
    :return:
    """

    def invoke_func(rId, sub_rId):
        # tm_st = time.time() * 1000
        tm_st, tm_end, respond = fp.invoke_function()
        # tm_end = time.time() * 1000
        tm_invoke = fix_str_len(fstr(tm_end - tm_st), 18)
        tm_st = fix_str_len(fstr(tm_st), 18)
        tm_end = fix_str_len(fstr(tm_end), 18)
        with open("logfile", "a+") as f:
            f.write(str(rId) + "-" +
                    fix_str_len(str(sub_rId), 2) + "-" +
                    fp.func_name +
                    ":" +
                    tm_st + "#" +
                    tm_end + "#" +
                    tm_invoke + "#" +
                    str(respond))

    list_task = []
    for i in range(task_num):
        t = Thread(target=invoke_func, args=(rId, i))
        t.start()
        if sync:
            list_task.append(t)
        else:
            t.join()
    for t in list_task:
        t.join()


class FuncOp:
    def __init__(self,
                 aws_id,
                 aws_key,
                 region,
                 role,
                 runtime,
                 memory,
                 func_name):
        self.aws_id = aws_id
        self.aws_key = aws_key
        self.region = region
        self.role = role
        self.runtime = runtime
        self.memory = memory
        self.func_name = func_name

    def dump_meta(self):
        """
        The basic information to record
        """
        return "{}#{}#{}#{}".format(
            self.region,
            self.runtime,
            self.memory,
            self.func_name)

    def get_client(self):

        session = boto3.Session(aws_access_key_id=self.aws_id,
                                aws_secret_access_key=self.aws_key,
                                region_name=self.region, )
        client = session.client(service_name="lambda")
        return client

    def delete_function(self):
        try:
            client = self.get_client()
            client.delete_function(FunctionName=self.func_name)
            print("successfully delete function：" + self.func_name)
            return True
        except Exception as e:
            print("wrongly delete function：" + self.func_name)
            print(str(e))
            return False

    def create_function(self, src_file, func_handler):
        """
        Create a new function
        :param src_file: 要上传的在lambda上执行的代码，是一个压缩的zip文件
        :param func_handler: 代码的入口函数名称
        :return:
        """
        try:
            client = self.get_client()
            with open(src_file, "rb") as zip_blob:
                response = client.create_function(
                    Code={'ZipFile': zip_blob.read()},
                    FunctionName=self.func_name,
                    Handler=func_handler,
                    MemorySize=self.memory,
                    Publish=True,  # Set to true to publish the first version of the function during creation
                    Role=self.role,
                    Runtime=self.runtime,
                    Timeout=300,
                )
                print("successfully create function：" + self.func_name)
                return True
        except Exception as e:
            print("wrongly create function：" + self.func_name)
            print(str(e))
            return False

    def invoke_function(self):
        try:
            client = self.get_client()
            tm_st = time.time() * 1000
            resp = client.invoke(FunctionName=self.func_name, InvocationType='RequestResponse')
            tm_end = time.time() * 1000
            try:
                resp = json.loads(resp['Payload'].read())
            except Exception as e:
                print(str(e), resp)
            if not resp:
                resp = "ERROR"
            out = "{}#{}".format(self.dump_meta(), resp)
            print("successfully invoke function：" + self.func_name)
            return tm_st, tm_end, out
        except Exception as e:
            print("wrongly invoke function：" + self.func_name)
            print(e)
            return False
