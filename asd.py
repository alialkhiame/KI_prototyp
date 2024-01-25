import numpy as np
import pandas as pd

# Number of data points
num_data_points = 100

# Number of features per data point
num_features = 10

# Generate random data for features
x = np.random.rand(num_data_points, num_features)

# Generate random labels (0, 1, or 2) for each data point
y = np.random.randint(0, 3, num_data_points)

# Combine features and labels into a DataFrame for easy CSV export
data = np.column_stack((x, y))
column_names = [f'feature_{i}' for i in range(num_features)] + ['label']
dataset = pd.DataFrame(data, columns=column_names)

# Save the dataset to a CSV file
dataset.to_csv('datsa.csv', index=False)
