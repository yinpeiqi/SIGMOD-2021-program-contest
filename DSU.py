import csv

father = {}

def _find(x):
    if father[x] == x:
        return x
    else:
        father[x] = _find(father[x])
        return father[x]


if __name__ == '__main__':
    data = []
    with open('train2.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    pair = len(data)
    set = {}
    for i in range(1, pair):
        set[data[i][1]] = data[i][4]
        set[data[i][2]] = data[i][5]

    for i in set:
        father[i] = i
    for i in range(1, pair):
        if data[i][3] == '1':
            father[_find(data[i][1])] = _find(data[i][2])

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
        for item in father_set[s]:
            print(set[item], item)
        print()
