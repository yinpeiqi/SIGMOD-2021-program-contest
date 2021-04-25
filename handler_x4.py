import pandas as pd
from clean_x4 import clean_x4

solved_spec = []
unsolved_spec = []

instance_list = set()

model_2_type = {"3502450": "rainbow", "3502460": "rainbow", "3502470": "rainbow", "3502480": "rainbow",
                "3502490": "rainbow", "3502491": "rainbow",
                "3503460": "basic", "3503470": "basic", "3503480": "basic", "3503490": "basic",
                "3533470": "speed", "3533480": "speed", "3533490": "speed", "3533491": "speed", "3533492": "speed",
                "3534460": "premium", "3534470": "premium", "3534480": "premium", "3534490": "premium",
                "3534491": "premium",
                "3521451": "alu", "3521452": "alu", "3521452": "alu", "3521462": "alu", "3521471": "alu",
                "3521472": "alu", "3521481": "alu", "3521482": "alu", "3521480": "alu", "3521491": "alu",
                "3521492": "alu",
                "3511460": "business", "3511470": "business", "3511480": "business", "3511490": "business",
                "3500450": "micro", "3500460": "micro", "3500470": "micro", "3500480": "micro",
                "3523460": "mobile", "3523470": "mobile", "3523480": "mobile",
                "3524460": "mini", "3524470": "mini", "3524480": "mini",
                "3531470": "ultra", "3531480": "ultra", "3531490": "ultra", "3531491": "ultra", "3531492": "ultra",
                "3531493": "ultra",
                "3532460": "slim", "3532470": "slim", "3532480": "slim", "3532490": "slim", "3532491": "slim",
                "3537490": "highspeed", "3537491": "highspeed", "3537492": "highspeed",
                "3535580": "imobile", "3535590": "imobile",
                "3536470": "cmobile", "3536480": "cmobile", "3536490": "cmobile",
                "3538480": "flash", "3538490": "flash", "3538491": "flash"}

sony_capacity_single = ["1tb", "256gb"]
sony_capacity_memtype_type = ["32gb", "4gb"]


def handle_x4(dataset: pd.DataFrame, STATE='Test'):
    dataset = clean_x4(dataset)
    for index, row in dataset.iterrows():
        instance_id = row['instance_id']
        brand = row['brand']
        capacity = row['capacity']
        mem_type = row['mem_type']
        type = row['type']
        model = row['model']
        item_code = row['item_code']
        title = row['title']
        pc = {}

        if type == '0' and brand == "intenso" and model in model_2_type.keys():
            type = model_2_type[model]

        pc['id'] = instance_id
        pc['title'] = title
        pc['brand'] = brand
        pc['capacity'] = capacity
        pc['mem_type'] = mem_type
        pc['type'] = type
        pc['model'] = model
        pc['item_code'] = item_code

        if brand == 'lexar':
            if capacity!= '0' and type!='0'and mem_type!='0':
                pc['identification'] = brand + ' ' + capacity + ' ' + mem_type + ' '+ type
                solved_spec.append(pc)
            else:
                unsolved_spec.append(pc)

        elif brand == 'sony':
            if mem_type == "microsd" and capacity!='0':
                pc['identification'] = brand + ' ' + capacity
                solved_spec.append(pc)
            elif mem_type!='0' and capacity!='0' and type!='0':
                pc['identification'] = brand + ' ' + capacity + ' ' + mem_type + ' ' + type
                solved_spec.append(pc)
            else:
                unsolved_spec.append(pc)

        elif brand == 'sandisk':
            if capacity!='0' and mem_type!='0':
                pc['identification'] = brand + ' ' + capacity + ' ' + mem_type + ' ' + model
                solved_spec.append(pc)
            else:
                unsolved_spec.append(pc)

        elif brand == 'pny':
            if capacity!='0' and mem_type!='0' and type!='0':
                pc['identification'] = brand + ' ' + capacity + ' ' + mem_type + ' ' + type
                solved_spec.append(pc)
            else:
                unsolved_spec.append(pc)

        elif brand == 'intenso':
            if capacity!='0' and type!='0':
                pc['identification'] = brand + ' ' + capacity + ' ' + type
                solved_spec.append(pc)
            else:
                unsolved_spec.append(pc)

        elif brand == 'kingston':
            if mem_type == '0' and 'data' in model:
                mem_type = 'usb'
            if mem_type!='0' and capacity!='0':
                pc['identification'] = brand + ' ' + capacity + ' ' + mem_type
                solved_spec.append(pc)
            else:
                unsolved_spec.append(pc)

        elif brand == 'samsung':
            if capacity == '0' and type!='0' and model!='0':  # tv
                pc['identification'] = brand + ' ' + type + ' ' + model
                solved_spec.append(pc)
            elif mem_type == '0' and capacity!='0' and type!='0' and model!='0':  # phone
                pc['identification'] = brand + ' ' + capacity + ' ' + type + ' ' + model
                solved_spec.append(pc)
            elif mem_type!='0' and capacity!='0':
                pc['identification'] = brand + ' ' + capacity + ' ' + mem_type
                solved_spec.append(pc)
            else:
                unsolved_spec.append(pc)

        elif brand == 'toshiba':
            if capacity!='0':
                pc['identification'] = brand + ' ' + capacity + ' ' + model
                solved_spec.append(pc)
            else:
                unsolved_spec.append(pc)

        elif brand == 'transcend':
            if capacity!='0' and mem_type!='0':
                pc['identification'] = brand + ' ' + capacity + ' ' + mem_type
                solved_spec.append(pc)
            else:
                unsolved_spec.append(pc)

        else:
            if brand!='0' and capacity!='0' and mem_type!='0':
                pc['identification'] = brand + ' ' + capacity + ' ' + mem_type
                solved_spec.append(pc)
            else:
                unsolved_spec.append(pc)

        instance_list.add(instance_id)

    unsolved_spec_cp = unsolved_spec.copy()
    solved_spec_cp = solved_spec.copy()

    for u in unsolved_spec_cp:
        for s in solved_spec_cp:
            if u['item_code'] != '0' and u['item_code'] == s['item_code']:
                u['identification'] = s['identification']
                solved_spec.append(u)
                unsolved_spec.remove(u)

    unsolved_spec_cp = unsolved_spec.copy()
    solved_spec_cp = solved_spec.copy()

    # for u in unsolved_spec_cp:
    #     if u['brand'] == 'intenso':
    #         pass
    #     elif u['brand'] == 'lexar':
    #         pass
    #     elif u['brand'] == 'sony':
    #         pass
    #     elif u['brand'] == 'sandisk':
    #         pass
    #     elif u['brand'] == 'pny':
    #         pass
    #     elif u['brand'] == 'kingston':
    #         pass
    #     elif u['brand'] == 'samsung':
    #         pass
    #     elif u['brand'] == 'toshiba':
    #         pass
    #     elif u['brand'] == 'transcend':
    #         pass

    for u in unsolved_spec_cp:
        if u['brand'] == 'sandisk':
            continue
        for s in solved_spec_cp:
            if u['brand'] != '0' and u['capacity'] != '0' and u['mem_type'] != '0' and u['type'] != '0':
                if u['brand'] == s['brand'] and u['capacity'] == s['capacity'] and u['mem_type'] == s['mem_type'] and u['type'] == s['type']:
                    u['identification'] = s['identification']
                    solved_spec.append(u)
                    break
            elif u['brand'] != '0' and u['capacity'] != '0' and u['mem_type'] != '0' and u['model'] != '0':
                if u['brand'] == s['brand'] and u['capacity'] == s['capacity'] and u['mem_type'] == s['mem_type'] and u['model'] == s['model']:
                    u['identification'] = s['identification']
                    solved_spec.append(u)
                    break
            elif u['brand'] != '0' and u['capacity'] != '0' and u['type'] != '0' and u['model'] != '0':
                if u['brand'] == s['brand'] and u['capacity'] == s['capacity'] and u['type'] == s['type'] and u['model'] == s['model']:
                    u['identification'] = s['identification']
                    solved_spec.append(u)
                    break
            elif u['brand'] != '0' and u['capacity'] != '0' and u['mem_type'] != '0':
                if u['brand'] == s['brand'] and u['capacity'] == s['capacity'] and u['mem_type'] == s['mem_type']:
                    u['identification'] = s['identification']
                    solved_spec.append(u)
                    break
            elif u['brand'] != '0' and u['capacity'] != '0' and u['type'] != '0':
                if u['brand'] == s['brand'] and u['capacity'] == s['capacity'] and u['type'] == s['type']:
                    u['identification'] = s['identification']
                    solved_spec.append(u)
                    break

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
