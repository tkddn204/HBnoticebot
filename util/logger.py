import os
import logging
from util.config import LOGGING_DIR, LOGGING_FILE

formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s >> %(message)s')

if LOGGING_DIR:
    if not os.path.exists(LOGGING_DIR):
        os.makedirs(LOGGING_DIR)

file_handler = logging.FileHandler(LOGGING_DIR+LOGGING_FILE)
file_handler.setFormatter(formatter)
file_handler.flush()

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

log = logging.getLogger(__name__)
log.setLevel('INFO')
log.addHandler(file_handler)
log.addHandler(console_handler)
