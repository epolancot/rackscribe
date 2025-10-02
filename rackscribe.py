import argparse
import logging
from datetime import datetime

from dotenv import load_dotenv

from src.commands import get_hostname, send_cmd
from src.inventory import load_device_attr, load_inventory
from src.logging_setup import logging_setup
from src.output import create_config_file, create_inventory_file, process_inventory_output
from src.sanitize import check_ip_address


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="rackscribe", description="Gather running configurations and serial numbers."
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-r", "--running_config", action="store_true", help="Collect all running configurations."
    )
    group.add_argument(
        "-s", "--serial_numbers", action="store_true", help="Collect serial numbers."
    )
    parser.add_argument(
        "-l",
        "--log_level",
        type=int,
        default=3,
        choices=range(5),
        help="Logging level: 0-Critical, 1-Error, 2-Warning, 3-Info, 4-Debug",
    )
    parser.add_argument(
        "-i", "--inventory", type=str, default="inventory/lab.yaml", help="Inventory yml file path."
    )
    parser.add_argument("-o", "--out_dir", type=str, default="output/", help="Output folder path.")

    args = parser.parse_args()

    load_dotenv()

    logging_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
    logging_setup(logging_levels[args.log_level])
    log = logging.getLogger("rackscribe")

    ip_list = load_inventory(args.inventory)

    if ip_list and len(ip_list) > 0:
        log.info("Loaded %d device(s).", len(ip_list))
        device_number = 0

        if args.running_config:
            log.info("RACKSCRIBE START - OPERATION RUNNING CONFIGURATIONS")
            for ip in ip_list:
                device_number += 1
                try:
                    if check_ip_address(ip):
                        log.info(f"Connecting to {ip} - Operation Gather Running Configurations")
                        device = load_device_attr(ip)
                        hostname = get_hostname(device)
                        output = send_cmd(device, "show running-config")
                        create_config_file(f"{device_number}. {hostname}", output)
                    else:
                        log.error(f"Invalid IP address: '{ip}'")
                except Exception as e:
                    log.warning(f"No configuration saved for {ip}. See logs for details. {e}")

        elif args.serial_numbers:
            log.info("RACKSCRIBE START - OPERATION GATHER INVENTORY")
            inventory_table: list[list[str]] = []

            for ip in ip_list:
                device_number += 1
                try:
                    if check_ip_address(ip):
                        log.info(f"Connecting to {ip}")
                        device = load_device_attr(ip)
                        hostname = get_hostname(device)
                        output = send_cmd(device, "show inventory")
                        device_inventory = process_inventory_output(hostname, output)
                        for item in device_inventory:
                            inventory_table.append(item)

                    else:
                        log.error(f"Invalid IP address: '{ip}'")
                except Exception as e:
                    log.warning(f"No serial numbers saved for {ip}. See logs for details. {e}")

            now = datetime.now()
            timestamp_str = now.strftime("%Y%m%d-%H%M%S")
            filename = f"Inventory_{timestamp_str}"
            create_inventory_file(filename, inventory_table)
        else:
            print("Use 'rackscribe --help' to display flag options.")
    else:
        log.error(f"Error loading IP address list. Check '{args.inventory}' ")


if __name__ == "__main__":
    main()
