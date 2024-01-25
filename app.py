import logging
import base64
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from flask import Flask, request, jsonify, render_template
from cleanData import CleanData  # Assuming CleanData is in cleanData.py
import json

from nero import nero
from preProcessour import preprocess_data

app = Flask(__name__)

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
    return render_template('index.html', sumValue=2)  # Replace 2 with actual value or function call

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']
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
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']
    target_column = request.form['target_column']
    selected_columns = json.loads(request.form['selected_columns'])
    column_to_check = request.form.get('column_to_check', None)
    percentage = int(request.form.get('percentage', 90))
    data_cleaner = CleanData(file, selected_columns, column_to_check, percentage)
    cleaned_data = data_cleaner.cleaned_data




    x = cleaned_data[selected_columns]
    y = cleaned_data[target_column]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    models = train_models(x_train, y_train)
    results = predict(models, x_test)
    plot_url = plot_results(results)
    results_html = results.to_html()

    return jsonify(predictions=results.to_dict(), plot_url=plot_url, results_html=results_html)

if __name__ == '__main__':
    app.run(debug=True)
