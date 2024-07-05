# importing libraries
import yaml
import os, sys
import pandas as pd

def write_schema_yaml(csv_file):
    # reading the dataset
    df = pd.read_csv(csv_file)

    # checking total columns
    total_cols = len(df.columns)

    # checking total columns name
    columns_name = df.columns.tolist()

    # checking datatypes
    columns_dtypes = df.dtypes.astype(str).tolist()

    # configuring schema dictionary
    schema = {
        "FileNames" : os.path.basename(csv_file),
        "TotalColumns" : total_cols,
        "ColumnsNames" : dict(zip(columns_name, columns_dtypes))
    }

    # directory variables
    ROOT_DIR = os.getcwd()
    SCHEMA_FILE_PATH = os.path.join(ROOT_DIR, 'configs', 'schema.yaml')

    # opening schema file path and write in schema.yaml
    with open(SCHEMA_FILE_PATH, "w") as file:
        yaml.dump(schema, file)

