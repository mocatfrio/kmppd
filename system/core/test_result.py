import pandas as pd
import system.config.config as config
import application.helpers.constant as C
import application.helpers.io as io
import application.helpers.getter as getter
import application.helpers.log as log
from dotenv import load_dotenv

load_dotenv()


PARAM = config.get_scenario()

def generate():
    result = {
        'LP Cardinality': generate_logs(C.LOCAL_PRECOMPUTE, C.KEY_CARDINALITY),
        'LP Dimensionality': generate_logs(C.LOCAL_PRECOMPUTE, C.KEY_DIMENSIONALITY),
        'LP Grid Size': generate_logs(C.LOCAL_PRECOMPUTE, C.KEY_GRID),

        'GP Cardinality': generate_logs(C.GLOBAL_PRECOMPUTE, C.KEY_CARDINALITY),
        'GP Dimensionality': generate_logs(C.GLOBAL_PRECOMPUTE, C.KEY_DIMENSIONALITY),
        'GP Grid Size': generate_logs(C.GLOBAL_PRECOMPUTE, C.KEY_GRID),
        'GP Site Number': generate_logs(C.GLOBAL_PRECOMPUTE, C.KEY_SITE_NUM),

        'QP Cardinality': generate_logs(C.RUN_QUERY, C.KEY_CARDINALITY),
        'QP Dimensionality': generate_logs(C.RUN_QUERY, C.KEY_DIMENSIONALITY),
        'QP Grid Size': generate_logs(C.RUN_QUERY, C.KEY_GRID),
        'QP Site Number': generate_logs(C.RUN_QUERY, C.KEY_SITE_NUM),
        'QP K': generate_logs(C.RUN_QUERY, C.KEY_K),
    }
    io.export_excel(C.LOG_PATH, C.LOG_PATH + 'result.xlsx', result)


def generate_logs(opt, effect_of):
    # generate header columns
    columns = []
    for parameter in get_parameter(opt):
        columns.append((parameter, ''))
    for metric in get_metric(opt):
        for method in PARAM['method']:
            columns.append((convert(metric), convert(method)))

    header = pd.MultiIndex.from_tuples(columns)

    dynamic_val = get_manipulative_values(effect_of)
    # generate rows 
    rows = []
    for val in dynamic_val:
        for data_type in PARAM['dataset_type']:
            # value of parameters 
            cardinality = PARAM['const_cardinality']
            dimension = PARAM['const_dimension']
            grid_size = PARAM['const_grid_size']
            site_num = PARAM['const_site_num']
            k = PARAM['const_k']
            
            if effect_of == C.KEY_CARDINALITY:
                cardinality = val
            elif effect_of == C.KEY_DIMENSIONALITY:
                dimension = val
            elif effect_of == C.KEY_GRID:
                grid_size = val
            elif effect_of == C.KEY_SITE_NUM:
                site_num = val
            elif effect_of == C.KEY_K:
                k = val

            row = [data_type, cardinality, dimension, grid_size]
            if opt == C.GLOBAL_PRECOMPUTE:
                row += [site_num]
            elif opt == C.RUN_QUERY:
                row += [site_num, k]
            
            # read the logs
            for metric in get_metric(opt):
                for method in PARAM['method']:
                    sim_id = getter.simulation_id(method, data_type, cardinality,
                                                  dimension, grid_size,
                                                  read_only=True)
                    log_path = getter.log_path(sim_id)
                    result = log.read(metric, log_path, site_num, k)
                    row.append(result)
            rows.append(row)

    df = pd.DataFrame(rows, columns=header)
    return df


def get_parameter(opt):
    if opt == C.LOCAL_PRECOMPUTE:
        return ['Data type', 'Number of data', 'Dimension', 'Grid size']
    elif opt == C.GLOBAL_PRECOMPUTE:
        return ['Data type', 'Number of data', 'Dimension', 'Grid size', 'Number of sites']
    elif opt == C.RUN_QUERY:
        return ['Data type', 'Number of data', 'Dimension', 'Grid size', 'Number of sites', 'k']


def get_metric(opt):
    if opt == C.LOCAL_PRECOMPUTE:
        return [C.KEY_INDEX_TIME, C.KEY_LP_TIME, C.KEY_INDEX_MEM, C.KEY_LP_MEM]
    elif opt == C.GLOBAL_PRECOMPUTE:
        return [C.KEY_GP_TIME, C.KEY_GP_MEM]
    elif opt == C.RUN_QUERY:
        return [C.KEY_QUERY_TIME, C.KEY_QUERY_MEM]


def get_manipulative_values(effect_of):
    if effect_of == C.KEY_CARDINALITY:
        return PARAM['cardinality']
    elif effect_of == C.KEY_DIMENSIONALITY:
        return PARAM['dimension']
    elif effect_of == C.KEY_GRID:
        return PARAM['grid_size']
    elif effect_of == C.KEY_SITE_NUM:
        return PARAM['site_num']
    elif effect_of == C.KEY_K:
        return PARAM['k']


def convert(key):
    convert = {
        C.KMPPD: 'KMPPD',
        C.OKMPPD: 'Optimized KMPPD',
        C.KEY_INDEX_TIME: 'Indexing Time',
        C.KEY_LP_TIME: 'Local Precomputing Time',
        C.KEY_GP_TIME: 'Global Precomputing Time',
        C.KEY_QUERY_TIME: 'Query Time',
        C.KEY_INDEX_MEM: 'Indexing Memory Usage',
        C.KEY_LP_MEM: 'Local Precomputing Memory Usage',
        C.KEY_GP_MEM: 'Global Precomputing Memory Usage',
        C.KEY_QUERY_MEM: 'Query Memory Usage',
    }
    return convert.get(key, None)

