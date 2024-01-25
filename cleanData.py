from collections import Counter

import pandas as pd
import logging
from io import StringIO

class CleanData:
    def __init__(self, file_stream, selected_columns=None, column_to_check=None, percentage=90):
        self.file_stream = file_stream
        self.selected_columns = selected_columns
        self.column_to_check = column_to_check
        self.percentage = percentage
        self.cleaned_data = self._read_and_clean_data()

    def _infer_delimiter_and_decimal(self):
        file_content = self.file_stream.read().decode('utf-8')
        self.file_stream.seek(0)  # Reset file_stream position
        lines = file_content.split('\n')

        delimiters = [',', ';', '\t', '|']
        delimiter_counts = {delimiter: lines[0].count(delimiter) for delimiter in delimiters}
        inferred_delimiter = max(delimiter_counts, key=delimiter_counts.get)

        decimal_counts = Counter(char for line in lines for char in line if char in [',', '.'])
        inferred_decimal = ',' if decimal_counts[','] > decimal_counts['.'] else '.'

        return inferred_delimiter, inferred_decimal

    def _read_and_clean_data(self):
        try:
            delimiter, decimal = self._infer_delimiter_and_decimal()
            file_content = StringIO(self.file_stream.read().decode('utf-8'))
            original_data = pd.read_csv(file_content, delimiter=delimiter, decimal=decimal)

            if self.selected_columns:
                data_to_clean = original_data[self.selected_columns]
            else:
                data_to_clean = original_data

            return self._clean_data(data_to_clean)
        except Exception as e:
            logging.error(f"Error processing data: {e}")
            raise

    def _clean_data(self, data):
        if data.empty:
            logging.error("No data provided.")
            return pd.DataFrame()

        try:
            data.dropna(inplace=True)
            if self.column_to_check and self.column_to_check in data.columns:
                data[self.column_to_check] = pd.to_numeric(data[self.column_to_check], errors='coerce')
                data.dropna(subset=[self.column_to_check], inplace=True)

                average_value = data[self.column_to_check].mean()
                lower_bound = average_value - (average_value * self.percentage / 100)
                upper_bound = average_value + (average_value * self.percentage / 100)

                cleaned_data = data[
                    (data[self.column_to_check] >= lower_bound) & (data[self.column_to_check] <= upper_bound)
                    ]
                return cleaned_data
            return data
        except Exception as e:
            logging.error(f"Error cleaning data: {e}")
            return pd.DataFrame()
