import os
#import loguru
import datetime
from loguru import logger

# мультиплатформенное вычисление пути для логов
logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
os.makedirs(logs_dir, exist_ok=True)
log_path = os.path.join(logs_dir, "tamam.log")

logger.remove()
logger.add(
    log_path,
    format="{time:DD-MM-YY HH:MM:SS} | {level} | {message}",
    level="DEBUG",
    rotation="1 week",
    compression="zip"
)

def tamam_logger(level, message):
    current_time = datetime.datetime.now()
    logger.log(level, message, time=current_time)