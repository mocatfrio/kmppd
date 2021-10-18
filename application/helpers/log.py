import os
import statistics
import application.helpers.io as io

# columns in csv
EVENT = 0
SITE_NUMBER = 1
K = 2
ON_SITE = 4
RUNTIME = 9
MEM_USAGE = 10


def read(metric, log_path, site_num, k, need_export=False):
    # get list of log name
    entries = os.listdir(log_path)
    log_files = [e for e in entries if "log" in e]

    # import and merge all logs
    logs = []
    for log_file in log_files:
        logs += io.import_csv(log_path, log_path + log_file)

    result = None

    if 'index' in metric:
        isStart = False
        data = []
        multiple_data = []
        for row in logs:
            if 'Start Local Processing' in row[EVENT]:
                if isStart and data:
                    multiple_data.append(statistics.mean(data))
                isStart = True
                data = []
            elif isStart:
                if 'End Local Processing' in row[EVENT]:
                    isStart = False
                    if data:
                        multiple_data.append(statistics.mean(data))
                elif 'Indexing Data' in row[EVENT]:
                    data.append(add_data(metric, row))
        if multiple_data:
            result = statistics.mean(multiple_data)
    
    elif 'local' in metric:
        isStart = False
        data = []
        multiple_data = []
        for row in logs:
            if 'Start Local Processing' in row[EVENT]:
                if isStart and data:
                    multiple_data.append(statistics.mean(data))
                isStart = True
                data = []
            elif isStart:
                if 'End Local Processing' in row[EVENT]:
                    isStart = False
                    if data:
                        multiple_data.append(statistics.mean(data))
                elif 'Local Processing' in row[EVENT]:
                    data.append(add_data(metric, row))
        if multiple_data:
            result = statistics.mean(multiple_data)
    
    elif 'global' in metric:
        isStart = False
        data = []
        multiple_data = []
        for row in logs:
            if 'Start Global Processing' in row[EVENT]:
                isStart = True
            elif 'Global Processing of Site' in row[EVENT] or 'End Global Processing' in row[EVENT]:
                if data:
                    multiple_data.append(sum(data))
                    data = []
                if 'End Global Processing' in row[EVENT]:
                    isStart = False
            elif isStart:
                if ('Get Local Top' in row[EVENT] or 'Global Processing' in row[EVENT]) and row[SITE_NUMBER] == str(site_num):
                    data.append(add_data(metric, row))
        if multiple_data:
            result = statistics.mean(multiple_data)

    elif 'query' in metric:
        data = []
        for row in logs:
            if 'End Query Processing' in row[EVENT] and row[SITE_NUMBER] == str(site_num) and row[K] == str(k):
                data.append(add_data(metric, row))
        if data:
            result = statistics.mean(data)

    if result:
        if 'time' in metric:
            result = str(round(result, 2)) + " Sec"
        else:
            result = str(round(result, 2)) + " MB"

    # if need_export: 
        # io.export_txt(C.GRAPH_PATH, C.GRAPH_PATH + log_name + ".txt", rows)
    return result


def add_data(metric, row):
    if 'time' in metric:
        return convert_to_sec(row[RUNTIME])
    elif 'mem' in metric:
        return float(row[MEM_USAGE])


def convert_to_sec(runtime):
    splitted_runtime = runtime.split(":")
    if len(splitted_runtime) < 3:
        splitted_runtime = [00] + splitted_runtime
    sec = (float(splitted_runtime[0]) * 3600) + (float(splitted_runtime[1]) * 60) + float(splitted_runtime[2])
    return sec 



