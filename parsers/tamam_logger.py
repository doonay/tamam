import os
import loguru

logs_dir = os.path.join(".", "logs")
os.makedirs(logs_dir, exist_ok=True)
log_path = os.path.join(logs_dir, "tamam.log")

logger = loguru.logger

# Конфигурация
logger.remove()
logger.add(
    log_path,
    format="{time:DD-MM-YY HH:MM:SS} | {level} | {message}",
    level="DEBUG",
    rotation="1 week",
    compression="zip"
)

def tamam_logger(level, message):
    logger.log(level, message)
