from application.classes.grid import Grid
from application.classes.result import Result
from application.helpers.progress import Progress
import application.helpers.constant as C
import application.core.reusable as sky
from prettyprinter import pprint


def init(pfile, cfile, grid_size, site_path, log, method=C.KMPPD, return_result=False):
    # indexing data
    log.start()
    grid = Grid(site_path, grid_size, pfile, cfile) 
    grid.indexing_data()
    log.end(method, 'Indexing Data')

    # init result
    result = Result(site_path=site_path)

    # local processing 
    log.start()
    products = grid.get_products()
    progress = Progress(len(products))
    for product in products:
        progress.counting()

        # compute reverse skyline for each product
        rsky = reverse_skyline(product, grid, result)

        # compute dynamic skyline for each customer 
        for customer in rsky:
            if result.is_calculated(customer):
                continue
            dynamic_skyline(customer, grid, result)
    log.end(method, 'Local Processing')

    # export the result
    result.export()
    if return_result:
        return result


def update(site_path, result, log, method=C.KMPPD):
    # global processing
    log.start()
    grid = Grid(site_path) 
    progress = Progress(len(result.get_all(C.PRODUCT)))
    for product in result.get_all(C.PRODUCT).values():
        progress.counting()

        # update reverse skyline 
        new_rsky = update_reverse_skyline(product, grid, result)

        # update dynamic skyline 
        for customer in new_rsky:
            update_dynamic_skyline(customer, grid, result, product)
            
    log.end(method, 'Global Processing')
    return result


def dynamic_skyline(customer, grid, result=None, product=None):
    # get all candidate products
    cand_products = grid.get_products()
    if product:
        cand_products.append(product)

    # find skyline
    dsky = sky.find_skyline(customer, cand_products) 
    if result:
        result.set_dsky(customer, dsky)
    return dsky
   

def update_dynamic_skyline(customer, grid, result, product):
    # grid is owned by updater site 
    # result is owned by initiator site 

    # reset dsky result 
    result.reset_dsky(customer)

    # get customer data
    customer_data = result.get_one(customer[C.ID], C.CUSTOMER)
    if customer_data:
        # get all cand products from updater site
        cand_products = grid.get_products()
        cand_products += [val for val in customer_data[C.DSKY].values()]
    
        # find final dynamic skyline
        dsky = sky.find_skyline(customer, cand_products)
    else:
        dsky = dynamic_skyline(customer, grid, product=product)
    result.set_dsky(customer, dsky, mode=C.UPDATE)
    return dsky


def reverse_skyline(product, grid, result):
    # get orthants
    orthants = grid.get_orthants(product[C.VAL])

    rsky = []
    for o_id, grid_in_orthant in orthants.items():
        osky, sliced_grid, full_grid = sky.find_skyline_of_orthant(product, grid_in_orthant, grid)
        result.set_orthant(C.PRODUCT, product, o_id, osky)
        
        # calculate midpoint skyline
        midsky = sky.calc_midskyline(product, osky)

        # get all candidate customers in the same region as products
        cand_customers = sum([grid.get_customers(grid_id=sg[C.GRID_POS],
                                                 boundary=sg[C.GRID_BOX])
                              for sg in sliced_grid], [])
        cand_customers += sum([grid.get_customers(grid_id=sg[C.GRID_POS])
                               for sg in full_grid], [])

        # find customers outside the midskyline
        rsky_per_orthant = sky.find_skyline(product, cand_customers, midsky) 
        rsky += rsky_per_orthant
    result.set_rsky(product, rsky)
    return rsky


def update_reverse_skyline(product, grid, result):
    # move rsky ke true rsky 
    result.update_true_rsky(product)

    existing_true_rsky = []
    rsky = []
    orthants = grid.get_orthants(product[C.VAL])
    for o_id in product[C.ORTHANT]:
        osky, sliced_grid, full_grid = sky.find_skyline_of_orthant(product, orthants[o_id], grid)
        result.set_orthant(C.PRODUCT, product, o_id, osky)

        # calculate midpoint skyline
        midsky = sky.calc_midskyline(product, osky)

        # get all candidate customers in the same region as products
        cand_customers = sum([grid.get_customers(grid_id=sg[C.GRID_POS], 
                                                 boundary=sg[C.GRID_BOX])
                              for sg in sliced_grid], [])
        cand_customers += sum([grid.get_customers(grid_id=sg[C.GRID_POS])
                               for sg in full_grid], [])
        
        # append with existing reverse skyline
        if o_id in product[C.TRUE_RSKY]:
            true_rsky = [val for val in product[C.TRUE_RSKY][o_id].values()]
            cand_customers += true_rsky
            existing_true_rsky += true_rsky
        
        # find customers outside the midskyline
        rsky_per_orthant = sky.find_skyline(product, cand_customers, midsky) 
        rsky += rsky_per_orthant

    # reset rsky 
    result.reset_rsky(product)
    result.set_rsky(product, rsky)

    # return rsky with the existing true rsky 
    return rsky + existing_true_rsky
