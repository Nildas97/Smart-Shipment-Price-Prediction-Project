# importing libraries
import os, sys
from src.exception import CustomException
from src.constant import *
from src.logger import logging
from datetime import datetime
from src.utils import read_yaml_file

# config data variable
# getting config file path from constant file
CONFIG_DATA = read_yaml_file(CONFIG_FILE_PATH)

class TrainingPipelineConfig:
    def __init__(self):
        try:
            # creating artifact dir
            self.artifact_dir = os.path.join(os.getcwd(), 'artifact', f"{datetime.now().strftime('%m%d%Y__%H%m%S')}")
            
        except Exception as e:
            raise CustomException(e, sys)
        
class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
    # calling training_pipeline_config from config.yaml
    # accessing the TrainingPipelineConfig class

        try:
            # data ingestion config key
            data_ingestion_key = CONFIG_DATA[DATA_INGESTION_CONFIG_KEY]

            # database and collection name
            self.database_name=data_ingestion_key[DATA_INGESTION_DATABASE_NAME]
            self.collection_name=data_ingestion_key[DATA_INGESTION_COLLECTION_NAME]
            
            # data ingestion dir
            # data ingestion dir created inside artifact dir
            self.data_ingestion_dir=os.path.join(training_pipeline_config.artifact_dir, data_ingestion_key[DATA_INGESTION_ARTIFACT_DIR])

            # raw data dir
            self.raw_data_dir=os.path.join(self.data_ingestion_dir,data_ingestion_key[DATA_INGESTION_RAW_DATA_DIR_KEY])

            # ingested data dir
            self.ingested_data_dir=os.path.join(self.data_ingestion_dir, data_ingestion_key[DATA_INGESTION_INGESTED_DATA_DIR_KEY])

            # train data file path
            self.train_file_path=os.path.join(self.data_ingestion_dir, data_ingestion_key[DATA_INGESTION_TRAIN_DIR_KEY])

            # test data file path
            self.test_file_path=os.path.join(self.data_ingestion_dir, data_ingestion_key[DATA_INGESTION_TEST_DIR_KEY])

            # test size, 20% data for testing
            self.test_size=0.2

        except Exception as e:
            raise CustomException(e, sys) 
