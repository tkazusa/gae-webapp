from collections import namedtuple
from flask import Flask, request render_template
debug(True)

from preprocess import Preprocesser
from predict import Predictor


class People:
    def _init_(self, INPUT_DATA):
        self.XX = INPUT_DATA[]
        self.XX = INPUT_DATA[]

    @property "people クラスに入れたらいい？"
    def status(self, INPUT_DTA):
        PreprocessedData = Preprocsser.preprocess(INPUT_DATA)
        status = Predictor.predict(PreprocessedData)
        return status


@app.route('/')
def index():
    return render_template('templates/index.html')


@app.route('/survival_predict', method=['GET'])
def render_input_form():
    return render_template('upload.html')


@app.route('/survival_predict', method=['POST'])
def result():
    INPUT_DATA = pd.DataFrame()
    INPUT_DATA['AA'] = request.form['AA']
    INPUT_DATA['AA'] = request.form['AA']
    INPUT_DATA['AA'] = request.form['AA']
    INPUT_DATA['AA'] = request.form['AA']
    INPUT_DATA['AA'] = request.form['AA']
    people = People(INPUT_DATA)
    return render_template('result.html',
                           aa=request.form['AA'],
                           aa=request.form['AA'],
                           aa=request.form['AA'],
                           aa=request.form['AA'],
                           status=People.status
                           )
