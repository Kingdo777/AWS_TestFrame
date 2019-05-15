import decimal
import json
import os
import subprocess
import time


def run_cmd(cmd):
    return os.popen(cmd).read().strip("\n")


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


def write_test():
    for i in range(20 * 1024):
        with open("/tmp/file", "w") as f:
            f.write("#")


def cpu_util_test(n):
    """
    CPU utilization test. Recording N timestamps continuously

    Args: N

    Return:
            The timestamps recorded. Only return unique timestamps
    """
    res = {}
    t1 = int(time.time() * 1000)
    while True:
        t2 = int(time.time() * 1000)
        if t2 - t1 >= n:
            break
        res[t2] = 0
    res = sorted(res.keys())
    i = len(res)
    # res = ";".join([fstr(v) for v in res])
    # return res
    print(i)
    return float(i / n)


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
    buf = str(err).split(",")[-2:]
    t, s = buf[-2].replace(" ", ""), buf[-1][1:-3]
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
    return "#".join(bufs)


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

    run_cmd("cp ./iperf3 /tmp/iperf3")
    run_cmd("chmod +x /tmp/iperf3")
    run_cmd("/tmp/iperf3 -s")
    sp = subprocess.Popen(["/tmp/iperf3",
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
    return bps
