import argparse

def main() -> None:
    parser = argparse.ArgumentParser(prog="rackscribe", description="Gather running configurations and serial numbers.")
    parser.add_argument("-r", "--running_config", action="store_true", help="Collect all running configurations.")
    parser.add_argument("-s", "--serial_numbers", action="store_true", help="Collect serial numbers.")
    args = parser.parse_args()

    if args.running_config:
        print('Running-config')
    elif args.serial_numbers:
        print('Serial numbers')
    else:
        print("Select an action")
        print("-r Collect all running configurations")
        print("-s Collect serial numbers")


if __name__ == '__main__':
    main()




