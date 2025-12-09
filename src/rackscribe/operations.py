import logging
import time
from collections.abc import Mapping
from pathlib import Path
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


def gather_running_configs(
    ip_list: list[str],
    out_dir: Path,
    show_stats: bool = False,
) -> None:
    """Connect to each device and save running configurations."""
    log.info("RACKSCRIBE START - OPERATION RUNNING CONFIGURATIONS")

    start = time.perf_counter()

    device_number = 0
    success_count = 0
    failure_count = 0

    for ip in ip_list:
        device_number += 1
        try:
            if not check_ip_address(ip):
                log.error(f"Invalid IP address: '{ip}'")
                failure_count += 1
                continue

            log.info(f"Connecting to host {ip} - Operation Gather Running Configurations")

            device: Mapping[str, Any] = load_device_attr(ip)
            hostname = get_hostname(device)
            output = send_cmd(device, "show running-config")
            final_output = remove_config_preamble(output)

            if create_config_file(f"{device_number}. {hostname}", out_dir, final_output):
                success_count += 1
            else:
                failure_count += 1
        except Exception as exc:  # noqa: BLE001
            failure_count += 1
            log.warning(
                f"No configuration saved for IP address {ip}. See rackscribe.log for details."
            )
            log.debug(
                f"Exception while collecting running configuration for IP address {ip}. Details: {exc}",
                exc_info=True,
            )
    elapsed = time.perf_counter() - start

    if show_stats:
        total = success_count + failure_count
        rate = success_count / elapsed if elapsed > 0 and total > 0 else 0.0
        log.info(
            f"[STATS] Running-config operation completed in {elapsed:2f} seconds | "
            f"Devices: {total} - Success: {success_count} - Failed: {failure_count} | "
            f"Rate: {rate:.2f} seconds per device."
        )
    else:
        log.debug(
            f"Running-config operation elapsed time: {elapsed:.2f} seconds "
            f"(success={success_count}, failure={failure_count})"
        )


def gather_serial_numbers(
    ip_list: list[str],
    out_file: str,
    out_dir: Path,
    show_stats: bool = False,
) -> None:
    """Connect to each device and collect serial numbers into an inventory table."""
    log.info("RACKSCRIBE START - OPERATION GATHER INVENTORY")

    start = time.perf_counter()

    device_number = 0
    inventory_table: list[list[str]] = []
    success_count = 0
    failure_count = 0

    for ip in ip_list:
        device_number += 1
        try:
            if not check_ip_address(ip):
                log.error(f"Invalid IP address: '{ip}'")
                failure_count += 1
                continue

            log.info(f"Connecting to host {ip}")

            device: Mapping[str, Any] = load_device_attr(ip)
            hostname = get_hostname(device)
            output = send_cmd(device, "show inventory")
            device_inventory = process_inventory_output(hostname, output)

            for item in device_inventory:
                inventory_table.append(item)

            log.info(f"Inventory information retrieved successfully from {hostname} ({ip})")
            success_count += 1

        except Exception as exc:  # noqa: BLE001
            failure_count += 1
            log.warning(f"No serial numbers saved for {ip}. See rackscribe.log for details.")
            log.debug(
                f"Exception while collecting inventory for IP address {ip}. Details: {exc}",
                exc_info=True,
            )

    write_ok = create_inventory_file(out_file, out_dir, inventory_table)

    elapsed = time.perf_counter() - start

    if show_stats:
        status = "Completed successfully" if write_ok else "Completed with output errors"
        total = success_count + failure_count
        rate = success_count / elapsed if elapsed > 0 and total > 0 else 0.0
        log.info(
            f"[STATS] Gather inventory operation completed in {elapsed:2f} seconds | "
            f"{status} | "
            f"Devices: {total} - Success: {success_count} - Failed: {failure_count} | "
            f"Rate: {rate:.2f} seconds per device."
        )
    else:
        log.debug(
            f"Gather inventory operation elapsed time: {elapsed:.2f} seconds "
            f"(success={success_count}, failure={failure_count})"
        )
