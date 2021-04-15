import pandas as pd
import re


def clean_X4(Xdata):
    names = Xdata.filter(items=['name'], axis=1).fillna('')
    brands = Xdata.filter(items=['brand'], axis=1).fillna('')
    sizes = Xdata.filter(items=['size'], axis=1).fillna('')
    instance_ids = Xdata.filter(items=['instance_id'], axis=1)
    names = names.values.tolist()
    brands = brands.values.tolist()
    sizes = sizes.values.tolist()
    instance_ids = instance_ids.values.tolist()

    result = []

    for row in range(len(instance_ids)):
        nameinfo = names[row][0]

        size_model = re.search(r'[0-9]?[0-9]{2}[Gg][Bb]', nameinfo)
        if size_model is not None:
            size_model = size_model.group()[:].upper()

        # print("size")
        # print(sizes[row][0])
        if sizes[row][0] != '':
            size_model = sizes[row][0].replace(' ', '')

        if size_model is not None:
            size_model = size_model.replace('GB', '')
            size_model = size_model.replace('TB', '')
            size_model = int(size_model)
        else:
            size_model = 0

        # print(instance_ids[row][0], brands[row][0], size_model)
        result.append([instance_ids[row][0], brands[row][0], size_model])

    mp = {}
    cnt = 0
    for i in range(len(result)):
        if result[i][1] is None:
            result[i][1] = 0
        else:
            if result[i][1] not in mp:
                cnt += 1
                mp[result[i][1]] = cnt
            result[i][1] = mp[result[i][1]]


    # print(result[0])
    result = pd.DataFrame(result)

    name = ['instance_id', 'brand', 'size']
    for i in range(len(name)):
        result.rename({i: name[i]}, inplace=True, axis=1)

    #
    # for i in range(result.shape[0]):
    #     print(result.iloc[i].values.tolist())
    return result
