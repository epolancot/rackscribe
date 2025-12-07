import argparse
import logging
from importlib.metadata import version

from dotenv import load_dotenv

from .inventory import load_inventory
from .logging_setup import setup_logging
from .operations import gather_running_configs, gather_serial_numbers


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rackscribe",
        description="Gather running configurations and serial numbers.",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-r",
        "--running_config",
        action="store_true",
        help="Gather running configurations.",
    )
    group.add_argument(
        "-s",
        "--serial_numbers",
        action="store_true",
        help="Collect serial numbers.",
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
        "-i",
        "--inventory",
        type=str,
        default="inventory/lab.yaml",
        help="Inventory yaml file path.",
    )
    parser.add_argument(
        "-o",
        "--out_dir",
        type=str,
        default="output/",
        help="Output folder path.",
    )
    parser.add_argument(
        "-f",
        "--out_file",
        type=str,
        default="Inventory",
        help="Output file name (for serial number operation).",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"Rackscribe {version('rackscribe')}",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    load_dotenv()

    logging_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
    setup_logging(level=logging_levels[args.log_level])
    log = logging.getLogger("rackscribe")

    ip_list = load_inventory(args.inventory)

    if not ip_list:
        log.error(f"Error loading IP address list. Check '{args.inventory}'.")
        return

    log.info("Loaded %d device(s).", len(ip_list))

    if args.running_config:
        gather_running_configs(ip_list)
    elif args.serial_numbers:
        gather_serial_numbers(
            ip_list=ip_list,
            out_file=args.out_file,
            out_dir=args.out_dir,
        )
    else:
        log.error(
            "No operation selected. Please select an operation. "
            "Use 'rackscribe --help' to display options.",
        )


if __name__ == "__main__":
    main()
