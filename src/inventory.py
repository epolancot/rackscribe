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
            inventory = list(dict.fromkeys(devices["inventory"]))

            return inventory
    except TypeError as e:
        log.error(f"Error loading inventory file.\n '{e}'.")
    except FileNotFoundError:
        log.error(f"Inventory file not found: '{path}'")

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
