import os, sys
from src.logger import logging
from src.exception import CustomException

import pandas as pd

from src.components.data_ingestion import DataIngestion
from src.components.data_preprocessing import DataTransformation
from src.components.model_preparation import ModelTrainer

if __name__ == "__main__":
    obj = DataIngestion()
    books_df, users_df, ratings_df = obj.initiate_data_ingestion()
    # print(books_df, users_df, ratings_df)
    data_transformation = DataTransformation()
    ratings, pivot_table, books_title = data_transformation.initiate_data_transformation(
        books_df, users_df, ratings_df
    )
    model_trainer = ModelTrainer()
    model_trainer.initiate_model_training(pivot_table)
