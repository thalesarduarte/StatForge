from typing import Any


def item_response(data: Any, message: str = "ok") -> dict[str, Any]:
    return {"success": True, "message": message, "data": data}


def list_response(items: list[Any], message: str = "ok") -> dict[str, Any]:
    return {"success": True, "message": message, "items": items, "total": len(items)}
