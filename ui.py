import pandas as pd
import random

class DataGenerator:
    def __init__(self, num_samples=10):
        self.num_samples = num_samples

    def generate_data(self):
        data = {
            'Feature1': [random.randint(1, 100) for _ in range(self.num_samples)],
            'Feature2': [random.uniform(0, 1) for _ in range(self.num_samples)],
            'Umsatz': [random.uniform(1000, 10000) for _ in range(self.num_samples)]
        }

        return pd.DataFrame(data)

    def save_to_csv(self, file_path='test_data.csv'):
        df = self.generate_data()
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")

# Beispiel für die Verwendung der Klasse
data_generator = DataGenerator(num_samples=20)
data_generator.save_to_csv(file_path='umsatz_data.csv')
