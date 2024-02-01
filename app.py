import json
import logging
import base64
import math
from io import BytesIO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nltk.lm import preprocessing

import news_api
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from flask import Flask, request, jsonify, render_template
# new
from matplotlib import style
from sklearn import preprocessing
import datetime
pd.options.mode.chained_assignment = None


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def read_and_clean_data(file):
    try:
        logger.info("Reading the data")
        data = pd.read_csv(file.stream, delimiter=';', decimal=',')
        mean_value = data['Umsatz'].mean()
        return data.fillna(mean_value)
    except Exception as e:
        logger.error(f"Error reading data: {e}")
        raise



def change_index_month(data):
    # Change "Monat" from string to int
    for idx in data.index:
        data.at[idx, "Monat"] = '{:02d}'.format(idx % 12 + 1)  # Format month as two-digit string

    # Generate "Datum" column, also set index to "Datum"
    data["Datum"] = data["Jahr"].astype(str) + "-" + data["Monat"].astype(str) + "-01"
    data.set_index("Datum", inplace=True)
    data.index = pd.to_datetime(data.index)
    print(data)
    return data


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
    print(predictions)
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

    # style.use("ggplot")

    return base64.b64encode(img.getvalue()).decode('utf8')


def plot_forecast(predictions, target_column_name, selected_columns):
    linear_prediction = predictions["Linear_Regression"]
    decision_prediction = predictions["Decision_Tree"]
    random_prediction = predictions["Random_Forest"]
    print("Linear prediction:\n", linear_prediction)
    print("Decision prediction:\n", decision_prediction)
    print("Random prediction:\n", random_prediction)
    print("target column:\n", selected_columns)

    style.use("ggplot")
    last_date = selected_columns.iloc[-1].name
    last_unix = last_date.timestamp()
    one_month = 86400 * 30
    next_unix = last_unix + one_month



    selected_columns["Linear Regression"] = np.nan
    selected_columns["Decision Tree Regression"] = np.nan
    selected_columns["Random Forest Regression"] = np.nan
    for i, j, k in zip(predictions["Linear_Regression"], predictions["Decision_Tree"], predictions["Random_Forest"]) :
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += 86400 * 30
        selected_columns.loc[next_date, "Linear Regression"] = i #[np.nan for _ in range(len(selected_columns.columns) - 1)] + [i]
        selected_columns.loc[next_date, "Decision Tree Regression"] = j
        selected_columns.loc[next_date, "Random Forest Regression"] = k

    # Initialise subplot
    figure, axis = plt.subplots(3,1, figsize=(8, 8))

    # Plot Linear Regression
    axis[0].plot(selected_columns[f"{target_column_name}"])
    axis[0].plot(selected_columns["Linear Regression"])
    axis[0].set_title("Linear Regression")

    # Plot Decision Tree Regression
    axis[1].plot(selected_columns[f"{target_column_name}"])
    axis[1].plot(selected_columns["Decision Tree Regression"])
    axis[1].set_title("Decision Tree Regression")

    # Plot Random Forest Regression
    axis[2].plot(selected_columns[f"{target_column_name}"])
    axis[2].plot(selected_columns["Random Forest Regression"])
    axis[2].set_title("Random Forest Regression")

    plt.xlabel("Datum")
    plt.ylabel(f"{target_column_name}")
    plt.tight_layout()
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')



def forecast(selected_cols, target_col):
    selected_cols.fillna(value=-99999, inplace=True)
    forecast_out = int(math.ceil(0.1 * len(selected_cols)))
    selected_cols["label"] = selected_cols[target_col].shift(-forecast_out)

    X = np.array(selected_cols.drop(["label"], axis=1))
    X = preprocessing.scale(X)
    X_lately = X[-forecast_out:]
    X = X[:-forecast_out]

    selected_cols.dropna(inplace=True)

    y = np.array(selected_cols["label"])

    # Train model/classifier
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    models = {
        'Linear_Regression': LinearRegression(),
        'Decision_Tree': DecisionTreeRegressor(),
        'Random_Forest': RandomForestRegressor()
    }

    for name, model in models.items():
        model.fit(X_train, y_train)
    predictions = {name: model.predict(X_lately) for name, model in models.items()}
    return predictions


def average_forecast(selected_cols, target_col_name):
    X1 = selected_cols
    pred_lin_result = pd.DataFrame()
    pred_dec_result = pd.DataFrame()
    pred_rf_result = pd.DataFrame()
    average_predictions = pd.DataFrame()

    for i in range(10):
        pred = forecast(X1.copy(), target_col_name)
        pred_df = pd.DataFrame(pred)

        pred_lin_result[f"Linear_Regression{i}"] = pred_df["Linear_Regression"]
        pred_dec_result[f"Decision_Tree{i}"] = pred_df["Decision_Tree"]
        pred_rf_result[f"Random_Forest{i}"] = pred_df["Random_Forest"]

        print(f"Pred{i}:\n", pred_df)

    pred_lin_result["Mean Linear Regression"] = pred_lin_result.mean(axis=1).round(decimals=2)
    pred_dec_result["Mean Decision Tree"] = pred_dec_result.mean(axis=1).round(decimals=2)
    pred_rf_result["Mean Random Forest"] = pred_rf_result.mean(axis=1).round(decimals=2)

    pred_lin_result = pred_lin_result["Mean Linear Regression"]
    pred_dec_result = pred_dec_result["Mean Decision Tree"]
    pred_rf_result = pred_rf_result["Mean Random Forest"]

    average_predictions["Linear_Regression"] = pred_lin_result
    average_predictions["Decision_Tree"] = pred_dec_result
    average_predictions["Random_Forest"] = pred_rf_result

    pred_lin_result.plot()
    pred_dec_result.plot()
    pred_rf_result.plot()
    plt.show()

    print("Result lin:\n", pred_lin_result)
    print("Result dec:\n", pred_dec_result)
    print("Result rf:\n", pred_rf_result)
    print("average:\n", average_predictions)

    return average_predictions





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
        cleaned_data = change_index_month(read_and_clean_data(file))
        logger.info(cleaned_data)
        target_column_name = request.form['target_column']

        selected_columns = request.form['selected_columns']
        logger.info(f"Selected columns: {selected_columns}")
        logger.info(f"Target column: {target_column_name}")

        logger.info(selected_columns)
        logger.info(f"Selected columns: {selected_columns}")
        selected_columns = json.loads(selected_columns)
        X = cleaned_data[selected_columns]
        X2 = cleaned_data[selected_columns]
        target_column = cleaned_data[target_column_name]

        average_predictions = average_forecast(X2, target_column_name)


        # New Output with improved graphic design
        predictions = forecast(X, target_column_name)
        predictions_df = pd.DataFrame(predictions)
        plot_url = plot_forecast(average_predictions, target_column_name, X)
        results_html = predictions_df.to_html()



        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        models = train_models(X_train, y_train)
        results = predict(models, X_test)
        plot_url = plot_results(results)
        results_html = results.to_html()
        """

        return jsonify(predictions=predictions_df.to_dict(), plot_url=plot_url,
                       results_html=results_html)

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify(error="Error in prediction"), 400


if __name__ == '__main__':
    app.run(debug=True)
