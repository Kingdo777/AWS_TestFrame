import random
import subprocess
import time
from threading import Thread
from utils import *


def ioload(size, cnt):
    """ One round of IO throughput test """

    proc = subprocess.Popen(["dd",
                             "if=/dev/urandom",
                             "of=/tmp/ioload.log",
                             "bs=%s" % size,
                             "count=%s" % cnt,
                             "conv=fdatasync",
                             "oflag=dsync"],
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()
    buf = err.split("\n")[-2].split(",")
    t, s = buf[-2], buf[-1]
    t = t.split(" ")[1]
    return "%s,%s" % (t, s)


def ioload_test(rd, size, cnt):
    """ioload_test
    IO throughput test using dd
    Args:
            rd: no. of rounds
            size: the size of data to write each time
            cnt: the times to write in each round
            (see doc of dd)
    Return:
            IO throughput, total time spent (round 1);
            ...; IO throughput, total time spent (round N)
    """
    bufs = []
    for i in range(rd):
        buf = ioload(size, cnt)
        bufs.append(buf)
    return ";".join(bufs)


def network_test(server_ip, port):
    """
    Network throughput test using iperf

    Args:
            port_offset: the offset of the port number;
            server_ip: the IP of the iperf server

    Return:
            throughput in bits, mean rtt, min rtt, max rtt
            (see doc of iperf)
    """
    sp = subprocess.Popen(["./iperf3",
                           "-c",
                           server_ip,
                           "-p",
                           str(port),
                           "-l",
                           "-t",
                           "1",
                           "-Z",
                           "-J"],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    out, err = sp.communicate()
    _d = json.loads(out)["end"]
    sender = _d["streams"][0]["sender"]
    bps = str(sender["bits_per_second"])
    # maxr = str(sender["max_rtt"])
    # minr = str(sender["min_rtt"])
    # meanr = str(sender["mean_rtt"])
    # return ",".join([bps, meanr, minr, maxr])
    return bps


print(network_test("202.114.7.185", "12345"))

#
# def cpu_util_test(n):
#     """
#     CPU utilization test. Recording N timestamps continuously
#
#     Args: N
#
#     Return:
#             The timestamps recorded. Only return unique timestamps
#     """
#     res = {}
#     t1 = int(time.time() * 1000)
#     while True:
#         t2 = int(time.time() * 1000)
#         if t2 - t1 >= n:
#             break
#         res[t2] = 0
#     res = sorted(res.keys())
#     i = len(res)
#     # res = ";".join([fstr(v) for v in res])
#     # return res
#     print(i)
#     return float(i / n)
#
#
# print(cpu_util_test(100))


# def func(r_id):
#     print(r_id)
#     tm_st = time.time() * 1000
#     time.sleep(random.uniform(1, 3))
#     tm_end = time.time() * 1000
#     tm_invoke = fix_str_len(fstr(tm_end - tm_st), 18)
#     tm_st = fix_str_len(fstr(tm_st), 18)
#     tm_end = fix_str_len(fstr(tm_end), 18)
#     with open("logfile1", "a+") as f:
#         f.write(
#             str(r_id) + ":" +
#             tm_st + "#" +
#             tm_end + "#" +
#             tm_invoke + "\n")
#
#
# task_list = []
# for i in range(5):
#     t = Thread(target=func, args=(i,))
#     t.start()
#     task_list.append(t)
#
# for t in task_list:
#     t.join()
