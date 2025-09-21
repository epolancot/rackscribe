from .connection import net_connection
from typing import Mapping, Any

def send_show(
    params: Mapping[str, Any],
    command: str,
    **kwargs: Any,
) -> str:
    with net_connection(params) as conn:
        return conn.send_command(command, **kwargs)