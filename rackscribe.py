import argparse
import logging
import os

from dotenv import load_dotenv

from src.commands import send_cmd_batch
from src.logging import logging_setup


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
    args = parser.parse_args()

    load_dotenv()

    logging_setup("INFO")
    log = logging.getLogger("rackscribe")

    if args.running_config:
        device = {
            "device_type": os.getenv("DEVICE_TYPE"),
            "host": "192.168.1.223",  # Pending
            "username": os.getenv("USERNAME"),
            "password": os.getenv("PASSWORD"),
            "secret": os.getenv("SECRET"),
        }

        log.info("Loaded %d device(s).", 5)

        result = send_cmd_batch(device, ["show run", "show inventory"])
        print(result)

    elif args.serial_numbers:
        print("Serial numbers")
    else:
        print("Select an action")
        print("-r Collect all running configurations")
        print("-s Collect serial numbers")


if __name__ == "__main__":
    main()
