# importing libraries
import pandas as pd
import numpy as np
import dill
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
        raise CustomException(e, sys) from e 

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
        raise CustomException(e, sys) from e 
    
def create_yaml_file_numerical_columns(column_list, yaml_file_path):
    if os.path.exists(yaml_file_path):
        numerical_columns = {'numerical_columns': column_list}

        with open(yaml_file_path, 'w') as yaml_file:
            yaml.dump(numerical_columns, yaml_file)

    else:
        numerical_columns = {'numerical_columns': column_list}

        with open(yaml_file_path, 'w') as yaml_file:
            yaml.dump(numerical_columns, yaml_file)


def create_yaml_file_categorical_columns_dataframe(dataframe, categorical_columns, yaml_file_path):
    try:
        with open(yaml_file_path, 'r') as existing_yaml_file:
            existing_data = yaml.safe_load(existing_yaml_file)
            
    except FileNotFoundError:
        existing_data = {}


    column_categories_dict = {}

    for column in categorical_columns:
        if column in dataframe.columns:
            categories = dataframe[column].unique().tolist()
            column_categories_dict[column] = categories


    existing_data["categorical_column"] = column_categories_dict

    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(existing_data, yaml_file)

def save_numpy_array_data(file_path:str, array:np.array):
    try:
        # directory path
        dir_path = os.path.dirname(file_path)

        # create directory according to directory path
        os.makedirs(dir_path, exist_ok=True)

        # opening and saving the data
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise CustomException(e, sys) from e 

def save_object(file_path:str, obj:object):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys) from e 
