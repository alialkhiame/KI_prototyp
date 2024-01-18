import json
import logging
import base64
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import news_api
import cleanData as cD
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

krieg = 0


def read_and_clean_data(file, selected_colums):
    try:
        logging.info("Reading the data")
        umsatz_data = pd.read_csv(file.stream, delimiter=';', decimal=',')
        column_to_check = 'Umsatz'
        percentage = 90

        # Convert the column to numeric values or remove it
        umsatz_data[column_to_check] = pd.to_numeric(umsatz_data[column_to_check], errors='coerce')
        umsatz_data.dropna(subset=[column_to_check], inplace=True)

        # Calculate average value and define lower and upper bounds
        average_value = umsatz_data[column_to_check].mean()
        lower_bound = average_value - (average_value * percentage / 100)
        upper_bound = average_value + (average_value * percentage / 100)

        # Filter out data outside the bounds
        umsatz_data = umsatz_data[
            (umsatz_data[column_to_check] >= lower_bound) & (umsatz_data[column_to_check] <= upper_bound)
            ]
        logging.debug(umsatz_data)

        mean_value = umsatz_data['Umsatz'].mean()
        return umsatz_data.fillna(mean_value)
    except Exception as e:
        logging.error(f"Error reading data: {e}")
        raise


def train_models(x_train, y_train):
    models = {
        'Linear_Regression': LinearRegression(),
        'Decision_Tree': DecisionTreeRegressor(),
        'Random_Forest': RandomForestRegressor()
    }
    for name, model in models.items():
        model.fit(x_train, y_train)
    return models


def predict(models, X_test):
    predictions = {name: model.predict(X_test) for name, model in models.items()}

    return pd.DataFrame(predictions)


def plot_results(results):
    results.plot(kind='bar')
    plt.title('Model Predictions')
    plt.xlabel('Data Points')
    plt.ylabel('Predicted Values')
    plt.tight_layout()
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')


@app.route('/')
def index():
    # Call to newsApi script to get sumValue
    sumValue = news_api.get_sum()
    krieg = sumValue
    return render_template('index.html', sumValue=sumValue)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    try:
        file = request.files['file']
        cleaned_data = read_and_clean_data(file, None)
        logging.info(cleaned_data)
        return jsonify(columns=cleaned_data.columns.tolist())
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.route('/predict', methods=['POST'])
def predict_route():
    try:
        if 'file' not in request.files:
            return jsonify(error="No file part"), 400
        file = request.files['file']
        cleaned_data = read_and_clean_data(file, None)
        logging.info(cleaned_data)

        logging.debug("i ama here ")
        logging.info(cleaned_data)

        target_column = request.form['target_column']

        selected_columns = request.form['selected_columns']
        logging.info(f"Selected columns: {selected_columns}")
        logging.info(f"Target column: {target_column}")

        selected_columns = json.loads(selected_columns)
        x = cleaned_data[selected_columns]
        y = cleaned_data[target_column]

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
        models = train_models(x_train, y_train)
        results = predict(models, x_test)
        plot_url = plot_results(results)
        results_html = results.to_html()
        logging.info(results)

        return jsonify(predictions=results.to_dict(), plot_url=plot_url, results_html=results_html)
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return jsonify(error="Error in prediction"), 400


if __name__ == '__main__':
    app.run(debug=True)
