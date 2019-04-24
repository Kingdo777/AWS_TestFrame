# -*- coding: utf-8 -*-
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

    def get_client(self):
        session = boto3.Session(aws_access_key_id=self.aws_id,
                                aws_secret_access_key=self.aws_key,
                                region_name=self.region, )
        client = session.client(service_name="lambda")
        return client

    def delete_function(self):
        try:
            client = self.get_client()
            client.delete_function(Functionname=self.func_name)
        except Exception as e:
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
        except Exception as e:
            print(str(e))
            return False

    def invoke_function(self):
        try:
            client = self.get_client()
            response = client.invoke(FunctionName=self.func_name)
            return response
        except Exception as e:
            print(e)
            return False
