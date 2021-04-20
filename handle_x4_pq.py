import pandas as pd
from clean_x4 import clean_x4


map = {}

def judge(ins):
    brand = ins['brand']
    capacity = ins['capacity']
    model = ins['model']
    type = ins['type']
    type2 = ins['type2']
    mem_type = ins['mem_type']
    id = brand + capacity
    if brand == 'intenso':
        if capacity == '8gb' and type == 'speed':
            return id + mem_type + type
        return id

    elif brand == 'lexar':
        if capacity == '128gb':
            return id + mem_type + type

        elif capacity == '64gb':
            return id + mem_type + type

        elif capacity == '32gb':
            return id + mem_type + type

        elif capacity == '16gb':
            return id + mem_type + type

        elif capacity == '8gb':
            if mem_type == 'sd' and (type == '0' or type == '300'):
                return id + mem_type + '300'
            return id + mem_type + type

        return id + mem_type + type



    elif brand == 'sony':
        if capacity == '1tb':
            return id + mem_type

        if capacity == '512gb':
            return id + mem_type

        if capacity == '256gb':
            return id

        if capacity == '128gb':
            return id + mem_type

        if capacity == '64gb':
            return id + mem_type

        if capacity == '32gb':
            if type == 'usmqx':
                return id + '1'
            elif type == 'usmr' or mem_type == 'usb':
                return id + '3'
            return id + type + mem_type

        if capacity == '16gb':
            return id + mem_type

        if capacity == '8gb':
            return id + mem_type

        if capacity == '4gb':
            if type == 'usmr':
                return id + '1'
            return id + mem_type

        return id + mem_type + type + model


    elif brand == 'sandisk':

        if capacity == '256gb':
            return id + mem_type + model

        elif capacity == '128gb':
            return id + mem_type + model

        elif capacity == '64gb':
            return id + mem_type + model

        elif capacity == '32gb':
            if model == 'ultra' and mem_type == 'microsd' \
                    or model == 'ext' and mem_type == 'sd'\
                    or model == 'ext' and mem_type == 'microsd':
                return id + '3'
            return id + model + mem_type

        elif capacity == '16gb':
            if model == 'ultra':
                return id + mem_type
            return id + model + mem_type

        elif capacity == '8gb':
            return id + model + mem_type

        elif capacity == '4gb':
            return id + model + mem_type

        return id + mem_type + type + model


    elif brand == 'pny':
        return id + mem_type

    elif brand == 'kingston':
        if capacity == '256gb':
            return id + mem_type

        elif capacity == '128gb':
            return id + mem_type + type2

        elif capacity == '64gb':
            return id + type2 + mem_type

        elif capacity == '32gb':
            return id + type2 + mem_type

        elif capacity == '16gb':
            if type == 'sdca3':
                return id + mem_type + type
            return id + mem_type

        elif capacity == '8gb':
            return id + mem_type

        elif capacity == '4gb':
            return id + mem_type

        return id + mem_type + type + model


    elif brand == 'samsung':
        if mem_type == 'sim':
            return id + mem_type + model + type
        elif mem_type in ('hd', 'qled', 'uhd'):
            return id + mem_type + model + type
        else:
            return id + mem_type + model


    elif brand == 'toshiba':
        if capacity == '128gb':
            if model == 'n401':
                return id + '1'
            elif model == 'u202':
                return id + '2'
            elif model == 'n302':
                return id + '3'
            elif mem_type == 'sd' and (model == '0' or model == 'n101'):
                return id + '4'
            elif mem_type == 'usb' and (model == '0' or model == 'n101'):
                return id + '5'
            return id + model + mem_type

        elif capacity == '64gb':
            return id + mem_type + model

        elif capacity == '32gb':
            if model == 'n401':
                return id + '1'
            elif mem_type == 'sd' and (model == '0' or model == 'n101'):
                return id + '2'
            return id + mem_type + model

        elif capacity == '16gb':
            return id + mem_type + model

        elif capacity == '8gb':
            if model == 'u302':
                return id + '1'
            elif mem_type == 'usb':
                return id + mem_type
            return id + mem_type + model

        return id + mem_type + type + model

    elif brand == 'transcend':
        return id + mem_type


def handle_x4_pq(data: pd.DataFrame):
    data = clean_x4(data)

    instance_list = []
    for index, row in data.iterrows():
        instance_id = row['instance_id']
        brand = row['brand']
        capacity = row['capacity']
        mem_type = row['mem_type']
        type = row['type']
        type2 = row['type2']
        model = row['model']
        item_code = row['item_code']
        title = row['title']

        idx = judge({
            'brand': brand,
            'capacity': capacity,
            'mem_type': mem_type,
            'type': type,
            'type2': type2,
            'model': model
        })

        instance_list.append({'instance_id': instance_id, 'idx': idx})

    couples = set()
    singles = set()
    for i in range(len(instance_list)):
        for j in range(i+1, len(instance_list)):
            if instance_list[i]['idx'] == instance_list[j]['idx']:
                couples.add((instance_list[i]['instance_id'], instance_list[j]['instance_id'], 1))
            else:
                singles.add((instance_list[i]['instance_id'], instance_list[j]['instance_id'], 0))

    STATE = 'Val'
    if STATE == 'Val':
        output = couples.union(singles)
        output = pd.DataFrame(output, columns=['left_instance_id', 'right_instance_id', 'label'])
    else:
        output = couples
        output = pd.DataFrame(output, columns=['left_instance_id', 'right_instance_id', 'label'])
        output.drop(columns=['label'], inplace=True)
    return output