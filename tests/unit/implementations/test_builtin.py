import json

from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from seriacade import PythonJsonCodec
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
def test_builtin_encoder(data: JsonType) -> None:
    """Trivial tests for builtin encoder."""
    codec = PythonJsonCodec()
    encoded = codec.encode_json(data)
    assert encoded == json.dumps(data, ensure_ascii=False).encode("utf-8")


@given(
    from_schema({})
    | st.integers()
    | st.text()
    | st.floats(allow_nan=False, allow_infinity=False)
    | st.booleans()
    | st.none()
)
@settings(max_examples=100)
def test_builtin_decoder(data: JsonType) -> None:
    """Trivial tests for builtin decoder."""
    codec = PythonJsonCodec()
    encoded = json.dumps(data).encode("utf-8")
    assert codec.decode_json(encoded) == data


@given(
    from_schema({})
    | st.integers()
    | st.text()
    | st.floats(allow_nan=False, allow_infinity=False)
    | st.booleans()
    | st.none()
)
@settings(max_examples=100)
def test_builtin_convert(data: JsonType) -> None:
    """Trivial tests for builtin converter."""
    codec = PythonJsonCodec()
    assert codec.convert_from_json(data) == data
    assert codec.convert_to_json(data) == data
