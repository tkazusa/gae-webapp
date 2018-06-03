import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

from preprocess import preprocess

DATA_PATH = "data/titanic.csv"

if __name__ == "__main__":
    TRAIN_DATA = pd.read_csv(DATA_PATH)
    PreprocessedData = preprocess(TRAIN_DATA)
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(PreprocessedData[['title',
                       'Embarked',
                       'class',
                       'Sex',
                       'SibSpGroup1',
                       'SibSpGroup2',
                       'SibSpGroup3',
                       'familySize',
                       'children',
                       'parents',
                       'responsibleFor',
                       # 'accompaniedBy',
                       'unaccompaniedChild']], PreprocessedData['Survived'])

    joblib.dump(rf, "rf.pkl")
