import os
import sys
import pickle
import numpy as np
import pandas as pd
from src.logger import logging
from src.exception import CustomException


def save_object(file_path, obj):
    """
    Save an object to a file using pickle.

    Args:
        file_path (str): Path to the file where the object will be saved.
        obj: The object to be saved.

    Raises:
        CustomException: If an exception occurs during object saving.
    """
    try:
        dir_path = os.path.dirname(file_path)

        # Create the directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)

        # Save the object to the file
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    """
    Load an object from a file using pickle.

    Args:
        file_path (str): The file path of the object to load.

    Returns:
        The loaded object.

    Raises:
        CustomException: If an error occurs while loading the object.
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)