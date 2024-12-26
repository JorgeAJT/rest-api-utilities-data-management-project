import logging

DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def setup_logger(name: str, level: int = DEFAULT_LOG_LEVEL, fmt: str = DEFAULT_LOG_FORMAT) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create handler and formatter
    handler = logging.StreamHandler()  # Send logs to the console
    handler.setFormatter(logging.Formatter(fmt))

    # Avoid adding duplicate handlers
    if not logger.handlers:
        logger.addHandler(handler)  # Associate the handler to the logger

    return logger
