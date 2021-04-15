import pandas as pd
import re

brand_list = ["intenso", "pny", "lexar", "sony", "sandisk", "kingston", "samsung", "toshiba", "transcend"]

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
        mem_type = '0'
        brand = '0'
        type = '0'
        model = '0'

        if sizes[row][0] != '':
            size = sizes[row][0].lower().replace(' ', '')
        else:
            size_model = re.search(r'[0-9]{1,4}[ ]*[gt][bo]', nameinfo)
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

        mem_model = re.search(r'ssd', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'micro[- ]?sd[hx]?c?', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'sd[hx]c', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'usb', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'sd', nameinfo)
        if mem_model is not None:
            mem_type = mem_model.group()
            if mem_type not in ('ssd', 'usb'):
                if 'micro' in mem_type:
                    mem_type = 'microsd'
                else:
                    mem_type = 'sd'


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


        elif brand == "lexar":
            model_model = re.search(r'xqd', nameinfo)
            if model_model is not None:
                model = model_model.group()

            type_model = re.search(r'((ljd)|[\s])[a-wy-z][0-9]{2}[a-z]?', nameinfo)
            if type_model is None:
                type_model = re.search(r'[\s][0-9]+00x(?![a-z0-9])', nameinfo)
            if type_model is None:
                type_model = re.search(r'[\s]x[0-9]+00', nameinfo)
            if type_model is not None:
                type = type_model.group().strip().replace('x', '').replace('l', '').replace('j', '').replace('d', '')
        # judge type and model


        elif brand == 'sony':
            type_model = re.search(r'usm[-]?[0-9]?[0-9]?[0-9]?[a-z]{1,4}', nameinfo)
            if type_model is not None:
                type = type_model.group().replace('-', '').replace('g', '')
                for c in range(ord('0'), ord('9')):
                    type = type.replace(chr(c), '')
            else:
                type_model = re.search(r'((class?e?[\s-]?)|(cl[ -]))[0-9]{1,4}', nameinfo)
                if type_model is not None:
                    type = type_model.group().replace('-', '').replace(' ', '')
                    for c in range(ord('a'), ord('z')):
                        type = type.replace(chr(c), '')
                    type = 'class ' + type
        # 1024: 1 TB
        # 256: ssd
        # 128: usmqx usb
        # 128: microsd
        # 64: usb
        # 32: usmqx
        # 32: sd | microsd
        # 32: usmr & usb | usb
        # 16: sd
        # 16: usb
        # 8: sd
        # 8: microsd
        # 8: usmqx usb
        # 4: usmr
        # 4: usmmp | usb

        elif brand == 'sandisk':
            model_model = re.search(r'glide', nameinfo)
            if model_model is None:
                model_model = re.search(r'ext', nameinfo)
            if model_model is None:
                model_model = re.search(r'ultra', nameinfo)
            if model_model is None:
                model_model = re.search(r'cruzer', nameinfo)
            if model_model is not None:
                model = model_model.group()
            print(nameinfo, model)
        # 256: ext
        # 256: glide
        # 128: ext
        # 128: ultra & microsd
        # 128: cruzer | usb (else)
        # 64: ultra & sd
        # 64: ultra & microsd
        # 64: ext & usb
        # 64: ultra & usb
        # 64: usb
        # 32: ultra & sd
        # 32: glide
        # 32: ultra microsd | ultra sd | ext sd
        # 16: ultra & sd
        # 16: microsd
        # 16: usb
        # 16: ext sd
        # 16: ext usb
        # 16: ext sd ?
        # 8: sd
        # 8: ultra & usb
        # 8: cruzer & usb
        # 8: ext sd
        # 4: cruzer
        # 4: microsd


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
