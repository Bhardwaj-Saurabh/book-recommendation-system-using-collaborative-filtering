import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass

import os
import sys

# Importing custom utility function for saving objects
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    """
    Configuration class for data transformation.
    """

    ratings_object_file_path: str = os.path.join("artifacts", "ratings.pkl")
    pivot_table_object_file_path: str = os.path.join("artifacts", "book_pivot.pkl")


class DataTransformation:
    """
    Class for performing data transformation.
    """

    def __init__(self):
        """
        Initializes the DataTransformation object with the default configuration.
        """
        # Initializing the data transformation configuration
        self.data_transformation_config = DataTransformationConfig()

    def initiate_data_transformation(
        self, books_data_path, users_data_path, ratings_data_path
    ):
        """
        Initiates the data transformation process.

        Reads the books, users and ratings data, applies the data transformation pipeline,
        and saves the final data. Logs the progress and handles any exceptions.

        Args:
            books_data_path (str): Path to the books data CSV file.
            users_data_path (str): Path to the users data CSV file.
            ratings_data_path (str): Path to the ratings data CSV file.

        Returns:
            Tuple[np.ndarray, np.ndarray, str]: Transformed train and test data arrays, and preprocessor object file path.

        Raises:
            CustomException: If an exception occurs during the data transformation process.
        """
        try:
            # Read the books data from CSV
            books_df = pd.read_csv(books_data_path)
            # Read the users data from CSV
            users_df = pd.read_csv(users_data_path)
            # Read the ratings data from CSV
            ratings_df = pd.read_csv(ratings_data_path)

            # Logging info message
            logging.info("Reading Data completed")

            logging.info(f"Books Dataframe Head:\n{books_df.head().to_string()}")
            logging.info(f"Users Dataframe Head:\n{users_df.head().to_string()}")
            logging.info(f"Ratings Dataframe Head:\n{ratings_df.head().to_string()}")

            logging.info("Filtering out users who have given less than 200 ratings")
            active_users_filter = ratings_df["user_id"].value_counts() > 200
            active_users = active_users_filter[active_users_filter].index
            ratings_df = ratings_df[ratings_df["user_id"].isin(active_users)]

            # Merging the ratings data with books data
            logging.info("Merging the ratings data with books data")
            merged_ratings_books_df = ratings_df.merge(books_df, on="ISBN")

            # Grouping the merged data by book title and counting the ratings
            logging.info(
                "Grouping the merged data by book title and counting the ratings"
            )
            book_rating_counts = (
                merged_ratings_books_df.groupby("title").rating.count().reset_index()
            )

            # Merging the rating counts with the merged ratings and books data
            logging.info(
                "Merging the rating counts with the merged ratings and books data"
            )
            final_ratings_df = merged_ratings_books_df.merge(
                book_rating_counts, on="title"
            )

            # Filtering the final ratings data to include books with at least 50 ratings
            logging.info(
                "Filtering the final ratings data to include books with at least 50 ratings"
            )
            final_ratings_df = final_ratings_df[final_ratings_df["rating_y"] >= 50]

            # Dropping duplicate entries based on title and user_id
            logging.info("Dropping duplicate entries based on title and user_id")
            final_ratings_df.drop_duplicates(["title", "user_id"], inplace=True)

            # Creating a pivot table for the user-book matrix
            logging.info("Creating a pivot table for the user-book matrix")
            user_book_matrix = final_ratings_df.pivot_table(
                columns="user_id", index="title", values="rating_y"
            )

            # Filling missing values in the pivot table with 0
            logging.info("Filling missing values in the pivot table with 0")
            user_book_matrix.fillna(0, inplace=True)

            # Logging info message
            logging.info("Saving the Final Ratings and Pivot Table objects")

            save_object(
                # Save the final rating objects
                file_path=self.data_transformation_config.ratings_object_file_path,
                obj=final_ratings_df,
            )
            save_object(
                # Save the pivot table objects
                file_path=self.data_transformation_config.pivot_table_object_file_path,
                obj=user_book_matrix,
            )

            return (
                self.data_transformation_config.ratings_object_file_path,
                self.data_transformation_config.pivot_table_object_file_path,
            )

        except Exception as e:
            # Logging error message
            logging.error("Error occurred during Data Transformation")
            # Raising custom exception with the original exception and system information
            raise CustomException(e, sys)
