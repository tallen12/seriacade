from seriacade.implementations import builtin, errors

try:
    from seriacade.implementations import pydantic

    PydanticJsonCodec = pydantic.PydanticJsonCodec
except ImportError:
    PydanticJsonCodec = errors.pydantic_not_installed_error

PythonJsonCodec = builtin.PythonJsonCodec
