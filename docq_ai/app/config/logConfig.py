# import sys
import logging
from app.config.settings import LOG_DIR

LOG_DIR.mkdir(exist_ok = True)
LOG_FILE = LOG_DIR / "docq.log"

logger = logging.getLogger("docq")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    LOG_FILE,
    mode="w",
    encoding="utf-8"
)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)