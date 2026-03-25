from typing import Any


def get_in(data: dict[str, Any] | None, path: list[str], default: Any = None) -> Any:
    current: Any = data or {}
    for key in path:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current
