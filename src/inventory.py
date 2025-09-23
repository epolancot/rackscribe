import os

import yaml


def load_inventory(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        devices = yaml.safe_load(f)

        return devices


def load_device_attr(ip: str) -> dict:
    device = {
        "device_type": os.getenv("DEVICE_TYPE"),
        "host": ip,
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
        "secret": os.getenv("SECRET"),
    }

    return device
