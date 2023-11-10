import pandas as pd
import random

# Generate sample data
data = {
    'Feature1': [random.randint(1, 100) for _ in range(10)],
    'Feature2': [random.uniform(0, 1) for _ in range(10)],
    'Target': [random.choice(['ClassA', 'ClassB']) for _ in range(10)]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Specify the file path to save the CSV file
file_path = 'test_data.csv'

# Save the DataFrame to a CSV file
df.to_csv(file_path, index=False)

print(f"Data saved to {file_path}")
