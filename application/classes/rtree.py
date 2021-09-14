import itertools
import uuid
import application.helpers.constant as C
import application.helpers.io as io
import application.helpers.helper as helper
import application.helpers.getter as getter
import application.core.reusable as sky


# node 
PARENT = 0
MBB = 1
CHILD = 2
IS_LEAF = 3

# skyline 
OBJ = 0 
MINDIST = 1
VALUE = 2


class RTree:
    def __init__(self, site_path, min_child=2, imported_data={}):
        # {node_id: [parent_id, bounding_box, child_id, is_leaf]}
        self.rtree = {int(k):v for k,v in imported_data.items()}
        self.root = self.rtree.pop(0, None) if imported_data else None
        self.min_children = min_child
        self.objects = []
        self.heap = []
        self.site_path = site_path


    def export(self):
        rtree_id = str(uuid.uuid4())
        rtree_path = getter.rtree_path(sitepath=self.site_path)
        rtree_filename = getter.rtree_path(sitepath=self.site_path, rtree_id=rtree_id,
                                           request=C.KEY_RTREE_FILE)
        
        # before exported, add rtree root id in the dict
        self.rtree[0] = self.root
        io.export_json(rtree_path, rtree_filename, self.rtree)
        return rtree_id
    

    def insert(self, obj):
        # format obj => {'id': '361',
        #                'label': 'customer-361', 
        #                'val': [131, 256, 249]}
        if self.root:
            node_id = self.find_leaf(obj[C.VAL])
            self.update_node(node_id, child_id=obj)
            self.root = self.adjust_tree(node_id)
        else:
            bounding_box = self.calc_bounding_box(obj[C.VAL])
            node_id = self.create_node(None, bounding_box, obj, True)
            self.root = node_id


    def search(self, boundary=None, query_point=None):
        # reset
        self.objects = [] 
        self.heap = []
        node_id = self.root

        # search
        if boundary:
            self.get_objects(node_id, boundary)
        if query_point:
            self.find_skyline(node_id, query_point)
        return self.objects


    def find_skyline(self, node_id, query_point):
        # BBS algorithm 
        for child in self.rtree[node_id][CHILD]:
            obj = [child]
            if self.rtree[node_id][IS_LEAF]:
                obj += self.calc_mindist(query_point[C.VAL], min_point=child[C.VAL])
            else:
                obj += self.calc_mindist(query_point[C.VAL], bounding_box=self.rtree[child][MBB])
            self.heap.append(obj)
        self.heap = sorted(self.heap, key=lambda x: x[MINDIST])
        while self.heap:
            expanded_obj = self.heap.pop(0)
            if sky.is_dominated(query_point, expanded_obj[VALUE], self.objects):
                continue
            if not type(expanded_obj[OBJ]) is dict:
                self.find_skyline(expanded_obj[OBJ], query_point)
            else:
                self.objects.append(expanded_obj[OBJ])


    """
    NODE  
    """


    def create_node(self, parent_id=None, bounding_box=None, child_id=None, is_leaf=False):
        node_id = max(self.rtree.keys()) + 1 if self.rtree else 1
        if child_id:
            child_id = self.as_list(child_id)
        self.rtree[node_id] = [parent_id, bounding_box, child_id, is_leaf]

        # update bounding box 
        if child_id and not bounding_box:
            self.update_node(node_id, child_id=child_id)
        return node_id


    def update_node(self, node_id, parent_id=None, bounding_box=None, child_id=None, is_leaf=False):
        if parent_id:
            self.rtree[node_id][PARENT] = parent_id
        if bounding_box:
            self.rtree[node_id][MBB] = bounding_box
        if is_leaf:
            self.rtree[node_id][IS_LEAF] = is_leaf
        if child_id:
            if type(child_id) is list:
                self.rtree[node_id][CHILD] = child_id
            else:
                self.rtree[node_id][CHILD].append(child_id)

            # update is leaf and bounding box
            if self.is_object(self.rtree[node_id][CHILD][0]):
                self.rtree[node_id][IS_LEAF] = True
                MBBs = [self.calc_bounding_box(obj[C.VAL]) for obj in self.rtree[node_id][CHILD]]
            else:
                self.rtree[node_id][IS_LEAF] = False
                MBBs = [self.rtree[child_id][MBB] for child_id in self.rtree[node_id][CHILD]]
            self.rtree[node_id][MBB] = self.adjust_bounding_box(MBBs)


    """ 
    Searching
    """


    def calc_mindist(self, query_point, min_point=None, bounding_box=None):
        mindist = None
        minpoint = None
        if bounding_box:
            corners = list(itertools.product(*bounding_box)) 
        if min_point:
            corners = [min_point]
        for corner in corners:
            dist = 0
            for i in range(len(corner)):
                dist += abs(query_point[i] - corner[i])
            try:
                if dist < mindist:
                    mindist = dist
                    minpoint = corner
            except:
                mindist = dist
                minpoint = corner
        return [mindist, minpoint]


    def expand_child(self, bounding_box, children):
        # search child with minimum boundary 
        min_boundary = None
        selected_child_id = None
        for child_id in children:
            bounding_box_2 = self.get_bounding_box(child_id)
            boundary = self.calc_boundary(bounding_box, bounding_box_2)
            try:
                if boundary < min_boundary:
                    min_boundary = boundary
                    selected_child_id = child_id
            except TypeError:
                min_boundary = boundary
                selected_child_id = child_id
        return selected_child_id 


    def find_leaf(self, obj_val, node_id=None):
        # start from root 
        if not node_id:
            node_id = self.root

        # if the leaf is found 
        if self.rtree[node_id][IS_LEAF]:
            return node_id

        # choose child for expansion
        bounding_box = self.calc_bounding_box(obj_val)
        child_id = self.expand_child(bounding_box, self.rtree[node_id][CHILD])
        return self.find_leaf(obj_val, child_id)
    

    def find_cand(self, node_id, boundary):
        # pruning the child outside the boundary
        cand = []
        for child_id in self.rtree[node_id][CHILD]:
            child_boundary = self.rtree[child_id][MBB]
            if helper.is_intersecting(child_boundary, boundary):
                cand.append(child_id)
        return cand


    def get_objects(self, node_id, boundary):
        # stop if it is leaf
        if self.rtree[node_id][IS_LEAF]:
            children = [node_id]
        else:
            children = self.find_cand(node_id, boundary)

        for child_id in children:
            if self.rtree[child_id][IS_LEAF]:
                for obj in self.rtree[child_id][CHILD]:
                    if helper.is_inside(obj[C.VAL], boundary):
                        self.objects.append(obj)
            else:
                self.get_objects(child_id, boundary)


    """ 
    Adjust Tree
    """ 


    def adjust_tree(self, node_id):            
        # check if the number of child of node is more than min children defined
        if len(self.rtree[node_id][CHILD]) > self.min_children:
            self.split_node(node_id)
        
        # stop if it is root 
        if not self.rtree[node_id][PARENT]:
            return node_id
        
        # continue to adjust the parents 
        return self.adjust_tree(self.rtree[node_id][PARENT])


    def pick_seeds(self, children):
        # get two children that form the largest boundary
        max_boundary = None
        seeds = [None, None]
        for i in range(0, len(children)):
            for j in range(i + 1, len(children)):
                bounding_box_1 = self.get_bounding_box(children[i])
                bounding_box_2 = self.get_bounding_box(children[j])
                boundary = self.calc_boundary(bounding_box_1, bounding_box_2)
                try:
                    if boundary > max_boundary:
                        max_boundary = boundary
                        seeds = [children[i], children[j]]
                except TypeError:
                    max_boundary = boundary
                    seeds = [children[i], children[j]]
        return seeds


    def split_node(self, node_id):
        # using quadratic-cost algorithm
        # pick seed
        seeds = self.pick_seeds(self.rtree[node_id][CHILD])
        new_set = [[seeds[0]], [seeds[1]]]

        # get other children besides seeds 
        if self.is_object(seeds[0]):
            obj_id = list(set([obj[C.ID] for obj in self.rtree[node_id][CHILD]]) - set([obj[C.ID] for obj in seeds]))
            idx  = [next((index for (index, d) in enumerate(self.rtree[node_id][CHILD]) if d[C.ID] == oid), None) for oid in obj_id]
            other_children = [self.rtree[node_id][CHILD][i] for i in idx]
        else:
            other_children = list(set(self.rtree[node_id][CHILD]) - set(seeds))
        
        # split other children 
        if other_children:
            for child_id in other_children:
                bounding_box = self.get_bounding_box(child_id)
                selected_seed_id = self.expand_child(bounding_box, seeds)
                new_set[seeds.index(selected_seed_id)].append(child_id)

        # update the existing node
        self.update_node(node_id, child_id=new_set[0])

        # create new root if it is root node
        if not self.rtree[node_id][PARENT]:
            new_root_id = self.create_node(parent_id=None, child_id=node_id)
            # update the parent of existing node
            self.update_node(node_id, parent_id=new_root_id)

        # create new splitted node 
        new_node_id = self.create_node(parent_id=self.rtree[node_id][PARENT])
        self.update_node(new_node_id, child_id=new_set[1])

        # update the parent to add the splitted node as new child
        self.update_node(self.rtree[node_id][PARENT], child_id=new_node_id)


    """ 
    Bounding box & Boundary
    """  


    def adjust_bounding_box(self, MBBs):
        dim = len(MBBs[0])
        MBB = [[min(map(min, [mbb[_] for mbb in MBBs])), max(map(max, [mbb[_] for mbb in MBBs]))] for _ in range(dim)]
        return MBB

  
    def calc_bounding_box(self, obj_val):
        return [[val, val] for val in obj_val]


    def calc_boundary(self, box_1, box_2):
        boundary = 0
        dim = len(box_1)
        for i in range(dim):
            boundary += max([max(box_1[i]), max(box_2[i])]) - min([min(box_1[i]), min(box_2[i])])
        return boundary   


    def get_bounding_box(self, child_id):
        if self.is_object(child_id):
            return self.calc_bounding_box(child_id[C.VAL])
        else:
            return self.rtree[child_id][MBB]


    """ 
    Helper
    """ 

    
    def as_list(self, x):
        if type(x) is list:
            return x
        else:
            return [x]
    
    def is_object(self, child):
        return type(child) is dict
    