import pandas as pd
import sys
import system.config.config as config
import application.helpers.constant as C
import application.helpers.io as io
import application.helpers.getter as getter
from dotenv import load_dotenv

load_dotenv()


PARAM = config.get_scenario()
METHOD = ['KMPPD', 'Optimized KMPPD']

def generate():
    result = {
        'Local Precomputing - Cardinality': cardinality(C.LOCAL_PRECOMPUTE),
        'Global Precomputing - Cardinality': cardinality(C.GLOBAL_PRECOMPUTE),
        'Query Processing - Cardinality': cardinality(C.RUN_QUERY),
    }
    

    # io.export_excel(C.STORAGE_PATH, 'result.xlsx', result)


def getParameter(opt):
    if opt == C.LOCAL_PRECOMPUTE:
        return ['Data type', 'Number of data', 'Dimension', 'Grid size']
    elif opt == C.GLOBAL_PRECOMPUTE:
        return ['Data type', 'Number of data', 'Dimension', 'Grid size', 'Number of sites']
    elif opt == C.RUN_QUERY:
        return ['Data type', 'Number of data', 'Dimension', 'Grid size', 'Number of sites', 'k']
    
def getMetric(opt):
    if opt == C.LOCAL_PRECOMPUTE:
        return ['Indexing time', 'Local precomputing time', 'Memory usage for indexing', 'Memory usage for local precomputing']
    elif opt == C.GLOBAL_PRECOMPUTE:
        pass
    elif opt == C.RUN_QUERY:
        pass

def cardinality(opt):
    # generate header columns
    columns = []
    for parameter in getParameter(opt):
        columns.append((parameter, ''))
    for metric in getMetric(opt):
        for method in METHOD:
            columns.append((metric, method))

    header = pd.MultiIndex.from_tuples(columns)

    # generate rows 
    rows = []
    for i in range(len(PARAM['cardinality'])):
        for data_type in PARAM['dataset_type']:
            # value of parameters 
            row = [data_type, PARAM['cardinality'][i], PARAM['const_dimension'], PARAM['const_grid_size']]
            if opt == C.GLOBAL_PRECOMPUTE:
                row.append(PARAM['const_site_num'])
            elif opt == C.RUN_QUERY:
                row.append(PARAM['const_k'])
            
            # get the result
            # get simulation id 
            sim_id = []
            for method in PARAM['method']:
                sim_id.append(getter.simulation_id(method, data_type, PARAM['cardinality'][i], 
                                                     PARAM['const_dimension'], PARAM['const_grid_size'],
                                                     custom_log_path=C.LOG_PROD_PATH, read_only=True))

            # read the logs
            for metric in getMetric(opt):
                pass
            
            print(row)
            print(sim_id)

            row += [0,0,0,0,0,0,0,0]
            rows.append(row)

    df = pd.DataFrame(rows,
                      columns=header)
    print(df)


