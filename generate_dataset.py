import pandas as pd

if __name__ == '__main__':
    LXdata = pd.read_csv('./test/cleanX2.csv')
    RXdata = pd.read_csv('./test/cleanX2.csv')
    # LXdata = LXdata.drop(
    #     ["brand", "cpu_brand", "cpu_model", "cpu_type", "cpu_frequency", "ram_capacity", "ram_type", "ram_frequency",
    #      "hdd_capacity", "ssd_capacity", "weight", "dimensions"], axis=1)
    # RXdata = RXdata.drop(
    #     ["brand", "cpu_brand", "cpu_model", "cpu_type", "cpu_frequency", "ram_capacity", "ram_type", "ram_frequency",
    #      "hdd_capacity", "ssd_capacity", "weight", "dimensions"], axis=1)
    Ydata = pd.read_csv('./data/Y2.csv')

    for col in LXdata.columns:
        LXdata.rename({col: 'left_' + col}, axis='columns', inplace=True)
        RXdata.rename({col: 'right_' + col}, axis='columns', inplace=True)
    data = pd.merge(Ydata, LXdata, left_on=['left_instance_id'], right_on=['left_instance_id'], how='left')
    data = pd.merge(data, RXdata, left_on=['right_instance_id'], right_on=['right_instance_id'], how='left')
    data.drop(['right_instance_id', 'left_instance_id'], axis=1)

    train_data = data.sample(frac=0.9, axis=0)
    test_data = data[~data.index.isin(train_data.index)]
    validate_data = data.sample(frac=(0.01 / 0.9), axis=0)
    train_data = train_data[~train_data.index.isin(validate_data.index)]
    train_data.to_csv("train.csv", sep=',', encoding='utf-8')
    test_data.to_csv("test.csv", sep=',', encoding='utf-8')
    validate_data.to_csv("validation.csv", sep=',', encoding='utf-8')
