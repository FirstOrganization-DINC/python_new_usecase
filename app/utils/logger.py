import logging
import os

# ✅ 1. Create a logger instance
logger = logging.getLogger("upload-api-logger")
logger.setLevel(logging.INFO)  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# ✅ 2. Define a common log format
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

# ✅ 3. Create a console handler for stdout
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# ✅ 4. Create a file handler to log into logs/app.log
os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/app.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
