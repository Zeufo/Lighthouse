from loguru import logger

from utils import setup_logger

try:
    setup_logger()

except KeyboardInterrupt:
    logger.critical("Keyboard Interrupt!")
