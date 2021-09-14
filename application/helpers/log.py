import os
import statistics
import application.helpers.io as io
import application.helpers.constant as C

# columns in csv
EVENT = 0
SITE_NUMBER = 1
K = 2
ON_SITE = 4
RUNTIME = 9
MEM_USAGE = 10

def read(method, data_type, data_num, dim_size, grid_size, metrics, site_num, k, need_export=False):
    rows = [] 
    
    sim_name = "_".join([method, data_type, data_num, dim_size, grid_size])
    log_name = "_".join([sim_name, str(metrics), str(site_num), str(k)])

    rows.append(" ")
    rows.append(str(sim_name))
    # get sim id 
    simulation = io.import_json(C.LOG_PATH, C.SIMULATION_INFO_FILE)
    sim_id = simulation.get(sim_name, None)
    if not sim_id:
        return 0
    # get list file 
    sim_log_path = C.LOG_PATH + "/" + sim_id + "/"
    entries = os.listdir(sim_log_path)
    # satukan log2
    log_files = [e for e in entries if "log" in e]
    # import log
    logs = []
    for log in log_files:
        logs += io.import_csv(sim_log_path, sim_log_path + log)

    result = "Tidak ada"
    # Waktu Indexing
    if metrics == 1:
        runtime = []
        for row in logs:
            if is_indexing(row):
                rows.append(str(row))
                rows.append("Runtime " + str(convert_to_sec(row[RUNTIME])))
                runtime.append(convert_to_sec(row[RUNTIME]))
        result = statistics.mean(runtime)
    # Waktu Local Processing
    elif metrics == 2:
        runtime = []
        for row in logs:
            if is_local_processing(row):
                rows.append(str(row))
                rows.append("Runtime " + str(convert_to_sec(row[RUNTIME])))
                runtime.append(convert_to_sec(row[RUNTIME]))
        result = statistics.mean(runtime)
    # Total Waktu Kueri
    elif metrics == 3:
        runtime = []
        if method == C.NAIVE:
            for row in logs:
                if is_query(row, site_num, k, method):
                    rows.append(str(row))
                    rows.append("Runtime " + str(convert_to_sec(row[RUNTIME])))
                    runtime.append(convert_to_sec(row[RUNTIME]))
        else:
            per_site_inisiator = []
            per_site_updater = []
            site_inisiator = None
            for row in logs:
                if is_query(row, site_num, k, method):
                    rows.append("========================================================")
                    rows.append(str(row))
                    rows.append("Runtime " + str(runtime))
                    rows.append("Per site inisiator " + str(per_site_inisiator))
                    rows.append("Per site updater " + str(per_site_updater))
                    if "Get local top" in row[EVENT]:
                        if site_inisiator and row[ON_SITE] < site_inisiator and site_inisiator < row[SITE_NUMBER]:
                            runtime = []
                            per_site_inisiator = []
                            per_site_updater = []
                        runtime.append(convert_to_sec(row[RUNTIME]))
                        site_inisiator = row[ON_SITE]
                    elif "Query processing" in row[EVENT]:
                        runtime.append(convert_to_sec(row[RUNTIME]))
                        break
                    elif "site" in row[EVENT]:
                        runtime.append(max(per_site_inisiator))
                        per_site_inisiator = [] # kembalikan ke kondisi awal 
                    elif "Load grid index" in row[EVENT]:
                        per_site_updater.append(convert_to_sec(row[RUNTIME]))
                    else:
                        per_site_updater.append(convert_to_sec(row[RUNTIME]))
                        per_site_inisiator.append(sum(per_site_updater))
                        per_site_updater = [] # kembalikan ke kondisi awal 
                    rows.append("AFTER")
                    rows.append("Runtime " + str(runtime))
                    rows.append("Per site inisiator " + str(per_site_inisiator))
                    rows.append("Per site updater " + str(per_site_updater))
        result = sum(runtime)
    # Memori Indexing
    elif metrics == 4:
        mem_usage = []
        for row in logs:
            if is_indexing(row):
                rows.append(str(row))
                rows.append("Mem usage " + str(mem_usage))
                mem_usage.append(float(row[MEM_USAGE]))
        result = statistics.mean(mem_usage)
    # Memori Local Processing
    elif metrics == 5:
        mem_usage = []
        for row in logs:
            if is_local_processing(row):
                rows.append(str(row))
                rows.append("Mem usage " + str(mem_usage))
                mem_usage.append(float(row[MEM_USAGE]))
        result = statistics.mean(mem_usage)
    # Biaya bandwith 
    elif metrics == 6:
        mem_usage = []
        if method == C.NAIVE:
            for row in logs:
                if is_query(row, site_num, k, method):
                    rows.append(str(row))
                    rows.append("Mem usage " + str(mem_usage))
                    mem_usage.append(float(row[MEM_USAGE]))
        else:
            per_site_inisiator = []
            per_site_updater = []
            site_inisiator = None
            for row in logs:
                if is_query(row, site_num, k, method):
                    rows.append(str(row))
                    rows.append("Runtime " + str(mem_usage))
                    rows.append("Per site inisiator " + str(per_site_inisiator))
                    rows.append("Per site updater " + str(per_site_updater))
                    if "Get local top" in row[EVENT]:
                        if site_inisiator and row[ON_SITE] < site_inisiator and site_inisiator < row[SITE_NUMBER]:
                            mem_usage = []
                            per_site_inisiator = []
                            per_site_updater = []
                        mem_usage.append(float(row[MEM_USAGE]))
                        site_inisiator = row[ON_SITE]
                    elif "Query processing" in row[EVENT]:
                        mem_usage.append(float(row[MEM_USAGE]))
                        break
                    elif "site" in row[EVENT]:
                        mem_usage.append(max(per_site_inisiator))
                        per_site_inisiator = [] # kembalikan ke kondisi awal 
                    elif "Load grid index" in row[EVENT]:
                        per_site_updater.append(float(row[MEM_USAGE]))
                    else:
                        per_site_updater.append(float(row[MEM_USAGE]))
                        per_site_inisiator.append(sum(per_site_updater))
                        per_site_updater = [] # kembalikan ke kondisi awal 
                    rows.append("=========================================")
                    rows.append("Runtime " + str(mem_usage))
                    rows.append("Per site inisiator " + str(per_site_inisiator))
                    rows.append("Per site updater " + str(per_site_updater))
        result = sum(mem_usage)
    if metrics == 1 or metrics == 2 or metrics == 3:
        rows.append(str(result) + " second")
    else:
        rows.append(str(result) + " MB")
    if need_export: 
        io.export_txt(C.GRAPH_PATH, C.GRAPH_PATH + log_name + ".txt", rows)
    return result

def convert_to_sec(runtime):
    splitted_runtime = runtime.split(":")
    if len(splitted_runtime) < 3:
        splitted_runtime = [00] + splitted_runtime
    sec = (float(splitted_runtime[0]) * 3600) + (float(splitted_runtime[1]) * 60) + float(splitted_runtime[2])
    return sec 

def is_indexing(row):
    return "Local processing" in row[EVENT] and "Indexing" in row[EVENT] and row[K] == '0'

def is_local_processing(row):
    # return "Local processing" in row[EVENT] and not "Indexing" in row[EVENT] and row[K] == '0'
    return "Local processing" in row[EVENT] and row[K] == '0'

def is_query(row, site_num, k, method):
    if method == C.NAIVE:
        return row[SITE_NUMBER] == site_num and row[K] == k
    else:
        return "Global processing" in row[EVENT] and row[SITE_NUMBER] == site_num and row[K] == k\
            or "Query processing" in row[EVENT] and row[SITE_NUMBER] == site_num and row[K] == k
