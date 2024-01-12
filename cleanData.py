import pandas as pd
import logging
from io import StringIO


def cleanData(data):
    """
    Cleans the provided CSV data.

    It includes removing rows with missing values in the 'Umsatz' column,
    converting the 'Umsatz' column to numeric values, and filtering out outliers
    based on a percentage threshold.

    Args:
        data (str): CSV data as a string.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """

    # Load revenue data from a CSV string
    if not data:
        logging.error("No data provided.")
        return pd.DataFrame()

    try:
        umsatz_data = pd.read_csv(StringIO(data))
    except Exception as e:
        logging.error(f"Error reading data: {e}")
        return pd.DataFrame()

    logging.info(data)

    # Remove rows with missing values
    umsatz_data.dropna(inplace=True)

    # Check and clean possible outliers or implausible values
    column_to_check = 'Umsatz'
    percentage = 90

    # Convert the column to numeric values or remove it
    umsatz_data[column_to_check] = pd.to_numeric(umsatz_data[column_to_check], errors='coerce')
    umsatz_data.dropna(subset=[column_to_check], inplace=True)

    # Calculate average value and define lower and upper bounds
    average_value = umsatz_data[column_to_check].mean()
    lower_bound = average_value - (average_value * percentage / 100)
    upper_bound = average_value + (average_value * percentage / 100)

    # Filter out data outside the bounds
    umsatz_data = umsatz_data[
        (umsatz_data[column_to_check] >= lower_bound) & (umsatz_data[column_to_check] <= upper_bound)
        ]
    logging.info(umsatz_data)
    return umsatz_data
