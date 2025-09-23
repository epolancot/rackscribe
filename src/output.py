import logging


def create_config_file(name: str, config: str) -> str:
    log = logging.getLogger("rackscribe")
    log.info(f"Creating configuration file '{name}'.")
    path = f"output/{name}.cfg"

    try:
        with open(path, "w") as f:
            f.write(config)
    except Exception as e:
        log.info("Error: %d.", e)

    log.info(f"File created. PATH: '{path}'.")
