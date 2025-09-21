from collections.abc import Mapping
from typing import Any

from .connection import net_connection


def send_show(
    params: Mapping[str, Any],
    command: str,
    **kwargs: Any,
) -> str:
    with net_connection(params) as conn:
        return conn.send_command(command, **kwargs)
