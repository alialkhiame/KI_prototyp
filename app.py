import json
import logging
import base64
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import news_api
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def read_and_clean_data(file):
    try:
        logger.info("Reading the data");
        data = pd.read_csv(file.stream)
        mean_value = data['Umsatz'].mean()
        return data.fillna(mean_value)
    except Exception as e:
        logger.error(f"Error reading data: {e}")
        raise


def train_models(X_train, y_train):
    models = {
        'Linear_Regression': LinearRegression(),
        'Decision_Tree': DecisionTreeRegressor(),
        'Random_Forest': RandomForestRegressor()
    }
    for name, model in models.items():
        model.fit(X_train, y_train)
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
    return render_template('index.html', sumValue=sumValue)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    try:
        file = request.files['file']
        cleaned_data = read_and_clean_data(file)
        logger.info(cleaned_data)
        return jsonify(columns=cleaned_data.columns.tolist())
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.route('/predict', methods=['POST'])
def predict_route():
    try:
        if 'file' not in request.files:
            return jsonify(error="No file part"), 400

        file = request.files['file']
        cleaned_data = read_and_clean_data(file)
        logger.info(cleaned_data)
        target_column = request.form['target_column']

        selected_columns = request.form['selected_columns']
        logger.info(f"Selected columns: {selected_columns}")
        logger.info(f"Target column: {target_column}")

        logger.info(selected_columns)
        logger.info(f"Selected columns: {selected_columns}")
        selected_columns = json.loads(selected_columns)
        X = cleaned_data[selected_columns]
        y = cleaned_data[target_column]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        models = train_models(X_train, y_train)
        results = predict(models, X_test)
        plot_url = plot_results(results)
        results_html = results.to_html()

        return jsonify(predictions=results.to_dict(), plot_url=plot_url, results_html=results_html)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify(error="Error in prediction"), 400


if __name__ == '__main__':
    app.run(debug=True)
