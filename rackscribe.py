import argparse
import logging

from dotenv import load_dotenv

from src.commands import send_cmd
from src.inventory import load_device_attr, load_inventory
from src.logging_setup import logging_setup
from src.output import create_config_file
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
        "-i", "--inventory", type=str, default="inventory/lab.yml", help="Inventory yml file path."
    )

    args = parser.parse_args()

    load_dotenv()

    logging_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
    logging_setup(logging_levels[args.log_level])
    log = logging.getLogger("rackscribe")

    ip_list = load_inventory(args.inventory)["devices"]
    log.info("Loaded %d device(s).", len(ip_list))

    # TESTING
    if args.running_config:
        device_number = 0

        for ip in ip_list:
            device_number += 1
            if check_ip_address(ip):
                log.info(f"Connecting to {ip}")
                device = load_device_attr(ip)
                output = send_cmd(device, "show running-config")
                create_config_file(f"{device_number}. config", output)
            else:
                log.info(f"Invalid IP address: '{ip}'")

    elif args.serial_numbers:
        print("Serial numbers")
    else:
        print("Use 'rackscribe --help' to display flag options.")
    # -----


if __name__ == "__main__":
    main()
