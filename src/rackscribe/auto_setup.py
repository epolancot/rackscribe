import logging
from pathlib import Path

import yaml


def auto_setup() -> bool:
    """Run initial RackScribe setup (inventory + .env)."""
    log = logging.getLogger("rackscribe")

    inventory_ok = create_initial_inventory_file()
    env_ok = create_initial_env_file()

    if inventory_ok and env_ok:
        log.info("Auto-setup operation completed.")
        return True

    if inventory_ok and not env_ok:
        log.warning("Auto-setup completed partially: inventory created, .env file failed.")
    elif env_ok and not inventory_ok:
        log.warning("Auto-setup completed partially: .env file created, inventory failed.")
    else:
        log.error("Auto-setup failed: inventory and .env file could not be created.")

    return False


def create_initial_inventory_file() -> bool:
    """Create an inventory folder and YAML file with a mock device IP address list."""
    log = logging.getLogger("rackscribe")
    inventory_file_path = Path("inventory") / "devices.yaml"

    # Do not overwrite existing credentials.
    if inventory_file_path.exists():
        log.info(f"devices.yaml file already exists at '{inventory_file_path}'. Skipping creation.")
        return True

    sample_inventory = [
        "10.0.1.10",
        "10.0.1.11",
        "10.0.1.12",
    ]

    folder_path = Path("inventory")
    file_path = folder_path / "devices.yaml"

    try:
        log.info(f"Creating sample inventory file at '{file_path}'.")

        folder_path.mkdir(parents=True, exist_ok=True)

        data = {"inventory": sample_inventory}
        with file_path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(
                data,
                f,
                default_flow_style=False,
                sort_keys=False,
            )

        log.info(f"Successfully created sample inventory file at '{file_path}'.")
        return True

    except PermissionError as exc:
        log.error(
            f"Permission error while trying to create inventory file at '{file_path}'. "
            "See rackscribe.log for details."
        )
        log.debug(
            f"Permission error while trying to create inventory file at '{file_path}': {exc}",
            exc_info=True,
        )
        return False

    except Exception as exc:  # noqa: BLE001
        log.error(
            f"Unexpected error while trying to create inventory file at '{file_path}'. "
            "See rackscribe.log for details."
        )
        log.debug(
            f"Unexpected error while trying to create inventory file at '{file_path}': {exc}",
            exc_info=True,
        )
        return False


def create_initial_env_file() -> bool:
    """
    Create an initial .env file with sample RackScribe variables.
    If a .env file already exists, it will not be overwritten.
    """
    log = logging.getLogger("rackscribe")
    env_path = Path(".env")

    # Do not overwrite existing credentials.
    if env_path.exists():
        log.info(f".env file already exists at '{env_path}'. Skipping creation.")
        return True

    content = (
        "# RackScribe environment configuration\n"
        "#\n"
        "# This file was generated using the auto-setup feature.\n"
        "# Replace the sample values below with your actual device settings.\n"
        "# Do NOT commit real credentials to version control.\n"
        "\n"
        "# Example device type (see Netmiko docs for supported types)\n"
        "DEVICE_TYPE=cisco_ios\n"
        "\n"
        "# Login credentials\n"
        "DEVICE_USERNAME=your-username\n"
        "DEVICE_PASSWORD=your-password\n"
        "\n"
        "# Optional enable/privileged password\n"
        "DEVICE_SECRET=your-enable-secret\n"
    )

    try:
        log.info(f"Creating initial .env file at '{env_path}'.")
        env_path.write_text(content, encoding="utf-8")
        log.info(f"Successfully created initial .env file at '{env_path}'.")
        return True

    except PermissionError as exc:
        log.error(
            f"Permission error while trying to create .env file at '{env_path}'. "
            "See rackscribe.log for details."
        )
        log.debug(
            f"Permission error while trying to create .env file at '{env_path}': {exc}",
            exc_info=True,
        )
        return False

    except Exception as exc:  # noqa: BLE001
        log.error(
            f"Unexpected error while trying to create .env file at '{env_path}'. "
            "See rackscribe.log for details."
        )
        log.debug(
            f"Unexpected error while trying to create .env file at '{env_path}': {exc}",
            exc_info=True,
        )
        return False
