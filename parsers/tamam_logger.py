import os
from loguru import logger
import loguru
loguru.logger.remove()

def tamam_logger(level, message):
    logs_dir = os.path.join(".", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, "tamam.log")

    loguru.logger.add(
        log_path,
        format="{time:DD-MM-YY HH:MM:SS} | {level} | {message}",
        level=level,
        #sink=log_path,
        rotation="1 week",
        compression="zip"
    )
    loguru.logger.log(level, message)
