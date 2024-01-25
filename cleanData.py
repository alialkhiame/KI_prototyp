import pandas as pd
import logging

class CleanData:
    def __init__(self, file_obj):
        self.file_obj = file_obj
        self.original_data_head = None
        self.cleaned_data = self._read_and_clean_data()

    def _read_and_clean_data(self):
        try:
            logging.info("Reading and cleaning the data")

            # Read the data from file object
            self.file_obj.seek(0)  # Reset file pointer to the beginning
            original_data = pd.read_csv(self.file_obj)

            # Keep a copy of the original head
            self.original_data_head = original_data.head()

            # Clean the data
            return self._clean_data(original_data)

        except Exception as e:
            logging.error(f"Error processing data: {e}")
            raise

    def _clean_data(self, data):
        """
        Cleans the provided DataFrame.
        """
        if data.empty:
            logging.error("No data provided.")
            return pd.DataFrame()

        try:
            # Remove rows with missing values
            data = data.dropna()

            # Iterate through columns and clean
            for column in data.columns:
                # Attempt to convert each column to numeric values
                data[column] = pd.to_numeric(data[column], errors='coerce')

            # Drop rows where any column is NaN after conversion
            cleaned_data = data.dropna()

            logging.info(cleaned_data)
            return cleaned_data
        except Exception as e:
            logging.error(f"Error cleaning data: {e}")
            return pd.DataFrame()
