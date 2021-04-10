from joblib import load, dump
import pandas as pd
import re
import numpy
from sklearn import metrics
from sklearn.svm import *
from sklearn.linear_model import *
from sklearn.tree import *
from clean_x2 import clean_X2
from clean_x3 import  clean_X3

RUNING = 0
TESTING = 1
GENERATE = 2
STATE = TESTING


website2id = {}
id2webstie = {}


def transform(Xdata):
    array = Xdata.values.tolist()
    columns = Xdata.columns.tolist()

    tot_id = 0
    for line in array:
        tot_id += 1
        website2id[line[0]] = tot_id
        id2webstie[tot_id] = line[0]

    result = []
    length = len(array)
    for i in range(length):
        for j in range(i + 1, length):
            temp = []
            temp.append(website2id[array[i][0]])
            temp.append(website2id[array[j][0]])
            for t in range(1, len(array[i])):
                temp.append(array[i][t])
                temp.append(array[j][t])
            result.append(temp)

    df = pd.DataFrame(result)
    col_len = len(columns)
    for i in range(col_len):
        df.rename(columns={(i * 2): 'left_' + columns[i], (i * 2 + 1): 'right_' + columns[i]}, inplace=True)
    df.index.name = 'id'
    X = df.reset_index().drop(['id'], axis=1).values.tolist()
    return X


true_table = []
def generate(data):
    array = data.values.tolist()
    columns = data.columns.tolist()

    result = []
    length = len(array)
    for i in range(length):
        for j in range(i + 1, length):
            temp = []
            temp.append(true_table[website2id[array[i][0]]][website2id[array[j][0]]])
            temp.append(website2id[array[i][0]])
            temp.append(website2id[array[j][0]])
            for t in range(1, len(array[i])):
                temp.append(array[i][t])
                temp.append(array[j][t])
            result.append(temp)

    df = pd.DataFrame(result)
    df.rename(columns={0: 'label'}, inplace=True)
    col_len = len(columns)
    for i in range(col_len):
        df.rename(columns={((i + 1) * 2 - 1): 'left_' + columns[i], ((i + 1) * 2): 'right_' + columns[i]}, inplace=True)
    return df


def generate_model(Xdata, dataset):
    Ydata = pd.read_csv('Y' + dataset + '.csv')

    Xarray = Xdata.sample(frac=1).values.tolist()

    tot_id = 0
    for line in Xarray:
        tot_id += 1
        website2id[line[0]] = tot_id

    Yarray = Ydata.values.tolist()
    for i in range(tot_id + 1):
        true_table.append([])
        for j in range(tot_id + 1):
            true_table[i].append(0)
        true_table[i][i] = 1

    for line in Yarray:
        lwebsite, rwebsite, label = line
        lid, rid, label = website2id[lwebsite], website2id[rwebsite], int(label)
        true_table[lid][rid] = label
        true_table[rid][lid] = label

    if STATE == TESTING:
        train_data = Xdata.sample(frac=0.7, axis=0)
        test_data = Xdata[~Xdata.index.isin(train_data.index)]

        train_data = generate(train_data)
        test_data = generate(test_data)
        return train_data, test_data

    elif STATE == GENERATE:
        train_data = Xdata.sample(frac=1, axis=0)
        train_data = generate(train_data)
        return train_data


def train(Xdata):
    model = load('model.pkl')
    predicted = model.predict(Xdata)
    result = []
    for i, j in zip(Xdata, predicted):
        temp = []
        temp.append(id2webstie[i[0]])
        temp.append(id2webstie[i[1]])
        temp.append(j)
        result.append(temp)

    df = pd.DataFrame(result)
    df.rename(columns={0: 'left_instance_id', 1: 'right_instance_id', 2: 'label'}, inplace=True)

    df.to_csv("output.csv", sep=',', encoding='utf-8', index=False)


def test_train(train_data, test_data=None):
    def handle(data):
        X = data.drop(['label'], axis=1).values.tolist()
        y = data.filter(['label'], axis=1).values.tolist()
        for i in range(len(y)):
            y[i] = y[i][0]
        return X, y

    X_train, y_train = handle(train_data)
    model = DecisionTreeClassifier()
    text_clf = model.fit(X_train, y_train)

    if test_data is not None:
        X_test, y_test = handle(test_data)
        y_pred = text_clf.predict(X_test)
        f1 = metrics.f1_score(y_pred, y_test)
        print(f1)
    else:
        dump(text_clf, 'model.pkl')


if __name__ == '__main__':
    STATE = TESTING
    dataset = '3'


    file_name = 'X'+ dataset + '.csv'
    Xdata = pd.read_csv(file_name)
    if 'name' not in Xdata.columns:
        if 'source' not in Xdata.filter(['instance_id']).sample(1).values[0][0]:
            Xdata = clean_X2(Xdata, file_name)
        else:
            Xdata = clean_X3(Xdata, file_name)
    # else:
    #     Xdata = clean_X4(Xdata, file_name)

    if STATE == RUNING:
        Xdata = transform(Xdata)
        train(Xdata)

    elif STATE == TESTING:
        Xdata.to_csv("./test/clean"+file_name, sep=',', index=False)
        train_data, test_data = generate_model(Xdata, dataset)
        test_train(train_data, test_data)

    elif STATE == GENERATE:
        train_data = generate_model(Xdata, dataset)
        test_train(train_data)
