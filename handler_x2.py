import pandas as pd
from legacy.clean_x3 import clean_x3

pc_aliases = {
    "2320": "3435", "v7482": "v7582", "810g2": "810", "2338": "2339",
    "346058u":"3460", "4291":"4290", "4287":"4290", "0622":"0627"}

cpu_model_aliases = {
    "hp": {"2410m":"2540m", "2620m":"2640m"},
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
             "2570p", "2760p", "0596"]

pc_core = ["e1572","e1771","810", "8560p","3438"]
pc_model_capacity = ["2325","3460"]
pc_capacity = ["9470m","3444","2339"]

solved_spec = []
unsolved_spec = []

instance_list = set()


def handle_x2(dataset: pd.DataFrame, STATE='Test'):
    dataset = clean_x3(dataset)

    for index, row in dataset.iterrows():
        instance_id = row['instance_id']
        brand = row['brand']
        cpu_core = row['cpu_core']
        cpu_model = row['cpu_model']
        cpu_frequency = row['cpu_frequency']
        pc_name = row['pc_name']
        capacity = row['ram_capacity']
        family = row['family']
        title = row['title']
        pc = {}

        if (cpu_model+' '+ family) in model_family_2_pcname.keys():
            pc_name = model_family_2_pcname[(cpu_model+' '+ family)]

        if pc_name in pc_aliases.keys():
            pc_name = pc_aliases[pc_name]

        if brand in cpu_model_aliases.keys():
            if cpu_model in cpu_model_aliases[brand].keys():
                cpu_model = cpu_model_aliases[brand][cpu_model]

        instance_list.add(instance_id)

        pc['id'] = instance_id
        pc['title'] = title

        if pc_name in pc_single:
            pc['identification'] = pc_name
            solved_spec.append(pc)
        elif pc_name in pc_capacity and capacity!='0':
            pc['identification'] = pc_name + ' ' + capacity
            solved_spec.append(pc)
        elif pc_name in pc_core and cpu_core != '0':
            pc['identification'] = pc_name + ' ' + cpu_core
            solved_spec.append(pc)
        elif pc_name in pc_model_capacity and cpu_model!='0' and capacity !='0':
            pc['identification'] = pc_name + ' ' + cpu_model + ' ' + capacity
            solved_spec.append(pc)
        elif pc_name != '0' and cpu_model != '0':
            pc['identification'] = pc_name + ' ' + cpu_model
            solved_spec.append(pc)
        elif pc_name != '0' and cpu_core != '0':
            pc['identification'] = pc_name + ' ' + cpu_core
            solved_spec.append(pc)
        elif pc_name != '0' and cpu_frequency != '0':
            pc['identification'] = pc_name + ' ' + cpu_frequency
            solved_spec.append(pc)
        else:
            unsolved_spec.append(pc)

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

    singles = set()
    for i in instance_list:
        for j in instance_list:
            if (i < j) and ((i, j, 1) not in couples):
                singles.add((i, j, 0))
            if (i > j) and ((j, i, 1) not in couples):
                singles.add((j, i, 0))

    if STATE == 'Val':
        output = couples.union(singles)
        output = pd.DataFrame(output, columns=['left_instance_id', 'right_instance_id', 'label'])
    else:
        output = couples
        output = pd.DataFrame(output, columns=['left_instance_id', 'right_instance_id', 'label'])
        output.drop(columns=['label'], inplace=True)

    return output
