#!/usr/bin/env python3

import config
from src import functions

if __name__ == '__main__':
    success = True
    zoneIds = functions.zoneIds()

    for host in config.hosts.keys():
        zoneId = zoneIds[host]

        records = functions.recordInfo(config.hosts[host], zoneId)
        for record in records:
            success = functions.autodetectAndUpdate(record) and success
