import decimal


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
    buf = open('/proc/meminfo').read()
    buf = ','.join([v.replace(' ', '') for v in
                    buf.split('\n') if v])

    return buf


def get_basic_info():
    mem_info = get_mem_info()
    res = {
        'mem_info': mem_info
    }
    return res
