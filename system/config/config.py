import os
from dotenv import load_dotenv
import application.helpers.constant as C

load_dotenv()

def get_scenario():
    parameter = {
        'cardinality': [500, 1000, 2000, 5000, 10000],
        'const_cardinality': 5000,
        'dimension': [2, 3, 4],
        'const_dimension': 3,
        'grid_size': [3, 4, 5, 6, 7],
        'const_grid_size': 5,
        'site_num': [2, 3, 4, 5, 6],
        'const_site_num': 4,
        'k': [10, 20, 30, 40, 50],
        'const_k': 30,
        'dataset_type': [C.IND, C.ANT, C.FC],
        'method': [C.KMPPD, C.OKMPPD, C.NAIVE]
    }
    
    if os.getenv("ENV") == 'dev':
        parameter['cardinality'] = [100, 500, 1000]
        parameter['const_cardinality'] = 500
        parameter['site_num'] = [2, 3]
        parameter['const_site_num'] = 3

    return parameter
