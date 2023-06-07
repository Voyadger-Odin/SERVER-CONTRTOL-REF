import argparse
import datetime
import socket
import sys
import psutil
from psutil._common import bytes2human

ACCESS_DENIED = ''
NON_VERBOSE_ITERATIONS = 4
RLIMITS_MAP = {
    "RLIMIT_AS": "virtualmem",
    "RLIMIT_CORE": "coredumpsize",
    "RLIMIT_CPU": "cputime",
    "RLIMIT_DATA": "datasize",
    "RLIMIT_FSIZE": "filesize",
    "RLIMIT_MEMLOCK": "memlock",
    "RLIMIT_MSGQUEUE": "msgqueue",
    "RLIMIT_NICE": "nice",
    "RLIMIT_NOFILE": "openfiles",
    "RLIMIT_NPROC": "maxprocesses",
    "RLIMIT_NPTS": "pseudoterms",
    "RLIMIT_RSS": "rss",
    "RLIMIT_RTPRIO": "realtimeprio",
    "RLIMIT_RTTIME": "rtimesched",
    "RLIMIT_SBSIZE": "sockbufsize",
    "RLIMIT_SIGPENDING": "sigspending",
    "RLIMIT_STACK": "stack",
    "RLIMIT_SWAP": "swapuse",
}

def print_(a, b):
    if sys.stdout.isatty() and psutil.POSIX:
        fmt = '\x1b[1;32m%-13s\x1b[0m %s' % (a, b)
    else:
        fmt = '%-11s %s' % (a, b)
    print(fmt)

def str_ntuple(nt, convert_bytes=False):
    if nt == ACCESS_DENIED:
        return ""
    if not convert_bytes:
        return ", ".join(["%s=%s" % (x, getattr(nt, x)) for x in nt._fields])
    else:
        return ", ".join(["%s=%s" % (x, bytes2human(getattr(nt, x)))
                          for x in nt._fields])

def run(pid, verbose=False):
    try:
        proc = psutil.Process(pid)
        pinfo = proc.as_dict(ad_value=ACCESS_DENIED)
    except psutil.NoSuchProcess as err:
        sys.exit(str(err))

    # collect other proc info
    with proc.oneshot():
        try:
            parent = proc.parent()
            if parent:
                parent = '(%s)' % parent.name()
            else:
                parent = ''
        except psutil.Error:
            parent = ''
        try:
            pinfo['children'] = proc.children()
        except psutil.Error:
            pinfo['children'] = []
        if pinfo['create_time']:
            started = datetime.datetime.fromtimestamp(
                pinfo['create_time']).strftime('%Y-%m-%d %H:%M')
        else:
            started = ACCESS_DENIED

    print_('pid', pinfo['pid'])
    print_('name', pinfo['name'])
    print_('parent', '%s %s' % (pinfo['ppid'], parent))
    print_('exe', pinfo['exe'])
    print_('cwd', pinfo['cwd'])
    print_('cmdline', ' '.join(pinfo['cmdline']))
    print_('started', started)

    cpu_tot_time = datetime.timedelta(seconds=sum(pinfo['cpu_times']))
    cpu_tot_time = "%s:%s.%s" % (
        cpu_tot_time.seconds // 60 % 60,
        str((cpu_tot_time.seconds % 60)).zfill(2),
        str(cpu_tot_time.microseconds)[:2])
    print_('cpu-tspent', cpu_tot_time)
    print_('cpu-times', str_ntuple(pinfo['cpu_times']))
    if hasattr(proc, "cpu_affinity"):
        print_("cpu-affinity", pinfo["cpu_affinity"])
    if hasattr(proc, "cpu_num"):
        print_("cpu-num", pinfo["cpu_num"])

    print_('memory', str_ntuple(pinfo['memory_info'], convert_bytes=True))
    print_('memory %', round(pinfo['memory_percent'], 2))
    print_('user', pinfo['username'])
    if psutil.POSIX:
        print_('uids', str_ntuple(pinfo['uids']))
    if psutil.POSIX:
        print_('uids', str_ntuple(pinfo['uids']))
    if psutil.POSIX:
        print_('terminal', pinfo['terminal'] or '')

    print_('status', pinfo['status'])
    print_('nice', pinfo['nice'])
    if hasattr(proc, "ionice"):
        try:
            ionice = proc.ionice()
        except psutil.Error:
            pass
        else:
            if psutil.WINDOWS:
                print_("ionice", ionice)
            else:
                print_("ionice", "class=%s, value=%s" % (
                    str(ionice.ioclass), ionice.value))

    print_('num-threads', pinfo['num_threads'])
    if psutil.POSIX:
        print_('num-fds', pinfo['num_fds'])
    if psutil.WINDOWS:
        print_('num-handles', pinfo['num_handles'])

    if 'io_counters' in pinfo:
        print_('I/O', str_ntuple(pinfo['io_counters'], convert_bytes=True))
    if 'num_ctx_switches' in pinfo:
        print_("ctx-switches", str_ntuple(pinfo['num_ctx_switches']))
    if pinfo['children']:
        template = "%-6s %s"
        print_("children", template % ("PID", "NAME"))
        for child in pinfo['children']:
            try:
                print_('', template % (child.pid, child.name()))
            except psutil.AccessDenied:
                print_('', template % (child.pid, ""))
            except psutil.NoSuchProcess:
                pass

    if pinfo['open_files']:
        print_('open-files', 'PATH')
        for i, file in enumerate(pinfo['open_files']):
            if not verbose and i >= NON_VERBOSE_ITERATIONS:
                print_("", "[...]")
                break
            print_('', file.path)
    else:
        print_('open-files', '')

    if pinfo['connections']:
        template = '%-5s %-25s %-25s %s'
        print_('connections',
               template % ('PROTO', 'LOCAL ADDR', 'REMOTE ADDR', 'STATUS'))
        for conn in pinfo['connections']:
            if conn.type == socket.SOCK_STREAM:
                type = 'TCP'
            elif conn.type == socket.SOCK_DGRAM:
                type = 'UDP'
            else:
                type = 'UNIX'
            lip, lport = conn.laddr
            if not conn.raddr:
                rip, rport = '*', '*'
            else:
                rip, rport = conn.raddr
            print_('', template % (
                type,
                "%s:%s" % (lip, lport),
                "%s:%s" % (rip, rport),
                conn.status))
    else:
        print_('connections', '')

    if pinfo['threads'] and len(pinfo['threads']) > 1:
        template = "%-5s %12s %12s"
        print_('threads', template % ("TID", "USER", "SYSTEM"))
        for i, thread in enumerate(pinfo['threads']):
            if not verbose and i >= NON_VERBOSE_ITERATIONS:
                print_("", "[...]")
                break
            print_('', template % thread)
        print_('', "total=%s" % len(pinfo['threads']))
    else:
        print_('threads', '')

    if hasattr(proc, "rlimit"):
        res_names = [x for x in dir(psutil) if x.startswith("RLIMIT")]
        resources = []
        for res_name in res_names:
            try:
                soft, hard = proc.rlimit(getattr(psutil, res_name))
            except psutil.AccessDenied:
                pass
            else:
                resources.append((res_name, soft, hard))
        if resources:
            template = "%-12s %15s %15s"
            print_("res-limits", template % ("RLIMIT", "SOFT", "HARD"))
            for res_name, soft, hard in resources:
                if soft == psutil.RLIM_INFINITY:
                    soft = "infinity"
                if hard == psutil.RLIM_INFINITY:
                    hard = "infinity"
                print_('', template % (
                    RLIMITS_MAP.get(res_name, res_name), soft, hard))

    if hasattr(proc, "environ") and pinfo['environ']:
        template = "%-25s %s"
        print_("environ", template % ("NAME", "VALUE"))
        for i, k in enumerate(sorted(pinfo['environ'])):
            if not verbose and i >= NON_VERBOSE_ITERATIONS:
                print_("", "[...]")
                break
            print_("", template % (k, pinfo['environ'][k]))

    if pinfo.get('memory_maps', None):
        template = "%-8s %s"
        print_("mem-maps", template % ("RSS", "PATH"))
        maps = sorted(pinfo['memory_maps'], key=lambda x: x.rss, reverse=True)
        for i, region in enumerate(maps):
            if not verbose and i >= NON_VERBOSE_ITERATIONS:
                print_("", "[...]")
                break
            print_("", template % (bytes2human(region.rss), region.path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="печать информации о процессе")
    parser.add_argument("pid", type=int, help="process pid", nargs='?')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help="дополнительная информация")
    args = parser.parse_args()
    run(args.pid, args.verbose)