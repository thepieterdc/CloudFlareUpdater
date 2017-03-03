import config
import json
import requests
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


def recordIds(records: dict, zoneId: str) -> list:
    """
    Gets the record IDs to use from CloudFlare.
    :param records: a list of record names
    :param zoneId: the zone ID
    :return: the record IDs for every record name
    """
    req = __get("/zones/{}/dns_records".format(zoneId))
    if req.get("success"):
        ret = []
        for host in req.get("result"):
            name = host.get("name")
            if name in records and host.get("type") in records[name]:
                ret.append({"id": host.get("id"), "name": name, "type": host.get("type")})
        return ret
    else:
        print("[ERROR] Could not get record IDs from CloudFlare. Make sure to use the Global API key, not the Origin CA one.")
        exit(2)


def update(recordType: str, recordName: str, recordId: str, recordValue: str, zoneId: str) -> bool:
    """
    Updates a given record with the new ip-address.
    :param recordType: the record type (A/AAAA)
    :param recordName: the record name
    :param recordId: the record id
    :param recordValue: the new value
    :param zoneId: the zone id
    :return: True if successful, else False
    """
    data = {"type": recordType, "name": recordName, "content": recordValue}
    req = __put("/zones/{}/dns_records/{}".format(zoneId, recordId), data)

    if req.get("success"):
        print("[SUCCESS] Set {} record for {} to {}.".format(recordType, recordName, recordValue))
        return True
    else:
        print("[ERROR] Failed to set {} record for {} to {}.".format(recordType, recordName, recordValue))
        print("        Error: {}".format(req.json()["error"]))
        return False


def autodetectAndUpdate(recordType: str, recordName: str, recordId: str, zoneId: str) -> bool:
    """
    Autodetects IP address of the current host and updates the
        requested record with it.
    :param recordType: the record type (A/AAAA)
    :param recordName: the record name
    :param recordId: the record id
    :param zoneId: the zone id
    :return: True if successful
    """
    if recordType not in recordValueDetectors:
        print("[ERROR] No autodetector for records of type {} found.".format(recordType))
        exit(4)

    recordValue = recordValueDetectors[recordType]()
    return update(recordType, recordName, recordId, recordValue, zoneId)


def zoneIds() -> dict:
    """
    Gets the zone IDs to use from CloudFlare.
    :return: the zone IDs for every host
    """
    req = __get("/zones")
    if req.get("success"):
        ret = {}
        for host in req.get("result"):
            if host.get("name") in config.hosts:
                ret[host.get("name")] = host.get("id")
        return ret
    else:
        print("[ERROR] Could not get zone IDs from CloudFlare.")
        exit(1)