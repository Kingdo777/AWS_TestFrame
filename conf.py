# -*- coding: utf-8 -*-
from collections import OrderedDict

CONGIF = {
    "creds":
        {
            "aws_id": "AKIAJHML3C57NFW4LQLA",
            "aws_key": "pq8oqVxWMoKDwIc4seYGtcj4u1dR6DATNoB0OJar"
        },
    "func":
        {
            "name_prefix": "py_lambda_test",
            "region": "us-west-2",
            "role_1": "arn:aws:iam::473540422335:role/service-role/kingdo",
            "role_2": "arn:aws:iam::473540422335:role/service-role/kingdo"
        }
}

# The default path for function code

CODE_PATH = {
    'python2.7': './code',
    'python3.7': './code',
    # 'nodejs6.10': './code/nodejs',
    # 'nodejs4.3': './code/nodejs',
    # 'java8': './code/java',
}

"""
The template request
sleep: set a value X here. The function will sleep for X seconds before return
stat: if let the measurement function will run the basic_stat subroutine
run: pass a cmd to the measurement function. if set the measurement function will run the specified string as an external command.
io: pass the parameters for the IO tests
net: pass the parameters for the network throughput tests
cpu: pass the parameters for the CPU tests
cpuu: pass the parameters for the CPU utilization tests
"""
PARA_TEMP = OrderedDict()
PARA_TEMP["sleep"] = 0  # change it to 0 for quick tests
PARA_TEMP["stat"] = dict(argv=1)
PARA_TEMP["run"] = dict(cmd=str)
PARA_TEMP["io"] = dict(rd=int, size=str, cnt=int)
PARA_TEMP["net"] = dict(port_offset=int, server_ip=str)
PARA_TEMP["cpu"] = dict(n=int)
PARA_TEMP["cpuu"] = dict(n=int)
