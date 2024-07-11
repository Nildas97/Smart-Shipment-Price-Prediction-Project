# importing libraries
import pandas as pd
import pymongo
import json
import os
from schema import write_schema_yaml
from dotenv import load_dotenv
from src.logger import logging

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

# database and collection variables
DATABASE_NAME = 'Machine_Learning'
COLLECTION_NAME = 'Dataset'

if __name__ == "__main__":

    # data file path directory
    DATA_FILE_PATH = os.path.join(ROOT_DIR, 'Data', 'train.csv')

    # file path directory
    FILE_PATH = os.path.join(ROOT_DIR, DATA_FILE_PATH)

    # generating schema file
    write_schema_yaml(csv_file=DATA_FILE_PATH)

    # reading the data
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns: {df.shape}")

    # converting the data to list then into json
    json_records = json.loads(df.to_json(orient='records'))
    # json_records = list(json.loads(df.T.to_json()).values())
    print(json_records[0])

    try:
        # establishing connection with mongodb
        client = pymongo.MongoClient(url)
        # accessing database and collection
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        # inserting the json records into collection
        collection.insert_many(json_records)
        print("Data inserted successfully!")

    except pymongo.errors.ConnectionError as conn_err:
        print(f"Connection error: {conn_err}")

    except pymongo.errors.OperationFailure as op_fail:
        print(f"Operation failed: {op_fail}")
        
    finally:
        # close the mongodb collection
        client.close()

    logging.info("Data pushed to Mongodb")
    

