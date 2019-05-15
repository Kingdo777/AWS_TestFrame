#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import time

from stats import *
from tool import *


def handler(event, context):
    tm_st = time.time() * 1000
    basic_info = get_basic_info()
    cpu_test_data = fstr(cpu_util_test(1000))
    io_load_test_data = ioload_test(1, 1024 * 1024 * 200, 1)
    net_test_data = network_test("127.0.0.1", "5201")
    # write_test()
    tm_end = time.time() * 1000
    time_info = [fix_str_len(fstr(tm_st), 18),
                 fix_str_len(fstr(tm_end), 18),
                 fix_str_len(fstr(tm_end - tm_st), 18)]
    # basic_info.update(time_info)
    res = "#".join(time_info + basic_info) + "#" \
          + cpu_test_data + "#" \
          + io_load_test_data + "#" \
          + net_test_data + "#" \
          + "\n"
    return res
