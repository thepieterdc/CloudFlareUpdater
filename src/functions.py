import config
import json
import requests
from src.record import Record
from src.zone import Zone
from src.autodetectors import recordValueDetectors


def __get(endpoint: str) -> dict:
    """
    Calls an endpoint of the CloudFlare API using GET.
    :param endpoint: the API endpoint to call
    :return: the JSON response
    """
    headers = {"X-Auth-Email": config.cf_email, "X-Auth-Key": config.cf_apikey}
    return requests.get("https://api.cloudflare.com/client/v4{}".format(endpoint), headers=headers).json()


def __post(endpoint: str, data: dict) -> dict:
    """
    Calls an endpoint of the CloudFlare API using POST.
    :param endpoint: the API endpoint to call
    :param data: the data to post
    :return: the JSON response
    """
    headers = {"X-Auth-Email": config.cf_email, "X-Auth-Key": config.cf_apikey}
    return requests.post("https://api.cloudflare.com/client/v4{}".format(endpoint), json=data, headers=headers).json()


def __put(endpoint: str, data: dict) -> dict:
    """
    Calls an endpoint of the CloudFlare API using PUT.
    :param endpoint: the API endpoint to call
    :param data: the data to put
    :return: the JSON response
    """
    headers = {"X-Auth-Email": config.cf_email, "X-Auth-Key": config.cf_apikey}
    return requests.put("https://api.cloudflare.com/client/v4{}".format(endpoint), data=json.dumps(data),
                        headers=headers).json()


def records(zone: Zone) -> []:
    """
    Gets information about a record to use from CloudFlare.
    :param records: a dictionary of record names to lists of requests record types
    :param zoneId: the zone ID
    :return: list of dictionaries with the record IDs, names, types and current values
    """
    req = __get("/zones/{}/dns_records".format(zone.id))
    if req.get("success"):
        ret = []
        for rec in req.get("result"):
            record = Record(rec, zone)
            if record.name in config.hosts[zone.name] and record.type in config.hosts[zone.name][record.name]:
                ret.append(record)
        return ret
    else:
        print(
            "[ERROR] Could not get record IDs from CloudFlare. Make sure to use the Global API key, not the Origin CA one.")
        exit(2)


def update(record: Record) -> bool:
    """
    Updates a given record with the new ip-address.
    :param recordInfo: the updated record
    :return: True if successful, else False
    """
    data = {"type": record.type, "name": record.name, "content": record.content, "ttl": record.ttl,
            "proxied": record.proxied}
    req = __put("/zones/{zoneId}/dns_records/{id}".format(zoneId=record.zone.id, id=record.id), data)

    if req.get("success"):
        print("[SUCCESS] Set {type} record for {name} to {value}.".format(value=record.content, type=record.type,
                                                                          name=record.name))
        return True
    else:
        print(
            "[ERROR] Failed to set {type} record for {name} to {value}.".format(value=record.content, type=record.type,
                                                                                name=record.name))
        print("        CF reported error: {}".format(req.get("error")))
        return False


def autodetectAndUpdate(record: Record) -> bool:
    """
    Autodetects IP address of the current host and updates the
        requested record with it.
    :param record: the record to update
    :return: True if successful
    """
    if record.type not in recordValueDetectors:
        print("[ERROR] No autodetector for records of type {} found.".format(record.type))
        exit(4)

    newval = recordValueDetectors[record.type]()
    if newval == record.content:
        print("[SUCCESS] {} record for {} not changed.".format(record.type, record.name))
        return True
    else:
        record.content = newval
        return update(record)


def zones() -> dict:
    """
    Gets the zones to use from CloudFlare.
    :return: the zones for every host
    """
    req = __get("/zones")
    if req.get("success"):
        ret = {}
        for host in req.get("result"):
            if host.get("name") in config.hosts:
                zone = Zone(host)
                zone.records = records(zone)
                ret[host.get("name")] = zone
        return ret
    else:
        print("[ERROR] Could not get zone IDs from CloudFlare.")
        exit(1)
