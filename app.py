from collections import namedtuple
from flask import Flask, request, render_template

from preprocess import preprocess
from predict import Predictor


class People:
    def _init_(self, INPUT_DATA):
        self.PassengerId = INPUT_DATAi["PassengerId"]
        self.Pclass = INPUT_DATA["Pclass"]
        self.Name = INPUT_DATA["Name"]
        self.Sex = INPUT_DATA["Sex"]
        self.Age = INPUT_DATA["Age"]
        self.SbSp = INPUT_DATA["SbSp"]
        self.Parch = INPUT_DATA["Parch"]
        self.Ticket = INPUT_DATA["Ticket"]
        self.Fare = INPUT_DATA["Fare"]
        self.Cabin = INPUT_DATA["Cabin"]
        self.Embarked = INPUT_DATA["Embarked"]

    @property #people クラスに入れたらいい？
    def status(self, INPUT_DTA):
        # INPUT_DATA is a dataframe
        PreprocessedData = Preprocsser.preprocess(INPUT_DATA)
        # preprocessed data is a dataframe
        status = Predictor.predict(PreprocessedData)
        return status


@app.route('/<title>')
def index(title):
    return render_template('templates/index.html', title=title)


@app.route('/survival_predict', method=['GET'])
def render_input_form():
    return render_template('upload.html')


@app.route('/survival_predict', method=['POST'])
def result():
    INPUT_DATA = {"PassengerId": request.form["Passengeer Id"],
                  "Pclass": request.form["Tciket class"],
                  "Name": request.form["Name"],
                  "Sex": request.form["Sex"],
                  "Age": request.form["Age"],
                  "SbSp": request.form["Number of siblings / spouses aboard the Titanic"],
                  "Parch": request.form["Number of parents / thildren abord the Titanic"],
                  "Ticket": request.form["Ticket number"],
                  "Fare": request.form["Passenger fare"],
                  "Cabin": request.form["Cabin number"],
                  "Embarked": request.form["Port of EMbarkation, \
                                           C=Cherbourg, \
                                           Q=Queenstown, \
                                           S=Southampton"]}
    INPUT_DATA = pd.DataFrame(INPUT_DATA)
    people = People(INPUT_DATA)
    return render_template('result.html',
                           status=People.status
                           )
