from collections import namedtuple

import pandas as pd
from flask import Flask, request, render_template

from preprocess import preprocess
from predict import Predictor
app = Flask(__name__)

class People:
    def __init__(self, INPUT_DATA):
        self.DATA = INPUT_DATA

    def status(self):
        # INPUT_DATA is a dataframe
        PreprocessedData = preprocess(self.DATA)
        # preprocessed data is a dataframe
        model = Predictor()
        status = model.predict(PreprocessedData)
        return status


@app.route('/<title>')
def index(title):
    return render_template('index.html', title=title)


@app.route('/survival_predict', methods=['GET'])
def render_input_form():
    return render_template('index.html')


@app.route('/survival_predict', methods=['POST'])
def result():
    INPUT_DATA = pd.DataFrame({
        "Pclass": [request.form["pclass"]],
        "Name": [request.form["name"]],
        "Ticket": [request.form["ticket"]],
        "Sex": [request.form["sex"]],
        "Age": [request.form["age"]],
        "SibSp": [request.form["Sibsp"]],
        "Parch": [request.form["parch"]],
        "Cabin": [request.form["cabin"]],
        "Embarked": [request.form["embarked"]]})

    people = People(INPUT_DATA)
    status = people.status()
    if status == 1:
        status = "dead"
    else: status = "alive"
    return render_template('result.html', status=status)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=3000)
