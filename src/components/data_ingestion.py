import os
import sys
from src.logger import logging  # Importing custom logger module
from src.exception import CustomException  # Importing custom exception module

import pandas as pd  # Importing pandas library 
from sklearn.model_selection import train_test_split  

# Importing dataclass decorator from dataclasses module
from dataclasses import dataclass  

## Data Ingestion configuration

@dataclass
class DataIngestionConfig:
    """
    Configuration class for data ingestion.
    """
    books_raw_data_path: str =  os.path.join('artifacts', 'books.csv')
    users_raw_data_path: str = os.path.join('artifacts', 'users.csv')  
    ratings_raw_data_path: str = os.path.join('artifacts', 'ratings.csv')  

class DataIngestion:
    """
    Class for performing data ingestion.
    """
    def __init__(self) -> None:
        """
        Initializes the DataIngestion object with the default configuration.
        """
        self.ingestion_config = DataIngestionConfig()  # Initializing the ingestion configuration
    
    def initiate_data_ingestion(self):
        """
        Initiates the data ingestion process.
        
        Reads the data from a CSV file
        and saves the data as CSV files. Logs the progress and handles any exceptions.
        
        Returns:
            Tuple[str, str]: Paths of the train and test data CSV files.
        
        Raises:
            CustomException: If an exception occurs during the data ingestion process.
        """
        logging.info("Data Ingestion started")  # Logging info message
        
        try:
            # Read the data from the CSV file
            books_df = pd.read_csv(os.path.join('Data', 'books.csv'), sep=';',
                       on_bad_lines='skip',
                       encoding='latin-1',
                       low_memory=False)
            logging.info('Reading the Books data as Pandas DataFrame')  # Logging info message

            users_df = pd.read_csv(os.path.join('Data', 'users.csv'), sep=';',
                       on_bad_lines='skip',
                       encoding='latin-1',
                       low_memory=False)

            logging.info('Reading the Users data as Pandas DataFrame')  # Logging info message

            ratings_df = pd.read_csv(os.path.join('Data', 'ratings.csv'), sep=';',
                       on_bad_lines='skip',
                       encoding='latin-1',
                       low_memory=False)
        
            logging.info('Reading the Ratings data as Pandas DataFrame')  

            # Columns to drop from books data identified during EDA
            books_drop_cols = ['Year-Of-Publication', 'Image-URL-S', 'Image-URL-M']

            logging.info('Droping the columns from books_df dataframe')  
            books_df.drop(books_drop_cols, axis = 1, inplace=True)

            logging.info('Renaming the columns name in books data for EASE OF USE')  
            # Renaming columns for better readability and consistency
            books_df.rename(columns={
                'Book-Title': 'title',
                'Book-Author': 'author',
                'Publisher': 'publisher',
                'Image-URL-L': 'url'
            }, inplace=True)

            logging.info('Renaming columns in the ratings data for consistency')  
            # Renaming columns in the ratings data for consistency
            ratings_df.rename(columns={
                'User-ID': 'user_id',
                'Book-Rating': 'rating'
                }, inplace=True)

            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(self.ingestion_config.books_raw_data_path), exist_ok=True)

            # Save the raw data as CSV file
            books_df.to_csv(self.ingestion_config.books_raw_data_path)
            users_df.to_csv(self.ingestion_config.users_raw_data_path)
            ratings_df.to_csv(self.ingestion_config.ratings_raw_data_path)

            logging.info('Raw data stored as CSV file') 

            logging.info("Data Ingestion completed")

            return (
                self.ingestion_config.books_raw_data_path,
                self.ingestion_config.users_raw_data_path,
                self.ingestion_config.ratings_raw_data_path
            )

        except Exception as e:
            logging.info("Exception occurred at Data Ingestion Stage")  # Logging info message
            raise CustomException(e, sys)  