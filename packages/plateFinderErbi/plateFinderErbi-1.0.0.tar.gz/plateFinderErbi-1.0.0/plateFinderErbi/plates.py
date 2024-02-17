import pandas as pd

rd = pd.read_excel('my_data.xlsx')

data = {}


def get_data_from_exel():
    person = input('Enter a name: ')
    for index, row in rd.iterrows():
        key = row['name']
        value = row['targa']
        data[key] = value
    result = data.get(person, None)

    if result is not None:
        print(f'This persons license plate is {data[person]}')
    else:
        print('Person not found')


get_data_from_exel()

