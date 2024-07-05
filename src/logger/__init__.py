# importing libraries
import logging
import os
import sys
from datetime import datetime

# log directory folder
LOG_DIR = "logs"

# getting the log directory folder
LOG_DIR = os.path.join(os.getcwd(), LOG_DIR)
os.makedirs(LOG_DIR, exist_ok=True)

# log file time stamp
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"

# log file name format
file_name = f"log{CURRENT_TIME_STAMP}.log"

# log file path
log_file_path = os.path.join(LOG_DIR, file_name)

# log file basic configuration
logging.basicConfig(filename=log_file_path,
                    filemode="w",
                    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
