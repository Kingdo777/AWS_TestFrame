import decimal
import os
import socket
import uuid
from urllib.request import urlopen

# Set it to your own servers
INST_PRIV_IP_DST = "8.8.8.8"
VM_PUB_ID_DST = "http://ip.42.pl/raw"


def fstr(f):
    """
    Convert a float number to string
    """

    ctx = decimal.Context()
    ctx.prec = 20
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')


def get_mem_info():
    """
    Get and format the content of /proc/meminfo
    """
    res = {}
    buf = open('/proc/meminfo').read()
    for v in [v.replace(' ', '') for v in buf.split('\n') if v]:
        res[v.split(':')[0]] = v.split(':')[1]
    return res


def get_vmstat():
    """
    Get and format the content of /proc/vmstat
    """
    buf = open("/proc/vmstat").read()
    buf = [v.replace(' ', ":") for v in buf.split("\n")]
    buf = ";".join(buf)
    return buf


def get_diskstat():
    """
    Get and format the content of /proc/diskstats
    """
    buf = open("/proc/diskstats").read()
    buf = [v for v in buf.split("\n") if v]
    buf = [
        v.replace(
            " ",
            ",").replace(
            ",,,,,,,",
            ",").replace(
            ",,,",
            "").lstrip(",") for v in buf]
    buf = ";".join(buf)
    return buf


def get_cpuinfo():
    """
    Get and format the content of /proc/cpuinfo
    """
    buf = "".join(open("/proc/cpuinfo").readlines())
    cpuinfo = buf.replace("\n", ";").replace("\t", "")
    return cpuinfo


def get_cpuinfo_short():
    """ Get CPU version information """
    buf = "".join(open("/proc/cpuinfo").readlines())
    cpuinfo = buf.replace("\n", ";").replace("\t", "")
    a1 = cpuinfo.count("processor")
    a2 = cpuinfo.split(";")[4].split(":")[1].strip()
    return "%s,%s" % (a1, a2)


def get_inst_id():
    """ Get the inst ID """
    log_file = '/tmp/inst_id.txt'
    new_id = str(uuid.uuid4())
    try:
        exist_id = open(log_file).read().strip('\n')
    except BaseException:
        open(log_file, 'w').write(new_id)
        exist_id = new_id
    return exist_id, new_id


def get_inst_priv_ip():
    """ Get inst private IP """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((INST_PRIV_IP_DST, 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def get_vm_priv_ip():
    """ Get VM private IP """
    ip = socket.gethostbyname(socket.getfqdn())
    return ip


def get_vm_pub_ip():
    """ Get VM public IP by querying external server """
    ip = "None"
    try:
        ip = str(urlopen(VM_PUB_ID_DST).read())
    except BaseException:
        pass
    return ip


def get_vm_id():
    """ Get VM ID from /proc/self/cgroup """
    buf = open('/proc/self/cgroup').read().split('\n')[-3].split('/')
    vm_id, inst_id = buf[1], buf[2]
    return vm_id, inst_id


def get_uptime():
    """ Get VM uptime """
    uptime = ','.join(open('/proc/uptime').read().strip('\n').split(' '))
    return uptime


def stat_other():
    hostname = os.popen('uname -n').read().strip('\n')
    kernel_ver = os.popen('uname -r').read().strip('\n')
    return [hostname, kernel_ver]


def get_basic_info():
    # 每个instance代表了一个container，同一个function的instance所在的container不会马上被回收，也就是说/tmp是暂时驻留的
    # new_id每次都是重新生成的，exist_id和new_id相同说明，该容器是第一次被创建，不同说明是已经存在于内存当中的
    exist_id, new_id = get_inst_id()
    # 这里我不是很能理解，难道说每个虚拟机的vm_id都相同，然后每一个instance的inst_id都是变得
    # 我认为exist_id就是表示了虚拟机下的容器，new_id标识的是一个新的instance
    vm_id, inst_id = get_vm_id()
    # 这个从侧面反映是否是在同一虚拟机中
    uptime = get_uptime()
    # vm_priv_ip = get_vm_priv_ip()
    # vm_pub_ip = get_vm_pub_ip()
    # inst_priv_ip = get_inst_priv_ip()
    # cpu_info = get_cpuinfo_short()

    res = {
        'exist_id': exist_id,
        'new_id': new_id,
        'vm_id': vm_id,
        'inst_id': inst_id,
        'uptime': uptime,
        # 'vm_priv_ip': vm_priv_ip,
        # 'vm_pub_ip': vm_pub_ip,
        # 'inst_priv_ip': inst_priv_ip,
        # 'cpu_info': cpu_info
    }
    return res
