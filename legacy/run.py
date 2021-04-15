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
dataset = '2'
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


def train(Xdata, website2id, id2website, dataset):
    global Flag
    model = load('model_'+str(dataset)+'.pkl')
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
        for file_name in ['X4.csv','X3.csv','X2.csv']:
            if file_name == 'X4.csv':
                dataset = '4'
            elif file_name == 'X3.csv':
                dataset = '3'
            else:
                dataset = '2'
            website2id = {}
            id2website = {}
            Xdata = pd.read_csv(file_name)
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
            train(Xdata, website2id, id2website, dataset)
