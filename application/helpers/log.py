import os
import statistics
import application.helpers.io as io
import application.helpers.constant as C
import application.helpers.getter as getter


# columns in csv
EVENT = 0
SITE_NUMBER = 1
K = 2
ON_SITE = 4
RUNTIME = 9
MEM_USAGE = 10


def read(method, data_type, data_num, dim_size, grid_size, metrics, site_num, k, need_export=False):
    sim_name = getter.simulation_name(method, data_type, data_num, dim_size, grid_size)
    log_name = getter.log_name(sim_name, metrics, site_num, k)

    # init rows
    rows = [] 
    rows.append(" ")
    rows.append(str(sim_name))

    # get sim id 
    simulation = io.import_json(C.LOG_PATH, C.SIMULATION_INFO_FILE)
    sim_id = simulation.get(sim_name, None)
    if not sim_id:
        return 0

    # get list of log name
    sim_log_path = C.LOG_PATH + "/" + sim_id + "/"
    entries = os.listdir(sim_log_path)
    log_files = [e for e in entries if "log" in e]

    # import and merge all logs
    logs = []
    for log in log_files:
        logs += io.import_csv(sim_log_path, sim_log_path + log)

    result = "Tidak ada"

    if 'time' in metrics:
        if metrics == C.KEY_QUERY_TIME:
            runtime = []

            # all_runtime = []
            # runtime = []
            if method == C.NAIVE:
                for row in logs:
                    if is_query(row, site_num, k, method):
                        rows.append(str(row))
                        rows.append("Runtime " + str(convert_to_sec(row[RUNTIME])))
                        runtime.append(convert_to_sec(row[RUNTIME]))
            else:
                per_site_inisiator = []
                per_site_updater = []
                runtime_per_cycle = []
                for row in logs:
                    if 'Start' in row[EVENT]:
                        per_site_inisiator = []
                        per_site_updater = []
                        runtime_per_cycle = []

                    elif "Site" in row[EVENT]:
                        if per_site_updater:
                            avg_update_time = statistics.mean(per_site_updater)
                            rows.append("Average Runtime Updater " + str(avg_update_time) + ' <-- ' + str(per_site_updater))
                            per_site_inisiator.append(avg_update_time)
                            runtime_per_cycle.append(sum(per_site_inisiator))
                            per_site_inisiator = []
                            per_site_updater = []

                    elif "Get Local Top" in row[EVENT]:
                        per_site_inisiator.append(convert_to_sec(row[RUNTIME]))

                    elif 'Global Processing' in row[EVENT] and not ('Site' in row(EVENT)):
                        per_site_updater.append(convert_to_sec(row[RUNTIME]))

                    elif "Query Processing" in row[EVENT]:
                        rows.append("Runtime per cycle " + str(runtime_per_cycle) + ' = ' + statistics.mean(runtime_per_cycle))
                        runtime_per_cycle = [statistics.mean(runtime_per_cycle)]
                        runtime_per_cycle.append(convert_to_sec(row[RUNTIME]))
                        rows.append("Runtime per cycle " + str(runtime_per_cycle))

                    elif 'End' in row[EVENT]:
                        runtime.append(sum(runtime_per_cycle))
                        rows.append("Total Runtime = " + str(runtime))
            result = statistics.mean(runtime)

        else:
            runtime = {}
            result_per_site = {}
            result = []
            for row in logs:
                if met_condition_of_metrics(metrics, row): 
                    if not (row[ON_SITE] in runtime):
                        runtime[row[ON_SITE]] = []
                    runtime[row[ON_SITE]].append(convert_to_sec(row[RUNTIME]))
            for k, v in runtime:
                result_per_site[k] = statistics.mean(v)
                result += v
                rows.append('Runtime on Site ' + str(k) + ' => ' + str(v) + ' = ' + str(result_per_site[k]))
            result = statistics.mean(result)
            rows.append('Runtime on All Site => ' + str(result))

    elif 'mem' in metrics:
        if metrics == C.KEY_QUERY_MEM:
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

        # Memori Indexing
        else:
            mem_usage = {}
            result_per_site = {}
            result = []
            for row in logs:
                if met_condition_of_metrics(metrics, row): 
                    if not (row[ON_SITE] in mem_usage):
                        mem_usage[row[ON_SITE]] = []
                    mem_usage[row[ON_SITE]].append(float(row[MEM_USAGE]))
            for k, v in mem_usage:
                result_per_site[k] = statistics.mean(v)
                result += v
                rows.append('Mem Usage on Site ' + str(k) + ' => ' + str(v) + ' = ' + str(result_per_site[k]))
            result = statistics.mean(result)
            rows.append('Mem Usage on All Site => ' + str(result))

    if 'time' in metrics:
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
    return "Indexing Data" in row[EVENT]


def is_local_processing(row):
    return "Local processing" in row[EVENT]


def is_query(row, site_num, k, method):
    if method == C.NAIVE:
        return row[SITE_NUMBER] == site_num and row[K] == k
    else:
        return "Global processing" in row[EVENT] and row[SITE_NUMBER] == site_num and row[K] == k\
            or "Query processing" in row[EVENT] and row[SITE_NUMBER] == site_num and row[K] == k


def is_start(row):
    return 'Start' in row[EVENT]


def is_end(row):
    return 'End' in row[EVENT]


def met_condition_of_metrics(metrics, row):
    if 'index' in metrics:
        return is_indexing(row)
    if 'local_processing' in metrics:
        return is_local_processing(row)