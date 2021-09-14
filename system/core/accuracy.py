""" 
This code is for checking the accuracy of proposed method
Local processing
"""
from application.classes.grid import Grid
from application.helpers.accuracy import Accuracy
from application.helpers.progress import Progress
import application.helpers.getter as getter
import application.helpers.constant as C
import application.core.kmppd as kmppd_sky
import application.core.okmppd as okmppd_sky


def check(site_id, pfile, cfile, grid_size, method):
    # get site path 
    data_type, data_num, dim_size = extract_info(pfile, cfile)
    sim_id = getter.simulation_id(method, data_type, data_num, dim_size, grid_size)
    site_path = getter.site_path(site_id, method, sim_id, C.KEY_SITE_STORAGE_PATH)

    # define path
    dataset_path = getter.dataset_path(site_id=site_id)  
    pfile = dataset_path + pfile
    cfile = dataset_path + cfile

    # init grid 
    grid = Grid(site_path, grid_size, pfile, cfile) 
    grid.indexing_data()

    # init accuracy instance 
    accuracy = Accuracy(method)

    # compute 
    if method == C.NAIVE_KMPP:
        naive_kmpp(grid, accuracy)
    elif method == C.KMPPD:
        kmppd(grid, accuracy)
    accuracy.export()


def kmppd(grid, accuracy):
    products = grid.get_products()
    customers = grid.get_customers()
    progress = Progress(len(products))
    for product in products:
        progress.counting()
        rsky = okmppd_sky.reverse_skyline(product, grid)
        true_rsky = naive(grid, product)
        accuracy.calculate(product, rsky, true_rsky, customers)
   

def naive_kmpp(grid, accuracy):
    products = grid.get_products()
    customers = grid.get_customers()
    progress = Progress(len(products))
    for product in products:
        progress.counting()
        rsky = kmppd_sky.reverse_skyline(product, grid)
        true_rsky = naive(grid, product)
        accuracy.calculate(product, rsky, true_rsky, customers)


def naive(grid, query_point):
    # naive method to search dynamic skyline
    true_rsky = []
    customers = grid.get_customers()
    for customer in customers:
        dsky = kmppd_sky.dynamic_skyline(customer, grid)
        dsky_id = set([obj[C.ID] for obj in dsky])
        if query_point[C.ID] in dsky_id:
            true_rsky.append(customer[C.ID])
    return true_rsky


def extract_info(pfile, cfile):
    # only filename 
    p_info = pfile.split(".")[0].split("_")
    c_info = cfile.split(".")[0].split("_")
    data_num = p_info[1] if p_info[1] == c_info[1] else [p_info[1], c_info[1]]
    return p_info[0], data_num, p_info[2]
