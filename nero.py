import pandas as pd
import matplotlib.pyplot as plt
import keras
from keras import layers


class NeuralNetwork:
    def __init__(self, num_classes):
        self.model = None
        self.input_shape = None
        self.num_classes = num_classes

    def load_data(self, csv_file):
        data = pd.read_csv(csv_file)
        # Assuming the last column is the target variable
        x = data.iloc[:, :-1].values
        y = data.iloc[:, -1].values
        self.input_shape = x.shape[1]  # Automatically determine the input shape
        return x, y

    def create_model(self):
        if self.input_shape is None:
            raise ValueError("Input shape not defined. Load data before creating the model.")

        self.model = keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=(self.input_shape,)),
            layers.Dense(64, activation='relu'),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        self.model.compile(optimizer='adam',
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])

    def train(self, x_train, y_train, epochs=10, batch_size=32):
        history = self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2)
        return history

    def test(self, x_test, y_test):
        test_loss, test_acc = self.model.evaluate(x_test, y_test)
        print(f"Test accuracy: {test_acc}, Test loss: {test_loss}")

    def plot_results(self, history):
        plt.figure(figsize=(12, 4))

        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'], label='Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Training and Validation Accuracy')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'], label='Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Training and Validation Loss')
        plt.legend()

        plt.show()


# Example usage:
nn = NeuralNetwork(num_classes=3)
x, y = nn.load_data('umsatz_data.csv')
nn.create_model()
history = nn.train(x, y, epochs=10, batch_size=32)
nn.plot_results(history)
