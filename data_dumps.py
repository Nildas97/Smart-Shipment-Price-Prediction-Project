# importing libraries
import pandas as pd
import pymongo
import json
import os
from dotenv import load_dotenv

# current working directory
ROOT_DIR = os.getcwd()

# env file path directory
ENV_FILE_PATH = os.path.join(ROOT_DIR, '.env')

# loading the .env file path
load_dotenv(dotenv_path=ENV_FILE_PATH)

# mongodb credentials
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
cluster_level = os.getenv('CLUSTER_LEVEL')

# mongodb url
url = f"mongodb+srv://{username}:{password}@{cluster_level}.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# data related variables
DATA_FILE_PATH = r"/mnt/d/Data Science/Python_Projects/smart_shipment/Smart-Shipment-Price-Prediction-Project/Data/train.csv"
DATABASE_NAME = 'Machine_Learning'
COLLECTION_NAME = 'Dataset'

if __name__ == "__main__":
    # reading the data
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns: {df.shape}")

    # converting the data to list then into json
    json_records = list(json.loads(df.T.to_json()).values())
    print(json_records[0])

    # establishing connection with mongodb
    client = pymongo.MongoClient(url)
    
    # accessing database and collection
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # resetting index
    df.reset_index(drop=True, inplace=True)

    # inserting the json records into collection
    collection.insert_many(json_records)

    # close the mongodb collection
    client.close()
