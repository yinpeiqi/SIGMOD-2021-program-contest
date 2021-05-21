import pandas as pd
from handler_x2 import handle_x2
from handler_x3 import handle_x3
from handler_x4 import handle_x4

Flag = True

if __name__ == '__main__':
    for file_name in ['data/X2.csv', 'data/X3.csv', 'data/X4.csv']:
        data = pd.read_csv(file_name)
        if 'name' not in data.columns:
            if 'source' not in data.filter(
                    ['instance_id']).sample(1).values[0][0]:
                output = handle_x2(data)
            else:
                output = handle_x3(data)
        else:
            output = handle_x4(data)

        if Flag:
            output.to_csv("output.csv", sep=',', encoding='utf-8', index=False)
            Flag = False
        else:
            output.to_csv(
                "output.csv",
                mode='a',
                sep=',',
                encoding='utf-8',
                index=False,
                header=None)
