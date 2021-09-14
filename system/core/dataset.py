import random
import pandas as pd 
import application.helpers.constant as C
import application.helpers.io as io
import application.helpers.getter as getter


MAX_VALUE_ANT = 300
MAX_VALUE = 200
DIST = 30
ADDITIONAL_DIST = 50
    

def generate(site_num, data_type, data_num, dim_size):
    # generate data per site
    for i in range(1, site_num + 1):
        site_path = getter.site_path(i)
        dataset_path = getter.dataset_path(site_path)
        for label in [C.PRODUCT, C.CUSTOMER]:
            filename = getter.dataset_path(sitepath=site_path, data_type=data_type,
                                           data_num=data_num,
                                           dim_size=dim_size, label=label,
                                           request=C.KEY_DATASET_FILE)
            if data_type == C.FC:
                # real data
                data = prepare_data(data_num, dim_size, label)
            else:
                data = create_data(data_num, dim_size, data_type, label)
            io.export_csv(dataset_path, filename, data)


def create_data(data_num, dim_size, data_type, label):
    randomize_data = {
        C.IND: randomize_ind,
        C.ANT: randomize_ant
    }
    col_name = ["id", "label"] + ["attr_" + str(i + 1) for i in range(dim_size)]
    data = [col_name]
    for i in range(data_num):
        row = [i + 1, label + "-" + str(i + 1)]
        row += randomize_data[data_type](dim_size)
        data.append(row)
    return data


def prepare_data(data_num, dim_size, label):
    # import original data 
    dataset_path = C.STORAGE_PATH + "covtype.csv"
    df = pd.read_csv(dataset_path)

    # normalisasi min-max 
    for col in df.columns:
        normalized_value = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
        df[col] = round(normalized_value * 100).astype(int)
    
    # get 10 first columns 
    df.drop([col for col in df.columns[10:]], axis=1, inplace=True)
    
    # insert label 
    df.insert(0, "label", [label + "-" + str(i+1) for i in range(len(df))], True)
    
    # get row 
    start_row, end_row = get_range_row(len(df), data_num)

    # get dim 
    # define columns
    if label == C.PRODUCT:
        cols = [1, 2, 4, 7, 9]
    else:
        cols = [5, 3, 6, 8, 10]

    result = [df.iloc[start_row:end_row, 0]]
    for d in range(dim_size): 
        result.append(df.iloc[start_row:end_row, cols[d]])
    df = pd.concat(result, axis=1)

    # reset index 
    df = df.reset_index(drop=True)
    df.insert(0, "id", [i + 1 for i in df.index], True)
    
    # convert df to list 
    result = [df.columns.tolist()]
    result += df.values.tolist()
    return result


def get_range_row(max_val, data_num):
    start_row = randomize(max_val=max_val)
    end_row = start_row + data_num
    if end_row > max_val:
        start_row, end_row = get_range_row(max_val, data_num)
    return start_row, end_row


def get_col_index(min_val, max_val, last_index):
    idx = randomize(min_val, max_val)
    if idx == last_index:
        idx = get_col_index(min_val, max_val, last_index)
    return idx


def randomize(min_val=0, max_val=None):
    if not max_val:
        max_val = MAX_VALUE
    if min_val > max_val:
        min_val = max_val
    range_start = random.randint(min_val, max_val) 
    range_end = range_start + random.randint(min_val, round(max_val/2))
    return random.randint(range_start, range_end)


def randomize_ind(dim_size):
    return [randomize() for _ in range(dim_size)]


def randomize_ant(dim_size):
    data = []
    is_selected = random.getrandbits(1)
    val = randomize()
    if val > MAX_VALUE_ANT:
        diff = val - MAX_VALUE_ANT
        val = MAX_VALUE_ANT - diff
    for i in range(dim_size):
        if i == 0:
            data.append(val)
        else:
            other_val = MAX_VALUE_ANT - val + random.randint(-DIST, DIST)
            if is_selected:
                other_val += random.randint(-ADDITIONAL_DIST, ADDITIONAL_DIST) + random.randint(-DIST, DIST)
            if other_val < 0:
                other_val = abs(other_val)
            elif other_val > MAX_VALUE_ANT:
                diff = other_val - MAX_VALUE_ANT
                other_val = MAX_VALUE_ANT - diff
            data.append(other_val)
    return data
