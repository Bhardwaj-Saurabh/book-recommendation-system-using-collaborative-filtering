from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from src.utils import save_object, load_object

from src.logger import logging
from src.exception import CustomException

import os
import sys
import numpy as np
import pandas as pd
from dataclasses import dataclass


@dataclass
class ModelTrainerConfig:
    """
    Configuration class for the ModelTrainer.

    Attributes:
        train_model_file_path (str): The file path to save the trained model.
    """
    train_model_file_path: str = os.path.join('artifacts', 'model.pkl')


class ModelTrainer:
    """
    Configuration class for the ModelTrainer.

    Attributes:
        train_model_file_path (str): The file path to save the trained model.
    """

    def __init__(self):
        self.model_training_config = ModelTrainerConfig()

    def initiate_model_training(self, user_book_matrix):
        """
        Train Nearest Neighbors models to find the best performing model.

        Args:
            user_book_matrix (pkl): pivot table data array with features variable.

        Raises:
            CustomException: If an exception occurs during model training and evaluation.
        """
        try:

            # Load the sparse matrix
            logging.info("Load the sparse matrix")
            user_book_matrix = load_object(user_book_matrix)

            logging.info("Creating a sparse matrix from the user-book matrix")
            # Creating a sparse matrix from the user-book matrix
            sparse_user_book_matrix = csr_matrix(user_book_matrix)

            logging.info("Initializing the NearestNeighbors model with 'brute' algorithm")
            # Initializing the NearestNeighbors model with 'brute' algorithm
            nearest_neighbors_model = NearestNeighbors(algorithm='brute')

            # Fitting the model to the sparse user-book matrix
            logging.info("Fitting the model to the sparse user-book matrix")
            nearest_neighbors_model.fit(sparse_user_book_matrix)

            logging.info(f"Best Model Found: {nearest_neighbors_model}")

            # Save the best model
            save_object(
                file_path=self.model_training_config.train_model_file_path,
                obj=nearest_neighbors_model
            )
        except Exception as e:
            raise CustomException(e, sys)