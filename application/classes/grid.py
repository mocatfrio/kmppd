import math
import csv
import itertools
import copy
import application.helpers.constant as C
import application.helpers.getter as getter
import application.helpers.io as io
import application.helpers.helper as helper
from application.classes.rtree import RTree
from prettyprinter import pprint


class Grid:
    def __init__(self, site_path, grid_size=None, pfile=None, cfile=None):
        self.site_path = site_path
        self.grid_path = getter.grid_path(sitepath=site_path)
        self.grid_file = getter.grid_path(sitepath=site_path,
                                          request=C.KEY_GRID_FILE)
        self.grid_info_file = getter.grid_path(sitepath=site_path,
                                               request=C.KEY_GRID_INFO_FILE)
        self.grid = io.import_json(self.grid_path, self.grid_file)
        self.grid_info = io.import_json(self.grid_path, self.grid_info_file)
    
        # save grid size 
        if not (C.GRID_SIZE in self.grid_info):
            self.grid_info[C.GRID_SIZE] = grid_size

        # save p file and c file 
        if pfile and cfile:
            self.pfile = pfile
            self.cfile = cfile
    

    def indexing_data(self):
        if self.grid:
            return

        # import data 
        pdict = []
        for site_id in self.pfile:
            pdict += [self.restructure(dict(obj), site_id)
                       for obj in list(csv.DictReader(open(self.pfile[site_id])))]
        cdict = []
        for site_id in self.cfile:
            cdict += [self.restructure(dict(obj), site_id)
                       for obj in list(csv.DictReader(open(self.cfile[site_id])))]

        # set range of grid box
        values = [obj[C.VAL] for obj in pdict + cdict]
        max_val = max(map(max, values))
        self.set_range(max_val)
    
        # indexing data 
        self.index_to_grid(C.PRODUCT, pdict)
        self.index_to_grid(C.CUSTOMER, cdict)
    
        # define boundary and RTree for each grid box 
        for grid_id in self.grid.keys():
            self.set_boundary(grid_id)
            self.generate_rtree(grid_id)
        
        # export all 
        io.export_json(self.grid_path, self.grid_file, self.grid)
        io.export_json(self.grid_path, self.grid_info_file, self.grid_info)


    """
    Grid Box
    """

    
    def set_range(self, max_val):
        if max_val % self.grid_info[C.GRID_SIZE] == 0:
            self.range = int(max_val / self.grid_info[C.GRID_SIZE])
        else:
            self.range = int((max_val + (self.grid_info[C.GRID_SIZE] - (max_val % self.grid_info[C.GRID_SIZE]))) / self.grid_info[C.GRID_SIZE])


    def set_boundary(self, grid_id):
        each_dim = [int(_) for _ in str(grid_id)]
        if not (C.GRID_BOUNDARY in self.grid_info):
            self.grid_info[C.GRID_BOUNDARY] = {}
        self.grid_info[C.GRID_BOUNDARY][grid_id] = tuple([(i * self.range, i * self.range + self.range)
                                                           for i in each_dim])


    def get_boundary(self, grid_id):
        if C.GRID_BOUNDARY in self.grid_info:
            return self.grid_info[C.GRID_BOUNDARY][grid_id]


    """
    Objects Setter
    """


    def restructure(self, dict_obj, site_id):
        # set columns
        excluded = ["id", "label"]  # columns in excel
        val_columns = list(set(dict_obj.keys()) - set(excluded))
        
        # restructure these columns
        dict_obj[C.ID] = "_".join([str(dict_obj[C.ID]), str(site_id)])
        dict_obj[C.VAL] = [int(dict_obj[key]) for key in val_columns]
        dict_obj[C.SITE_ID] = site_id

        # delete unneeded columns 
        for key in val_columns:
            dict_obj.pop(key, None)
        return dict_obj


    def index_to_grid(self, type, dict_obj):
        for obj in dict_obj:
            pos = self.get_pos(obj[C.VAL])
            if not (pos in self.grid): 
                self.grid[pos] = {}
            if not (type in self.grid[pos]):
                self.grid[pos][type] = {}
            additional_info = {C.POS: pos}
            self.grid[pos][type][obj[C.ID]] = {**obj, **additional_info}


    def get_pos(self, obj_val):
        pos = ""
        for val in obj_val:
            if val % self.range == 0:
                if not val:
                    idx = 0
                else:
                    idx = int((val/self.range) - 1)
            else:
                idx = int(math.floor(val/self.range))
            pos += str(idx)
        return pos
        

    """
    Objects Getter
    """


    def get_objects(self, grid_id=None, obj_type=None, obj_id=None, boundary=None):
        # get object based on id
        if obj_id:
            return self.grid[grid_id][obj_type][obj_id]
        
        # get collection of object
        objects = []
        if boundary:
            # get object based on boundary using the RTree 
            if obj_type in self.grid_info[C.GRID_RTREE][grid_id]:
                rtree = self.import_rtree(self.grid_info[C.GRID_RTREE][grid_id][obj_type])
                objects = rtree.search(boundary=boundary)
        else:
            # get object based on grid pos / all object 
            if grid_id is None:
                grid_id = list(self.grid.keys())
            for pos in self.as_list(grid_id):
                if obj_type in self.grid[pos]:
                    for val in self.grid[pos][obj_type].values():
                        objects.append(val)
        return objects


    def get_customers(self, grid_id=None, customer_id=None, boundary=None):
        return self.get_objects(grid_id=grid_id, 
                                obj_type=C.CUSTOMER,
                                obj_id=customer_id, 
                                boundary=boundary)


    def get_products(self, grid_id=None, product_id=None, boundary=None):
        return self.get_objects(grid_id=grid_id, 
                                obj_type=C.PRODUCT,
                                obj_id=product_id, 
                                boundary=boundary)


    """
    Neighbors
    """


    def get_neighbors(self, grid_id, orthant, level=1):
        result = []
        grid_id = self.as_int(grid_id)
        orthant = self.as_int(orthant)
        dim = len(grid_id)

        # get center box first 
        center_pos = [(grid_id[_] + level) if orthant[_] == 1 else (grid_id[_] - level)
                      for _ in range(dim)]
        if any(c < 0 for c in center_pos):
            return result
        result.append(self.as_str(center_pos))

        # expand to each dimension
        for i in range(dim):
            min = 0 if orthant[i] == 0 else center_pos[i] + 1
            max = center_pos[i] if orthant[i] == 0 else self.grid_info[C.GRID_SIZE] + 1
            cand = [copy.copy(center_pos) for _ in range(max-min)]
            for j in range(len(cand)):
                cand[j][i] = min
                min += 1
            cand = [self.as_str(c) for c in cand]
            result += cand
        return result


    """
    Orthants
    """


    def get_orthants(self, query_point):
        result = {}
        dim = len(query_point)

        # define orthant id
        for i in range(2**dim): 
            orthant_id = format(i, '#0{}b'.format(dim + 2))[2:]
            result[orthant_id] = {}

        for grid_id, grid_boundary in self.grid_info[C.GRID_BOUNDARY].items():
            # define orthant id for each grid box
            orthants = self.set_orthant(grid_boundary, query_point)

            # to check if any grid that divided into two or more orthant 
            part_num = len(orthants) 

            # grouping
            for orthant_id, grid_boundary in orthants.items():
                if not (part_num in result[orthant_id]):
                    result[orthant_id][part_num] = {}
                result[orthant_id][part_num][grid_id] = grid_boundary
        return result


    def set_orthant(self, grid_boundary, query_point):
        MIN = 0
        MAX = 1
        orthants = {}
        orthant_id = []
        orthant_box = []
        dim = len(query_point)

        # define orthant for each grid box 
        for i in range(dim):
            orthant_id_perdim = []
            orthant_box_perdim = []
            if grid_boundary[i][MIN] <= query_point[i]:
                orthant_id_perdim.append(0)
                if grid_boundary[i][MAX] > query_point[i]:
                    orthant_id_perdim.append(1)
                    orthant_box_perdim = [(grid_boundary[i][MIN], query_point[i]), 
                                          (query_point[i] + 1, grid_boundary[i][MAX])]
            else:
                orthant_id_perdim.append(1)
            if not orthant_box_perdim:
                orthant_box_perdim.append(grid_boundary[i])
            orthant_id.append(orthant_id_perdim)
            orthant_box.append(orthant_box_perdim)

        orthant_id = ["".join([str(i) for i in list(_)])
                              for _ in list(itertools.product(*orthant_id))]
        orthant_box = list(itertools.product(*orthant_box))
        for i in range(len(orthant_id)):
            orthants[orthant_id[i]] = tuple(orthant_box[i])
        return orthants


    def get_intersecting_grid(self, ADR, grid_in_orthant):
        # evaluate more 
        result = {}
        for part_num in grid_in_orthant:
            for grid_id in grid_in_orthant[part_num]:
                intersecting_region = helper.is_intersecting(grid_in_orthant[part_num][grid_id], ADR, True)
                if intersecting_region:
                    result[grid_id] = intersecting_region
        return result


    """
    RTree 
    """


    def generate_rtree(self, grid_id):
        for obj_type in self.grid[grid_id].keys():
            # init rtree 
            rtree = RTree(self.site_path)
            for obj_val in self.grid[grid_id][obj_type].values():
                rtree.insert(obj_val)
    
            # export rtree
            rtree_id = rtree.export()

            # save rtree 
            if not C.GRID_RTREE in self.grid_info:
                self.grid_info[C.GRID_RTREE] = {}
            if not grid_id in self.grid_info[C.GRID_RTREE]:
                self.grid_info[C.GRID_RTREE][grid_id] = {}
            self.grid_info[C.GRID_RTREE][grid_id][obj_type] = rtree_id


    def import_rtree(self, rtree_id):
        filepath = getter.rtree_path(sitepath=self.site_path)
        filename = getter.rtree_path(sitepath=self.site_path, rtree_id=rtree_id,
                                     request=C.KEY_RTREE_FILE)
        rtree = RTree(self.site_path, 
                      imported_data=io.import_json(filepath, filename)) 
        return rtree 


    def find_local_skyline(self, query_point, grid_id):
        skyline = []
        if C.PRODUCT in self.grid_info[C.GRID_RTREE][grid_id]:
            rtree = self.import_rtree(self.grid_info[C.GRID_RTREE][grid_id][C.PRODUCT])
            skyline = rtree.search(query_point=query_point)
        return skyline


    """
    Helper 
    """


    def as_int(self, str):
        return [int(_) for _ in str]


    def as_list(self, x):
        if type(x) is list:
            return x
        else:
            return [x]
    

    def as_str(self, list_of_int):
        return "".join([str(_) for _ in list_of_int])


    def print(self):
        pprint(self.grid)