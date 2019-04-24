#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import time

from stats import *


def run_cmd(cmd):
    return os.popen(cmd).read().strip("\n")


def handler(event, context):
    tm_st = time.time() * 1000
    basic_info = get_basic_info()

    tm_end = time.time() * 1000
    time_info = [fstr(tm_st), fstr(tm_end), fstr(tm_end - tm_st)]
    # basic_info.update(time_info)
    res = "#".join(time_info + basic_info)
    print(res)
    return res
