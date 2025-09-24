import logging
import os

import yaml


def load_inventory(path: str) -> dict:
    log = logging.getLogger("rackscribe")
    try:
        with open(path, encoding="utf-8") as f:
            devices = yaml.safe_load(f)

            return devices
    except Exception as e:
        log.info(f"Error loading inventory file.\n '{e}'.")


def load_device_attr(ip: str) -> dict:
    device = {
        "device_type": os.getenv("DEVICE_TYPE"),
        "host": ip,
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
        "secret": os.getenv("SECRET"),
    }

    return device
