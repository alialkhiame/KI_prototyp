from flask import Flask, request, render_template, jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression
import io
import matplotlib.pyplot as plt
import base64
from io import BytesIO
# Load default data
from flask import Flask
# Import your dataGen class
from dataGen import dataGen

app = Flask(__name__)



app = Flask(__name__)

# Create an instance of the dataGen class
data_generator = dataGen()

# Use the generate_data method to initialize default_data
default_data = data_generator.generate_data()

# ... rest of your Flask app code ...


@app.route('/')
def index():
    return render_template('index.html')  # HTML file with upload and selection options

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        data = pd.read_csv(file.stream)
    else:
        data = default_data

    # Send column names to frontend for variable selection
    return jsonify(columns=data.columns.tolist())

@app.route('/predict', methods=['POST'])
def predict():
    data = pd.read_csv(io.StringIO(request.form['data']))
    selected_columns = request.form.getlist('selected_columns')
    X = data[selected_columns]
    y = data['target_column']  # Define your target column

    model = LinearRegression()
    model.fit(X, y)

    # Predictions and plotting
    predictions = model.predict(X)
    plt.figure()
    plt.plot(data['some_time_column'], predictions)  # Modify as needed
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return jsonify(predictions=predictions.tolist(), plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
