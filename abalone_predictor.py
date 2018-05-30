import numpy as np
from sklearn.externals import joblib

from settings import (
    Y_TRAIN_PREDICTION_PATH,
    MODEL_PATH,
)


class AbalonePredictor:
    """アワビの年齢推定をおこなうクラス"""
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

        # 本章の後半で利用します
        tp = np.load(Y_TRAIN_PREDICTION_PATH)
        self.y_train = tp[0]
        self.prediction = tp[1]

    def predict(self, input_sex,
                length, diameter, height, weight):
        """アワビの推定年齢を返す"""
        # 4章と同じ方法で年齢推定を行う
        if input_sex == 0:
            sex = [1, 0, 0]
        elif input_sex == 2:
            sex = [0, 0, 1]
        else:
            sex = [0, 1, 0]
        # 元データに合わせて連続値は200で除算する
        target = np.array(
            sex + [length/200, diameter/200,
                   height/200, weight/200])
        return self.model.predict(
           target.reshape(1, -1))
