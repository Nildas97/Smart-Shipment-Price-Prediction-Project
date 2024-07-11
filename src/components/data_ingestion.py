# get the data from databases/fetch the data from mongodb database
# split the data into train and test
# initiate data ingestion steps

# DATA INGESTION

# importing libraries
import pandas as pd
import numpy as np
import os, sys
import shutil
from src.logger import logging
from src.constant import *
from src.exception import CustomException
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.utils import read_yaml_file, get_collection_as_dataframe
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
    # calling DataIngestionConfig using object 
    # data_ingestion_config from config.yaml
        try:
            logging.info(f"{'>>'*15}Data Ingestion log started.{'<<'*15} \n\n")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)
        
    def get_data_from_mongodb(self):
        # read the dataset
        # getting database and collection name
        try:
            logging.info(f"Exporting collection data as pandas dataframe")
            df:pd.DataFrame = get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name
                )
            logging.info("Saving Data from Database to local folder ....")
            
            # calling raw data dir from data_ingestion_config
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            
            logging.info(f" Raw Data directory : {raw_data_dir}")
            
            # creating raw data directory
            os.makedirs(raw_data_dir, exist_ok=True)

            # defining csv file name variable 
            # to store the fetched data from database
            csv_file_name = 'train.csv'
            # creating file path variable for storing fetched data
            raw_file_path = os.path.join(raw_data_dir, csv_file_name)

            # saving the raw data csv file
            df.to_csv(raw_file_path)

            # before splitting, data should be in a separate directory
            # calling ingested data dir from data_ingestion_config
            ingested_data_dir = os.path.join(self.data_ingestion_config.ingested_data_dir)
            # creating ingested data directory
            os.makedirs(ingested_data_dir, exist_ok=True)
            # creating file path variable for storing ingested data
            ingested_file_path = os.path.join(self.data_ingestion_config.ingested_data_dir, csv_file_name)

            # copying the raw data from raw data file path to ingested data file path
            shutil.copy2(raw_file_path, ingested_file_path)

            logging.info(" Data stored in ingested Directory ")

            return ingested_file_path
        
        except Exception as e:
            raise CustomException(e, sys) from e 
        
    
    def split_csv_to_train_test(self, csv_file_name):
        # splitting the ingested data into train & test

        # calling file path variables from data_ingestion_config for train & test
        train_file_path = self.data_ingestion_config.train_file_path
        test_file_path = self.data_ingestion_config.test_file_path
        
        # creating file paths for train and test
        os.makedirs(train_file_path)
        os.makedirs(test_file_path)

        # reading the data
        data = pd.read_csv(csv_file_name, index_col=0)

        # calling the test size from data_ingestion_config
        size = self.data_ingestion_config.test_size

        # splitting the data in train & test
        train_data, test_data = train_test_split(data, test_size=size, random_state=42)

        # saving the train data in train_file_path
        train_file_path = os.path.join(train_file_path,FILE_NAME)

        # saving the test data in test_file_path
        test_file_path = os.path.join(test_file_path,FILE_NAME)

        # saving data in csv format
        train_data.to_csv(train_file_path)
        test_data.to_csv(test_file_path)
        
        logging.info(f" Train File path : {train_file_path}")
        logging.info(f" Test File path : {test_file_path}")
        
        # calling data_ingestion_artifact from artifact entity
        data_ingestion_artifact = DataIngestionArtifact(
            train_file_path=train_file_path, 
            test_file_path=test_file_path)
        
        return data_ingestion_artifact

    def initiate_data_ingestion(self):
        try:
            # calling first function
            logging.info("Donwloading data from mongo ")
            ingested_file_path = self.get_data_from_mongodb()
            
            logging.info("Splitting data .... ")
            
            # calling second function
            return self.split_csv_to_train_test(csv_file_name=ingested_file_path)
        
        except Exception as e:
            raise CustomException(e, sys)
        