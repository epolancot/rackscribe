import argparse
import os
from dotenv import load_dotenv
from src.connection import net_connection
from src.commands import send_show

def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(prog="rackscribe", description="Gather running configurations and serial numbers.")
    parser.add_argument("-r", "--running_config", action="store_true", help="Collect all running configurations.")
    parser.add_argument("-s", "--serial_numbers", action="store_true", help="Collect serial numbers.")
    args = parser.parse_args()

    if args.running_config:
        device = {
            'device_type' : os.getenv('DEVICE_TYPE'),
            'host' : '', # Pending
            'username' : os.getenv('USERNAME'),
            'password' : os.getenv('PASSWORD'),
            'secret' : os.getenv('SECRET')
        }
        
        result = send_show(device, "show run")
        print(result)

    elif args.serial_numbers:
        print('Serial numbers')
    else:
        print("Select an action")
        print("-r Collect all running configurations")
        print("-s Collect serial numbers")

if __name__ == '__main__':
    main()




