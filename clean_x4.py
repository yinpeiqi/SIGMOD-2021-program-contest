import pandas as pd
import re

brand_list = ["intenso", "lexar", "sony", "pny", "sandisk", "kingston", "samsung", "toshiba", "transcend"]

intenso_type = ["basic", "premium", "rainbow", "speed"]

def clean_x4(Xdata):
    names = Xdata.filter(items=['name'], axis=1).fillna('')
    prices = Xdata.filter(items=['price'], axis=1).fillna('')
    sizes = Xdata.filter(items=['size'], axis=1).fillna('')
    brands = Xdata.filter(items=['brand'], axis=1).fillna('')
    instance_ids = Xdata.filter(items=['instance_id'], axis=1)
    names = names.values.tolist()
    prices = prices.values.tolist()
    sizes = sizes.values.tolist()
    brands = brands.values.tolist()
    instance_ids = instance_ids.values.tolist()

    result = []

    for row in range(len(instance_ids)):
        nameinfo = names[row][0].lower()

        size = '0'
        price = '0'
        brand = '0'
        type = '0'
        model = '0'

        if sizes[row][0] != '':
            size = sizes[row][0].lower().replace(' ', '')
        else:
            size_model = re.search(r'[0-9]{1,4}[ ]*[g][b]', nameinfo)
            if size_model is not None:
                size = size_model.group()[:].lower()

        if prices[row][0] != '':
            price = prices[row][0]

        if brands[row][0] != '':
            brand = brands[row][0].lower()
        else:
            for b in brands:
                if b in nameinfo:
                    brand = b
                    break

        if brand == "intenso":
            model_model = re.search(r'[0-9]{7}', nameinfo)
            if model_model is not None:
                model = model_model.group()[:]

            type_model = re.search(r'[a-z]+\s(?=line)', nameinfo.lower())
            if type_model is not None:
                type = type_model.group()[:]
            else:
                for t in intenso_type:
                    if t in nameinfo:
                        type = t
                        break

            print(nameinfo,model,type)

        elif brand == "lexar":
            pass


        # print(nameinfo,brand)

        # print(instance_ids[row][0], brands[row][0], size_model)
        # result.append([instance_ids[row][0], brands[row][0], size_model])

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
