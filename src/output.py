import logging


def create_config_file(hostname: str, show_run_output: str) -> str:
    log = logging.getLogger("rackscribe")
    log.info(f"Creating configuration file '{hostname}'.")
    path = f"output/configurations/{hostname}.cfg"

    try:
        with open(path, "w") as f:
            f.write(show_run_output)
        log.info(f"File created. PATH: '{path}'.")
    except Exception as e:
        log.error(f"Error while creating configuration file: {e}")


def process_inventory_output(hostname: str, show_inventory_output: dict[int, str]) -> str:
    print(show_inventory_output)
    for key in show_inventory_output:
        print(show_inventory_output[key])
