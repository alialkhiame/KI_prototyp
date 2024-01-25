import pandas as pd
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
import os


class nero:
    def __init__(self, model_save_path='umsatz_model.h5'):
        self.model_save_path = model_save_path
        self.model = None
        if os.path.exists(self.model_save_path):
            self.model = tf.keras.models.load_model(self.model_save_path)

    def create_model(self, input_shape):
        self.model = Sequential([
            Dense(64, activation='relu', input_shape=(input_shape,)),
            Dense(64, activation='relu'),
            Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def train_model(self, X, y, epochs=10):
        if self.model is None:
            self.create_model(X.shape[4])
        self.model.fit(X, y, epochs=epochs)
        self.model.save(self.model_save_path)

    def predict(self, X):
        if self.model is None:
            raise Exception("Model not trained or loaded.")
        return self.model.predict(X)

# Example usage:
# umsatz_model = UmsatzModel()
# umsatz_model.train_model(X_train, y_train)
# predictions = umsatz_model.predict(X_test)
