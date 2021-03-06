import application.helpers.constant as C
import application.helpers.io as io
import application.helpers.getter as getter
import application.core.kmppd as kmppd
import application.core.okmppd as okmppd
from application.classes.result import Result

import sys

class Site:
    def __init__(self, site_id, log, sim_id):
        self.id = site_id
        self.log = log
        self.sim_id = sim_id

        # define path
        self.site_path = getter.site_path(site_id)
        self.site_info_file = getter.site_path(site_id, request=C.KEY_SITE_INFO_FILE)
        self.site_info = io.import_json(self.site_path, self.site_info_file)
        self.dataset_path = getter.dataset_path(self.site_path)


    def precompute(self, method, data_type, data_num, dim_size, grid_size):
        self.log.on_site(self.id)
        storage_path = getter.site_path(self.id, method, self.sim_id, C.KEY_SITE_STORAGE_PATH)
        pfile, cfile = self.get_filename(data_type, data_num, dim_size)
        
        # local processing
        if method == C.KMPPD:
            kmppd.init(pfile, cfile, grid_size, storage_path, self.log)
        elif method == C.OKMPPD:
            okmppd.init(pfile, cfile, grid_size, storage_path, self.log)

        # update site info and export
        self.site_info[getter.keyname(method, self.sim_id)] = True
        io.export_json(self.site_path, self.site_info_file, self.site_info)


    def get_final_result(self, site_num, method):
        storage_path = getter.site_path(self.id, method, self.sim_id, C.KEY_SITE_STORAGE_PATH)
        result = Result(site_path=storage_path, final=True, site_num=site_num)
        return result


    def compute(self, method, top_k_data):
        self.log.on_site(self.id)
        storage_path = getter.site_path(self.id, method, self.sim_id, C.KEY_SITE_STORAGE_PATH)

        # global processing
        if method == C.KMPPD:
            result = kmppd.update(storage_path, top_k_data, self.log)
        elif method == C.OKMPPD:
            result = okmppd.update(storage_path, top_k_data, self.log)
        return result


    def get_filename(self, data_type, data_num, dim_size):
        # separate data size  
        pdata_num = data_num[0] if type(data_num) is list else data_num
        cdata_num = data_num[1] if type(data_num) is list else data_num

        # define filename 
        pfile = {self.id: getter.dataset_path(sitepath=self.site_path,
                                              data_type=data_type, data_num=pdata_num,
                                              dim_size=dim_size, label=C.PRODUCT,
                                              request=C.KEY_DATASET_FILE)}
        cfile = {self.id: getter.dataset_path(sitepath=self.site_path, 
                                              data_type=data_type, data_num=cdata_num,
                                              dim_size=dim_size, label=C.CUSTOMER,
                                              request=C.KEY_DATASET_FILE)}
        return pfile, cfile


    def get_local_top(self, method, k):
        self.log.on_site(self.id)
        storage_path = getter.site_path(self.id, method, self.sim_id, C.KEY_SITE_STORAGE_PATH)

        self.log.start()
        result = Result(site_path=storage_path)
        key = C.TRUE_RSKY
        top_k_product = result.get_top(k, key=key)
        top_k_data = {C.PRODUCT: {}, C.CUSTOMER: {}}
        
        # get product and customer complete info
        for p_id in top_k_product:
            product = result.get_one(p_id, C.PRODUCT)
            top_k_data[C.PRODUCT][p_id] = product
            if not (key in product):
                continue
            for orthant_id in product[key]:
                for customer in product[key][orthant_id].values():
                    if customer[C.ID] in top_k_data[C.CUSTOMER]:
                        continue
                    top_k_data[C.CUSTOMER][customer[C.ID]] = result.get_one(customer[C.ID], C.CUSTOMER)
        
        # init result of top k product 
        result = Result(site_path=storage_path, json_data=top_k_data)
        self.log.end(method, 'Get Local Top')
        return result
        

    def is_local_precomputed(self, method):
        if getter.keyname(method, self.sim_id) in self.site_info:
            return self.site_info[getter.keyname(method, self.sim_id)]

        is_exist = []
        list_dir = ['grid', 'result', 'rtree']
        storage_path = getter.site_path(self.id, method, self.sim_id, C.KEY_SITE_STORAGE_PATH)
        if io.dir_is_exist(storage_path):
            for dir in list_dir:
                if io.dir_is_exist(storage_path + '/' + dir):
                    is_exist.append(True)
                else:
                    is_exist.append(False)
        return len(is_exist) == len(list_dir) and all(is_exist)
    
    
    def is_global_precomputed(self, site_num, method):
        storage_path = getter.site_path(self.id, method, self.sim_id, C.KEY_SITE_STORAGE_PATH)
        result_global_path = getter.result_path(sitepath=storage_path, site_num=site_num, request=C.RESULT_GLOBAL_PATH)

        is_exist = []
        if io.dir_is_exist(result_global_path):
            dirs = io.list_files(result_global_path)
            for dir in dirs:
                if 'final' in dir and 'product' in dir:
                    is_exist.append(True)
                if 'final' in dir and 'customer' in dir:
                    is_exist.append(True)
        return len(is_exist) == 2
