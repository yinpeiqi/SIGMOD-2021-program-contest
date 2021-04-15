import pandas as pd
from handler_x2 import handle_x2
from handler_x3 import handle_x3

Flag = True
website2id = {}
id2webstie = {}

def transform(Xdata):
    Xdata = Xdata.filter(['instance_id', 'name'], axis=1)
    website2id = {}
    id2webstie = {}
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
            for t in range(0, len(array[i])):
                temp.append(array[i][t])
                temp.append(array[j][t])
            result.append(temp)

    df = pd.DataFrame(result)
    col_len = len(columns)
    df.rename(columns={0:"left_instance_id",1:"right_instance_id",2:"left_title",3:"right_title"}, inplace=True)
    df.drop(columns=["left_title","right_title"],inplace=True)
    return df

if __name__ == '__main__':
    for file_name in ['X2.csv','X3.csv','X4.csv']:
        data = pd.read_csv(file_name)
        if 'name' not in data.columns:
            if 'source' not in data.filter(['instance_id']).sample(1).values[0][0]:
                output = handle_x2(data)
            else:
                output = handle_x3(data)
        else:
            data = transform(data)
            output = data

        if Flag:
            output.to_csv("output.csv", sep=',', encoding='utf-8', index=False)
            Flag = False
        else:
            output.to_csv("output.csv", mode='a', sep=',', encoding='utf-8', index=False, header=None)