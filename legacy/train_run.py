import math

from joblib import load, dump
import pandas as pd
import re
import numpy
from sklearn import metrics
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import VotingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier, PassiveAggressiveClassifier
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.naive_bayes import ComplementNB
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline

RUNNING = 0
TESTING = 1
GENERATE = 2
STATE = TESTING
Flag = True




def transform(Xdata, website2id, id2website):
    array = Xdata.values.tolist()
    columns = Xdata.columns.tolist()

    tot_id = 0
    for line in array:
        tot_id += 1
        website2id[line[0]] = tot_id
        id2website[tot_id] = line[0]

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
    return X, website2id, id2website


def train(Xdata, website2id, id2website, file_name):
    global Flag
    data = pd.read_csv('train'+file_name)
    data = data.drop(['id'], axis=1).values.tolist()
    X, y = [], []
    for line in data:
        X.append(line[3] + '  --------------  ' + line[4])
        y.append(line[0])
        X.append(line[4] + '  --------------  ' + line[3])
        y.append(line[0])
    text_clf = Pipeline([
        ('tfidf', TfidfVectorizer(lowercase=False, max_df=1, ngram_range=(1, 1), sublinear_tf=True)),
        ('clf3', PassiveAggressiveClassifier(C=1, loss="hinge"))])
    model = text_clf.fit(X, y)

    temp = Xdata
    Xdata = []
    titles = []
    for line in temp:
        Xdata.append([line[0], line[1]])
        titles.append(line[2] + '  --------------  ' + line[3])
    predicted = model.predict(titles)
    result = []
    print(len(Xdata))
    print(predicted)
    t = 0
    for i, j in zip(Xdata, predicted):
        temp = []
        temp.append(id2website[i[0]])
        temp.append(id2website[i[1]])
        temp.append(j)
        if j == 1:
            t += 1
        result.append(temp)
    lab1, lab0 = [], []
    for mes in result:
        if mes[2] == 1:
            lab1.append(mes)
        else:
            lab0.append(mes)
    result = []
    result.extend(lab1)
    result.extend(lab0)
    print(t)
    df = pd.DataFrame(result)
    df.rename(columns={0: 'left_instance_id', 1: 'right_instance_id', 2: 'label'}, inplace=True)

    if Flag:
        df.to_csv("output.csv", sep=',', encoding='utf-8', index=False)
        Flag = False
    else:
        df.to_csv("output.csv", mode='a', sep=',', encoding='utf-8', index=False, header=None)




if __name__ == '__main__':
    STATE = RUNNING

    if STATE == RUNNING:
        for read_file in ['X4.csv','X3.csv','X2.csv']:
            website2id = {}
            id2website = {}
            Xdata = pd.read_csv(read_file)
            if 'name' not in Xdata.columns:
                if 'source' not in Xdata.filter(['instance_id']).sample(1).values[0][0]:
                    file_name = '../X2.csv'
                else:
                    file_name = '../X3.csv'
            else:
                file_name  = '../X4.csv'

            Xarray = Xdata.sample(frac=1).values.tolist()
            Xtemp = []
            for line in Xarray:
                temp = []
                if file_name == 'X4.csv':
                    temp.append(line[-1])
                    mess = line[0]
                else:
                    temp.append(line[0])
                    mess = line[-1]
                for i in range(1, len(line) - 1):
                    if line[i] is not None and (type(line[i]) != float or not math.isnan(line[i])) and str(
                            line[i]) not in mess:
                        mess = mess + ' - ' + str(line[i])
                temp.append(mess)
                Xtemp.append(temp)
            Xarray = Xtemp
            Xdata = pd.DataFrame(Xarray)
            Xdata.rename(columns={0: 'instance_id', 1: 'title'}, inplace=True)
            Xdata, website2id, id2website = transform(Xdata, website2id, id2website)
            train(Xdata, website2id, id2website, file_name)
