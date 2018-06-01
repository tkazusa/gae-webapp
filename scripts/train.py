import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

PREPROCESSED_PATH = "data/preprocessed.csv"
if __name__ == "__main__":
    train = pd.read_csv(PREPROCESSED_PATH)
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(train[['title',
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
                  'accompaniedBy',
                  'unaccompaniedChild']], train['Survived'])

    joblib.dump(rf, "rf.pkl")
