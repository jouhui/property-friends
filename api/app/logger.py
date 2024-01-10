import logging
import sys

from .config import settings


def get_logger(
    log_to_file: bool = True, filename: str = "logs/api.log", log_to_stdout: bool = True
) -> logging.Logger:
    """Build the logger for the API. The log level is set to DEBUG if `dev_mode=True` in the
    environment variables, and to INFO otherwise.

    Args:
        log_to_file (bool, optional):
            Whether to save the logs into a file. Defaults to True.
        filename (str, optional):
            The filename in which the logs will be saved. Only used if `log_to_file=True`.
            Defaults to "logs/api.log".
        log_to_stdout (bool, optional):
            Whether to log to the standard output. Defaults to True.

    Raises:
        ValueError: If both `log_to_file` and `log_to_stdout` are False.

    Returns:
        logging.Logger: The logger for the API.
    """

    if not log_to_file and not log_to_stdout:
        raise ValueError(
            "At least one of log_to_file or log_to_stdout must be True to effectively log."
        )

    logger = logging.getLogger()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    if log_to_file:
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if log_to_stdout:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    if settings.dev_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    return logger


logger = get_logger()
