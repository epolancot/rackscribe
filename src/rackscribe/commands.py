from collections.abc import Mapping
from typing import Any, cast

from .connection import net_connection


# Send one command
def send_cmd(
    params: Mapping[str, Any],
    command: str,
    **kwargs: Any,
) -> str:
    """Send one command."""

    with net_connection(params) as conn:
        return cast(str, conn.send_command(command, **kwargs))


# Send several commands
def send_cmd_batch(
    params: Mapping[str, Any],
    commands: list[str],
    **kwargs: Any,
) -> dict[str, str]:
    """Send several commands in one session."""
    output: dict[str, str] = {}
    with net_connection(params) as conn:
        for i, cmd in enumerate(commands, start=1):
            output[str(i)] = conn.send_command(cmd, **kwargs)

    return output


def get_hostname(params: Mapping[str, Any]) -> str:
    with net_connection(params) as conn:
        prompt = conn.find_prompt()
        hostname = prompt[:-1]
        return cast(str, hostname)
