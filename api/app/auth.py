from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from .config import settings

api_key_header = APIKeyHeader(name="X-API-Key")
api_keys = [settings.api_key]


def get_valid_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """Return the API key if it is valid, otherwise raises an exception.

    Args:
        api_key_header (str, optional): The API key header.

    Raises:
        HTTPException: If the API key is invalid.

    Returns:
        str: The validated API key.
    """
    if api_key_header in api_keys:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
