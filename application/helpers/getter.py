import uuid
import application.helpers.constant as C
import application.helpers.io as io


def site_path(site_id, method=None, sim_id=None, request=C.KEY_SITE_PATH):
    file_ext = ".json"
    site_path = C.STORAGE_PATH + "site_" + str(site_id) + "/"
    if request == C.KEY_SITE_PATH:
        return site_path
    if request == C.KEY_SITE_STORAGE_PATH:
        return site_path + "_".join([method, sim_id]) + "/"
    if request == C.KEY_SITE_INFO_FILE:
        return site_path + "site_info" + file_ext


def site_id(sitepath):
    return sitepath.split("/")[-3].split("_")[-1]


def grid_path(sitepath=None, site_id=None, request=C.KEY_GRID_PATH):
    file_ext = ".json"
    if site_id:
        sitepath = site_path(site_id)
    grid_path = sitepath + "grid/"
    if request == C.KEY_GRID_PATH:
        return grid_path
    if request == C.KEY_GRID_FILE:
        return grid_path + "grid" + file_ext
    if request == C.KEY_GRID_INFO_FILE:
        return grid_path + "grid_info" + file_ext


def rtree_path(sitepath=None, site_id=None, rtree_id=None, request=C.KEY_RTREE_PATH):
    file_ext = ".json"
    if site_id:
        sitepath = site_path(site_id)
    rtree_path = sitepath + "rtree/"
    if request == C.KEY_RTREE_PATH:
        return rtree_path
    if request == C.KEY_RTREE_FILE:
        return rtree_path + rtree_id + file_ext


def result_path(sitepath=None, site_id=None, request=C.RESULT_PATH, opt=None):
    file_ext = ".json"
    if site_id:
        sitepath = site_path(site_id)
    result_path = sitepath + "result/"
    if opt:
        if opt == "final":
            global_filename = "_".join([C.RESULT_GLOBAL_FILE, opt, ""])
        else:
            global_filename = "_".join([C.RESULT_GLOBAL_FILE, "after", "site", opt, ""])
    if request == C.RESULT_PATH:
        return result_path
    if request == C.RESULT_PRODUCT_FILE:
        if opt:
            return result_path + global_filename + C.PRODUCT + file_ext
        else:
            return result_path + C.PRODUCT + file_ext
    if request == C.RESULT_CUSTOMER_FILE:
        if opt:
            return result_path + global_filename + C.CUSTOMER + file_ext
        else:
            return result_path + C.CUSTOMER + file_ext
    if request == C.RESULT_MC_FILE:
        if opt:
            return result_path + global_filename + C.MC + file_ext
        else:
            return result_path + C.MC + file_ext


def dataset_path(sitepath=None, site_id=None, data_type=None, data_num=None, dim_size=None, label=None, request=C.KEY_DATASET_PATH):
    file_ext = ".csv"
    if site_id:
        sitepath = site_path(site_id)
    dataset_path = sitepath + "dataset/"
    if request == C.KEY_DATASET_PATH:
        return dataset_path
    if request == C.KEY_DATASET_FILE:
        return dataset_path + "_".join([data_type, str(data_num), str(dim_size), label]) + file_ext


def graph_path(sitepath=None, site_id=None, graph_type=None, opt=None):
    if site_id:
        sitepath = site_path(site_id)
    graph_path = C.GRAPH_PATH + graph_type + '/'
    if 'site_path' in locals():
        graph_path += sitepath
    if opt:
        graph_path += opt + '/'
    return graph_path


def simulation_name(method, data_type, data_num, dim_size, grid):
    if type(data_num) is list:
        data_num = "-".join([str(_) for _ in data_num])
    else:
        data_num = str(data_num)
    return "_".join([method, data_type, data_num, str(dim_size), str(grid)])


def simulation_id(method, data_type, data_num, dim_size, grid_size):
    sim_info = io.import_json(C.LOG_PATH, C.SIMULATION_INFO_FILE)
    sim_name = simulation_name(method, data_type, data_num, dim_size, grid_size)
    if sim_name in sim_info:
        # read sim id 
        sim_id = sim_info[sim_name]
    else:
        # generate new sim_id 
        sim_id = str(uuid.uuid4())
        sim_info[sim_name] = sim_id
        io.export_json(C.LOG_PATH, C.SIMULATION_INFO_FILE, sim_info)
    return sim_id


def log_name(sim_name, metrics, site_num, k):
    return "_".join([sim_name, str(metrics), str(site_num), str(k)])
