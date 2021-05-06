import pandas as pd
import re

brands = ['dell', 'lenovo', 'acer', 'asus', 'hp']

cpu_brands = ['intel', 'amd']

intel_cores = [' i3', ' i5', ' i7', '2 duo', 'celeron', 'pentium', 'centrino']
amd_cores = ['e-series', 'a8', 'radeon', 'athlon', 'turion', 'phenom']

families = {
    'hp': [r'elitebook', r'compaq', r'folio', r'pavilion'],
    'lenovo': [r' x[0-9]{3}[t]?', r'x1 carbon'],
    'dell': [r'inspiron'],
    'asus': [r'zenbook', ],
    'acer': [r'aspire', r'extensa', ],
    '0': []
}


def clean_x3(data):
    instance_ids = data.filter(items=['instance_id'], axis=1)
    titles = data.filter(items=['title'], axis=1)
    information = data.drop(['instance_id'], axis=1)
    information = information.fillna('')
    instance_ids = instance_ids.values.tolist()
    information = information.values.tolist()
    titles = titles.values.tolist()

    result = []
    for row in range(len(instance_ids)):
        information[row].sort(key=lambda i: len(i), reverse=True)
        row_info = titles[row][0]
        for mess in information[row]:
            if mess not in row_info:
                row_info = row_info + ' - ' + mess

        brand = '0'
        cpu_brand = '0'
        cpu_core = '0'
        cpu_model = '0'
        cpu_frequency = '0'
        ram_capacity = '0'
        display_size = '0'
        name_number = '0'
        name_family = '0'

        item = row_info
        lower_item = item.lower()

        rest_info = re.split(r'\s[:\\/-]\s', titles[row][0])
        name_info = rest_info[0]
        useless = ['amazon', 'other laptops', 'miniprice']
        for name in useless:
            if name in rest_info[0].lower():
                name_info = rest_info[1]

        for b in brands:
            if b in lower_item:
                brand = b
                break

        for b in cpu_brands:
            if b in lower_item:
                cpu_brand = b
                break
        if cpu_brand != 'intel':
            for b in amd_cores:
                if b in lower_item:
                    cpu_core = b.strip()
                    cpu_brand = 'amd'
                    break
        if cpu_brand != 'amd':
            for b in intel_cores:
                if b in lower_item:
                    cpu_core = b.strip()
                    cpu_brand = 'intel'
                    break

        if cpu_brand == 'intel':
            result_model = re.search(
                r'[\- ][0-9]{4}[Qq]?[MmUu](?![Hh][Zz])', item)
            if result_model is None:
                result_model = re.search('[\\- ][0-9]{3}[Qq]?[Mm]', item)
            if result_model is None:
                result_model = re.search('[\\- ][MmQq][0-9]{3}', item)
            if result_model is None:
                result_model = re.search('[\\- ][PpNnTt][0-9]{4}', item)
            if result_model is None:
                result_model = re.search('[\\- ][0-9]{4}[Yy]', item)
            if result_model is None:
                result_model = re.search('[\\- ][Ss]?[Ll][0-9]{4}', item)
            if result_model is None:
                result_model = re.search('[\\- ]867', item)
            if result_model is None:
                result_model = re.search(
                    '[\\- ]((1st)|(2nd)|(3rd)|([4-9]st))[ ][Gg]en', item)
            if result_model is not None:
                cpu_model = result_model.group()[1:].lower()
        elif cpu_brand == 'amd':
            if cpu_core == 'a8':
                cpu_core = 'a-series'
            result_model = re.search(r'([AaEe][0-9][\- ][0-9]{4})', item)
            if result_model is None:
                result_model = re.search('[\\- ]HD[\\- ][0-9]{4}', item)
            if result_model is None:
                result_model = re.search('[\\- ][AaEe][\\- ][0-9]{3}', item)
            if result_model is not None:
                cpu_core = result_model.group()[:1].lower() + '-series'
                cpu_model = result_model.group()[1:].lower().replace(' ', '-')
            if cpu_core in ('radeon', 'athlon', 'turion', 'phenom'):
                if result_model is None:
                    result_model = re.search('[\\- ][NnPp][0-9]{3}', item)
                if result_model is None:
                    result_model = re.search(
                        '[\\- ](64[ ]?[Xx]2)|([Nn][Ee][Oo])', item)
                if result_model is not None:
                    cpu_model = result_model.group().lower().replace('-', '').replace(' ', '')

        result_frequency = re.search(
            r'[123][ .][0-9]?[0-9]?[ ]?[Gg][Hh][Zz]', item)
        if result_frequency is not None:
            result_frequency = re.split(r'[GgHhZz]', result_frequency.group())[
                0].strip().replace(' ', '.')
            if len(result_frequency) == 3:
                result_frequency = result_frequency + '0'
            if len(result_frequency) == 1:
                result_frequency = result_frequency + '.00'
            result_frequency = result_frequency
            cpu_frequency = result_frequency

        result_ram_capacity = re.search(
            r'[\s-][12468][\s]?[Gg][Bb]([-\s]|([Rr][Aa][Mm]))', item)
        if result_ram_capacity is None:
            result_ram_capacity = re.search(
                r'[\s-][12468][\s]?[Gg][-\s]', item)
        if result_ram_capacity is not None:
            ram_capacity = result_ram_capacity.group().lower()\
                .replace('-', ' ').replace('b', '').replace('r', '').replace('a', '').replace('m', '').replace(' ', '')

        result_display_size = re.search(r'1[0-9]([. ][0-9])?\"', item)
        if result_display_size is not None:
            display_size = result_display_size.group().replace(" ", ".")[:-1]
        else:
            result_display_size = re.search(
                r'1[0-9]([. ][0-9])?[- ][Ii]nch(?!es)', item)
        if result_display_size is not None and display_size == '0':
            display_size = result_display_size.group().replace(" ", ".")[:-5]
        elif result_display_size is None:
            result_display_size = re.search(
                r'(?<!x)[ ]1[0-9][. ][0-9]([ ]|(\'\'))(?!x)', item)
        if result_display_size is not None and display_size == '0':
            display_size = result_display_size.group().replace(
                "\'", " ").strip().replace(' ', '.')

        if brand == 'lenovo':
            result_name_number = re.search(
                r'[\- ][0-9]{4}[0-9a-zA-Z]{3}(?![0-9a-zA-Z])', name_info)
            if result_name_number is None:
                result_name_number = re.search(
                    r'[\- ][0-9]{4}(?![0-9a-zA-Z])', name_info)
            if result_name_number is not None:
                name_number = result_name_number.group().replace(
                    '-', '').strip().lower()[:4]
        elif brand == 'hp':
            result_name_number = re.search(r'[0-9]{4}[pPwW]', name_info)
            if result_name_number is None:
                result_name_number = re.search(
                    r'15[\- ][a-zA-Z][0-9]{3}[a-zA-Z]{2}', name_info)
            if result_name_number is None:
                result_name_number = re.search(r'[\s]810[\s](G2)?', name_info)
            if result_name_number is None:
                result_name_number = re.search(r'[0-9]{4}[mM]', name_info)
            if result_name_number is None:
                result_name_number = re.search(
                    r'((DV)|(NC))[0-9]{4}', name_info)
            if result_name_number is None:
                result_name_number = re.search(r'[0-9]{4}DX', name_info)
            if result_name_number is not None:
                name_number = result_name_number.group().lower().replace('-', '').replace(' ', '')
        elif brand == 'dell':
            result_name_number = re.search(
                r'1[57][Rr]?[\s]?([0-9]{4})?[\s]([iI])?[0-9]{4}', name_info)
            if result_name_number is None:
                result_name_number = re.search(
                    r'[\s][A-Za-z][0-9]{3}[A-Za-z][\s]', name_info)
            if result_name_number is not None:
                name_number = result_name_number.group().lower().replace(
                    '-', '').replace('i', '').strip().split(' ')[-1]
        elif brand == 'acer':
            result_name_number = re.search(
                r'[A-Za-z][0-9][\- ][0-9]{3}', name_info)
            if result_name_number is None:
                result_name_number = re.search(r'AS[0-9]{4}', name_info)
            if result_name_number is None:
                result_name_number = re.search(
                    r'[0-9]{4}[- ][0-9]{4}', name_info)
            if result_name_number is not None:
                name_number = result_name_number.group().lower().replace(' ', '-').replace('-', '')
                if len(name_number) == 8:
                    name_number = name_number[:4]
        elif brand == 'asus':
            result_name_number = re.search(
                r'[A-Za-z]{2}[0-9]?[0-9]{2}[A-Za-z]?[A-Za-z]', name_info)
            if result_name_number is not None:
                name_number = result_name_number.group().lower().replace(' ', '-').replace('-', '')

        for pattern in families[brand]:
            result_name_family = re.search(pattern, lower_item)
            if result_name_family is not None:
                name_family = result_name_family.group().strip()
                break

        result.append([
            instance_ids[row][0],
            brand,
            cpu_brand,
            cpu_core,
            cpu_model,
            cpu_frequency,
            ram_capacity,
            display_size,
            name_number,
            name_family,
            titles[row][0].lower()
        ])

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
        'pc_name',
        'family',
        'title'
    ]
    for i in range(len(name)):
        result.rename({i: name[i]}, inplace=True, axis=1)

    return result
