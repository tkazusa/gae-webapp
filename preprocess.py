import pandas as pd
import re

from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.externals import joblib


def preprocess(data):
    """Preprocess input data from form for the model
    Args:
       data: pandas DataFrame
    Returns:
       PreprocecssedData: pandas DataFrame
    """
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

    data = data.dropna(how="any")
    data = data.astype({"Pclass": int, "Age": int, "SibSp": int, "Parch": int})

    data["title"] = data.Name.apply(deriveTitles)

    # and encode these new titles for later
    le = preprocessing.LabelEncoder()
    titles = ['adult', 'gentry', 'miss', 'military', 'other', 'child']
    le.fit(titles)

    data.Embarked.fillna(value="S", inplace=True)
    data['encodedTitle'] = le.transform(data['title']).astype('int')
    data = data.assign(SibSpGroup1=data['SibSp'] < 2)
    data = data.assign(SibSpGroup2=data['SibSp'].between(2, 3, inclusive=True))
    data = data.assign(SibSpGroup3=data['SibSp'] > 2)
    data = data.assign(ParChGT2=data['Parch'] > 2)
    data = data.assign(familySize=data['Parch'] + data['SibSp'])
    data = data.assign(children=data.apply(lambda row: deriveChildren(row['Age'], row['Parch']), axis = 1))
    data['parents'] = data.apply(lambda row: deriveParents(row['Age'], row['Parch']), axis = 1)
    data['responsibleFor'] = data.apply(lambda row: deriveResponsibleFor(row['children'], row['SibSp']), axis = 1)
    # data['accompaniedBy'] = data.apply(lambda row: deriveAccompaniedBy(row['parents'], row['SibSp']), axis = 1)
    data['unaccompaniedChild'] = data.apply(lambda row: unaccompaniedChild(row['Age'], row['Parch']), axis = 1)

    # drop unused columns
    print(data.columns)
    data = data.drop(['Name', 'Cabin', 'Parch', 'SibSp', 'title', 'Ticket'], axis=1)

    # label encode string features
    categorical_names = {}
    categorical_features = ['Embarked', 'Sex']
    for feature in categorical_features:
        le = preprocessing.LabelEncoder()
        le.fit(data[feature])
        data[feature] = le.transform(data[feature])
        categorical_names[feature] = le.classes_

    data['title'] = data['encodedTitle'].astype(int, copy=False)
    data['class'] = data['Pclass'].astype(int, copy=False)
    data = data.drop(['Pclass'], axis=1)
    data = data.drop(['encodedTitle'], axis=1)
 
    if 'Survived' in data.columns:
        data['Survived'] = data['Survived'].astype(int, copy=False)
        return data.drop(['Survived'], axis=1), data['Survived']
    else:
        return data
