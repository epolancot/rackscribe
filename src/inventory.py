import logging
import os

import yaml


def load_inventory(path: str) -> list:
    """Load inventory from .yaml file and return set (unique IPs)"""
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


def load_device_attr(ip: str) -> dict:
    device = {
        "device_type": os.getenv("DEVICE_TYPE"),
        "host": ip,
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
        "secret": os.getenv("SECRET"),
    }

    return device
