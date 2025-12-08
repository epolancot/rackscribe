import logging
import os

import yaml


def load_inventory(path: str) -> list:
    """Load inventory from .yaml file. Use dict.fromkeys() to filter duplicates"""
    devices = None
    log = logging.getLogger("rackscribe")
    try:
        with open(path, encoding="utf-8") as f:
            devices = yaml.safe_load(f)

        if not isinstance(devices, dict):
            log.error(f"Invalid inventory format in file: {path}")
            return []

        # Case-insensitive key handling
        normalized_devices = {k.lower(): v for k, v in devices.items()}

        if "inventory" not in normalized_devices:
            log.error(
                f"Missing 'inventory' key in inventory file: '{path}'. See README for proper inventory file format."
            )
            return []

        inventory = list(dict.fromkeys(normalized_devices["inventory"]))
        return inventory

    except FileNotFoundError:
        log.error(f"Inventory file not found: {path}")

    except yaml.YAMLError as exc:
        log.error(f"Invalid YAML format in inventory file {path}: {exc}")

    except Exception as exc:
        log.exception(f"Unexpected error loading inventory file {path}: {exc}")
        raise
    return []


def load_device_attr(ip: str) -> dict:
    device = {
        "device_type": os.getenv("DEVICE_TYPE"),
        "host": ip,
        "username": os.getenv("DEVICE_USERNAME"),
        "password": os.getenv("DEVICE_PASSWORD"),
        "secret": os.getenv("DEVICE_SECRET"),
    }

    return device
