import os
from dotenv import load_dotenv

load_dotenv()

# path 
APP_PATH = os.getenv("BASE_PATH") + 'application/' 
SYSTEM_PATH = os.getenv("BASE_PATH") + 'system/' 
GRAPH_PATH = SYSTEM_PATH + 'graph/' 
STORAGE_PATH = SYSTEM_PATH + 'database/' 
LOG_PATH = APP_PATH + "logs/"
SIMULATION_INFO_FILE = LOG_PATH + "simulation" + ".json"
# ACCURACY_PATH = os.getenv("STORAGE_PATH") + "accuracy/"

# dataset 
FC = "fc"
ANT = "ant"
IND = "ind"

# method
KMPPD = "kmppd"
OKMPPD = 'optimized_kmppd'
NAIVE = "naive"

# keys 
PRODUCT = "product"
CUSTOMER = "customer"
ID = "id"
VAL = "val"
LABEL = "label"
POS = "pos"
SITE_ID = "site_id"
ORTHANT_ID = "orthant_id"

ADR = "anti_dominance_region"
ORTHANT = "orthant"
OSKY = "orthant_skyline"
DSKY = "dynamic_skyline"
HISTORY_DSKY = "dynamic_skyline_history"
RSKY = "reverse_skyline"
TRUE_RSKY = "true_reverse_skyline"
UPDATED_RSKY = "reverse_skyline_update"
MC = "market_contribution"

# site keys 
IS_DONE = "is_done"

# grid keys 
GRID_BOUNDARY = "boundary"
GRID_RTREE = "rtree"
GRID_SIZE = "size"

# keywords  
KEY_SITE_PATH = "site_path"
KEY_SITE_STORAGE_PATH = "site_storage_path"
KEY_SITE_INFO_FILE = "site_info_file"
KEY_DATASET_PATH = "dataset_path"
KEY_DATASET_FILE = "dataset_file"
KEY_GRID_PATH = "grid_path"
KEY_GRID_FILE = "grid_file"
KEY_GRID_INFO_FILE = "grid_info_file"
KEY_RTREE_PATH = "grid_path"
KEY_RTREE_FILE = "grid_file"
KEY_GRAPH_PATH = "graph_path"
KEY_GRAPH_TYPE_PATH = "graph_type_path"

# keywords of effect
KEY_SITE_NUM = 'site_num'
KEY_DATA_NUM = 'data_num'
KEY_DIM = 'dim_size'
KEY_GRID = 'grid_size'
KEY_K = 'k_size'

# keywords of metrics
KEY_INDEX_TIME = 'index_time'
KEY_LP_TIME = 'local_processing_time'
KEY_QUERY_TIME = 'query_time'
KEY_INDEX_MEM = 'index_mem' 
KEY_LP_MEM = 'local_processing_mem'
KEY_BANDWITH_COST = 'bandwith'

# result keys
RESULT_PATH = "result_path"
RESULT_PRODUCT_FILE = "result_product_file"
RESULT_CUSTOMER_FILE = "result_customer_file"
RESULT_MC_FILE = "result_market_contribution_file"
RESULT_GLOBAL_FILE = "result_global"

# bounding box 
MIN = 0
MAX = 1

# mode
CREATE = "create"
UPDATE = "update"

# skyline
GRID_POS = 0
GRID_BOX = 1
OBJ = 0
DIFF = 1
IS_DOMINATED = 2