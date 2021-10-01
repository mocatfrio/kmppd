import os
from dotenv import load_dotenv
import application.helpers.constant as C
import application.helpers.io as io
import system.config.config as config

load_dotenv()

PARAM = config.get_scenario()

if os.getenv("ENV") == 'dev':
    FILENAME = 'dev_'
else:
    FILENAME = ''


def generate():
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


def delete_script():
    files = io.list_files(os.getenv("BASE_PATH"), only_file=True)
    for f in files:
        if os.getenv("ENV") == 'dev':
            need_to_delete = (f[-3:] == '.sh') and ('dev' in f)
        else:
            need_to_delete = (f[-3:] == '.sh') and (not 'dev' in f)

        if need_to_delete:
            io.delete_file(f)
            print(f, 'is succesfully deleted!')


def generate_script_to_generate_dataset():
    command = C.GEN_DATASET
    rows = [
        '#! /bin/bash',
        '',
        '# GENERATE DATA',
        '# python3 index.py -o ' + command + ' -s <site_num> -t <dataset_type> -n <data_num> -d <dim_size>',
        '',
        '# example:',
        '# python3 index.py -o ' + command + ' -s 6 -t ind -n 500 -d 2',
        ''
    ]
    number_of_scenario = 0
    for dt in PARAM['dataset_type']:
        for dim in PARAM['dimension']:
            for num in PARAM['cardinality']:
                row = 'python3 index.py -o ' + command + ' -s ' + str(max(PARAM['site_num'])) + ' -t ' + dt + ' -n ' + str(num) + ' -d ' + str(dim)
                number_of_scenario += 1
                rows.append(row)
            rows.append('')
        rows.append('')
    
    filename = FILENAME + 'generate_dataset.sh'
    with open (filename, 'w') as rsh:
        for row in rows:
            rsh.writelines(row + '\n')
    print('Script', filename, 'containing', number_of_scenario, 'scenarios is successfully created!')


def generate_script_to_local_processing(param):
    command = C.PRECOMPUTE
    for method in PARAM['method']:
        if method == 'naive':
            continue
        rows = [
            '#! /bin/bash',
            '',
            '# LOCAL PROCESSING',
            '# python3 index.py -o ' + command + ' -s <site_num> -t <dataset_type> -n <data_num> -d <dim_size> -m <method> -g <grid_size>',
            '',
            '# example:',
            '# python3 index.py -o ' + command + ' -s 3 -t ind -n 500 -d 2 -m kmppd -g 5',
            ''
        ]
        if param == 1:
            rows.append('# CARDINALITY')
        elif param == 2:
            rows.append('# DIMENSIONALITY')
        elif param == 3:
            rows.append('# GRID SIZE')

        number_of_scenario = 0
        for dt in PARAM['dataset_type']:
            vals = PARAM[get_key(param)]
            for val in vals:
                if param == 1:
                    row = 'python3 index.py -o ' + command + ' -s ' + str(max(PARAM['site_num'])) + ' -t ' + dt + ' -n ' + str(val) + ' -d ' + str(PARAM['const_dimension']) + ' -m ' + method + ' -g ' + str(PARAM['const_grid_size'])
                elif param == 2:
                    row = 'python3 index.py -o ' + command + ' -s ' + str(max(PARAM['site_num'])) + ' -t ' + dt + ' -n ' + str(PARAM['const_cardinality']) + ' -d ' + str(val) + ' -m ' + method + ' -g ' + str(PARAM['const_grid_size'])
                elif param == 3:
                    row = 'python3 index.py -o ' + command + ' -s ' + str(max(PARAM['site_num'])) + ' -t ' + dt + ' -n ' + str(PARAM['const_cardinality']) + ' -d ' + str(PARAM['const_dimension']) + ' -m ' + method + ' -g ' + str(val)
                number_of_scenario += 1
                rows.append(row)
            rows.append('')
        
        filename = FILENAME + '_'.join(['local_processing', method, get_key(param)]) + '.sh'
        with open (filename, 'w') as rsh:
            for row in rows:
                rsh.writelines(row + '\n')
        print('Script', filename, 'containing', number_of_scenario, 'scenarios is successfully created!')


def get_key(param):
    if param == 1:
        return 'cardinality'
    elif param == 2:
        return 'dimension'
    elif param == 3:
        return 'grid_size'

