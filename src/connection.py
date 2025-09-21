from netmiko import ConnectHandler
from typing import Iterator, Mapping, Any
from contextlib import contextmanager

@contextmanager
def net_connection(params: Mapping[str, Any],
                *,
                use_enable: bool | None = None,) -> Iterator[ConnectHandler]:
    
    conn = None
    host = params.get("host", "unknown")

    try:
        conn = ConnectHandler(**params)
        if use_enable is None:
            use_enable = bool(params.get("secret"))
        if use_enable:
            conn.enable()
        yield conn
    except Exception as e:
            print(f"Unexpected error talking to {host}")
            raise
    finally:
            if conn is not None:
                try:
                    conn.disconnect()
                except Exception:
                    print(f"Disconnect failed for {host}")

