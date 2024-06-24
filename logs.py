# importing libraries
from flask import Flask
from src.logger import logging


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    logging.info("starting flask app and also testing logging file")
    return "success analytics project"


if __name__ == "__main__":
    app.run(debug=True)
