# importing libraries
import pandas as pd
import yaml
import os, sys
from src.exception import CustomException
from src.constant import *
from src.logger import logging
from datetime import datetime
from src.data_access.data_access import mongodb_client

# defining function to read_yaml_file 
# takes str as input gives dict as output
def read_yaml_file(file_path:str)->dict:
    try:
        # open to read yaml file
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e, sys)
    

# defining function to get_collection_as_dataframe
# converts the json data into dataframe
def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    try:
        # calling mongodb client
        client = mongodb_client()

        # reading the data & getting database and collection name as list
        df = pd.DataFrame(list(client[database_name][collection_name].find()))
        
        # removing customer_id from the database
        if "_id" in df.columns:
            df.drop("_id", axis=1) 
        return df
    
    except Exception as e:
        raise CustomException(e, sys)