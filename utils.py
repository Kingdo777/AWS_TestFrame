# -*- coding: utf-8 -*-
import json
import os
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


def make_zip_file():
    """
    生成上传到AWS的压缩文件
    :return:
    """
    with ZipFile('tmp.zip', 'w') as myzip:
        os.chdir('code')
        myzip.write('index.py')
        myzip.write('stats.py')
        os.chdir('..')


def send_request(fp, task_num):
    """
    发起调用请求
    :param
        task_num: 并发度
        fp: FuncOp对象
    :return:
    """

    def invoke_func():
        respond = fp.invoke_function()
        with open("logfile", "a+") as f:
            f.write(fp.func_name + ":" + str(respond))

    list_task = []
    for i in range(task_num):
        t = Thread(target=invoke_func)
        # t.daemon = True
        t.start()
        list_task.append(t)
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
            with open(src_file) as zip_blob:
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
            resp = client.invoke(FunctionName=self.func_name, InvocationType='RequestResponse')
            try:
                resp = json.loads(resp['Payload'].read())
            except Exception as e:
                print(str(e), resp)
            if not resp:
                resp = "ERROR"
            out = "{}#{}".format(self.dump_meta(), resp)
            print("successfully invoke function：" + self.func_name)
            return out
        except Exception as e:
            print("wrongly invoke function：" + self.func_name)
            print(e)
            return False
