from typing import Protocol, TypeVar, runtime_checkable

from seriacade.json.types import JsonType

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


@runtime_checkable
class JsonEncoderProtocol(Protocol[T_contra]):
    """Protocol to encode an object to JSON formatted bytes."""

    def encode_json(self, obj: T_contra) -> bytes:
        """Encode an instance of the given type to bytes.

        Args:
            obj (T_contra): Instance of the given type.

        Returns:
            bytes: JSON formatted bytes representing the object.
        """
        ...


@runtime_checkable
class JsonDecoderProtocol(Protocol[T_co]):
    """Protocol to decode from JSON formatted bytes to an instance of the given type."""

    def decode_json(self, data: bytes) -> T_co:
        """Decode bytes to an instance of the given type.

        Args:
            data (bytes): Formatted bytes representing the object.

        Returns:
            T_co: An instance of the given type decoded from the bytes.
        """
        ...


@runtime_checkable
class JsonConverterProtocol(Protocol[T]):
    """Protocol to convert between a Python object that represents JSON and an instance of the given type."""

    def convert_to_json(self, data: T) -> JsonType:
        """Convert from an object of the given type to a Python representation of JSON.

        Args:
            data (T): Instance of an object to be converted to JSON.

        Returns:
            JsonType: Python representation of the JSON of the object.
        """
        ...

    def convert_from_json(self, data: JsonType) -> T:
        """Convert from a Python representation of JSON to an instance of the given type.

        Args:
            data (JsonType): Python representation of the JSON for the given object.

        Returns:
            T: The converted object of the given type.
        """
        ...


@runtime_checkable
class JsonSchemaProviderProtocol(Protocol[T_co]):
    """A protocol for a class that can generate a JSON schema for the given type."""

    def json_schema(self) -> JsonType:
        """Generate a JSON schema for the given type.

        Returns:
            JsonType: JSON schema as a Python object.
        """
        ...


@runtime_checkable
class JsonCodecProtocol(
    JsonEncoderProtocol[T],
    JsonDecoderProtocol[T],
    JsonConverterProtocol[T],
    Protocol[T],
):
    """Protocol to define a full codec for an instance of the given type, implementing a JSON encoder and decoder."""


@runtime_checkable
class JsonCodecWithSchemaProtocol(JsonCodecProtocol[T], JsonSchemaProviderProtocol[T], Protocol[T]):
    """A protocol to define a codec with a provided schema.

    Basically an intersection type of `JsonCodecProtocol` and `JsonSchemaProviderProtocol`,
    may be removed if python supports intersection types properly.
    """
