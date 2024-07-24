# DATA TRANSFORMATION 

# importing libraries
import pandas as pd
import numpy as np
import os, sys
from src.logger import logging
from src.constant import *
from src.exception import CustomException
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from src.utils import *
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer


# read data in transformation schema
TRANSFORMATION_YAML = read_yaml_file(file_path=TRANSFORMATION_FILE_PATH)

# column data accessed from schema.yaml
TARGET_COLUMNS = TRANSFORMATION_YAML[TARGET_COLUMNS_KEY]
NUMERICAL_COLUMNS = TRANSFORMATION_YAML[NUMERICAL_COLUMN_KEY]
CATEGORICAL_COLUMNS = TRANSFORMATION_YAML[CATEGORICAL_COLUMN_KEY]
DROP_COLUMNS = TRANSFORMATION_YAML[DROP_COLUMN_KEY]

# transformation columns
OUTLIERS_COLUMNS = TRANSFORMATION_YAML[OUTLIERS_COLUMN_KEY]
SCALING_COLUMNS = TRANSFORMATION_YAML[SCALING_COLUMN_KEY]

class Feature_Engineering(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        logging.info(f"{'>>'*15}Feature Engineering log started.{'<<'*15} \n\n")
        logging.info(" Numerical Columns , Categorical Columns , Target Column initialised in Feature engineering Pipeline ")
    
    
    # dropping columns
    # data should be in DataFrame format
    def drop_columns(self, X:pd.DataFrame):
        columns_to_drop = DROP_COLUMNS
        logging.info(f"Dropping columns: {columns_to_drop}")
        
        X.drop(columns=columns_to_drop, axis=1, inplace=True)
        return X
    
    # replacing spaces with underscore
    def replace_spaces_with_underscore(self, df):
        df = df.rename(columns=lambda x:x.replace(" ", "_"))
        return df
    
    # for numerical nan values
    # replacing NAN values with random data
    def replace_nan_with_random_data(self, df, column_label):
        if column_label not in df.columns:
            print(f"Column '{column_label}' not found in the Dataframe")
            return df

        # copying original data
        original_data = df[column_label].copy()
        # checking nan value indexes
        nan_indexes = df[df[column_label].isna()].index
        # getting length of nan value indexes
        num_nan = len(nan_indexes)
        # dropping nan values
        existing_values = original_data.dropna().values
        # filling nan with random values
        random_values = np.random.choice(existing_values, num_nan)

        df.loc[nan_indexes, column_label] = random_values

        # original mean and median
        original_mean = original_data.mean()
        original_median = original_data.median()

        # new mean and median
        new_mean = df[column_label].mean()
        new_median = df[column_label].median()

        return df
    
    # for categorical nan values
    def drop_rows_with_nan(self, X:pd.DataFrame, column_label:str):
        # Log the shape before dropping NaN values
        logging.info(f"Shape before dropping NaN values: {X.shape}")
        
        # Drop rows with NaN values in the specified column
        X = X.dropna(subset= [column_label])

        # Log the shape after dropping NaN values
        logging.info(f"Shape after dropping NaN values: {X.shape}")
        
        logging.info("Dropped NaN values.")
        X = X.reset_index(drop=True)

        return X

    # trimming outliers using quantile method
    def trim_outliers_by_quantile(self, df, column_label, upper_quantile=0.95, lower_quantile=0.5):
        if column_label not in df.columns:
            print(f"Column '{column_label}' not found in the DataFrame")
            return df
        
        column_data = df[column_label]
        lower_bound = column_data.quantile(lower_quantile)
        upper_bound = column_data.quantile(upper_quantile)

        trimmed_data = column_data.clip(lower = lower_bound, upper = upper_bound)

        df[column_label] = trimmed_data

        return df
    
    # removing outliers using trimming function
    def remove_outliers(self, X):
        for column in OUTLIERS_COLUMNS:
            logging.info(f"Removing Outlier from column :{column}")
            X = self.trim_outliers_by_quantile(df= X, column_label=column)

        return X 
    
    # running the data modifications
    def run_data_modification(self, data):
        # copy the data
        X = data.copy()

        # initiating replace_spaces_with_underscore function
        logging.info(" Editing Column Lables ......")
        X = self.replace_spaces_with_underscore(X)

        try:
            # dropping the columns
            X = self.drop_columns(X)
        except Exception:
            print("Test Data does not consists of some Dropped Columns")


        logging.info("----------------")
        logging.info('Replace nan with random Data')
        for column in ['Artist_Reputation', 'Height', 'Width']:
            # Removing nan rows
            logging.info(f"Removing NaN values from the column : {column} ")
            X = self.replace_nan_with_random_data(X, column_label=column)

        logging.info("----------------")
        logging.info(' Dropping rows with nan')
        for column in ['Weight', 'Material', 'Remote_Location']:
            # Removing nan rows
            logging.info(f"Dropping Rows from column : {column}")
            X = self.drop_rows_with_nan(X, column_label=column)

        
        logging.info("----------------")
        logging.info(" Removing Outliers ")
        X = self.remove_outliers(X)

        return X
    
    # data modification function
    def data_wrangling(self, X:pd.DataFrame):
        try:
            # Data Modification 
            data_modified = self.run_data_modification(data= X)
            
            logging.info(" Data Modification Done")

            return data_modified
        except Exception as e:
            raise CustomException(e, sys) from e

    # fit function
    def fit(self, X,y = None):
        return self
    
    # transform function
    def transform(self, X:pd.DataFrame, y = None):
        try:
            data_modified = self.data_wrangling(X)
            
            #data_modified.to_csv("data_modified.csv",index=False)
            logging.info(" Data Wrangling Done ")
            
            logging.info(f"Original Data  : {X.shape}")
            logging.info(f"Shape Modified Data : {data_modified.shape}")
            return data_modified
        except Exception as e:
            raise CustomException(e, sys) from e


class DataPreProcessor:
    def __init__(self, numerical_cols, categorical_cols):
        self.numerical_cols = numerical_cols
        self.categorical_cols = categorical_cols

        # Define preprocessing steps using a Pipeline
        categorical_transformer = Pipeline(
            steps = [('onehot', OneHotEncoder(handle_unknown='ignore'))]
            )

        numerical_transformer = Pipeline(
            steps = [('log_transform', FunctionTransformer(np.log1p, validate=False))]
            )
        
        # Create a ColumnTransformer to apply transformations
        self.preprocessor = ColumnTransformer(
            transformers = [
                ('cat', categorical_transformer, self.categorical_cols),
                ('num', numerical_transformer, self.numerical_cols)
            ],
            remainder='passthrough'
        )

    def get_preprocessor(self):
        return self.preprocessor
    
    def fit_transform(self, data):
        transformed_data = self.preprocessor.fit_transform(data)

        return transformed_data
    
class DataTransformation:
    def __init__(self, data_transformation_config:DataTransformationConfig, 
                    data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"\n{'*'*15} Data Transformation log started {'*'*15}\n\n")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def get_feature_engineering_object(self):
        try:
            feature_engineering = Pipeline(steps=[('fe', Feature_Engineering())])
            return feature_engineering
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def separate_numerical_categorical_columns(self, df):
        numerical_columns = []
        categorical_columns = []

        for column in df.columns:
            if df[column].dtype == 'int64' or df[column].dtype == 'float64':
                numerical_columns.append(column)

            else:
                categorical_columns.append(column)

            return numerical_columns, categorical_columns
        
    def initiate_data_transformation(self):
        try:
            # Data validation Artifact ------>Accessing train and test files 
            logging.info("Obtaining training and test file path.")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            logging.info("Loading training and test data as pandas DataFrame.")
            logging.info(f" Accessing train file from :{train_file_path}\
                            Test File Path:{test_file_path} ")      

            # read the data
            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)
            
            logging.info(f"Target Column :{TARGET_COLUMNS}")
            logging.info(f"Numerical Column :{NUMERICAL_COLUMNS}")
            logging.info(f"Categorical Column :{CATEGORICAL_COLUMNS}")

            # all columns of dataset
            col = NUMERICAL_COLUMNS + CATEGORICAL_COLUMNS + TARGET_COLUMNS

            # All columns 
            logging.info("All columns: {}".format(col))

            # Feature Engineering 
            logging.info("Obtaining feature engineering object.")
            feat_engg_obj = self.get_feature_engineering_object()

            logging.info("Applying feature engineering object on training DataFrame and testing DataFrame")
            logging.info(">>>" * 15 + " Training data " + "<<<" * 15)
            logging.info("Feature Engineering - Train Data ")
            train_df = feat_engg_obj.fit_transform(X= train_df)

            logging.info(">>>" * 20 + " Test data " + "<<<" * 20)
            logging.info("Feature Engineering - Test Data ")
            test_df = feat_engg_obj.transform(X= test_df)

            # Train Data 
            logging.info("Feature Engineering of train and test Completed.")
            feat_engg_train_df:pd.DataFrame = train_df.copy()
            logging.info(f" Columns in feature engineering Train {feat_engg_train_df.columns}")
            logging.info("Feature Engineering - Train Completed")
            feat_engg_test_df:pd.DataFrame = test_df.copy()

            logging.info(f" Columns in feature engineering test {feat_engg_test_df.columns}")
            logging.info("Saving feature engineered training and testing DataFrame.")
            
            # Getting numerical and categorical of Transformed data 
            
            # Train and Test 
            input_feature_train_df = feat_engg_train_df.drop(columns=TARGET_COLUMNS, axis=1)
            train_target_array = feat_engg_train_df[TARGET_COLUMNS]
        
            input_feature_test_df = feat_engg_test_df.drop(columns=TARGET_COLUMNS, axis=1)
            test_target_array = feat_engg_test_df[TARGET_COLUMNS]
            
            ### Preprocessing 
            logging.info("*" * 20 + " Applying preprocessing object on training DataFrame and testing dataframe " + "*" * 20)
            
            logging.info(f" Scaling Columns : {SCALING_COLUMNS}")
        
            # Transforming Data 
            numerical_cols, categorical_cols = self.separate_numerical_categorical_columns(df=input_feature_train_df)

            # Saving column labels for prediction
            create_yaml_file_numerical_columns(column_list=NUMERICAL_COLUMNS, yaml_file_path=PREDICTION_FILE_PATH)
            create_yaml_file_categorical_columns_dataframe(dataframe=input_feature_train_df, categorical_columns=CATEGORICAL_COLUMNS, yaml_file_path=PREDICTION_FILE_PATH)
            
            logging.info(f" Transformed Data Numerical Columns :{numerical_cols}")
            logging.info(f" Transformed Data Categorical Columns :{categorical_cols}")

            # setting columns in order
            column_order = numerical_cols + categorical_cols

            input_feature_train_df = input_feature_train_df[column_order]
            input_feature_test_df = input_feature_test_df[column_order]

            data_preprocessor = DataPreProcessor(numerical_cols=numerical_cols, categorical_cols=categorical_cols)

            preprocessor = data_preprocessor.get_preprocessor()

            # fit the data
            transformed_train_array = data_preprocessor.fit_transform(data=input_feature_train_df) 
            train_target_array = train_target_array
            transformed_test_array = data_preprocessor.fit_transform(data=input_feature_test_df)
            test_target_array = test_target_array
            
            # log the shape of the transformed data
            logging.info("-----------------Transformed Data-----------------")
            
            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            os.makedirs(transformed_train_dir, exist_ok=True)
            os.makedirs(transformed_test_dir, exist_ok=True)

            # save the transformed_train and transformed_test file
            logging.info("Saving transformed train and transformed test data")

            transformed_train_file_path = os.path.join(transformed_train_dir, 'train.npz')
            train_target_file_path = os.path.join(transformed_train_dir, 'train_target.npz')
            transformed_test_file_path = os.path.join(transformed_test_dir, 'test.npz')
            test_target_file_path = os.path.join(transformed_test_dir, 'test_target.npz')

            # save the data
            save_numpy_array_data(file_path=transformed_train_file_path, array=transformed_train_array)
            save_numpy_array_data(file_path=train_target_file_path, array=train_target_array)
            save_numpy_array_data(file_path=transformed_test_file_path, array=transformed_test_array)
            save_numpy_array_data(file_path=test_target_file_path, array=test_target_array)

            logging.info("Train and Test data saved to file")

            # saving feature engineering and preprocessor object
            logging.info("Saving the feature engineering object")

            # feature_engineering_object_file_path = self.data_transformation_config.feature_engineering_object_file_path
            feat_engg_obj_file_path = self.data_transformation_config.feat_engg_obj_file_path

            save_object(file_path=feat_engg_obj_file_path, obj=feat_engg_obj)
            save_object(file_path=os.path.join(ROOT_DIR, PICKLE_DIR_NAME_KEY,
                                os.path.basename(feat_engg_obj_file_path)), obj=feat_engg_obj)
            
            logging.info("Saving object")
            
            preprocessor_file_path = self.data_transformation_config.processed_object_file_path

            save_object(file_path=preprocessor_file_path, obj=preprocessor)

            save_object(os.path.join(ROOT_DIR, PICKLE_DIR_NAME_KEY,
                        os.path.basename(preprocessor_file_path)), obj=preprocessor)
            
            data_transformation_artifact = DataTransformationArtifact(
                    transformed_train_file_path = transformed_train_file_path,
                    transformed_test_file_path = transformed_test_file_path,
                    train_target_file_path = train_target_file_path,
                    test_target_file_path = test_target_file_path,
                    feat_engg_obj_file_path = feat_engg_obj_file_path,
            )

            return data_transformation_artifact
        
        except Exception as e:
            raise CustomException(e, sys) from e
    