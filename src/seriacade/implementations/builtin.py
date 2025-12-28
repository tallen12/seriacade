import json
from typing import override

from seriacade.json.interfaces import JsonCodecProtocol
from seriacade.json.types import JsonType


class PythonJsonCodec(JsonCodecProtocol[JsonType]):
    """A codec for converting JSON using the builtin python json module."""

    def __init__(self, encoding: str = "utf-8") -> None:
        self.encoding: str = encoding

    @override
    def encode_json(self, obj: JsonType) -> bytes:
        """Encode JSON to bytes using the builtin python json module.

        Args:
            obj (JsonType): Python representation of json data to encode.

        Returns:
            bytes: JSON formatted string encoded as bytes.
        """
        return json.dumps(obj, allow_nan=False, ensure_ascii=False).encode(self.encoding)

    @override
    def decode_json(self, data: bytes) -> JsonType:
        """Decode JSON formatted string as bytes to a python representation.

        Args:
            data (bytes): Bytes to decode

        Returns:
            JsonType: Python representation of json data decoded from the bytes.
        """
        return json.loads(data)

    @override
    def convert_from_json(self, data: JsonType) -> JsonType:
        """Convert from a python representation of a json.

        For PythonJsonCodec this is a nop since JsonType is already a python representation.

        Args:
            data (JsonType): Python representation of json data.

        Returns:
            JsonType: Python representation of json data, same as input.
        """
        return data

    @override
    def convert_to_json(self, data: JsonType) -> JsonType:
        """Convert to a python representation of the json.

        For PythonJsonCodec this is a nop since JsonType is already a python representation.

        Args:
            data (JsonType): Python representation of json data.

        Returns:
            JsonType: Python representation of json data, same as input.
        """
        return data
