import itertools
import application.helpers.constant as C


def is_dominated(query_point, new_obj, skyline_points, is_single=True):
    # restructure skyline points and new objects
    data = [[obj, diff(query_point[C.VAL], obj[C.VAL]), False]
             for obj in skyline_points]
    if is_single:
        data.append(["new_obj", diff(query_point[C.VAL], new_obj), False])
    else:
        data += [[obj, diff(query_point[C.VAL], obj), False]
                 for obj in new_obj]

    # compare 
    compare(data)

    # filter result
    if is_single:
        result = [res for res in data if type(res[C.OBJ]) is str][0]
        return result[C.IS_DOMINATED]
    else:
        result = [res[C.OBJ] for res in data if res[C.IS_DOMINATED] and type(res[C.OBJ]) is tuple]
        return len(result) == len(new_obj)


def find_skyline(query_point, cand, midskyline=None):
    # restructure candidates and midskyline
    if midskyline:
        data = [[obj, diff(query_point[C.VAL], obj[C.VAL]), False] 
                 for obj in cand]
        data += [[obj[C.ID], diff(query_point[C.VAL], obj[C.VAL]), False]
                 for obj in midskyline]
    else:
        data = [[obj, diff(query_point[C.VAL], obj[C.VAL]), False]
                 for obj in cand if not is_same(obj, query_point)]

    # compare 
    compare(data)

    # filter result
    if midskyline:
        skyline = [res[C.OBJ] for res in data if not res[C.IS_DOMINATED]
                   and type(res[C.OBJ]) is dict]
    else:
        skyline = [res[C.OBJ] for res in data if not res[C.IS_DOMINATED]]
    return skyline


def compare(arr):
    # divide and conquer algorithm
    if len(arr) > 1:
        # finding the mid of the array
        mid = len(arr)//2

        # dividing array into left and right 
        left = arr[:mid]
        right = arr[mid:]
        compare(left)
        compare(right)

        # check domination 
        i = 0
        while i < len(left):
            if left[i][C.IS_DOMINATED]:
                i += 1
                continue
            j = 0
            while j < len(right):
                if right[j][C.IS_DOMINATED]:
                    j += 1
                    continue
                dom = check_domination(left[i][C.DIFF], right[j][C.DIFF])
                if dom == 1:
                    right[j][C.IS_DOMINATED] = True
                elif dom == 2:
                    left[i][C.IS_DOMINATED] = True
                j += 1
            i += 1

        # sorting 
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i][C.IS_DOMINATED] <= right[j][C.IS_DOMINATED]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        # checking if any element was left
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1


def check_domination(val1, val2):
    # return value : 
    # 0 (saling mendominasi)
    # 1 (val1 mendominasi)
    # 2 (val2 mendominasi)
    result = [0 for i in range(len(val1))]
    for i in range(len(val1)):
        if float(val1[i]) < float(val2[i]):
            result[i] = 1
        elif float(val1[i]) > float(val2[i]):
            result[i] = 2
    if 1 in result:
        if 2 in result:
            return 0
        return 1
    return 2


def calc_midskyline(query_point, skyline_points):
    # calculate midpoint of skyline 
    midskyline = []
    for sky_point in skyline_points:
        midpoint = {
            C.ID: sky_point[C.ID],
            C.VAL: [(query_point[C.VAL][i] + sky_point[C.VAL][i])/2
                    for i in range(len(query_point[C.VAL]))]
        }
        midskyline.append(midpoint)
    return midskyline


def diff(arr1, arr2):
    return [abs(arr1[i] - arr2[i]) for i in range(len(arr1))]


def is_same(point1, point2):
    return point1[C.ID] == point2[C.ID] and point1[C.VAL] == point2[C.VAL]


def get_sliced_grid(grid_in_orthant):
    return sum([[[k, v] for k, v in grid_in_orthant[key].items()]
                for key in grid_in_orthant.keys() if key != 1], [])


def get_full_grid(grid_in_orthant):
    return sum([[[k, v] for k, v in grid_in_orthant[key].items()]
                for key in grid_in_orthant.keys() if key == 1], [])


def need_to_check(neighbor, grid_in_orthant):
    return 1 in grid_in_orthant and neighbor in grid_in_orthant[1]


def find_skyline_of_orthant(query_point, grid_in_orthant, grid):
    # get all cand products in sliced grid
    sliced_grid = get_sliced_grid(grid_in_orthant)
    cand_products = sum([grid.get_products(grid_id=sg[C.GRID_POS], 
                                           boundary=sg[C.GRID_BOX])
                        for sg in sliced_grid], [])

    # get all cand products in full grid
    full_grid = get_full_grid(grid_in_orthant)
    cand_products += sum([grid.get_products(grid_id=sg[C.GRID_POS])
                         for sg in full_grid], [])

    # find skyline
    skyline = find_skyline(query_point, cand_products) 
    return skyline, sliced_grid, full_grid


def find_skyline_of_orthant_optimized(query_point, orthant_id, grid_in_orthant, grid, product=None):
    osky_grid = []

    # get all cand products in sliced grid
    sliced_grid = get_sliced_grid(grid_in_orthant)
    osky_grid += sliced_grid
    cand_products = sum([grid.get_products(grid_id=sg[C.GRID_POS],
                                           boundary=sg[C.GRID_BOX])
                              for sg in sliced_grid], [])
    if product:
        cand_products.append(product)

    # find skyline in the sliced grid
    skyline = find_skyline(query_point, cand_products)

    # find additional skyline in neighbors 
    n_level = 1
    while n_level > 0:
        neighbors = grid.get_neighbors(query_point[C.POS], orthant_id, n_level)
        is_dom = []
        for n_pos in neighbors:
            if not need_to_check(n_pos, grid_in_orthant):
                continue 

            # check if neighbor grid is dominated based on its corners 
            corners = list(itertools.product(*grid_in_orthant[1][n_pos])) 
            status = is_dominated(query_point, corners, skyline, is_single=False)
            is_dom.append(status)
            if status:
                continue

            # recompute skyline
            cand_products = grid.get_products(grid_id=n_pos)
            skyline = find_skyline(query_point, skyline + cand_products) 
            osky_grid.append([n_pos, grid_in_orthant[1][n_pos]])

        if all(is_dom):
            n_level = 0
        else:
            n_level += 1
    return skyline, osky_grid


def update_skyline_of_orthant_optimized(query_point, orthant_id, grid_in_orthant, grid):
    # find grid that intersecting with anti dominance region 
    intersecting_grid = grid.get_intersecting_grid(query_point[C.ORTHANT][orthant_id][C.ADR], grid_in_orthant)

    # get candidate products in the intersecting_grid 
    cand_products = sum([grid.get_products(grid_id=key, boundary=value)
                         for key, value in intersecting_grid.items()], [])
    
    # append with existing orthant skyline 
    if orthant_id in query_point[C.ORTHANT] and\
    C.OSKY in query_point[C.ORTHANT][orthant_id]:
        cand_products += query_point[C.ORTHANT][orthant_id][C.OSKY]
   
    # update orthant skyline
    skyline = find_skyline(query_point, cand_products) 
    return skyline, intersecting_grid
