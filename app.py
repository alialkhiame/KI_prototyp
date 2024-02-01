import logging
import base64
from io import BytesIO

from typing import io
import traceback
import cleaned_data as cd
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from flask import Flask, request, jsonify, render_template
from cleanData import CleanData  # Assuming CleanData is in cleanData.py
import json
import nero
import io

app = Flask(__name__)

krieg = 0


def train_models(x_train, y_train):
    models = {
        'Linear_Regression': LinearRegression(),
        'Decision_Tree': DecisionTreeRegressor(),
        'Random_Forest': RandomForestRegressor()
    }
    x_train = x_train.astype('float32')
    y_train = y_train.astype('float32')
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
    plt.clf()
    return base64.b64encode(img.getvalue()).decode('utf8')


def change_index_month(data):
    # Change "Monat" from string to int
    for idx in data.index:
        data.at[idx, "Monat"] = idx % 12 + 1

    # Generate "Datum" column, also set index to "Datum"
    data.Monat = data.Monat.astype(str)
    data.Jahr = data.Jahr.astype(str)
    data["Datum"] = data["Jahr"] + "-" + data["Monat"] + "-01"
    data.set_index("Datum", inplace=True)
    data.index = pd.to_datetime(data.index)
    print(data)
    return data

@app.route('/')
def index():
    sumValue = 0
    return render_template('index.html', sumValue=sumValue)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']
    print(file)
    selected_columns = request.form.get('selected_columns', None)
    column_to_check = request.form.get('column_to_check', None)
    percentage = int(request.form.get('percentage', 90))

    if selected_columns:
        selected_columns = json.loads(selected_columns)

    data_cleaner = CleanData(file, selected_columns, column_to_check, percentage)
    cleaned_data = data_cleaner.cleaned_data

    return jsonify(columns=cleaned_data.columns.tolist())


@app.route('/predict', methods=['POST'])
def predict_route():
    # Validate request
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    try:
        # Extract and preprocess request data
        file, target_column, selected_columns, column_to_check, percentage = extract_request_data(request)

        # Clean data
        cleaned_data = clean_data(file, selected_columns, column_to_check, percentage)
        print(cleaned_data)

        # Process with Nero
        nero_predictions_plot = 1

        # Train and predict with custom models
        results_dict, plot_url, results_html = train_and_predict_with_custom_models(cleaned_data, target_column,
                                                                                    selected_columns)

        return jsonify(predictions=results_dict, plot_url=plot_url, results_html=results_html,
                       nero=nero_predictions_plot)
    except Exception as e:
        print("An error occurred:", str(e))
        traceback.print_exc()
        return jsonify(error="An error occurred during processing."), 500


def extract_request_data(request):
    target_column = request.form['target_column']
    selected_columns = json.loads(request.form['selected_columns'])
    column_to_check = request.form.get('column_to_check', None)
    percentage = int(request.form.get('percentage', 90))
    file = request.files['file']
    return file, target_column, selected_columns, column_to_check, percentage


def clean_data(file, selected_columns, column_to_check, percentage):
    data_cleaner = CleanData(file, selected_columns, column_to_check, percentage)
    return data_cleaner.cleaned_data


def process_with_nero(cleaned_data):
    cleaned_data_nero = cd.cleaner(cleaned_data)
    try:
        umsatz_model = nero.Nero()
        x_train_scaled, x_test_scaled, y_train, y_test = umsatz_model.load_and_preprocess_data(cleaned_data_nero)
        umsatz_model.train_model(x_train_scaled, y_train)
        nero_predictions = umsatz_model.predict(x_test_scaled)
        nero_predictions_plot = umsatz_model.plot_resultsNero(y_test, nero_predictions)
        return nero_predictions_plot
    except Exception as e:
        print("Processing with Nero failed:", str(e))
        return None


def train_and_predict_with_custom_models(cleaned_data, target_column, selected_columns):
    x = cleaned_data[selected_columns]
    y = cleaned_data[target_column]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    models = train_models(x_train, y_train)
    results = predict(models, x_test)
    plot_url = plot_results(results)
    results_html = results.to_html()
    return results.to_dict(), plot_url, results_html


if __name__ == '__main__':
    app.run(debug=True)
