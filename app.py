import json
import logging

from flask import Flask, request, render_template, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import io
import matplotlib.pyplot as plt
import base64
from io import BytesIO

from sklearn.tree import DecisionTreeRegressor

import news_api

app = Flask(__name__)
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger
logger = logging.getLogger(__name__)

@app.route('/')
def index():

    # Call to newsApi script to get sumValue
    sumValue = news_api.get_sum()

    return render_template('index.html', sumValue=sumValue)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']
    # logger.info("file")
    # logger.info(file)
    try:
        data = pd.read_csv(io.StringIO(file.stream.read().decode('UTF-8')))
        mean_value = data['Umsatz'].mean()
        cleaned_data = data.fillna(mean_value)
        # logger.info("Clean Data")
        # logger.info(cleaned_data)
    except Exception as e:
        return jsonify(error=str(e)), 400

    cleaned_json = cleaned_data.head().to_json(orient='records')
    columns = cleaned_data.columns.tolist()

    return jsonify(columns=columns, data=json.loads(cleaned_json))


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = pd.read_csv(request.files['data'])
        selected_columns = request.form['selected_columns']
        target_column = request.form['target_column']

        mean_value = data['Umsatz'].mean()
        cleaned_data = data.fillna(mean_value)

        # Convert JSON string back to list
        selected_columns = json.loads(selected_columns)
        print(selected_columns)
        # Validate data
        if not all(str(column) in map(str, cleaned_data.columns) for column in selected_columns + [target_column]):
            print(cleaned_data.columns)
            return jsonify(error="Some columns are missing"), 400

        X = cleaned_data[selected_columns]
        y = cleaned_data[target_column]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = LinearRegression()
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        # Linear Regression
        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)
        lr_predictions = lr_model.predict(X_test)

        # Decision Tree Regressor
        dt_model = DecisionTreeRegressor()
        dt_model.fit(X_train, y_train)
        dt_predictions = dt_model.predict(X_test)

        # Random Forest Regressor
        rf_model = RandomForestRegressor()
        rf_model.fit(X_train, y_train)
        rf_predictions = rf_model.predict(X_test)

        # Preparing the results
        results = pd.DataFrame({
            'Linear_Regression': lr_predictions,
            'Decision_Tree': dt_predictions,
            'Random_Forest': rf_predictions
        })

        # Plotting the results

        results.plot(kind='bar')
        plt.title('Model Predictions')
        plt.xlabel('Data Points')
        plt.ylabel('Predicted Values')
        plt.tight_layout()

        # Saving plot to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        # Encoding the image in base64
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        logger.info("plot_url")
        logger.info(plot_url)




        # Converting DataFrame to HTML table
        results_html = results.to_html()
        plot_url = base64.b64encode(img.getvalue()).decode()
        return jsonify(predictions=dt_predictions.tolist(), plot_url=plot_url)

    except Exception as e:
        return jsonify(error=str("nothing changing")), 400






if __name__ == '__main__':
    print("KI_")
    app.run(debug=True, port=8080)
