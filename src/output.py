import logging
import re

import pandas as pd

_INVENTORY_RE = re.compile(
    # Regex used in process_inventory_output() to get the values for name, description and serial number from "show inventory" command.
    # VID and PID fields included. Add these field if needed.
    r"""
        NAME:\s*"(?P<name>[^"]+)",\s*
        DESCR:\s*"(?P<description>[^"]+)"\s*
        PID:\s*[^,]*\s*,\s*
        VID:\s*[^,]*\s*,\s*
        SN:\s*(?P<sn>[^\r\n]*)
    """,
    re.MULTILINE | re.VERBOSE,
)


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


def process_inventory_output(hostname: str, show_inventory_output: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for m in _INVENTORY_RE.finditer(show_inventory_output):
        name = m.group("name")
        description = m.group("description")
        sn = (m.group("sn") or "").strip() or "N/A"
        rows.append([hostname, name, description, sn])
    return rows


# Test write excel
def create_inventory_file(filename: str) -> str:
    TABLE_COLUMNS = ["Hostname", "Name", "Description", "Serial Number"]

    df = pd.DataFrame([], columns=TABLE_COLUMNS)
    df.to_excel(f"{filename}.xlsx", index=False)
