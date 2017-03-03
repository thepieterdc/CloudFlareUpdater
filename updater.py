#!/usr/bin/env python3

import config
from src import functions

if __name__ == '__main__':
    success = True
    zoneIds = functions.zoneIds()

    for host in config.hosts.keys():
        zoneId = zoneIds[host]

        recordIds = functions.recordIds(config.hosts[host], zoneId)
        for record in recordIds:
            success = functions.autodetectAndUpdate(record["type"], record["name"], record["id"], zoneId) and success
