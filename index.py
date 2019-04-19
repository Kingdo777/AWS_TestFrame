#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time

from stats import *


def run_cmd(cmd):
    return os.popen(cmd).read().strip("\n")


def handler(event, context):
    tm_st = time.time() * 1000
    basic_info = get_basic_info()

    tm_end = time.time() * 1000
    time_info = {
        "start_time": fstr(tm_st),
        "end_time": fstr(tm_end),
        "run_time": fstr(tm_end - tm_st)
    }
    basic_info.update(time_info)
    return basic_info


print(handler({}, {}))
