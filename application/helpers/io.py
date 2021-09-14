import os
import csv
import json
import shutil
from pathlib import Path


def import_json(filepath, filename):
    obj_dict = {}
    if os.path.isdir(filepath):
        if os.path.isfile(filename):
            with open(filename) as json_file:
                obj_dict = json.load(json_file)
    return obj_dict


def import_csv(filepath, filename, skip_column=True):
    # import csv to row biasa 
    data = []
    if os.path.isdir(filepath):
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            if skip_column:
                next(reader)
            data = list(reader)
    return data


def export_json(filepath, filename, obj_dict):
    check_path(filepath)
    # write logs to the json file
    with open(filename, "w") as write_file:
        json.dump(obj_dict, write_file, indent=4)
    print("Exporting data", filename, "is success!")


def export_txt(filepath, filename, lst):
    check_path(filepath)
    # write logs to the csv/txt file
    with open(filename, "w") as write_file:
        write_file.writelines('\n'.join(lst))
    print("Exporting data", filename, "is success!")
    return


def export_csv(filepath, filename, lst, mode="w"):
    check_path(filepath)
    # write logs to the csv file    
    with open(filename, mode) as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        for row in lst:
            writer.writerow(row)
    print("Exporting data", filename, "is success!")


def export_graph(filepath, filename, plot, format='png', dpi=300):
    try:
        check_path(filepath)
        plot.savefig(filepath + filename, format=format, dpi=dpi)
        print("Exporting scatterplot", filename, "is success!")
    except Exception as e:
        print(e)


def check_path(filepath):
    Path(filepath).mkdir(parents=True, exist_ok=True)


def delete_dir(del_dir):
    try:
        shutil.rmtree(del_dir)
    except:
        print("Directory", del_dir, "is not found!")