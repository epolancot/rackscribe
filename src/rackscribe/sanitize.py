import ipaddress
import re
from pathlib import Path


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


def validate_output_path(out_dir: str) -> Path:
    """
    Validate and normalize the output directory.
    Returns a Path object if valid, raises ValueError if not.
    """
    path = Path(out_dir).expanduser()

    if path.is_absolute() and not path.exists():
        raise ValueError(
            f"Output path '{out_dir}' appears to be an absolute root path that does not exist "
            f"or is not writable. Try a relative path like 'output/' or './output/'"
        )
    return path
