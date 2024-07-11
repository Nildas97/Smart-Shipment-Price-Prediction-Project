# importing libraries
import os, sys
from src.logger import logging
from src.constant import *
from src.exception import CustomException
from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.components.data_ingestion import DataIngestion

class Pipeline():
    def __init__(self, training_pipeline_config = TrainingPipelineConfig())->None:
        try:
            self.training_pipeline_config = training_pipeline_config
        except Exception as e:
            raise CustomException(e, sys)

    # defining start_data_ingestion function
    # returns DataIngestionArtifact as output
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            # to start data ingestion we need to call 
            # DataIngestionConfig also training_pipeline_config
            data_ingestion = DataIngestion(
                data_ingestion_config=DataIngestionConfig
                (self.training_pipeline_config))
            
            # initiating data ingestion
            return data_ingestion.initiate_data_ingestion()
        
        except Exception as e:
            raise CustomException(e, sys) 

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            
        except Exception as e:
            raise CustomException(e, sys)