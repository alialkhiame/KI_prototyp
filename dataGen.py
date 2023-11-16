import pandas as pd
import numpy as np

class dataGen:
    def __init__(self):
        # Setting the random seed for reproducibility
        np.random.seed(0)

    def generate_data(self):
        years = list(range(2000, 2023))
        data = {
            "Year": years,
            "Kosten": [100] + [100 + np.random.randint(-10, 11) for _ in years[1:]],
            "Umwetterung": np.random.randint(1, 11, len(years)),
            "Arbeits": np.random.uniform(50, 100, len(years)),
            "Inflation": np.random.uniform(0, 5, len(years)),
            "Gewinn": [100] + [100 + np.random.randint(-10, 11) for _ in years[1:]],
            "Eigenkapital": np.random.randint(10000, 100000, len(years)),
            "Fremdkapital": np.random.randint(10000, 100000, len(years)),
            "Umsatz": np.random.randint(50000, 500000, len(years)),
            "Arbeitslosenquote": np.random.uniform(3, 10, len(years)),
            "API_Factors": np.random.randint(1, 100, len(years)),
            "GDP": np.random.randint(100000, 1000000, len(years))
        }
        return pd.DataFrame(data)
