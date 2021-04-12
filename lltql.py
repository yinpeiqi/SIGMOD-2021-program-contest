import math

import pandas as pd

website2id = {}
true_table = []

def generate(data, name):
    array = data.values.tolist()
    columns = data.columns.tolist()

    result = []
    length = len(array)
    for i in range(length):
        for j in range(i+1, length):
            temp = []
            temp.append(true_table[website2id[array[i][0]]][website2id[array[j][0]]])
            for t in range(1, len(array[i])):
                temp.append(array[i][t])
                temp.append(array[j][t])
            result.append(temp)

    df = pd.DataFrame(result)
    df.rename(columns={0: 'label'}, inplace=True)
    # col_len = len(columns)
    # for i in range(col_len):
    #     df.rename(columns={((i+1)*2+1): 'left_'+columns[i], ((i+1)*2): 'right_'+columns[i]}, inplace=True)
    df.rename(columns={1: 'left_title', 2: 'right_title'}, inplace=True)
    df.index.name = 'id'
    df.to_csv(name+".csv", sep=',', encoding='utf-8')


if __name__ == '__main__':
    dataset = '4'
    Xdata = pd.read_csv('X' + dataset + '.csv')
    Xarray = Xdata.sample(frac=1).values.tolist()
    Xtemp = []
    for line in Xarray:
        temp = []
        temp.append(line[-1])
        mess = line[0]
        for i in range(1, len(line)-1):
            if line[i] is not None and (type(line[i]) != float or not math.isnan(line[i])) and str(line[i]) not in mess:
                mess = mess + ' - ' + str(line[i])
        temp.append(mess)
        Xtemp.append(temp)
    Xarray = Xtemp
    Xdata = pd.DataFrame(Xarray)
    Xdata.rename(columns={0: 'instance_id', 1: 'title'}, inplace=True)
    # if dataset == '4':
    #     Xdata = Xdata.filter(['instance_id', 'name'], axis=1)
    # else:
    #     Xdata = Xdata.filter(['instance_id', 'title'], axis=1)
    Ydata = pd.read_csv('Y' + dataset + '.csv')

    print(Xdata)
    tot_id = 0
    for line in Xarray:
        tot_id += 1
        website2id[line[0]] = tot_id

    Yarray = Ydata.values.tolist()
    for i in range(tot_id+1):
        true_table.append([])
        for j in range(tot_id+1):
            true_table[i].append(0)
        true_table[i][i] = 1

    for line in Yarray:
        lwebsite, rwebsite, label = line
        lid, rid, label = website2id[lwebsite], website2id[rwebsite], int(label)
        true_table[lid][rid] = label
        true_table[rid][lid] = label


    train_data = Xdata.sample(frac=1, axis=0)
    # test_data = Xdata[~Xdata.index.isin(train_data.index)]

    generate(train_data, 'train' + dataset)
    # generate(test_data, 'test' + dataset)