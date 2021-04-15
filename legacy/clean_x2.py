from joblib import load, dump
import pandas as pd
import re
import numpy
from sklearn import metrics
from sklearn.svm import *
from sklearn.linear_model import *
from sklearn.tree import *


brands = ['dell', 'lenovo', 'hp', 'acer', 'asus']
brands_map = {'dell': 1, 'lenovo': 2, 'hp': 3, 'acer': 4, 'asus': 5}

cpu_brands = ['intel', 'amd']
cpu_brands_map = {'intel': 1, 'amd': 2}

cores = [' i3', ' i5', ' i7']
cores_map = {'i3': 1, 'i5': 2, 'i7': 3}

colors = ['steel gray', 'grey',
          'cool steel', 'steel',
          'clarinet black', 'black',
          'iron silver', 'cool silver', 'platinum silver', 'silver aluminum', 'silver',
          'indigo blue', ]


def clean_X2(Xdata):
    instance_ids = Xdata.filter(items=['instance_id'], axis=1)
    titles = Xdata.filter(items=['title'], axis=1)
    information = Xdata.drop(['instance_id'], axis=1)
    information = information.fillna('')
    instance_ids = instance_ids.values.tolist()
    information = information.values.tolist()
    titles = titles.values.tolist()

    result = []
    for row in range(len(instance_ids)):
        information[row].sort(key=lambda i: len(i), reverse=True)
        rowinfo = titles[row][0]
        for mess in information[row]:
            if mess not in rowinfo:
                rowinfo = rowinfo + ' - ' + mess

        brand = '0'
        cpu_brand = '0'
        cpu_core = '0'
        cpu_model = '0'
        cpu_frequency = '0'
        ram_capacity = '0'
        display_size = '0'
        name_number = '0'

        item = rowinfo
        lower_item = item.lower()

        rest_info = re.split(r'\s[:\\/-]\s', titles[row][0])
        name_info = rest_info[0]
        if 'amazon' in rest_info[0].lower():
            name_info = rest_info[1]
        # name_info = re.split(r'(\swith)|(,\s)|(windows)', name_info)[0]
        # for color in colors:
        #     if color in name_info:
        #         name_info = name_info.replace(color, '')
        # name_info = name_info.replace('()', '')
        # name_info = name_info.replace(' / ', '')

        for b in brands:
            if b in lower_item:
                brand = brands_map[b]
                break

        for b in cpu_brands:
            if b in lower_item:
                cpu_brand = cpu_brands_map[b]
                break

        for b in cores:
            if b in lower_item:
                cpu_core = cores_map[b.strip()]
                cpu_brand = cpu_brands_map['intel']
                break

        result_model = re.search(r'[\- ][0-9]{3}[0-9L][MmUu]', item)
        if result_model is not None:
            cpu_model = result_model.group()[1:].lower()
            for c in range(ord('a'), ord('z')):
                cpu_model = cpu_model.replace(chr(c), str(c - ord('a') + 1))
        if cpu_brand == cpu_brands_map['amd']:
            result_model = re.search(r'([A-Z][0-9]-[0-9]{4})', item)
            if result_model is not None:
                cpu_core = result_model.group().lower()[0:2]
                for c in range(ord('a'), ord('z')):
                    cpu_core = cpu_core.replace(chr(c), str(c - ord('a') + 1))
                cpu_model = result_model.group().lower()[3:]

        result_frequency = re.search(r'(([1-9]\d*\.?\d*)|(0\.\d*[1-9]))[\s]?[Gg][Hh][Zz]', item)
        if result_frequency is not None:
            result_frequency = re.split(r'[\sGgHhZz]', result_frequency.group())[0]
            if len(result_frequency) == 3:
                result_frequency = result_frequency + '0'
            if len(result_frequency) == 1:
                result_frequency = result_frequency + '.00'
            result_frequency = result_frequency
            cpu_frequency = result_frequency

        result_ram_capacity = re.search(
            r'[1-9][\s]?[Gg][Bb][\s]?((S[Dd][Rr][Aa][Mm])|(D[Dd][Rr]3)|([Rr][Aa][Mm])|(Memory))', item)
        if result_ram_capacity is not None:
            ram_capacity = result_ram_capacity.group()[:1]

        result_display_size = re.search(r'[1](([0-9])|([0-9].[0-9]))(([\s]?[\-\s][\s]?[Ii]nch[^e])|([\"]))', item)
        if result_display_size is not None:
            display_size = re.split(r'([\s]?[\-\s][\s]?[Ii]nch|[\"])', result_display_size.group())[0].replace(' ', '.')
        else:
            result_display_size = re.search(r'\s[1](([0-9])|([0-9].[0-9]))\s[^Ii]', item)
            if result_display_size is not None:
                display_size = result_display_size.group()[:-1].strip().replace(' ', '.')


        if brand == brands_map['lenovo']:
            result_name_number = re.search(r'[0-9]{4}[0-9a-zA-Z]{3}', name_info)
            if result_name_number is None:
                result_name_number = re.search(r'[0-9]{4}', name_info)
            if result_name_number is not None:
                name_number = result_name_number.group().strip().lower()
        elif brand == brands_map['hp']:
            result_name_number = re.search(r'[0-9]{4}[pPwW]', name_info)
            if result_name_number is None:
                result_name_number = re.search(r'15-[a-zA-Z][0-9]{3}[a-zA-Z]{2}', name_info)
            if result_name_number is None:
                result_name_number = re.search(r'[0-9]{3}[\s][A-Za-z][0-9]', name_info)
            if result_name_number is None:
                result_name_number = re.search(r'[0-9]{4}[mM]', name_info)
            if result_name_number is not None:
                name_number = result_name_number.group().lower().replace('-', '').replace(' ', '')
        elif brand == brands_map['dell']:
            result_name_number = re.search(r'[a-zA-Z][0-9]{3}[a-zA-Z]', name_info)
            if result_name_number is None:
                result_name_number = re.search(r'[0-9]{3}-[0-9]{3}', name_info)
            if result_name_number is not None:
                name_number = result_name_number.group().lower().replace('-', '')
        elif brand == brands_map['acer']:
            result_name_number = re.search(r'[A-Za-z][0-9]-[0-9]{3}', name_info)
            if result_name_number is not None:
                name_number = result_name_number.group().lower().replace('-', '')

        # print(name_info)
        # print(name_number)
        for c in range(ord('a'), ord('z')):
            name_number = name_number.replace(chr(c), str( (c-ord('a')+1)%10 ) )

        result.append([
            instance_ids[row][0],
            brand,
            cpu_brand,
            cpu_core,
            cpu_model,
            cpu_frequency,
            ram_capacity,
            display_size,
            name_number
            # titles[row][0].lower()
        ])

    for col in range(3, len(result[0])):
        mp = {}
        cnt = 0
        for i in range(len(result)):
            if result[i][col] == '0':
                continue
            if result[i][col] not in mp:
                cnt += 1
                mp[result[i][col]] = cnt
            result[i][col] = mp[result[i][col]]


    result = pd.DataFrame(result)
    name = [
        'instance_id',
        'brand',
        'cpu_brand',
        'cpu_core',
        'cpu_model',
        'cpu_frequency',
        'ram_capacity',
        'display_size',
        'pc_name'
    ]
    for i in range(len(name)):
        result.rename({i: name[i]}, inplace=True, axis=1)

    return result
