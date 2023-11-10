from flask import Flask, render_template, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # You can choose any other algorithm from scikit-learn

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    # Read CSV file into a Pandas DataFrame
    df = pd.read_csv(file)

    # Assume the last column is the target variable (goal)
    goal_column = df.columns[-1]

    # Separate features and target variable
    X = df.drop(goal_column, axis=1)
    y = df[goal_column]

    # User-selected algorithm (Random Forest as an example)
    clf = RandomForestClassifier()

    # Train the model
    clf.fit(X, y)

    # Make predictions
    predictions = clf.predict(X)  # You may want to use new data for predictions

    # Pass the predictions to the template
    return render_template('result.html', predictions=predictions)

if __name__ == '__main__':
    app.run(debug=True)
