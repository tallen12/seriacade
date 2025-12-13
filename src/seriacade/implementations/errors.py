def pydantic_not_installed_error(*args, **kwargs):
    raise ImportError(
        "Pydantic is not installed. Install sericade with pydantic extra to use pydantic based codecs."
    )
