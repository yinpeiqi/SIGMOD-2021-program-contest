import csv
import pandas as pd
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
father = {}

def _find(x):
    if father[x] == x:
        return x
    else:
        father[x] = _find(father[x])
        return father[x]

def get_title(data):
    return ("{0: <20}{1: <10}{2: <10}{3: <10}{4: <20}{5: <10}{6: <10}{7: <20}{8: <100}"
            .format(str(data[0]),str(data[1]),str(data[2]),str(data[3]),str(data[4]),
                    str(data[5]),str(data[6]),str(data[7]),str(data[8])))

if __name__ == '__main__':
    data = []
    data = pd.read_csv("test/cleanX4.csv")
    set = {}
    for i in range(len(data)):
        set[data[i:i+1]['instance_id'].values[0]] = get_title(data[i:i+1].values.tolist()[0])

    map_table = pd.read_csv("../Y4.csv")
    for i in set:
        father[i] = i
    for i in range(len(map_table)):
        if map_table[i:i+1]['label'].values[0] == 1:
            father[_find(map_table[i:i+1]['left_instance_id'].values[0])] = _find(map_table[i:i+1]['right_instance_id'].values[0])

    father_set = {}
    # for i in set:
    #     if father[i] not in father_set:
    #         father_set[father[i]] = [i]
    #     else:
    #         father_set[father[i]].append(i)
    for i in set:
        if _find(i) not in father_set:
            father_set[_find(i)] = [i]
        else:
            father_set[_find(i)].append(i)


    print(len(father_set))
    for s in father_set:
        if len(father_set[s]) >= 1:
            for item in father_set[s]:
                print(set[item], item)
            print()