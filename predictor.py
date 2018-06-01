import numpy as np
from sklearn.externals import joblib
from settings import MODEL_PATH

class Predictor:
    """推定をおこなうクラス"""
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self):
        return self.model.predict(data)
