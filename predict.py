import numpy as np
from sklearn.externals import joblib
from configs.settings import MODEL_PATH


class Predictor(object):
    """推定をおこなうクラス"""
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self, data):
        print(data.columns)
        print(data.head())
        return self.model.predict(data)
