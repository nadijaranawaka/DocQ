# import sys
import logging
from config.settings import LOG_DIR

LOG_DIR.mkdir(exist_ok = True)
LOG_FILE = LOG_DIR / "docq.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE,mode="w",encoding="utf-8"),
        # logging.StreamHandler(sys.stdout)
    ]
)