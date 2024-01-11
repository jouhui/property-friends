from typing import Callable

import structlog
from fastapi import Request
from starlette.concurrency import iterate_in_threadpool

logger = structlog.get_logger()


async def log_middleware(request: Request, call_next: Callable):
    """Log each request and response.

    Args:
        request (Request): Input request.
        call_next (Callable): The function to be called next for that request.

    Returns:
        The response for the request.
    """

    body = await request.body()
    request_body = body.decode("utf-8")

    logger.info("Incoming request", method=request.method, url=request.url, body=request_body)
    response = await call_next(request)

    response_body = [section async for section in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    decoded_response_body = response_body[0].decode()

    logger.info(
        "Response",
        status_code=response.status_code,
        response_body=decoded_response_body,
        method=request.method,
    )
    return response
