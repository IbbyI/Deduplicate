import logging


FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(
    format=FORMAT, filename="deduplicate.log", filemode="w", level=logging.INFO
)
logger = logging.getLogger(__name__)


def log(level: str, message: str, exc_info: bool = False) -> None:
    """
    Write Log Messages to File.
    Args:
        level (str): Level of the Log.
        Available Levels:
            info (default): Additional Info Recorded.
            warning: Potential Issue.
            error: Severe/Critical Issue.
        message (str): Log Message to Write to File.
        exc_info (bool): Exception Info to Write to File, False by Default.
    """
    log_levels = {
        "info": logger.info,
        "warning": logger.warning,
        "error": logger.error,
    }
    level = level.lower()

    write_log = log_levels.get(level, logger.info)
    return write_log(message, exc_info=exc_info)
