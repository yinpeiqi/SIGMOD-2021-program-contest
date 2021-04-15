import pandas
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from joblib import dump, load
import numpy

def read(file_name):

    data = pandas.read_csv(file_name)
    X = data.drop(['label', 'id'], axis=1).values.tolist()
    y = data.filter(['label'], axis=1).values.tolist()
    for i in range(len(y)):
        y[i] = y[i][0]
    return X, y

if __name__ == '__main__':
    X_train, y_train = read('train.csv')
    X_test, y_test = read('test.csv')
    model = SVC()
    text_clf = model.fit(X_train, y_train)
    # dump(text_clf, 'model.pkl')
    predicted = text_clf.predict(X_test)
    rate = numpy.mean(predicted == y_test)
    print(rate)