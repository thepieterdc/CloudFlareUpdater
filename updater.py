import config
import functions

if __name__ == '__main__':
    zoneIds = functions.zoneIds()

    for host in config.hosts.keys():
        recordIds = functions.recordIds(config.hosts[host], zoneIds[host])
        for record in recordIds.keys():
            functions.update(record, recordIds[record], functions.ip(), zoneIds[host])