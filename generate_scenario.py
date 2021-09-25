from os import listdir, getenv, remove
from os.path import isfile, join
from dotenv import load_dotenv
import application.helpers.constant as C

load_dotenv()


CARDINALITY = [500, 1000, 2000, 5000, 10000]
CONST_CARDINALITY = 5000
DIMENSIONALITY = [2, 3, 4]
CONST_DIMENSIONALITY = 3
GRID_SIZE = [3, 4, 5, 6, 7]
CONST_GRID_SIZE = 5
SITE_NUM = [2, 3, 4, 5, 6]
CONST_SITE_NUM = 4
K = [10, 20, 30, 40, 50]
CONST_K = 30
DATASET_TYPE = [C.IND, C.ANT, C.FC]
METHOD = [C.KMPPD, C.OKMPPD, C.NAIVE]



def delete_script():
    files = [f for f in listdir(getenv("BASE_PATH")) if isfile(join(getenv("BASE_PATH"), f))]
    for f in files:
        if (f[-3:] == '.sh') and (f != 'dev.sh'):
            remove(f)
            print(f, 'is succesfully deleted!')


def generate_script_to_generate_dataset():
    rows = [
        '#! /bin/bash',
        '',
        '# GENERATE DATA',
        '# python3 index.py -o generate_dataset -s <site_num> -t <dataset_type> -n <data_num> -d <dim_size>',
        '',
        '# example:',
        '# python3 index.py -o generate_dataset -s 6 -t ind -n 500 -d 2',
        ''
    ]
    
    number_of_scenario = 0
    for dt in DATASET_TYPE:
        for dim in DIMENSIONALITY:
            for num in CARDINALITY:
                row = 'python3 index.py -o generate_dataset -s ' + str(max(SITE_NUM)) + ' -t ' + dt + ' -n ' + str(num) + ' -d ' + str(dim)
                number_of_scenario += 1
                rows.append(row)
            rows.append('')
        rows.append('')
    
    filename = 'generate_dataset.sh'
    with open (filename, 'w') as rsh:
        for row in rows:
            rsh.writelines(row + '\n')
    print('Script', filename, 'containing', number_of_scenario, 'scenarios is successfully created!')


def generate_script_to_local_processing(param):
    for method in METHOD:
        if method == 'naive':
            continue
        rows = [
            '#! /bin/bash',
            '',
            '# LOCAL PROCESSING',
            '# python3 index.py -o precompute -s <site_num> -t <dataset_type> -n <data_num> -d <dim_size> -m <method> -g <grid_size>',
            '',
            '# example:',
            '# python3 index.py -o precompute -s 3 -t ind -n 500 -d 2 -m kmppd -g 5',
            ''
        ]
        if param == 1:
            rows.append('# CARDINALITY')
        elif param == 2:
            rows.append('# DIMENSIONALITY')
        elif param == 3:
            rows.append('# GRID SIZE')

        number_of_scenario = 0
        for dt in DATASET_TYPE:
            vals = get_manipulation_val(param)
            for val in vals:
                if param == 1:
                    row = 'python3 index.py -o precompute -s ' + str(max(SITE_NUM)) + ' -t ' + dt + ' -n ' + str(val) + ' -d ' + str(CONST_DIMENSIONALITY) + ' -m ' + method + ' -g ' + str(CONST_GRID_SIZE)
                elif param == 2:
                    row = 'python3 index.py -o precompute -s ' + str(max(SITE_NUM)) + ' -t ' + dt + ' -n ' + str(CONST_CARDINALITY) + ' -d ' + str(val) + ' -m ' + method + ' -g ' + str(CONST_GRID_SIZE)
                elif param == 3:
                    row = 'python3 index.py -o precompute -s ' + str(max(SITE_NUM)) + ' -t ' + dt + ' -n ' + str(CONST_CARDINALITY) + ' -d ' + str(CONST_DIMENSIONALITY) + ' -m ' + method + ' -g ' + str(val)
                number_of_scenario += 1
                rows.append(row)
            rows.append('')
        
        filename = '_'.join(['local_processing', method, get_key(param)]) + '.sh'
        with open (filename, 'w') as rsh:
            for row in rows:
                rsh.writelines(row + '\n')
        print('Script', filename, 'containing', number_of_scenario, 'scenarios is successfully created!')


def get_manipulation_val(param):
    if param == 1:
        return CARDINALITY
    elif param == 2:
        return DIMENSIONALITY
    elif param == 3:
        return GRID_SIZE


def get_key(param):
    if param == 1:
        return 'cardinality'
    elif param == 2:
        return 'dimensionality'
    elif param == 3:
        return 'grid_size'


if __name__ == '__main__':
    print('Commands:')
    print('1. Delete script sh')
    print('2. Generate dataset')
    print('3. Local processing')
    command = int(input('Choose command: '))

    if command == 1:
        delete_script()
    if command == 2:
        generate_script_to_generate_dataset()
    elif command == 3:
        print('Parameters:')
        print('1. Cardinality of data')
        print('2. Dimensionality of data')
        print('3. Grid size')
        param = int(input('Choose parameter: '))

        generate_script_to_local_processing(param)


