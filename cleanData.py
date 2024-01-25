import pandas as pd
import logging
from collections import Counter


class CleanData:
    def __init__(self, file):
        self.file = file
        self.original_data_head = None
        self.cleaned_data = self._read_and_clean_data(file)

    def _infer_delimiter_and_decimal(self):
        """Infer the most common delimiter and decimal point in a CSV file."""
        with open(self.file, 'r') as f:
            lines = f.readlines()

        # Count delimiters
        delimiters = [',', ';', '\t', '|']
        delimiter_counts = {delimiter: lines[0].count(delimiter) for delimiter in delimiters}
        inferred_delimiter = max(delimiter_counts, key=delimiter_counts.get)

        # Infer decimal
        decimal_counts = Counter(char for line in lines for char in line if char in [',', '.'])
        inferred_decimal = ',' if decimal_counts[','] > decimal_counts['.'] else '.'
        logging.info()
        return inferred_delimiter, inferred_decimal

    def _read_and_clean_data(self, file):
        try:
            self.file = file
            logging.info("Reading and cleaning the data")

            # Infer the delimiter and decimal point
            delimiter, decimal = self._infer_delimiter_and_decimal()

            # Read the data
            original_data = pd.read_csv(self.file, delimiter=delimiter, decimal=decimal)

            # Keep a copy of the original head
            self.original_data_head = original_data.head()

            # Select relevant columns
            umsatz_data = original_data[self.selected_columns]

            # Clean the data
            return umsatz_data

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
            data.dropna(inplace=True)

            # Check and clean possible outliers or implausible values
            column_to_check = 'Umsatz'
            percentage = 90

            # Convert the column to numeric values or remove it
            data[column_to_check] = pd.to_numeric(data[column_to_check], errors='coerce')
            data.dropna(subset=[column_to_check], inplace=True)

            # Calculate average value and define lower and upper bounds
            average_value = data[column_to_check].mean()
            lower_bound = average_value - (average_value * percentage / 100)
            upper_bound = average_value + (average_value * percentage / 100)

            # Filter out data outside the bounds
            cleaned_data = data[
                (data[column_to_check] >= lower_bound) & (data[column_to_check] <= upper_bound)
                ]

            logging.info(cleaned_data)
            return cleaned_data
        except Exception as e:
            logging.error(f"Error cleaning data: {e}")
            return pd.DataFrame()

