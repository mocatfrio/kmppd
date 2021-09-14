from application.classes.grid import Grid
from application.classes.result import Result
from application.helpers.progress import Progress
import application.helpers.constant as C
import application.helpers.helper as helper
import application.core.kmppd as kmppd
import application.core.reusable as sky


def init(pfile, cfile, grid_size, site_path, log, method=C.OKMPPD, return_result=False):
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


def update(site_path, result, log, method=C.OKMPPD):
    # load grid data
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
    # get orthants 
    orthants = grid.get_orthants(customer[C.VAL])
    if product:
        products_orthant = helper.find_orthant(customer[C.VAL], product[C.VAL])
    
    # find skyline in each orthant 
    dsky = []
    for o_id, grid_in_orthant in orthants.items():
        if product and o_id == products_orthant:
            osky, osky_grid = sky.find_skyline_of_orthant_optimized(customer, o_id, grid_in_orthant, grid, product=product)
        else:
            osky, osky_grid = sky.find_skyline_of_orthant_optimized(customer, o_id, grid_in_orthant, grid)
        if result:
            result.set_orthant(C.CUSTOMER, customer, o_id, osky)
        dsky += osky

    # find dynamic skyline
    dsky = sky.find_skyline(customer, dsky)
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
        dsky = []

        # get cand products based on orthants
        orthants = grid.get_orthants(customer[C.VAL])
        if C.ORTHANT in customer_data:
            for o_id in customer_data[C.ORTHANT]:
                osky, intersecting_grid = sky.update_skyline_of_orthant_optimized(customer_data, o_id, orthants[o_id], grid)
                result.set_orthant(C.CUSTOMER, customer_data, o_id, osky)
                dsky += osky
            dsky = sky.find_skyline(customer, dsky)
    else:
        dsky = kmppd.dynamic_skyline(customer, grid, product=product)
    result.set_dsky(customer, dsky, mode=C.UPDATE)
    return dsky


def reverse_skyline(product, grid, result=None):
    # get orthants
    orthants = grid.get_orthants(product[C.VAL])
    
    rsky = []
    for o_id, grid_in_orthant in orthants.items():
        # find skyline in each orthant
        osky, osky_grid = sky.find_skyline_of_orthant_optimized(product, o_id, grid_in_orthant, grid)
        if result:
            result.set_orthant(C.PRODUCT, product, o_id, osky)

        # calculate midpoint skyline
        midsky = sky.calc_midskyline(product, osky)

        # get all candidate customers in the same region as products
        cand_customers = sum([grid.get_customers(grid_id=sg[C.GRID_POS],
                                                 boundary=sg[C.GRID_BOX])
                              for sg in osky_grid], [])

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
        osky, intersecting_grid = sky.update_skyline_of_orthant_optimized(product, o_id, orthants[o_id], grid)
        result.set_orthant(C.PRODUCT, product, o_id, osky)
    
        # calculate midpoint skyline
        midsky = sky.calc_midskyline(product, osky)

        # get all candidate customers in the same region as products
        cand_customers = sum([grid.get_customers(grid_id=key, boundary=value)
                              for key, value in intersecting_grid.items()], [])
        
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
