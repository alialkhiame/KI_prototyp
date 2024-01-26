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
        if self.model is None:
            self.create_model((X.shape[1],))
        self.model.fit(X, y, epochs=epochs)
        # Change the save format to '.keras'
        self.model.save(self.model_save_path.replace('.h5', '.keras'))

    def predict(self, X):
        if self.model is None:
            raise Exception("Model not trained or loaded.")
        return self.model.predict(X)


# Load and prepare data
file = "Umsatz_data.csv"
cleaned_data = pd.read_csv(file)

# Selecting the correct columns for input features and target variable
input_features = ['Jahre', 'Wetherstatus', 'Inflationrate', 'InvestionindemMarkt',
                  'Kriegwahrscheinlichkeit', 'Gewinn', 'Zinsen']
x = cleaned_data[input_features]
y = cleaned_data["Umsatz"]

# Rest of your code for splitting, scaling, training, and plotting...


# Split data into train and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# Scale the features
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

# Train the model
umsatz_model = Nero()
umsatz_model.train_model(x_train_scaled, y_train)

# Predict and plot the results
predictions =  umsatz_model.predict(x_test_scaled)
plt.scatter(y_test, predictions)
plt.xlabel("Actual Umsatz")
plt.ylabel("Predicted Umsatz")
plt.title("Actual vs Predicted Umsatz")
plt.show()
