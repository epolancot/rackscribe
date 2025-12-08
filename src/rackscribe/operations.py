import logging
from collections.abc import Mapping
from typing import Any

from .commands import get_hostname, send_cmd
from .inventory import load_device_attr
from .output import (
    create_config_file,
    create_inventory_file,
    process_inventory_output,
    remove_config_preamble,
)
from .sanitize import check_ip_address

log = logging.getLogger("rackscribe")


def gather_running_configs(ip_list: list[str]) -> None:
    """Connect to each device and save running configurations."""
    log.info("RACKSCRIBE START - OPERATION RUNNING CONFIGURATIONS")

    device_number = 0

    for ip in ip_list:
        device_number += 1
        try:
            if not check_ip_address(ip):
                log.error(f"Invalid IP address: '{ip}'")
                continue

            log.info(f"Connecting to host {ip} - Operation Gather Running Configurations")

            device: Mapping[str, Any] = load_device_attr(ip)
            hostname = get_hostname(device)
            output = send_cmd(device, "show running-config")
            final_output = remove_config_preamble(output)

            create_config_file(f"{device_number}. {hostname}", final_output)
        except Exception as exc:  # noqa: BLE001
            log.warning(f"No configuration saved for IP address {ip}. See logs for details. {exc}")


def gather_serial_numbers(
    ip_list: list[str],
    out_file: str,
    out_dir: str,
) -> None:
    """Connect to each device and collect serial numbers into an inventory table."""
    log.info("RACKSCRIBE START - OPERATION GATHER INVENTORY")

    device_number = 0
    inventory_table: list[list[str]] = []

    for ip in ip_list:
        device_number += 1
        try:
            if not check_ip_address(ip):
                log.error(f"Invalid IP address: '{ip}'")
                continue

            log.info(f"Connecting to host {ip}")

            device: Mapping[str, Any] = load_device_attr(ip)
            hostname = get_hostname(device)
            output = send_cmd(device, "show inventory")
            device_inventory = process_inventory_output(hostname, output)

            for item in device_inventory:
                inventory_table.append(item)
        except Exception as exc:  # noqa: BLE001
            log.warning(f"No serial numbers saved for {ip}. See logs for details. {exc}")

    create_inventory_file(out_file, out_dir, inventory_table)
