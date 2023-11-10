import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer

class UmsatzPredictor:
    def __init__(self, data_path='umsatz_data.csv'):
        self.data_path = data_path
        self.df = pd.read_csv(self.data_path)
        self.features = self.df.drop('Umsatz', axis=1)
        self.target = self.df['Umsatz']
        self.model = None
        self.preprocess_data()

    def preprocess_data(self):
        # One-hot encode categorical features
        categorical_columns = self.features.select_dtypes(include=['object']).columns
        if categorical_columns.any():
            self.df = pd.get_dummies(self.df, columns=categorical_columns)

        # Separate features and target variable
        self.features = self.df.drop('Umsatz', axis=1)
        self.target = self.df['Umsatz']

        # Check for and handle NaN values
        imputer = SimpleImputer(strategy='median')
        self.features = pd.DataFrame(imputer.fit_transform(self.features), columns=self.features.columns)

    def train_model(self, test_size=0.2):
        X_train, X_test, y_train, y_test = train_test_split(
            self.features, self.target, test_size=test_size, random_state=42
        )

        # Use RandomForestRegressor as an example algorithm
        self.model = RandomForestRegressor()
        if(X_train == nan||y_train==nan)
        self.model.fit(X_train, y_train)

        # Evaluation of the model
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print(f'Mean Squared Error: {mse}')

    def make_predictions(self, new_data):
        # Check for and handle NaN values in new_data
        if 'Wether_status' in new_data.columns:
            new_data['Wether_status'] = new_data['Wether_status'].fillna(new_data['Wether_status'].mode()[0])

        imputer = SimpleImputer(strategy='median')
        new_data = pd.DataFrame(imputer.fit_transform(new_data), columns=new_data.columns)

        predictions = self.model.predict(new_data)
        return predictions

    def generate_future_dates(self, num_years=3):
        last_date = pd.to_datetime(self.df.index[-1])  # assuming the DataFrame has a datetime index
        future_dates = pd.date_range(last_date, periods=num_years * 365, freq='D')[1:]  # exclude the last date
        return future_dates

    def predict_future_umsatz(self, num_years=3):
        future_dates = self.generate_future_dates(num_years)
        future_features = pd.DataFrame(index=future_dates, columns=self.features.columns)

        # Fill in future_features with realistic or hypothetical data
        # For simplicity, you can use the median of each feature from the existing data
        for feature in self.features.columns:
            if feature not in future_features.columns:
                future_features[feature] = np.nanmedian(self.features[feature])

        # Make predictions for future Umsatz
        future_predictions = self.make_predictions(future_features)
        future_df = pd.DataFrame({'Umsatz': future_predictions}, index=future_dates)

        return future_df

# Set the seed before generating random data
np.random.seed(42)

# Generiere zufällige Daten
num_years = 5  # Ändere dies auf die Anzahl der Jahre, die du vorhersagen möchtest
data = {
    'Jahre': np.arange(1, num_years + 1),
    'Wether_status': np.random.choice(['Sunny', 'Cloudy', 'Rainy'], size=num_years),
    'Inflationrate': np.random.uniform(0.01, 0.05, size=num_years),
    'Investion_in_dem_Markt': np.random.uniform(100000, 500000, size=num_years),
    'Krieg_wahrscheinlichkeit': np.random.uniform(0, 0.1, size=num_years),
    'Gewinn': np.random.uniform(50000, 200000, size=num_years),
    'Zinsen': np.random.uniform(0.02, 0.1, size=num_years),
    'Umsatz': np.random.uniform(500000, 1000000, size=num_years)
}

# Introduce some NaN values
data['Umsatz'][1] = np.nan
data['Wether_status'][3] = np.nan

df = pd.DataFrame(data)
df.to_csv('umsatz_data.csv', index=False)

# Beispiel für die Verwendung der Klasse
umsatz_predictor = UmsatzPredictor('./umsatz_data.csv')
umsatz_predictor.train_model()

# Vorhersagen für die nächsten 3 Jahre
future_predictions = umsatz_predictor.predict_future_umsatz(num_years=3)
print(future_predictions)
