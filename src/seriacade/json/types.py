from __future__ import annotations

from typing import TypeAlias

JsonPrimitive: TypeAlias = None | str | float | int | bool
JsonType: TypeAlias = JsonPrimitive | dict[str, "JsonType"] | list["JsonType"]
