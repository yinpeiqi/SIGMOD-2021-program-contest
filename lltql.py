import pandas as pd

website2id = {}
true_table = []

def generate(data, name):
    array = data.values.tolist()
    columns = data.columns.tolist()

    result = []
    length = len(array)
    for i in range(length):
        for j in range(i, length):
            temp = []
            temp.append(true_table[website2id[array[i][0]]][website2id[array[j][0]]])
            for t in range(len(array[i])):
                temp.append(array[i][t])
                temp.append(array[j][t])
            result.append(temp)

    df = pd.DataFrame(result)
    df.rename(columns={0: 'label'}, inplace=True)
    col_len = len(columns)
    for i in range(col_len):
        df.rename(columns={((i+1)*2-1): 'left_'+columns[i], ((i+1)*2): 'right_'+columns[i]}, inplace=True)
    df = df.drop(['right_instance_id', 'left_instance_id'], axis=1)
    df = df.fillna('')
    df.index.name = 'id'

    df.to_csv(name+".csv", sep=',', encoding='utf-8')


if __name__ == '__main__':
    Xdata = pd.read_csv('./test/cleanX2.csv')
    Ydata = pd.read_csv('./data/Y2.csv')

    Xarray = Xdata.sample(frac=1).values.tolist()

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


    train_data = Xdata.sample(frac=0.8, axis=0)
    test_data = Xdata[~Xdata.index.isin(train_data.index)]

    generate(train_data, 'train')
    generate(test_data, 'test')