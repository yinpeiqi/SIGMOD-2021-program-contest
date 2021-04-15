import math

import argparse
import time

import pandas
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.pipeline import Pipeline

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--training_data_file', type=str, default='train.json')
    args = parser.parse_args()

    # data = pandas.read_csv('train2.csv')
    # data = data.drop(['id'], axis=1).values.tolist()
    X, y = [], []
    # for line in data:
    #     X.append(line[3]+'  --------------  '+line[4])
    #     y.append(line[0])
    #     X.append(line[4]+'  --------------  '+line[3])
    #     y.append(line[0])
    # data = pandas.read_csv('train3.csv')
    # data = data.drop(['id'], axis=1).values.tolist()
    # for line in data:
    #     X.append(line[3]+'  --------------  '+line[4])
    #     y.append(line[0])
    #     X.append(line[4]+'  --------------  '+line[3])
    #     y.append(line[0])
    data = pandas.read_csv('../train4.csv')
    data = data.drop(['id'], axis=1).values.tolist()
    for line in data:
        X.append(line[3]+'  --------------  '+line[4])
        y.append(line[0])
        X.append(line[4]+'  --------------  '+line[3])
        y.append(line[0])
    tq = time.time()
    text_clf = Pipeline([
        ('tfidf', TfidfVectorizer(lowercase=True, max_df=0.375, ngram_range=(1, 2), sublinear_tf=True)),
        ('clf3', PassiveAggressiveClassifier(C=1.5,loss="hinge", max_iter=2000))])
    model = text_clf.fit(X, y)
    y_pred = text_clf.predict(X)
    f1 = metrics.f1_score(y_pred, y)
    print(y_pred)
    tt, rr = 0, 0
    for t in y_pred:
        if t == 1:
            tt += 1
        else:
            rr += 1
    print(tt, rr)
    print('f_score=', f1, "time=", time.time()-tq)

    Flag = True
    for read_file in ['X4.csv', 'X3.csv', 'X2.csv']:
        website2id = {}
        id2website = {}
        Xdata = pandas.read_csv(read_file)

        ids = Xdata.filter(['instance_id'], axis=1).values.tolist()
        Xarray = Xdata.drop(['instance_id'], axis=1).sample(frac=1).values.tolist()
        Xtemp = []
        for line, id in zip(Xarray, ids):
            temp = []
            temp.append(id)
            mess = ''
            for i in range(0, len(line)):
                if line[i] is not None and (type(line[i]) != float or not math.isnan(line[i])) and str(
                        line[i]) not in mess:
                    mess = mess + ' - ' + str(line[i])
            temp.append(mess)
            Xtemp.append(temp)
        Xarray = Xtemp

        length = len(Xarray)
        id_data = []
        titles = []
        for i in range(length):
            for j in range(i + 1, length):
                id_data.append([Xarray[i][0], Xarray[j][0]])
                titles.append(Xarray[i][1]+'  --------------  '+Xarray[j][1])
        predicted = model.predict(titles)
        result = []
        print(predicted)
        t = 0
        for i, j in zip(id_data, predicted):
            if j == 1:
                temp = []
                temp.append(i[0])
                temp.append(i[1])
                result.append(temp)
                t += 1
        print(t)
        df = pandas.DataFrame(result)
        df.rename(columns={0: 'left_instance_id', 1: 'right_instance_id'}, inplace=True)
        if Flag:
            df.to_csv("output.csv", sep=',', encoding='utf-8', index=False)
            Flag = False
        else:
            df.to_csv("output.csv", mode='a', sep=',', encoding='utf-8', index=False, header=None)
