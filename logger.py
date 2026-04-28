# # logger.py
# import logging
# import config

# logging.basicConfig(
#     filename=config.LOG_FILE,
#     level=logging.INFO,
#     format="%(asctime)s - %(message)s"
# )

# def log_event(message):
#     logging.info(message)

# import time

# def log_event(message):
#     with open("logs.txt", "a") as f:
#         f.write(f"{time.ctime()} - {message}\n")

import os
import time

LOG_FILE = "logs/logs.txt"

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

def log_event(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")