import json

from flask import Flask, request, render_template, jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import io
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']

    try:
        data = pd.read_csv(file.stream)
        mean_value = data['Umsatz'].mean()
        cleaned_data = data.fillna(mean_value)

    except Exception as e:
        return jsonify(error=str(e)), 400

    return jsonify(columns=cleaned_data.columns.tolist())


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

        # Plotting
        plt.figure()
        plt.scatter(X_test.iloc[:, 0], y_test)
        plt.plot(X_test.iloc[:, 0], predictions, color='red')
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return jsonify(predictions=predictions.tolist(), plot_url=plot_url)
    except Exception as e:
        return jsonify(error=str(e)), 400


if __name__ == '__main__':
    print("KI_")
    app.run(debug=True)
