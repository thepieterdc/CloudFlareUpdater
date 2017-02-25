import config
import json
import requests


def __get(endpoint: str) -> dict:
    """
    Calls an endpoint of the CloudFlare API using GET.
    :param endpoint: the API endpoint to call
    :return: the json response
    """
    headers = {"X-Auth-Email": config.cf_email, "X-Auth-Key": config.cf_apikey}
    return requests.get("https://api.cloudflare.com/client/v4{}".format(endpoint), headers=headers).json()


def __post(endpoint: str, data: dict) -> dict:
    """
    Calls an endpoint of the CloudFlare API using POST.
    :param endpoint: the API endpoint to call
    :param data: the data to post
    :return: the json response
    """
    headers = {"X-Auth-Email": config.cf_email, "X-Auth-Key": config.cf_apikey}
    return requests.post("https://api.cloudflare.com/client/v4{}".format(endpoint), json=data, headers=headers).json()


def __put(endpoint: str, data: dict) -> dict:
    """
    Calls an endpoint of the CloudFlare API using PUT.
    :param endpoint: the API endpoint to call
    :param data: the data to put
    :return: the json response
    """
    headers = {"X-Auth-Email": config.cf_email, "X-Auth-Key": config.cf_apikey}
    return requests.put("https://api.cloudflare.com/client/v4{}".format(endpoint), data=json.dumps(data),
                        headers=headers).json()


def ip() -> str:
    """
    Gets the WAN IP address.
    :return: WAN IP address of this host
    """
    req = requests.get("http://ipinfo.io").json()
    return req.get("ip")


def recordIds(records: list, zoneId: str) -> dict:
    """
    Gets the record id's to use from CloudFlare.
    :param records: a list of record names
    :param zoneId: the zone id
    :return: the record id's for every record name
    """
    req = __get("/zones/{}/dns_records".format(zoneId))
    if req.get("success"):
        ret = {}
        for host in req.get("result"):
            if host.get("name") in records:
                ret[host.get("name")] = host.get("id")
        return ret
    print("[ERROR] Could not get record id's from CloudFlare.")
    exit(2)


def update(record: str, recordId: str, ip: str, zoneId: str) -> bool:
    """
    Updates a given record with the new ip-address.
    :param record: the record name
    :param recordId: the record id
    :param ip: the new value
    :param zoneId: the zone id
    :return: True if successful
    """
    data = {"type": "A", "name": record, "content": ip}
    req = __put("/zones/{}/dns_records/{}".format(zoneId, recordId), data)
    if req.get("success"):
        return True
    print("[ERROR] Could not perform update on CloudFlare.")
    exit(3)


def zoneIds() -> dict:
    """
    Gets the zone id's to use from CloudFlare.
    :return: the zone id's for every host
    """
    req = __get("/zones")
    if req.get("success"):
        ret = {}
        for host in req.get("result"):
            if host.get("name") in config.hosts:
                ret[host.get("name")] = host.get("id")
        return ret
    print("[ERROR] Could not get zone id's from CloudFlare.")
    exit(1)
