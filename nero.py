import base64
from io import BytesIO

import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend such as 'Agg'
import matplotlib.pyplot as plt

import os

class Nero:
    def __init__(self, model_save_path='umsatz_model.h5'):
        self.model_save_path = model_save_path
        self.model = tf.keras.models.load_model(self.model_save_path) if os.path.exists(self.model_save_path) else None

    def create_model(self, input_shape):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=input_shape),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def train_model(self, X, y, epochs=10):
        # Check if the model exists and has the correct input shape
        if self.model is None or self.model.input_shape[1] != X.shape[1]:
            self.create_model((X.shape[1],))

        self.model.fit(X, y, epochs=epochs)
        self.model.save(self.model_save_path.replace('.h5', '.keras'))

        if self.model is None:
            self.create_model((X.shape[1],))
        self.model.fit(X, y, epochs=epochs)
        self.model.save(self.model_save_path.replace('.h5', '.keras'))

    def predict(self, X):
        if self.model is None:
            raise Exception("Model not trained or loaded.")
        return self.model.predict(X)

    def load_and_preprocess_data(self, cleaned_data):
        # Load data from a file stream
        print("cleaned_data")
        target_variable = 'Umsatz'
        # Selecting the correct columns for input features and target variable
        input_features = ['Jahre', 'Wetherstatus', 'Inflationrate', 'InvestionindemMarkt',
                          'Kriegwahrscheinlichkeit', 'Gewinn', 'Zinsen']
        # Check and fill missing columns with default values
        for feature in input_features:
            if feature not in cleaned_data.columns:
                cleaned_data[feature] = 0  # Replace 0 with an appropriate default value for each feature

        # Ensure the target variable is in the data
        if target_variable not in cleaned_data.columns:
            raise ValueError(f"Target variable '{target_variable}' not found in the data.")

        x = cleaned_data[input_features]
        y = cleaned_data[target_variable]
        x = x.astype('float32')
        y = y.astype('float32')

        # Split data into train and test sets
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

        # Scale the features
        scaler = StandardScaler()
        x_train_scaled = scaler.fit_transform(x_train)
        x_test_scaled = scaler.transform(x_test)

        return x_train_scaled, x_test_scaled, y_train, y_test

    def plot_resultsNero(self, y_test, predictions):

        print(predictions)
        plt.scatter(y_test, predictions)
        plt.xlabel("Actual Umsatz")
        plt.ylabel("Predicted Umsatz")
        plt.title("Nero")
        plt.tight_layout()
        plt.show()
        img = BytesIO()
        plt.savefig(img, format='png')
        plt.clf()
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode('utf8')
