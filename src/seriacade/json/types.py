from __future__ import annotations

type JsonPrimitive = None | str | float | int | bool
type JsonType = JsonPrimitive | dict[str, "JsonType"] | list["JsonType"]
