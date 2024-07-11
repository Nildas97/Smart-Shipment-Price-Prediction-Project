# importing libraries
import os, sys



FILE_NAME = "data.csv"
# current working directory
ROOT_DIR = os.getcwd()
# config directory
CONFIG_DIR = 'config'
# schema file name
SCHEMA_FILE = 'config.yaml'
# config.yaml file complete path
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, SCHEMA_FILE)

# create variable related to our data ingestion pipeline
# variables should also match with the config.yaml file variables
DATA_INGESTION_CONFIG_KEY = 'data_ingestion_config'
DATA_INGESTION_DATABASE_NAME = 'database_name'
DATA_INGESTION_COLLECTION_NAME = 'collection_name'
DATA_INGESTION_ARTIFACT_DIR = 'data_ingestion'
DATA_INGESTION_RAW_DATA_DIR_KEY = 'raw_data_dir'
DATA_INGESTION_INGESTED_DATA_DIR_KEY = 'ingested_data_dir'
DATA_INGESTION_TRAIN_DIR_KEY = 'ingested_train_dir'
DATA_INGESTION_TEST_DIR_KEY = 'ingested_test_dir'
CONFIG_FILE_KEY = 'config'
