import pandas as pd
import matplotlib.pyplot as plt
import application.helpers.getter as getter
import application.helpers.io as io

EXT = 'png'
DPI = 300
GRAPH_TYPE = 'scatterplot'


def generate(pfile, cfile, site_num=1):
    for i in range(1, site_num + 1):
        site_id = str(i)
        dataset_path = getter.dataset_path(site_id=site_id)
        graph_path = getter.graph_path(site_id=site_id, graph_type=GRAPH_TYPE) 

        # import data 
        if pfile:
            new_pfile = dataset_path + pfile
            p_df = pd.read_csv(new_pfile)
            opt = "product"
        if cfile:
            new_cfile = dataset_path + cfile
            c_df = pd.read_csv(new_cfile)
            opt = "customer"
        if pfile and cfile:
            frames = [p_df, c_df]
            df = pd.concat(frames)
            opt = "all"
        elif not pfile:
            df = c_df
        elif not cfile:
            df = p_df
        # generate graph 
        x_attr = df.columns[2]
        y_attr = df.columns[3]
        graph = df.plot(kind='scatter',x=x_attr, y=y_attr, color='Black') 
        graph.set_xlabel("")
        graph.set_ylabel("")

        # uncomment if u want to display the plot 
        # plt.show()

        # generate filename 
        total_data = 0
        if pfile:
            total_data += int(pfile.split("_")[1])
            filename = "_".join([GRAPH_TYPE, pfile.split("_")[0], str(total_data), pfile.split("_")[2], "site", site_id, opt]) + "." + EXT
        if cfile:
            total_data += int(cfile.split("_")[1])
            filename = "_".join([GRAPH_TYPE, cfile.split("_")[0], str(total_data), cfile.split("_")[2], "site", site_id, opt]) + "." + EXT
        
        # save the plot
        io.export_graph(graph_path, filename, plt, EXT, DPI)
