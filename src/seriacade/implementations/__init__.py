import seriacade.implementations.builtin as builtin
import seriacade.implementations.errors as errors

try:
    import seriacade.implementations.pydantic as pydantic

    PydanticJsonCodec = pydantic.PydanticJsonCodec
except ImportError:
    PydanticJsonCodec = errors.pydantic_not_installed_error
    pass

PythonJsonCodec = builtin.PythonJsonCodec
