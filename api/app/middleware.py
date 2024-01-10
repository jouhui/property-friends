from typing import Callable

from fastapi import Request

from .logger import logger


async def log_middleware(request: Request, call_next: Callable):
    """Log each request and response.

    Args:
        request (Request): Input request.
        call_next (Callable): The function to be called next for that request.

    Returns:
        The response for the request.
    """
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
