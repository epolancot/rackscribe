import logging
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import Any

from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException


@contextmanager
def net_connection(
    params: Mapping[str, Any],
    *,
    use_enable: bool | None = None,
) -> Iterator[ConnectHandler]:
    conn = None
    host = params.get("host", "unknown")

    log = logging.getLogger("rackscribe")

    try:
        conn = ConnectHandler(**params)
        if use_enable is None:
            use_enable = bool(params.get("secret"))
        if use_enable:
            conn.enable()
        yield conn
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as exc:
        log.error(f"Error talking to {host}: {exc}")
        raise

    except Exception as exc:
        log.error(f"Unexpected error talking to {host}: {exc}")
        raise

    finally:
        if conn is not None:
            try:
                conn.disconnect()
            except Exception:
                log.error(f"Disconnect failed for {host}.")
