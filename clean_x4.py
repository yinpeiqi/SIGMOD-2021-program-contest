import pandas as pd
import re

brand_list = ["intenso", "pny", "lexar", "sony", "sandisk", "kingston", "samsung", "toshiba", "transcend"]

intenso_type = ["basic", "rainbow", "high speed", "speed", "premium", "alu", "business", "micro",
                "imobile", "cmobile", "mini", "ultra", "slim", "flash", "mobile"]

colors = ['prism white', 'prism black', 'prism green', 'prism blue', 'canary yellow',
          'flamingo pink', 'cardinal red', 'smoke blue', 'deep blue', 'coral orange',
          'black sky', 'gold sand', 'blue mist and peach cloud', 'orchid gray',
          'metallic copper', 'lavender purple', 'ocean blue', 'pure white', 'alpine white',
          'copper', 'red', 'black', 'blue', 'white', 'silver', 'gold', 'violet', 'purple',
          'brown', 'orange', 'coral', 'pink']


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
        type2 = ' 0'
        model = '0'
        item_code = '0'
        generation = '0'
        sd_code = '0'

        if sizes[row][0] != '':
            size = sizes[row][0].lower().replace(' ', '')
        else:
            size_model = re.search(r'[0-9]{1,4}[ ]*[gt][bo]', nameinfo)
            if size_model is not None:
                size = size_model.group()[:].lower().replace(' ', '')

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
            mem_model = re.search(r'drive', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'sd', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'secure digital', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'xqd', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'ljd', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'sim', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'speicherstick', nameinfo)
        if mem_model is not None:
            mem_type = mem_model.group()
            if mem_type not in ('ssd', 'usb', 'xqd', 'sim'):
                if 'drive' in mem_type:
                    mem_type = 'usb'
                elif 'speicherstick' in mem_type:
                    mem_type = 'usb'
                elif 'micro' in mem_type:
                    mem_type = 'microsd'
                elif 'ljd' in mem_type:
                    mem_type = 'usb'
                else:
                    mem_type = 'sd'

        item_code_model = re.search(r'\((mk)?[0-9]{6,10}\)', nameinfo)
        if item_code_model is not None:
            item_code = item_code_model.group()[1:-1]

        gen_model = re.search(r'(usb)[\- ][123][.][012]', nameinfo)
        if gen_model is not None:
            if mem_type == '0':
                mem_type = 'usb'
            generation = gen_model.group()[-3:].replace('.0', '').replace('.1', '').replace('.2', '')
        else:
            gen_model = re.search(r'uhs[\\]?[\- ]?[i1](?!i)', nameinfo)
            if gen_model is not None:
                generation = 1
            if gen_model is None:
                gen_model = re.search(r'uhs[\\]?[\- ]?(2|(ii))', nameinfo)
                if gen_model is not None:
                    generation = 2
            if gen_model is not None and mem_type == '0':
                mem_type = 'sd'

        sd_model = re.search(r'(clas[es][e]?[\- ]?[2468])|(cl[\- ]?[2468])', nameinfo)
        if sd_model is not None:
            sd_code = sd_model.group()[-1:]
        if sd_model is None:

            sd_model = re.search(r'(clas[es][e]?[\- ]?10)|(cl[\- ]?10)', nameinfo)
            if sd_model is not None:
                sd_code = 10


        if brand == "intenso":
            model_model = re.search(r'[0-9]{7}', nameinfo)
            if model_model is not None:
                model = model_model.group()[:]

            type_model = re.search(r'(high\s)?[a-z]+\s(?=line)', nameinfo)
            if type_model is not None:
                type = type_model.group()[:].replace(' ', '')
                mem_type = 'usb'
            else:
                for t in intenso_type:
                    if t in nameinfo:
                        type = t.replace(' ', '')
                        break

        elif brand == "lexar":

            type_model = re.search(r'((ljd)|[\s])[a-wy-z][0-9]{2}[a-z]?', nameinfo)
            if type_model is not None and mem_type == '0':
                mem_type = 'usb'
            if type_model is None:
                type_model = re.search(r'[\s][0-9]+x(?![a-z0-9])', nameinfo)
            if type_model is None:
                type_model = re.search(r'(([\s][x])|(beu))[0-9]+', nameinfo)
            if type_model is not None:
                type = type_model.group().strip() \
                    .replace('x', '').replace('l', '').replace('j', '').replace('d', '') \
                    .replace('b', '').replace('e', '').replace('u', '')
        # judge type and model

        elif brand == 'sony':
            if mem_type == '0':
                if ('ux' in nameinfo) or ('uy' in nameinfo) or ('sr' in nameinfo):
                    mem_type = 'microsd'
                elif 'uf' in nameinfo:
                    mem_type = 'sd'
                elif 'usm' in nameinfo:
                    mem_type = 'usb'

            if size == '1tb':
                mem_type = 'usb'
            else:
                type_model = re.search(r'((sf)|(usm))[-]?[0-9a-z]{1,6}', nameinfo)
                if type_model is not None:
                    type = type_model.group().replace('-', '').replace('g', '')
                    for c in range(ord('0'), ord('9')):
                        type = type.replace(chr(c), '')
                    if type == 'sfn' and mem_type == '0':
                        mem_type = 'sd'
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
                if mem_type == '0' and model in ('cruzer', 'glide'):
                    mem_type = 'usb'
            # print(nameinfo, model)
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

        elif brand == 'pny':
            type_model = re.search(r'att.*?[3-4]', nameinfo)
            if type_model is not None:
                type = type_model.group().replace(' ', '').replace('-', '')
                type = 'att' + list(filter(lambda ch: ch in '0123456789', type))[0]
                if mem_type == '0':
                    mem_type = 'usb'


        elif brand == 'kingston':
            # microsd: SDCS2, SDCG3, MLPMR2, SDCE, SDCIT
            # sd: SDS2, SDG3, MLPR2
            # usb: DT Locker+ G3, DT Vault Privacy, DT2000, DT4000G2, DT100G3, DT70, DT80, DT Duo,
            # DT Elite G2, DT G4, DT Kyson, DataTraveler Micro 3.1, DataTraveler MicroDuo 3C,
            # DT SE9, DataTraveler microDuo 3.0 G2, DT Exodia, IronKey D300, IronKey S1000
            if ('savage' in nameinfo) or ('hx' in nameinfo) or ('hyperx' in nameinfo):
                model = 'hyperx'
                mem_type = 'usb'
            model_model = re.search(r'(dt[i 0-9])|(data[ ]?traveler)', nameinfo)
            if model_model is not None:
                model = 'dt'
                mem_type = 'usb'
                type_model = re.search(r'((dt)|(data[ ]?traveler))[ ]?[1-9][0-9][0-9]?[0-9]?[ g]', nameinfo)
                if type_model is not None:
                    type = type_model.group()[:].replace(' ', '').replace('g', '').replace('dt', '').replace(
                        'datatraveler', '')
                if type_model is None:
                    type_model = re.search(r'dt[ ]?i[ g]', nameinfo)
                    if type_model is not None:
                        type = 'i'
                if type_model is None:
                    type_model = re.search(r'se[- ]?9', nameinfo)
                    if type_model is not None:
                        type = 'se9'
                if mem_type == '0' and type != '0':
                    mem_type = 'usb'
                type2_model = re.search(r'(g[ ]?[1-4])|(gen[ ]?[1-4])', nameinfo)
                if type2_model is not None:
                    type2 = type2_model.group()[:].replace('gen', 'g').replace(' ', '')
            if model_model is None:
                if 'ultimate' in nameinfo:
                    if mem_type == '0':
                        mem_type = 'sd'
                    model = 'ultimate'
                if 'sd4' in nameinfo or sd_code == '4':
                    type = 'sd4'
                elif 'sda10' in nameinfo or (mem_type == 'sd' and sd_code == '10'):
                    type = 'sda10'
                elif 'sdcac' in nameinfo:
                    type = 'sdcac'
                elif 'sda3' in nameinfo:
                    type = 'sda3'
                elif 'sdc10' in nameinfo or 'sdcit' in nameinfo or (mem_type == 'microsd' and sd_code == '10'):
                    type = 'sdc10'
                elif 'sdca3' in nameinfo:
                    type = 'sdca3'
                if mem_type == '0' and type != '0':
                    if type == 'sd4' or type == 'sda10' or type == 'sda3':
                        mem_type = 'sd'
                    else:
                        mem_type = 'microsd'
        # 512, 256, 128: judge by memtype
        # 64: g2, g4
        # 32: g2
        # 16: microsd, sd, usb ????
        # 8: microsd, usb

        elif brand == 'samsung':
            if 'lte' in nameinfo:
                model_model = re.search(r'[\s][a-z][0-9]{1,2}[a-z]?[\s]', nameinfo)
                if model_model is None:
                    model_model = re.search(r'[\s]note[\s]?[0-9]{1,2}\+?[\s]?(ultra)?', nameinfo)
                if model_model is None:
                    model_model = re.search(r'prime[ ]?((plus)|\+)', nameinfo)
                if model_model is None:
                    model_model = re.search(r'prime', nameinfo)
                if model_model is not None:
                    model = model_model.group().replace(' ', '').replace('plus', '+')
                mem_type = 'sim'
            elif 'tv' in nameinfo:
                size_model = re.search(r'[0-9]{2}[- ]?inch', nameinfo)
                if size_model is not None:
                    size = size_model.group()[:2]
                mem_model = re.search(r'(hd)|(qled)|(uhd)', nameinfo)
                if mem_model is not None:
                    mem_type = mem_model.group()
                model_model = re.search(r'[a-z]{1,2}[0-9]{4}', nameinfo)
                if model_model is not None:
                    model = model_model.group()
            else:
                if mem_type == 'ssd':
                    model_model = re.search(r'[\s]t[0-9][\s]', nameinfo)
                    if model_model is not None:
                        model = model_model.group().strip()
                else:
                    model_model = re.search(r'(pro)|(evo)', nameinfo)
                    if model_model is not None:
                        model = model_model.group()
                        model_model = re.search(r'(\+)|(plus)', nameinfo)
                        if model_model is not None:
                            model = model + model_model.group().replace('plus', '+')
                    if model == 'evo+' and mem_type == '0':
                        mem_type = 'microsd'
            for c in colors:
                if c in nameinfo:
                    type = c
                    break
        # LTE: color(type), gb, model
        # TV: color(type), inch(model)
        # others: gb

        elif brand == 'toshiba':
            model_model = re.search(r'[\s\-n][a-z][0-9]{3}', nameinfo)
            if model_model is not None:
                model = model_model.group()[1:]
                ch = model[0]
                if ch == 'u':
                    mem_type = 'usb'
                elif ch == 'n':
                    mem_type = 'sd'
                elif ch == 'm':
                    mem_type = 'microsd'
            if model == '0' and 'silber' in nameinfo:
                model = 'n401'
            speed_model = re.search(r'[1-9][0-9]{1,2}[ ]?mb/s', nameinfo)
            if speed_model is not None:
                speed = re.search(r'[0-9]{2,3}', speed_model.group()).group()
                if model == '0' and mem_type in ('usb', 'microsd', 'sd'):
                    if mem_type == 'usb':
                        ch = 'u'
                    elif mem_type == 'microsd':
                        ch = 'm'
                    else:
                        ch = 'n'
                    if speed == '260':
                        model = ch + '101'
                    elif speed == '90':
                        model = ch + '302'
            if mem_type == 'usb' and generation == '2' and model == '0':
                model = 'u202'
            if mem_type == 'sd' and generation == '2' and model == '0':
                model = 'n101'

        elif brand == 'transcend':
            pass

        result.append([
            instance_ids[row][0],
            brand,
            size,
            price,
            mem_type,
            type,
            type2,
            model,
            item_code,
            generation,
            sd_code,
            nameinfo
        ])
    result = pd.DataFrame(result)

    name = ['instance_id', 'brand', 'capacity', 'price', 'mem_type', 'type', 'type2', 'model', 'item_code',
            'generation', 'sd_code', 'title']
    for i in range(len(name)):
        result.rename({i: name[i]}, inplace=True, axis=1)

    return result
