import logging

DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def setup_logger(name: str, level: int = DEFAULT_LOG_LEVEL, fmt: str = DEFAULT_LOG_FORMAT) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt))

    if not logger.handlers:
        logger.addHandler(handler)

    return logger
