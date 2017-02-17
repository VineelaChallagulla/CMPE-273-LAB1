#!/usr/bin/python

# Network Socket Monitoring Tool

import collections
import psutil


def main():
    pid_num_of_connections_map = {}
    pid_connections_map = {}

    for c in psutil.net_connections():
        if pid_num_of_connections_map.get(c.pid):
            connections = pid_num_of_connections_map[c.pid] + 1
            pid_num_of_connections_map[c.pid] = connections
        else:
            pid_num_of_connections_map[c.pid] = 1
        pid_connections_map.setdefault(c.pid, []).append(c)
    pid_connections_descending = \
        collections.OrderedDict(sorted(pid_num_of_connections_map.items(),
                                key=lambda (k, v): v, reverse=True))
    print '"pid",', '"laddr","raddr","status"'

    for pid in pid_connections_descending:
        for c in pid_connections_map[pid]:
            laddr = '%s:%s' % c.laddr
            raddr = '-'
            if c.raddr:
                raddr = '%s:%s' % c.raddr
            print '"' + str(c.pid or '-') + '"' + ', "' + laddr + '"' \
                + ', ' + '"' + str(raddr) + '"' + ', ' + '"' \
                + str(c.status) + '"'


if __name__ == '__main__':
    main()
