import argparse
import logging

from dotenv import load_dotenv

from src.commands import get_hostname, send_cmd
from src.inventory import load_device_attr, load_inventory
from src.logging_setup import logging_setup
from src.output import create_config_file, process_inventory_output
from src.sanitize import check_ip_address


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="rackscribe", description="Gather running configurations and serial numbers."
    )
    parser.add_argument(
        "-r", "--running_config", action="store_true", help="Collect all running configurations."
    )
    parser.add_argument(
        "-s", "--serial_numbers", action="store_true", help="Collect serial numbers."
    )
    parser.add_argument("-l", "--log_level", type=int, default=3, help="Logging level.")
    parser.add_argument(
        "-i", "--inventory", type=str, default="inventory/lab.yaml", help="Inventory yml file path."
    )

    args = parser.parse_args()

    load_dotenv()

    logging_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
    logging_setup(logging_levels[args.log_level])
    log = logging.getLogger("rackscribe")

    ip_list = load_inventory(args.inventory)

    # TESTING

    if ip_list and len(ip_list) > 0:
        log.info("Loaded %d device(s).", len(ip_list))
        device_number = 0

        if args.running_config:
            for ip in ip_list:
                device_number += 1
                try:
                    if check_ip_address(ip):
                        log.info(f"Connecting to {ip}")
                        device = load_device_attr(ip)
                        hostname = get_hostname(device)
                        output = send_cmd(device, "show running-config")
                        create_config_file(f"{device_number}. {hostname}", output)
                    else:
                        log.error(f"Invalid IP address: '{ip}'")
                except Exception:
                    log.warning(f"No configuration saved for {ip}. See above for details.")

        elif args.serial_numbers:
            inventory_table_rows: list[list[str]] = []
            for ip in ip_list:
                device_number += 1
                try:
                    if check_ip_address(ip):
                        log.info(f"Connecting to {ip}")
                        device = load_device_attr(ip)
                        hostname = get_hostname(device)
                        output = send_cmd(device, "show inventory")
                        processed_output = process_inventory_output(hostname, output)
                        inventory_table_rows.append(processed_output)

                    else:
                        log.error(f"Invalid IP address: '{ip}'")
                except Exception:
                    log.warning(f"No serial numbers saved for {ip}. See above for details.")
        else:
            print("Use 'rackscribe --help' to display flag options.")
    else:
        log.error(f"Error loading IP address list. Check '{args.inventory}' ")
    # -----


if __name__ == "__main__":
    main()
