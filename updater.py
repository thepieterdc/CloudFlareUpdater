#!/usr/bin/env python3

import config
from src import functions

if __name__ == '__main__':
    zoneIds = functions.zoneIds()

    for host in config.hosts.keys():
        recordIds = functions.recordIds(config.hosts[host].keys(), zoneIds[host])
        for recordName in recordIds.keys():
            for recordType in config.hosts[host][recordName]:
                functions.autodetectAndUpdate(recordType, recordName, recordIds[recordName], zoneIds[host])
