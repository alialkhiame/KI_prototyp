import pandas as pd

def month_to_number(month):
    months = {
        'Januar': 1, 'Februar': 2, 'März': 3, 'April': 4, 'Mai': 5, 'Juni': 6,
        'Juli': 7, 'August': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'Dezember': 12
    }
    return months.get(month, 0)

def cleaner(cleaned_data):
    # Rename columns
    rename_dict = {
        'Jahr': 'year',
        'Monat': 'month',
        'Umsatz': 'revenue',
        'InvestionindemMarkt': 'investitionimmarkt',
        'Weatherstatus': 'weatherstatus',
        'Inflationrate': 'inflationrate'
    }
    cleaned_data.rename(columns=rename_dict, inplace=True)

    # Drop date-related columns if they exist
    for col in ['year', 'month', 'day']:
        if col in cleaned_data.columns:
            cleaned_data.drop(col, axis=1, inplace=True)

    # Select specific columns
    required_columns = ['index', 'revenue', 'weatherstatus', 'investitionimmarkt', 'inflationrate']
    selected_columns = [col for col in cleaned_data.columns if col in required_columns]

    # Keep only the required columns
    cleaned_data = cleaned_data[selected_columns]

    # Create the desired array
    result_array = cleaned_data.to_numpy()

    # Print the array (you can remove this line in production)
    print("Data After Cleaning")
    print(result_array)

# Example usage
# df = pd.read_csv('your_data_file.csv') # replace with your actual file
# cleaner(df)
