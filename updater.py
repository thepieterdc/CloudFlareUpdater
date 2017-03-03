#!/usr/bin/env python3

import config
from src import functions

if __name__ == '__main__':
    success = True
    zones = functions.zones()

    for host in config.hosts.keys():
        zone = zones[host]
        for record in zone.records:
            success = functions.autodetectAndUpdate(record) and success
