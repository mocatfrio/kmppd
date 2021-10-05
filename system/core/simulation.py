import application.helpers.constant as C
import application.helpers.io as io
import application.helpers.getter as getter
import application.helpers.helper as helper
import application.core.kmppd as kmppd
from application.helpers.logger import Logger
from application.classes.site import Site


def local_precompute(site_num, method, data_type, data_num, dim_size, grid_size):
    # get simulation id 
    sim_id = getter.simulation_id(method, data_type, data_num,
                                  dim_size, grid_size)
    
    # init logger 
    log = Logger(site_num=site_num, method=method,
                 data_type=data_type, data_num=data_num,
                 dim_size=dim_size, grid_size=grid_size,
                 sim_id=sim_id)

    # local processing 
    log.write(method, 'Start Local Processing', with_info=False)
    sites = local_processing(site_num, method, data_type, data_num, dim_size, grid_size, log, sim_id)
    log.write(method, 'End Local Processing', with_info=False)


def global_precompute(site_num, method, data_type, data_num, dim_size, grid_size):
    # get simulation id 
    sim_id = getter.simulation_id(method, data_type, data_num,
                                  dim_size, grid_size)

    # init logger 
    log = Logger(site_num=site_num, method=method,
                 data_type=data_type, data_num=data_num,
                 dim_size=dim_size, grid_size=grid_size,
                 sim_id=sim_id)

    # local processing 
    log.write(method, 'Start Global Processing', with_info=False)
    global_result = global_processing(site_num, method, data_type, data_num, dim_size, grid_size, log, sim_id)
    log.write(method, 'End Global Processing', with_info=False)


def run_query(k, site_num, method, data_type, data_num, dim_size, grid_size):
    # get simulation id 
    sim_id = getter.simulation_id(method, data_type, data_num,
                                  dim_size, grid_size)

    # init logger 
    log = Logger(site_num=site_num, k=k, method=method,
                 data_type=data_type, data_num=data_num,
                 dim_size=dim_size, grid_size=grid_size,
                 sim_id=sim_id)

    # run query 
    if method == C.NAIVE:
        result = naive_approach(k, site_num, method, data_type, data_num,
                                dim_size, grid_size, log, sim_id)
    else:
        result = strategic_approach(k, site_num, method, data_type, data_num,
                                    dim_size, grid_size, log, sim_id)

    # save the result 
    result_path = C.LOG_PATH + sim_id + "/"
    result_filename = result_path + "query_result_" + str(k) + ".json"
    io.export_json(result_path, result_filename, result)


def strategic_approach(k, site_num, method, data_type, data_num, dim_size, grid_size, log, sim_id):
    # query processing
    log.write(method, 'Start Query Processing', with_info=False)
    log.start()
    global_result = global_processing(site_num, method, data_type, data_num, dim_size, grid_size, log, sim_id)
    candidates = helper.sort_dict(global_result, k)
    log.end(method, "End Query Processing")
    return candidates


def local_processing(site_num, method, data_type, data_num, dim_size, grid_size, log, sim_id):
    # init sites and local processing
    sites = {}
    for i in range(1, site_num + 1):
        sites[i] = Site(site_id=i, log=log, sim_id=sim_id)
        if sites[i].is_local_precomputed(method):
            print('Site', i, 'already local precomputed')
            continue
        sites[i].precompute(method, data_type, data_num, dim_size, grid_size)
    return sites


def global_processing(site_num, method, data_type, data_num, dim_size, grid_size, log, sim_id):
    # defined
    FIXED_K = 100 

     # local processing 
    sites = local_processing(site_num, method, data_type, data_num, dim_size, grid_size, log, sim_id)

    # global processing 
    global_result = {}
    for site_id in sites:
        if sites[site_id].is_global_precomputed(site_num, method):
            print('Site', site_id, 'already global precomputed')
            result = sites[site_id].get_final_result(site_num, method)

        else:        
            log.write(method, 'Global Processing of Site ' + str(site_id), with_info=False)
            result = sites[site_id].get_local_top(method, FIXED_K)
            for neighbor_id in sites:
                if site_id == neighbor_id:
                    continue
                sites[neighbor_id].compute(method, result)
                result.export(neighbor_id=neighbor_id, site_num=site_num)
            result.export(neighbor_id="final", site_num=site_num)

        global_result = {**global_result,
                         **result.get_top(key=C.UPDATED_RSKY)}
    return global_result


def naive_approach(k, site_num, method, data_type, data_num, dim_size, grid_size, log, sim_id):
    log.write(method, 'Start Naive', with_info=False)

    # init sites and collect all data
    global_pfile = {}
    global_cfile = {}
    for i in range(1, site_num + 1):
        site = Site(site_id=i, log=log, sim_id=sim_id)
        pfile, cfile = site.get_filename(data_type, data_num, dim_size)
        global_pfile = {**global_pfile, **pfile}
        global_cfile = {**global_cfile, **cfile}

    # compute using kmppd 
    site_path = getter.site_path("central", method, sim_id, C.KEY_SITE_STORAGE_PATH)
    result = kmppd.init(global_pfile, global_cfile, grid_size, site_path, log, C.NAIVE, return_result=True)

    # query processing 
    log.start()
    candidates = result.get_top(k)
    log.end(method, "Query Processing")
    log.write(method, 'End Naive', with_info=False)
    return candidates


def reset(method=None, data_type=None, data_num=None, dim_size=None, grid_size=None, sim_name=None, delete_logs=False):
    # generate sim name 
    if not sim_name:
        sim_name = getter.simulation_name(method, data_type, data_num, dim_size, grid_size)

    # delete simulation name in simulation info 
    sim_info = io.import_json(C.LOG_PATH, C.SIMULATION_INFO_FILE)
    sim_id = sim_info.pop(sim_name, None)
    method = sim_name.split("_")[0]
    io.export_json(C.LOG_PATH, C.SIMULATION_INFO_FILE, sim_info)

    if not sim_id:
        return

    # delete logs
    if delete_logs:
        del_dir = C.LOG_PATH + sim_id + "/"
        io.delete_dir(del_dir)

    # delete storage
    dirs = io.list_files(C.STORAGE_PATH)
    for dir in dirs:
        if "site" in dir:
            # delete directory 
            del_dir = C.STORAGE_PATH + dir + "/" + method + "_" + sim_id + "/"
            io.delete_dir(del_dir)
                
            # delete site info
            site_path = C.STORAGE_PATH + dir + "/"
            site_info_file = C.STORAGE_PATH + dir + "/" + "site_info.json"
            site_info = io.import_json(site_path, site_info_file)
            del_key = None
            for key in site_info:
                if sim_id in key:
                    del_key = key
                    break
            if del_key:
                site_info.pop(del_key, None)
            io.export_json(site_path, site_info_file, site_info)
