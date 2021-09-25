import time
import os
import datetime
import psutil
import application.helpers.constant as C
import application.helpers.io as io


class Logger:
    def __init__(self, site_num=None, k=None, method=None, data_type=None,
                 data_num=None,dim_size=None, grid_size=None, on_site=None,
                 sim_id=None):
        self.info = {
            "site_num": self.as_str(site_num),
            "k": self.as_str(k),
            "method": self.as_str(method),
            "on_site": self.as_str(on_site),
            "data_type": self.as_str(data_type),
            "data_num": self.as_str(data_num),
            "dim_size": self.as_str(dim_size),
            "grid_size": self.as_str(grid_size),
        }
        self.start_time = None
        self.end_time = None
        self.ext = ".csv"
        self.log_path = C.LOG_PATH + sim_id + "/"
        self.log_file = self.log_path + "log_" + str(datetime.datetime.now().date()) + self.ext
    

    def start(self):
        self.start_time = time.time()


    def end(self, method=None, event=None):
        self.end_time = time.time()
        self.write(method, event)


    def write(self, method=None, event=None, with_info=True):
        desc = self.generate_event(method, event)
        self.write_log(desc, with_info)


    def on_site(self, site_id):
        self.info["on_site"] = site_id


    def get_info(self):
        return self.info


    def generate_event(self, method, event):
        desc = ''
        if method == C.NAIVE:
            desc += 'Naive Approach'
        elif method == C.KMPPD:
            desc += 'Strategic Approach (KMPPD)'
        elif method == C.OKMPPD:
            desc += 'Strategic Approach (Optimized-KMPPD)'
        else:
            desc += 'Unknown'
        return ' - '.join([desc, event])


    def as_str(self, var):
        if var is None:
            return "-"
        if type(var) is str:
            return var
        if type(var) is list:
            return " - ".join(var)
        return str(var)


    def calc_runtime(self):
        hours, the_rest = divmod(self.end_time - self.start_time, 3600)
        minutes, seconds = divmod(the_rest, 60)
        return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)
    

    def calc_mem_usage(self):
        process = psutil.Process(os.getpid())
        mem = process.memory_info().rss / 1024 ** 2     # MB
        return mem


    def write_log(self, event, with_info=True):
        rows = []

        # add column name 
        if not os.path.exists(self.log_file):
            col_name = ["Event"]
            col_name += [mystr.replace("_", " ").title() for mystr in list(self.info.keys())]
            col_name += ["Runtime (S)", "Mem Usage (MB)", "Timestamp"]
            rows.append(col_name)

        # logging
        row = [event]
        if with_info:
            row += list(self.info.values()) + [self.calc_runtime(), self.calc_mem_usage(), datetime.datetime.now()]
        rows.append(row)
        io.export_csv(self.log_path, self.log_file, rows, "a")
        
    