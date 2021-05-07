import pandas as pd
from clean_x2 import clean_x2

pc_aliases = {
    "2320": "3435", "v7482": "v7582", "810g2": "810", "2338": "2339",
    "346058u": "3460", "4291": "4290", "4287": "4290", "0622": "0627"}

cpu_model_aliases = {
    "hp": {"2410m": "2540m", "2620m": "2640m"},
    "acer": {},
    "lenovo": {},
    "asus": {},
    "dell": {}
}

model_family_2_pcname = {
    "4010u aspire": "e1572"
}

pc_single = ["v7582", "15f009wm", "3093", "ux31a", "v3772", "v3572", "m731r", "e3111",
             "v3111", "15p030nr", "e5771", "e1731", "3437 ", "2170p", "e1532", "e1522",
             "e1571", "e5571", "15d053cl", "v5573", "3448", "8460p", "8570p",
             "2570p", "2760p", "0596", "547578", "547150", "547375"]

pc_core = ["e1572", "e1771", "810", "8560p", "3438"]
pc_model_capacity = ["2325", "3460"]
pc_capacity = ["9470m", "3444", "2339"]

solved_spec = []
unsolved_spec = []

instance_list = set()


def handle_x2(dataset: pd.DataFrame):
    """ Call clean_x2.py;

    Give an identification for each record according to their cleaned field values
    and match records based on their identification

    :param dataset: X2.csv

    :return:
            A DataFrame of matched pairs which contains following columns:
            {left_instance_id: the left instance of a matched pair
             left_instance_id: the right instance of a matched pair}
    """

    dataset = clean_x2(dataset)

    for index, row in dataset.iterrows():
        instance_id = row['instance_id']
        brand = row['brand']
        cpu_core = row['cpu_core']
        cpu_model = row['cpu_model']
        cpu_frequency = row['cpu_frequency']
        display_size = row['display_size']
        pc_name = row['pc_name']
        capacity = row['ram_capacity']
        family = row['family']
        title = row['title']
        pc = {}

        if (cpu_model + ' ' + family) in model_family_2_pcname.keys():
            pc_name = model_family_2_pcname[(cpu_model + ' ' + family)]

        if pc_name in pc_aliases.keys():
            pc_name = pc_aliases[pc_name]

        if brand in cpu_model_aliases.keys():
            if cpu_model in cpu_model_aliases[brand].keys():
                cpu_model = cpu_model_aliases[brand][cpu_model]

        instance_list.add(instance_id)

        pc['id'] = instance_id
        pc['title'] = title
        pc['brand'] = brand
        pc['pc_name'] = pc_name
        pc['cpu_model'] = cpu_model
        pc['capacity'] = capacity
        pc['cpu_core'] = cpu_core
        pc['family'] = family
        pc['cpu_frequency'] = cpu_frequency
        pc['display_size'] = display_size

        if pc_name != '0' and cpu_model != '0' and capacity != '0' and cpu_core != '0':
            pc['identification'] = brand + ' ' + pc_name + \
                ' ' + cpu_model + ' ' + capacity + ' ' + cpu_core
            solved_spec.append(pc)
        else:
            unsolved_spec.append(pc)

    for u in unsolved_spec.copy():
        for s in solved_spec.copy():
            if u['brand'] != '0' and u['pc_name'] != '0' and u['capacity'] != '0' and u['cpu_model'] != '0':
                if u['brand'] == s['brand'] and u['pc_name'] == s['pc_name'] and u['capacity'] == s['capacity'] and \
                        u['cpu_model'] == s['cpu_model']:
                    if u['family'] == '0' or s['family'] == '0' or u['family'] == s['family']:
                        u['identification'] = s['identification']
                        solved_spec.append(u)
                        unsolved_spec.remove(u)
                        break
            elif u['brand'] != '0' and u['pc_name'] != '0' and u['cpu_core'] != '0' and u['cpu_model'] != '0':
                if u['brand'] == s['brand'] and u['pc_name'] == s['pc_name'] and u['cpu_model'] == s['cpu_model'] and \
                        u['cpu_core'] == s['cpu_core']:
                    if u['family'] == '0' or s['family'] == '0' or u['family'] == s['family']:
                        u['identification'] = s['identification']
                        solved_spec.append(u)
                        unsolved_spec.remove(u)
                        break
            elif u['brand'] != '0' and u['capacity'] != '0' and u['cpu_core'] != '0' and u['pc_name'] != '0':
                if u['brand'] == s['brand'] and u['pc_name'] == s['pc_name'] and u['cpu_core'] == s['cpu_core'] and \
                        u['capacity'] == s['capacity']:
                    if u['family'] == '0' or s['family'] == '0' or u['family'] == s['family']:
                        u['identification'] = s['identification']
                        solved_spec.append(u)
                        unsolved_spec.remove(u)
                        break
            elif u['brand'] != '0' and u['capacity'] != '0' and u['cpu_core'] != '0' and u['cpu_model'] != '0':
                if u['brand'] == s['brand'] and u['capacity'] == s['capacity'] and u['cpu_core'] == s['cpu_core'] and \
                        u['cpu_model'] == s['cpu_model']:
                    if u['family'] == '0' or s['family'] == '0' or u['family'] == s['family']:
                        u['identification'] = s['identification']
                        solved_spec.append(u)
                        unsolved_spec.remove(u)
                        break
            elif u['brand'] != '0' and u['cpu_model'] != '0' and u['pc_name'] != '0':
                if u['brand'] == s['brand'] and u['pc_name'] == s['pc_name'] and u['cpu_model'] == s['cpu_model']:
                    if u['family'] == '0' or s['family'] == '0' or u['family'] == s['family']:
                        u['identification'] = s['identification']
                        solved_spec.append(u)
                        unsolved_spec.remove(u)
                        break
            elif u['brand'] != '0' and u['capacity'] != '0' and u['cpu_model'] != '0' and u['display_size'] != '0' and \
                    u['cpu_frequency'] != '0':
                if u['brand'] == s['brand'] and u['capacity'] == s['capacity'] and \
                        u['cpu_model'] == s['cpu_model'] and u['display_size'] == s['display_size'] and \
                        u['cpu_frequency'] == s['cpu_frequency']:
                    if u['family'] == '0' or s['family'] == '0' or u['family'] == s['family']:
                        u['identification'] = s['identification']
                        solved_spec.append(u)
                        unsolved_spec.remove(u)
                        break
            elif u['brand'] != '0' and u['capacity'] != '0' and u['pc_name'] != '0' and u['display_size'] != '0' and \
                    u['cpu_frequency'] != '0':
                if u['brand'] == s['brand'] and u['capacity'] == s['capacity'] and u['pc_name'] == s['pc_name'] and \
                        u['display_size'] == s['display_size'] and u['cpu_frequency'] == s['cpu_frequency']:
                    if u['family'] == '0' or s['family'] == '0' or u['family'] == s['family']:
                        u['identification'] = s['identification']
                        solved_spec.append(u)
                        unsolved_spec.remove(u)
                        break

    for i in unsolved_spec:
        if i in solved_spec:
            continue
        for j in unsolved_spec:
            if j in solved_spec:
                continue
            if i['id'] == j['id']:
                continue
            if i['brand'] == j['brand'] and i['capacity'] == j['capacity'] and \
               i['cpu_core'] == j['cpu_core'] and i['cpu_model'] == j['cpu_model'] and \
               i['pc_name'] == j['pc_name']:
                i['identification'] = i['brand'] + i['capacity'] + \
                    i['cpu_core'] + i['cpu_model'] + i['pc_name']
                j['identification'] = i['identification']
                if i not in solved_spec:
                    solved_spec.append(i)
                if j not in solved_spec:
                    solved_spec.append(j)

    clusters = dict()

    for s in solved_spec:
        if s['identification'] in clusters.keys():
            clusters[s['identification']].append(s['id'])
        else:
            clusters.update({s['identification']: [s['id']]})

    for u in unsolved_spec:
        if u['title'] in clusters.keys():
            clusters[u['title']].append(u['id'])
        else:
            clusters.update({u['title']: [u['id']]})

    couples = set()
    for c in clusters.keys():
        if len(clusters[c]) > 1:
            for i in clusters[c]:
                for j in clusters[c]:
                    if i < j:
                        couples.add((i, j, 1))
                    if i > j:
                        couples.add((j, i, 1))

    output = couples
    output = pd.DataFrame(
        output,
        columns=[
            'left_instance_id',
            'right_instance_id',
            'label'])
    output.drop(columns=['label'], inplace=True)

    return output
