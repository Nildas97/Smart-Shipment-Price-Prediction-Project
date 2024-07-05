# importing libraries
import pandas as pd
import numpy as np
import pymongo
import json
import os, sys
from dotenv import load_dotenv

# defining mongodb_client
def mongodb_client():
    ROOT_DIR = os.getcwd()
    ENV_FILE_PATH = os.path.join(ROOT_DIR, '.env')

    # loading the .env file path
    load_dotenv(dotenv_path=ENV_FILE_PATH)

    # accessing credentials from .env file
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    cluster_level = os.getenv('CLUSTER_LEVEL')

    # mongodb_url
    mongodb_url = f"mongodb+srv://{username}:{password}@{cluster_level}.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    print(mongodb_url)

    # pymongo client
    client = pymongo.MongoClient(mongodb_url)

    return client
