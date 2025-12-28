from typing import NoReturn


def pydantic_not_installed_error(*_, **__) -> NoReturn:
    """Raise an ImportError if pydantic is not installed.

    Raises:
        ImportError: _description_

    Returns:
        NoReturn: _description_
    """
    msg = "Pydantic is not installed. Install seriacade with pydantic extra to use pydantic based codecs."
    raise ImportError(msg)
