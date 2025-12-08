import ipaddress
import re


def check_ip_address(ip: str) -> bool:
    """Ensure IP address is valid"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def check_valid_chars(filepath: str) -> bool:
    """Checks valid characters for file paths and names"""
    pattern = r"^(?:/[^/]+)*?/?(?:[^/]+\.[a-zA-Z0-9]+)?$"
    if not re.fullmatch(pattern, filepath):
        return False
    else:
        return True
