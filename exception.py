# importing libraries
import os
import sys
from flask import Flask
from src.logger import logging
from src.exception import CustomException

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        raise Exception("We are testing our custom exception file")
    except Exception as e:
        test = CustomException(e, sys)

        logging.info(test.error_message)
        logging.info("starting flask app and also testing logging file")

        return "success analytics project"


if __name__ == "__main__":
    app.run(debug=True)
