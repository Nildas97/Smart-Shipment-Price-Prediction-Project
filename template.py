# importing libraries
import os
from pathlib import Path
import logging

# logging format
logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s: %(levelname)s]: %(message)s"
)

# while loop
while True:
    project_name = input("Enter your project name: ")
    if project_name != "":
        break

logging.info(f"Creating project by name: {project_name}")

list_of_files = [
    # ".github/workflows/.gitkeep",
    # ".github/workflows/main.yaml",
    # f"src/{project_name}/__init__.py",
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/config/__init__.py",
    f"{project_name}/constant/__init__.py",
    f"{project_name}/exception/__init__.py",
    # f"{project_name}/predictor.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"configs/config.yaml",
    f"configs/schema.yaml",
    "requirements.txt",
    "schema.yaml",
    "setup.py",
    "main.py",
    "app.py",
    "logs.py",
    "dvc.yaml",
    "exception.py",
]

# checking all the files in the list of files
for filepath in list_of_files:
    filepath = Path(filepath)
    # splitting file directory and file name
    filedir, filename = os.path.split(filepath)
    # if file directory is empty
    if filedir != "":
        # create file directory
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating a new directory at : {filedir} for file: {filename}")
    # if filepath does not exists
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0): 
        # open and create files and folder in filepath
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating a new file: {filename} for path: {filepath}")
    else:
        logging.info(f"file is already present at: {filepath}")
