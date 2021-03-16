import pandas as pd
import re

brands = {'dell', 'lenovo', 'hp', 'acer', 'asus'}
cpu_brands = {'intel', 'amd'}
cores = {' i3', ' i5', ' i7'}

if __name__ == '__main__':
    Xdata = pd.read_csv('./data/X2.csv')
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
        rowinfo = ''
        for mess in information[row]:
            if mess not in rowinfo:
                rowinfo = rowinfo + ' - ' + mess

        brand = ''
        cpu_brand = ''
        cpu_core = ''
        cpu_model = ''
        cpu_frequency = ''
        ram_capacity = ''
        display_size = ''

        item = rowinfo
        lower_item = item.lower()

        for b in brands:
            if b in lower_item:
                brand = b
                break

        for b in cpu_brands:
            if b in lower_item:
                cpu_brand = b
                break

        for b in cores:
            if b in lower_item:
                cpu_core = b
                break

        result_model = re.search(r'[\- ][0-9]{4}[A-Z]', item)
        if result_model is not None:
            cpu_model = result_model.group()[1:].lower()
        if cpu_brand == 'amd':
            result_model = re.search(r'([A-Z][0-9]-[0-9]{4})', item)
            if result_model is not None:
                cpu_model = result_model.group().lower()

        result_frequency = re.search(r'(([1-9]\d*\.?\d*)|(0\.\d*[1-9]))[\s]?[Gg][Hh][Zz]', item)
        if result_frequency is not None:
            result_frequency = re.split(r'[\sGgHhZz]', result_frequency.group())[0]
            if len(result_frequency) == 3:
                result_frequency = result_frequency + '0'
            if len(result_frequency) == 1:
                result_frequency = result_frequency + '.00'
            result_frequency = result_frequency
            cpu_frequency = result_frequency

        result_ram_capacity = re.search(r'[1-9][\s]?[Gg][Bb][\s]?((S[Dd][Rr][Aa][Mm])|(D[Dd][Rr]3)|([Rr][Aa][Mm])|(Memory))', item)
        if result_ram_capacity is not None:
            ram_capacity = result_ram_capacity.group()[:1]

        result_display_size = re.search(r'[1](([0-9])|([0-9].[0-9]))(([\-\s][Ii]nch)|([\"]))', item)
        if result_display_size is not None:
            display_size = re.split(r'([\-\s][Ii]nch|[\"])', result_display_size.group())[0]
        else:
            result_display_size = re.search(r'\s[1](([0-9])|([0-9].[0-9]))\s', item)
            if result_display_size is not None:
                display_size = result_display_size.group().strip()

        result.append(
            [instance_ids[row][0], brand, cpu_brand, cpu_core, cpu_model, cpu_frequency, ram_capacity, display_size,
             titles[row][0].lower()])


    result = pd.DataFrame(result)
    result.rename({0: 'instance_id',
                 1: 'brand',
                 2: 'cpu_brand',
                 3: 'cpu_core',
                 4: 'cpu_model',
                 5: 'cpu_frequency',
                 6: 'ram_capacity',
                 7: 'display_size',
                 8: 'information'
            }, inplace=True, axis=1)
    result.to_csv("./test/cleanX2.csv", sep=',')
