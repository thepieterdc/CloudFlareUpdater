import config
import json
import requests
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


def records(zone: Zone) -> {}:
    """
    Gets information about a record to use from CloudFlare.
    :param records: a dictionary of record names to lists of requests record types
    :param zoneId: the zone ID
    :return: list of dictionaries with the record IDs, names, types and current values
    """
    req = __get("/zones/{}/dns_records".format(zoneId))
    if req.get("success"):
        ret = []
        for host in req.get("result"):
            name = host.get("name")
            if name in records and host.get("type") in records[name]:
                ret.append({
                    "zoneId": zoneId,
                    "id": host.get("id"),
                    "name": name,
                    "type": host.get("type"),
                    "currentValue": host.get("content")
                })
        return ret
    else:
        print("[ERROR] Could not get record IDs from CloudFlare. Make sure to use the Global API key, not the Origin CA one.")
        exit(2)


def update(recordInfo: dict, newValue: str) -> bool:
    """
    Updates a given record with the new ip-address.
    :param recordInfo: dictionary with the record type (A/AAAA), name, id, and zoneId
    :param newValue: the new value for the record
    :return: True if successful, else False
    """
    data = {"type": recordInfo["type"], "name": recordInfo["name"], "content": newValue}
    req = __put("/zones/{zoneId}/dns_records/{id}".format(**recordInfo), data)

    if req.get("success"):
        print("[SUCCESS] Set {type} record for {name} to {value}.".format(value=newValue, **recordInfo))
        return True
    else:
        print("[ERROR] Failed to set {type} record for {name} to {value}.".format(value=newValue, **recordInfo))
        print("        CF reported error: {}".format(req.get("error")))
        return False


def autodetectAndUpdate(recordInfo: dict) -> bool:
    """
    Autodetects IP address of the current host and updates the
        requested record with it.
    :param recordInfo: dictionary with Records.
    :return: True if successful
    """
    if recordInfo["type"] not in recordValueDetectors:
        print("[ERROR] No autodetector for records of type {} found.".format(recordInfo["type"]))
        exit(4)

    recordValue = recordValueDetectors[recordInfo["type"]]()
    if recordValue == recordInfo["currentValue"]:
        print("[SUCCESS] {type} record for {name} not changed.".format(**recordInfo))
        return True
    else:
        return update(recordInfo, recordValue)


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
