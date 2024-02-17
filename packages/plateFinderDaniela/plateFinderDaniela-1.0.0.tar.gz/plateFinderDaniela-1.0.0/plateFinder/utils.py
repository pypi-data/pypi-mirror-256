import pandas as pd

def get_data_from_excel():
    df = pd.read_excel('my_data.xlsx')
    data_dict = {}
    for index, row in df.iterrows():
        key = row['targa']
        value = row['name'] + ' ' + row['surname']
        data_dict[key] = value
    return data_dict