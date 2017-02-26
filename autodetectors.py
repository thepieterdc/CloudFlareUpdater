import requests

def ip() -> str:
    """
    Gets the WAN IPv4 address.
    :return: WAN IPv4 address of this host
    """
    req = requests.get("http://ipinfo.io").json()
    return req.get("ip")


def ipv6() -> str:
    """
    Gets the WAN IPv6 address.
    :return: WAN IPv6 address of this host
    """
    raise NotImplementedError

recordValueDetectors = {"A": ip, "AAAA": ipv6}

