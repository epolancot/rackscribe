import logging

LOGGER_NAME = "rackscribe"


def setup_logging(level: str = "INFO", log_file: str = "rackscribe.log") -> logging.Logger:
    """
    Configure application-wide logging.

    Args:
        level:
            Logging level name (e.g., "DEBUG", "INFO", "WARNING").
        log_file:
            Path to the log file to write to.

    Returns:
        The configured logger instance.
    """
    logger = logging.getLogger(LOGGER_NAME)

    # If handlers are already configured, just return the existing logger.
    if logger.handlers:
        return logger

    # Resolve level string to numeric constant, defaulting to INFO.
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Catch all level logs
    logger.setLevel(logging.DEBUG)

    # logs.log file logging format
    formatter_file = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s : %(message)s")

    # console logging format
    formatter_console = logging.Formatter("%(message)s")

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter_file)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter_console)
    logger.addHandler(console_handler)

    return logger
