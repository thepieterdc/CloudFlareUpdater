import requests
import functools


@functools.lru_cache(maxsize=None)
def ip() -> str:
    """
    Gets the WAN IPv4 address.
    :return: WAN IPv4 address of this host
    """
    req = requests.get("https://4.ifcfg.me/ip")
    return req.text.strip()


@functools.lru_cache(maxsize=None)
def ipv6() -> str:
    """
    Gets the WAN IPv6 address.
    :return: WAN IPv6 address of this host
    """
    req = requests.get("https://6.ifcfg.me/ip")
    return req.text.strip()


recordValueDetectors = {"A": ip, "AAAA": ipv6}

