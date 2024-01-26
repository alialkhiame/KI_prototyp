import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from nero import nero  # Assuming your class is in a file named nero.py


# Function to preprocess the input data
def preprocess_data(data):
    # Convert 'Jahr' and 'Monat' to datetime and extract relevant features
    data['Date'] = pd.to_datetime(data['Jahr'].astype(str) + ' ' + data['Monat'])
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data.drop(['Jahr', 'Monat', 'Date'], axis=1, inplace=True)

    # Define numerical and categorical columns
    numerical_cols = ['Year', 'Month', 'Bodenrinnen', 'Duschrinnen', 'Berlin', 'Hamburg', 'Fulda', 'Stuttgart', 'Paris', 'Zinsen in %', 'Inflation in %', 'W_Berlin', 'W_Hamburg', 'W_Fulda', 'W_Stuttgart', 'W_Paris']
    target_col = ['Umsatz']  # Target variable

    # Create a transformer for scaling numerical data
    numerical_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())])  # Scaling data

    # Combine transformers into a preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols)])

    # Separate features and target
    X = data[numerical_cols]
    y = data[target_col]

    # Preprocess the data
    X = preprocessor.fit_transform(X)

    return X, y.values.ravel()




def change_index_month(data):
    # Change "Monat" from string to int
    for idx in data.index:
        data.at[idx, "Monat"] = idx % 12 + 1

    # Generate "Datum" column, also set index to "Datum"
    data.Monat = data.Monat.astype(str)
    data.Jahr = data.Jahr.astype(str)
    data["Datum"] = data["Jahr"] + "-" + data["Monat"] + "-01"
    data.set_index("Datum", inplace=True)
    data.index = pd.to_datetime(data.index)

    return data