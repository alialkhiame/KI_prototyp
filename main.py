import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Preparing the data for the model
from dataGen import df

X = df.drop(['Year', 'Umsatz'], axis=1)  # Features (excluding Year and Umsatz)
y = df['Umsatz']  # Target (Umsatz)

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Creating and training the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predicting on the test set and calculating the Mean Squared Error
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Predicting Umsatz for 2023, 2024, and 2025
# We will use the mean values of the features for these predictions
future_years = pd.DataFrame([X.mean()] * 3)
future_years.index = [2023, 2024, 2025]
predicted_umsatz = model.predict(future_years)

# Displaying the predicted Umsatz
for year, umsatz in zip([2023, 2024, 2025], predicted_umsatz):
    print(f"Year: {year}, Predicted Umsatz: {umsatz}")
