
import application.helpers.constant as C
import application.helpers.getter as getter
import application.helpers.io as io
import application.helpers.helper as helper


class Result:
    def __init__(self, site_path=None, json_data=None):
        self.site_path = site_path
        self.result_path = getter.result_path(sitepath=site_path)
        self.result_pfile = getter.result_path(sitepath=site_path,
                                               request=C.RESULT_PRODUCT_FILE)
        self.result_cfile = getter.result_path(sitepath=site_path,
                                               request=C.RESULT_CUSTOMER_FILE)
        self.result_mc_file = getter.result_path(sitepath=site_path,
                                                 request=C.RESULT_MC_FILE)
    
        # import file result
        if json_data:
            self.result = json_data
        else:
            self.result = {
                C.PRODUCT: io.import_json(self.result_path, self.result_pfile),
                C.CUSTOMER: io.import_json(self.result_path, self.result_cfile),
            }


    """ 
    Getter Data
    """


    def get_all(self, obj_type=C.PRODUCT):
        return self.result[obj_type]


    def get_one(self, obj_id, obj_type=C.PRODUCT):
        if obj_id in self.result[obj_type]:
            return self.result[obj_type][obj_id]
        else:
            return None


    def get_top(self, k=None, key=C.TRUE_RSKY, with_product_info=False):
        key = C.TRUE_RSKY if k else C.UPDATED_RSKY

        # calculate market contribution of all products in the result 
        market_contribution = {}
        for product in self.result[C.PRODUCT].values():
            market_contribution[product[C.ID]] = 0
            if not (key in self.result[C.PRODUCT][product[C.ID]]):
                continue
            for orthant_id in self.result[C.PRODUCT][product[C.ID]][key]:
                for customer in self.result[C.PRODUCT][product[C.ID]][key][orthant_id].values():
                    market_contribution[product[C.ID]] += customer[C.MC]

        # sorting market contribution 
        result = helper.sort_dict(market_contribution, k)
        
        # add obj info 
        if with_product_info:
            result = {obj: {**self.get_main_attr(self.get_one(obj, C.PRODUCT)), 
                        **{C.MC: result[obj]}} 
                    for obj in result}
        return result


    def get_main_attr(self, obj_dict):
        main_attr = [C.ID, C.LABEL, C.VAL, C.POS, C.SITE_ID]
        result = {}
        for attr in main_attr:
            result[attr] = obj_dict[attr]
        return result


    """
    Setter
    """


    def init_obj(self, obj_type, obj):
        if not (obj[C.ID] in self.result[obj_type]):
            self.result[obj_type][obj[C.ID]] = obj


    def set_dsky(self, customer, dsky, mode=C.CREATE):
        self.init_obj(C.CUSTOMER, customer)
        self.result[C.CUSTOMER][customer[C.ID]][C.DSKY] = {ob[C.ID]: self.get_main_attr(ob) for ob in dsky}
        for product in dsky:
            prob_score = 1/len(dsky)
            if mode == C.CREATE:
                self.set_market_contribution(product, customer, prob_score, C.TRUE_RSKY)
            else:
                if product[C.ID] in self.result[C.PRODUCT]:
                    self.set_market_contribution(product, customer, prob_score, C.UPDATED_RSKY)


    def set_rsky(self, product, rsky):
        self.init_obj(C.PRODUCT, product)
        for customer in rsky:

            # cari customer ada di orthant mana nya si product 
            orthant_id = helper.find_orthant(product[C.VAL], customer[C.VAL])
            if not C.RSKY in self.result[C.PRODUCT][product[C.ID]]:
                self.result[C.PRODUCT][product[C.ID]][C.RSKY] = {}
            if not orthant_id in self.result[C.PRODUCT][product[C.ID]][C.RSKY]:
                self.result[C.PRODUCT][product[C.ID]][C.RSKY][orthant_id] = {}

            # append customer 
            self.result[C.PRODUCT][product[C.ID]][C.RSKY][orthant_id][customer[C.ID]] = self.get_main_attr(customer)


    def set_orthant(self, obj_type, obj, orthant_id, orthant_sky):
        self.init_obj(obj_type, obj)
        if not (C.ORTHANT in self.result[obj_type][obj[C.ID]]):
            self.result[obj_type][obj[C.ID]][C.ORTHANT] = {}

        # calculate anti dominance region 
        anti_dominance_region = []
        dim = len(obj[C.VAL])
        points = [o[C.VAL] for o in orthant_sky] + [obj[C.VAL]]
        for i in range(dim):
            val = [p[i] for p in points]
            each_dim = [min(val), max(val)]
            anti_dominance_region.append(each_dim)

        # save orthant skyline 
        self.result[obj_type][obj[C.ID]][C.ORTHANT][orthant_id] = {
            C.ADR: anti_dominance_region,
            C.OSKY: [self.get_main_attr(ob) for ob in orthant_sky]
        }

    
    def set_market_contribution(self, product, customer, prob_score, key=C.TRUE_RSKY):
        self.init_obj(C.PRODUCT, product)
        # cari customer ada di orthant mana nya si product 
        orthant_id = helper.find_orthant(product[C.VAL], customer[C.VAL])
        # save customer in reverse skyline of product 
        if not key in self.result[C.PRODUCT][product[C.ID]]:
            self.result[C.PRODUCT][product[C.ID]][key] = {}
        if not orthant_id in self.result[C.PRODUCT][product[C.ID]][key]:
            self.result[C.PRODUCT][product[C.ID]][key][orthant_id] = {}
        # append customer and market contribution in true reverse skyline
        self.result[C.PRODUCT][product[C.ID]][key][orthant_id][customer[C.ID]] = {**self.get_main_attr(customer), **{C.MC: prob_score}}
    

    def reset_dsky(self, customer):
        if customer[C.ID] in self.result[C.CUSTOMER]:
            self.result[C.CUSTOMER][customer[C.ID]][C.HISTORY_DSKY] = self.result[C.CUSTOMER][customer[C.ID]][C.DSKY].copy()
            self.result[C.CUSTOMER][customer[C.ID]][C.DSKY] = {}


    def reset_rsky(self, product):
        self.result[C.PRODUCT][product[C.ID]][C.RSKY] = {}
 

    def export(self, neighbor_id=None):
        if neighbor_id:
            self.result_pfile = getter.result_path(sitepath=self.site_path,
                                                   request=C.RESULT_C.PRODUCT_FILE,
                                                   opt=str(neighbor_id))
            self.result_cfile = getter.result_path(sitepath=self.site_path,
                                                   request=C.RESULT_C.CUSTOMER_FILE,
                                                   opt=str(neighbor_id))
            self.result_mc_file = getter.result_path(sitepath=self.site_path,
                                                     request=C.RESULT_MC_FILE,
                                                     opt=str(neighbor_id))
        io.export_json(self.result_path, self.result_pfile, self.result[C.PRODUCT])
        io.export_json(self.result_path, self.result_cfile, self.result[C.CUSTOMER])
    
    
    def update_true_rsky(self, product):
        if C.UPDATED_RSKY in self.result[C.PRODUCT]:
            self.result[C.PRODUCT][product[C.ID]][C.TRUE_RSKY] = self.result[C.PRODUCT][product[C.ID]][C.UPDATED_RSKY].copy()
            self.result[C.PRODUCT][product[C.ID]][C.UPDATED_RSKY] = {}


    def is_calculated(self, customer, mode=C.CREATE):
        key = C.DSKY if mode == C.CREATE else C.HISTORY_DSKY
        return customer[C.ID] in self.result[C.CUSTOMER] and\
               key in self.result[C.CUSTOMER][customer[C.ID]]
            