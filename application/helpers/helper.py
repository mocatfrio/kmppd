import application.helpers.constant as C


def is_intersecting(region1, region2, get_intersecting_region=False):
    dim = len(region1)
    result = []
    for i in range(dim):
        if not ((region1[i][C.MIN] > region2[i][C.MAX]) or (region1[i][C.MAX] < region2[i][C.MIN])):
            min_val = max([region1[i][C.MIN], region2[i][C.MIN]])
            max_val = min([region1[i][C.MAX], region2[i][C.MAX]])
            result.append([min_val, max_val])
    if len(result) == dim:
        return result if get_intersecting_region else True
    else:
        return False


def is_inside(val, boundary):
    dim = len(boundary)
    perdim = []
    for i in range(dim):
        perdim.append((val[i] >= boundary[i][C.MIN]) and (val[i] <= boundary[i][C.MAX]))
    return all(perdim) 


def find_orthant(query_point_val, obj_val):
    res = []
    dim = len(query_point_val)
    for i in range(dim):
        if obj_val[i] <= query_point_val[i]:
            res.append('0')
        else:
            res.append('1')
    res = ''.join(res)
    return res


def sort_dict(obj_dict, k=None, descending=True):
    if not k:
        k = len(obj_dict)
    if type(obj_dict[list(obj_dict.keys())[0]]) is dict:
        mc = {key: value[C.MC] for key, value in obj_dict.items()}
    else: 
        mc = obj_dict
    sorted_mc = sorted(mc.items(), key=lambda x: x[1], reverse=descending)
    return {_: obj_dict[_] for _ in [sorted_mc[i][0] for i in range(0, k)]}


def split_datasize(var):
    if len(var.split("-")) > 1:
        return [int(v) for v in var.split("-")]
    else:
        return int(var)
