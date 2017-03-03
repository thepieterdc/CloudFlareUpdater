#!/usr/bin/env python3

import config
from src import functions

if __name__ == '__main__':
    success = True
    zones = functions.zones()

    for host in config.hosts.keys():
        zone = zones[host]

        records = functions.recordInfo(config.hosts[host], zone)
        for record in records:
            success = functions.autodetectAndUpdate(record) and success
