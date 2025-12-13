import itertools
from dataclasses import dataclass

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema
from pydantic import BaseModel, TypeAdapter

from seriacade.implementations.pydantic import (
    PydanticAdapterJsonCodec,
    PydanticJsonCodec,
    PydanticModelJsonCodec,
)
from seriacade.json import JsonType


@given(
    from_schema({})
    | st.integers()
    | st.text()
    | st.floats(allow_nan=False, allow_infinity=False)
    | st.booleans()
    | st.none()
)
@settings(max_examples=100)
def test_pydantic_codec_encode_with_builtin_types(data: JsonType) -> None:
    """Trivial test to ensure all builtin types are handled by the Pydantic codec."""
    codec = PydanticJsonCodec(type(data))
    encoded = codec.encode_json(data)
    assert isinstance(encoded, bytes)
    assert encoded == TypeAdapter(type(data)).dump_json(data)


@given(
    from_schema({})
    | st.integers()
    | st.text()
    | st.floats(allow_nan=False, allow_infinity=False)
    | st.booleans()
    | st.none()
)
@settings(max_examples=100)
def test_pydantic_codec_decode_with_builtin_types(data: JsonType) -> None:
    """Trivial test to ensure all builtin types are handled by the Pydantic codec."""
    codec = PydanticJsonCodec(type(data))
    encoded = TypeAdapter(type(data)).dump_json(data)
    decoded = codec.decode_json(encoded)
    assert isinstance(decoded, type(data))
    assert decoded == data


class PydanticModel(BaseModel):
    integer_val: int
    text: str
    booleans: bool
    optional: str | None


@dataclass
class DataClassModel:
    integer_val: int
    text: str
    booleans: bool
    optional: str | None


TEST_PARAMETRIZATION = list(
    itertools.product([PydanticModel], [PydanticJsonCodec, PydanticModelJsonCodec])
) + list(
    itertools.product([DataClassModel], [PydanticJsonCodec, PydanticAdapterJsonCodec])
)


@pytest.mark.parametrize("model, codec", TEST_PARAMETRIZATION)
def test_pydantic_codec_encode_for_model(model, codec):
    """Test to make sure encoding works for expected models."""
    codec = codec(model)
    data = model(integer_val=1, text="test", booleans=True, optional=None)
    encoded: bytes = codec.encode_json(data)
    expected_encoded = (
        """{"integer_val":1,"text":"test","booleans":true,"optional":null}"""
    )
    assert isinstance(encoded, bytes)
    assert encoded == expected_encoded.encode("utf-8")


@pytest.mark.parametrize(
    "model, codec",
    TEST_PARAMETRIZATION,
)
def test_pydantic_codec_decode_for_model(model, codec):
    """Test to make sure decoding works for expected models."""
    codec = codec(model)
    data = model(integer_val=1, text="test", booleans=True, optional=None)
    encoded = (
        """{"integer_val":1,"text":"test","booleans":true,"optional":null}""".encode(
            "utf-8"
        )
    )
    decoded = codec.decode_json(encoded)

    assert isinstance(decoded, model)
    assert decoded == data


@pytest.mark.parametrize("model, codec", TEST_PARAMETRIZATION)
def test_pydantic_codec_convert_to_json_for_model(model, codec):
    """Test to make sure convert to json works for expected models."""
    codec = codec(model)
    data = model(integer_val=1, text="test", booleans=True, optional=None)
    json_data = {"integer_val": 1, "text": "test", "booleans": True, "optional": None}
    converted = codec.convert_to_json(data)
    assert isinstance(converted, dict)
    assert converted == json_data


@pytest.mark.parametrize("model, codec", TEST_PARAMETRIZATION)
def test_pydantic_codec_convert_from_json(model, codec):
    """Test to make sure convert from json works for expected models."""
    codec = codec(model)
    data = model(integer_val=1, text="test", booleans=True, optional=None)
    json_data = {"integer_val": 1, "text": "test", "booleans": True, "optional": None}
    converted = codec.convert_from_json(json_data)

    assert isinstance(converted, model)
    assert converted == data
