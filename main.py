from src.pipeline.train import Pipeline
from src.logger import logging

def main():
    try:

        pipeline = Pipeline()
        pipeline.run_pipeline()

    except Exception as e:
        logging.error(f"{e}")
        print(e)


if __name__ == "__main__":
    main()