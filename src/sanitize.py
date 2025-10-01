import ipaddress
import re


def check_ip_address(ip: str) -> bool:
    """Ensure IP address is valid"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def check_path(filepath: str) -> bool:
    """Ensure folder path provided is valid"""
    pattern = r"^(?:/[^/]+)*?/?(?:[^/]+\.[a-zA-Z0-9]+)?$"
    if not re.fullmatch(pattern, filepath):
        return False
    else:
        return True
