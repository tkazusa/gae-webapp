import pandas as pd
import re

from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.externals import joblib

PATH = "data/titanic.csv"

def deriveTitles(s):
    title = re.search('(?:\S )(?P<title>\w*)', s).group('title')

    if title == "Mr":             return "adult"
    elif title == "Don":          return "gentry"
    elif title == "Dona":         return "gentry"
    elif title == "Miss":         return "miss" # we don't know whether miss is an adult or a child
    elif title == "Col":          return "military"
    elif title == "Rev":          return "other"
    elif title == "Lady":         return "gentry"
    elif title == "Master":       return "child"
    elif title == "Mme":          return "adult"
    elif title == "Captain":      return "military"
    elif title == "Dr":           return "other"
    elif title == "Mrs":          return "adult"
    elif title == "Sir":          return "gentry"
    elif title == "Jonkheer":     return "gentry"
    elif title == "Mlle":         return "miss"
    elif title == "Major":        return "military"
    elif title == "Ms":           return "miss"
    elif title == "the Countess": return "gentry"
    else:                         return "other"


def deriveChildren(age, parch):
    if(age < 18):
        return parch
    else:
        return 0


def deriveParents(age, parch):
    if(age > 17):
        return parch
    else:
        return 0


def deriveResponsibleFor(children, SibSp):
    if(children > 0):
        return children / (SibSp + 1)
    else:
        return 0


def unaccompaniedChild(age, parch):
    if((age < 16) & (parch == 0)):
        return True
    else:
        return False


if __name__ == "__main__":
    train = pd.read_csv(PATH)
    train["title"] = train.Name.apply(deriveTitles)

    # and encode these new titles for later
    le = preprocessing.LabelEncoder()
    titles = ['adult', 'gentry', 'miss', 'military', 'other', 'child']
    le.fit(titles)

    train.Embarked.fillna(value="S", inplace=True)
    train['encodedTitle'] = le.transform(train['title']).astype('int')
    train = train.assign(SibSpGroup1=train['SibSp'] < 2)
    train = train.assign(SibSpGroup2=train['SibSp'].between(2, 3, inclusive=True))
    train = train.assign(SibSpGroup3=train['SibSp'] > 2)
    train = train.assign(ParChGT2=train['Parch'] > 2)
    train = train.assign(familySize=train['Parch'] + train['SibSp'])
    train = train.assign(children=train.apply(lambda row: deriveChildren(row['Age'], row['Parch']), axis = 1))
    train['parents'] = train.apply(lambda row: deriveParents(row['Age'], row['Parch']), axis = 1)
    train['responsibleFor'] = train.apply(lambda row: deriveResponsibleFor(row['children'], row['SibSp']), axis = 1)
    train['accompaniedBy'] = train.apply(lambda row: deriveAccompaniedBy(row['parents'], row['SibSp']), axis = 1)
    train['unaccompaniedChild'] = train.apply(lambda row: unaccompaniedChild(row['Age'], row['Parch']), axis = 1)

    # drop unused columns
    train = train.drop(['Name', 'Cabin', 'Fare', 'Parch', 'SibSp', 'Ticket', 'title'], axis=1)

    # label encode string features
    categorical_names = {}
    categorical_features = ['Embarked', 'Sex']
    for feature in categorical_features:
        le = preprocessing.LabelEncoder()
        le.fit(train[feature])
        train[feature] = le.transform(train[feature])
        categorical_names[feature] = le.classes_

    train['title'] = train['encodedTitle'].astype(int, copy=False)
    train['class'] = train['Pclass'].astype(int, copy=False)
    train = train.drop(['Pclass'], axis=1)
    train = train.drop(['encodedTitle'], axis=1)
    train['Survived'] = train['Survived'].astype(int, copy=False)

    train.to_csv("data/preprocessed.csv")

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
