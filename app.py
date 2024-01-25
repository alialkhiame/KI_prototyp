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
from nero import nero
import logging
import cleanData
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

krieg = 0


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
   # sumValue = news_api.get_sum()
   # krieg = sumValue
    sumValue=2
    return render_template('index.html', sumValue=sumValue)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    try:
        file = request.files['file']
        data_cleaner = cleanData.CleanData(file)
        cleaned_data = data_cleaner.cleaned_data
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
        data_cleaner = cleanData.CleanData(file)
        cleaned_data = data_cleaner.cleaned_data
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
       # callNero(x_train, y_train, x_test)
        models = train_models(x_train, y_train)
        results = predict(models, x_test)
        plot_url = plot_results(results)
        results_html = results.to_html()
        logging.info(results)

        return jsonify(predictions=results.to_dict(), plot_url=plot_url, results_html=results_html)
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return jsonify(error="Error in prediction"), 400


def callNero(X_train, y_train, X_test):
    umsatz_model = nero()
    umsatz_model.train_model(X_train, y_train)
    predictions = umsatz_model.predict(X_test)
    print(predictions)
    return predictions


if __name__ == '__main__':
    app.run(debug=True)
