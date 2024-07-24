# importing libraries
import os, sys


# CONFIG FILE PATH

FILE_NAME = "data.csv"
# current working directory
ROOT_DIR = os.getcwd()
# config directory
CONFIG_DIR = 'config'
# config file name
CONFIG_FILE = 'config.yaml'
# config.yaml file complete path
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, CONFIG_FILE)

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


# SCHEMA FILE PATH

# current working directory
ROOT_DIR = os.getcwd()
# config directory
CONFIG_DIR = 'config'
# config file name
SCHEMA_FILE = 'schema.yaml'
# schema.yaml file complete path
SCHEMA_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, SCHEMA_FILE)


# TRANSFORMATION_FILE_PATH

# current working directory
ROOT_DIR = os.getcwd()
# config directory
CONFIG_DIR = 'config'
# transformation file name
TRANSFORMATION_FILE = 'transformation.yaml'
# transformation.yaml file complete path
TRANSFORMATION_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, TRANSFORMATION_FILE)

TARGET_COLUMNS_KEY = 'target_columns'
NUMERICAL_COLUMN_KEY = 'numerical_columns'
CATEGORICAL_COLUMN_KEY = 'categorical_columns'
OUTLIERS_COLUMN_KEY = 'outliers_columns'
DROP_COLUMN_KEY = 'drop_columns'
SCALING_COLUMN_KEY = 'scaling_columns'

# create variable related to our data transformation pipeline
DATA_TRANSFORMATION_CONFIG_KEY = 'data_transformation_config'
DATA_TRANSFORMATION_DIR = 'data_transformation_dir'
DATA_TRANSFORMATION_DIR_NAME_KEY = 'transformed_dir'
DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY = 'transformed_train_dir'
DATA_TRANSFORMATION_TEST_DIR_NAME_KEY = 'transformed_test_dir'
DATA_TRANSFORMATION_PROCESSED_DIR_KEY = 'processed_dir'
DATA_TRANSFORMATION_PROCESSED_FILE_KEY = 'processed_object_file_name'
DATA_TRANSFORMATION_FEAT_ENGG_FILE_KEY = 'feature_engg_file'

PICKLE_DIR_NAME_KEY = 'prediction_file'

# PREDICTION FILE PATH

# current working directory
ROOT_DIR = os.getcwd()
# config directory
CONFIG_DIR = 'config'
# prediction file name
PREDICTION_FILE = 'prediction.yaml'
# prediction.yaml file complete path
PREDICTION_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, PREDICTION_FILE)
