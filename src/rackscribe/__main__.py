import argparse
import logging
from importlib.metadata import version

from dotenv import load_dotenv

from .inventory import load_inventory
from .logging_setup import setup_logging
from .operations import gather_running_configs, gather_serial_numbers
from .sanitize import validate_output_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rackscribe",
        description="Collect running configurations and serial numbers from network devices and generate inventory reports.",
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
    group.add_argument(
        "--auto-setup",
        action="store_true",
        help="Create a sample inventory file and .env template (does not overwrite existing files).",
    )

    parser.add_argument(
        "-l",
        "--log_level",
        type=int,
        default=3,
        choices=range(5),
        help="Logging level: 0-Critical, 1-Error, 2-Warning, 3-Info (default), 4-Debug",
    )
    parser.add_argument(
        "-i",
        "--inventory",
        type=str,
        default="inventory/devices.yaml",
        help="Inventory YAML file path (default: inventory/devices.yaml).",
    )
    parser.add_argument(
        "-o",
        "--out_dir",
        type=str,
        default="outputs/",
        help="Output folder path (default: output/).",
    )
    parser.add_argument(
        "-f",
        "--out_file",
        type=str,
        default="Inventory",
        help="Base output file name for inventory Excel export (default: Inventory).",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show elapsed time and operation statistics at the end of operation.",
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

    try:
        out_dir = validate_output_path(args.out_dir)
    except ValueError as exc:
        log.error(str(exc))
        return

    ip_list = load_inventory(args.inventory)

    if not ip_list:
        log.error(f"Error loading IP address list. Check '{args.inventory}'.")
        return

    log.info(f"Loaded {len(ip_list)} device(s).")

    if args.running_config:
        gather_running_configs(ip_list, out_dir=out_dir, show_stats=args.stats)
    elif args.serial_numbers:
        gather_serial_numbers(
            ip_list=ip_list,
            out_file=args.out_file,
            out_dir=out_dir,
            show_stats=args.stats,
        )
    else:
        log.error(
            "No operation selected. Please select an operation. "
            "Use 'rackscribe --help' to display options.",
        )


if __name__ == "__main__":
    main()
