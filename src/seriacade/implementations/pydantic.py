from pydantic import BaseModel, TypeAdapter

from seriacade.json import (
    JsonCodecProtocol,
    JsonCodecWithSchemaProtocol,
    JsonConverterProtocol,
    JsonSchemaProviderProtocol,
    JsonType,
)
from seriacade.json.interfaces import TypeVar

PydanticType = TypeVar("PydanticType", bound=BaseModel)
AnyType = TypeVar("AnyType")


class PydanticModelJsonCodec(
    JsonCodecProtocol[PydanticType],
    JsonConverterProtocol[PydanticType],
    JsonSchemaProviderProtocol[PydanticType],
):
    """Provides a json codec implementation for arbitrary pydantic models."""

    def __init__(self, model_type: type[PydanticType]) -> None:
        self.model_type = model_type

    def encode_json(self, obj: PydanticType) -> bytes:
        return obj.model_dump_json().encode("utf-8")

    def decode_json(self, data: bytes) -> PydanticType:
        return self.model_type.model_validate_json(data)

    def convert_from_json(self, data: JsonType) -> PydanticType:
        return self.model_type.model_validate(data)

    def convert_to_json(self, data: PydanticType) -> JsonType:
        return data.model_dump()

    def json_schema(self) -> JsonType:
        return self.model_type.model_json_schema()


class PydanticAdapterJsonCodec(
    JsonCodecProtocol[AnyType],
    JsonConverterProtocol[AnyType],
    JsonSchemaProviderProtocol[AnyType],
):
    """Provides a json codec implementation for arbitrary data using pydantic TypeAdapters.

    This should work for python dataclasses for some limitations. See: https://docs.pydantic.dev/latest/concepts/type_adapter/
    """

    def __init__(self, model_type: type[AnyType]) -> None:
        self.model_type = TypeAdapter(model_type)

    def encode_json(self, obj: AnyType) -> bytes:
        return self.model_type.dump_json(obj)

    def decode_json(self, data: bytes) -> AnyType:
        return self.model_type.validate_json(data)

    def convert_from_json(self, data: JsonType) -> AnyType:
        return self.model_type.validate_python(data)

    def convert_to_json(self, data: AnyType) -> JsonType:
        return self.model_type.dump_python(data)

    def json_schema(self) -> JsonType:
        return self.model_type.json_schema()


class PydanticJsonCodec(
    JsonCodecProtocol[AnyType],
    JsonConverterProtocol[AnyType],
    JsonSchemaProviderProtocol[AnyType],
):
    """Codec that derives the correct pydantic codec for the given type.

    If the type is derived from BaseModel load a PydanticModelJsonCodec
    If the type is not derived from BaseMode load a PydanticAdapterJsonCodec and attempt to use a TypeAdapter.
    """

    def __init__(self, model_type: type[AnyType]) -> None:
        self.codec: JsonCodecWithSchemaProtocol[AnyType]
        if issubclass(model_type, BaseModel):
            base_model_type = model_type
            self.codec = PydanticModelJsonCodec(base_model_type)
        else:
            self.codec = PydanticAdapterJsonCodec(model_type)

    def encode_json(self, obj: AnyType) -> bytes:
        """Encode obj to bytes using pydantic codecs.

        Args:
            obj (AnyType): Instance of object for this codec.

        Returns:
            bytes: JSON formatted string encoded as bytes.
        """
        return self.codec.encode_json(obj)

    def decode_json(self, data: bytes) -> AnyType:
        """Decode JSON formatted string as bytes to a python representation.

        Args:
            data (bytes): JSON formatted bytes.

        Returns:
            AnyType: Decoded object of given type for this codec.
        """
        return self.codec.decode_json(data)

    def convert_from_json(self, data: JsonType) -> AnyType:
        """Convert from a python representation of a JSON to an instance of the given type.

        Args:
            data (JsonType): Python representation of json data.

        Returns:
            AnyType: Decoded object of given type for this codec.
        """
        return self.codec.convert_from_json(data)

    def convert_to_json(self, data: AnyType) -> JsonType:
        """Convert from an instance of the given type to a python representation of a JSON.

        Args:
            data (AnyType): Instance of an object of a given type.

        Returns:
            JsonType: Python representation of json data.
        """
        return self.codec.convert_to_json(data)

    def json_schema(self) -> JsonType:
        """Generate a json schema for this codec.

        Returns:
            JsonType: Json schema as a python object.
        """
        return self.codec.json_schema()
