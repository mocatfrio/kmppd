import matplotlib.pyplot as plt
# import matplotlib.ticker as mticker
import application.helpers.constant as C
import application.helpers.log as log
import application.helpers.io as io
import application.helpers.getter as getter

EXT = 'png'
DPI = 300
GRAPH_TYPE = 'line_graph'


def generate(effect, data_type, metric):
    if metric == C.KEY_INDEX_TIME:
        y_label = "Waktu Pengindeksan Data (detik)"
    elif metric == C.KEY_LP_TIME:
        y_label = "Waktu Pemrosesan Lokal (detik)"
    elif metric == C.KEY_QUERY_TIME:
        y_label = "Total Waktu Kueri (detik)"
    elif metric == C.KEY_INDEX_MEM:
        y_label = "Penggunaan Memori Pengindeksan Data (MB)"
    elif metric == C.KEY_LP_MEM:
        y_label = "Penggunaan Memori Pemrosesan Lokal (MB)"
    elif metric == C.KEY_QUERY_MEM:
        y_label = "Biaya Bandwith (MB)"

    # define control variable 
    site_num = "4"
    data_num = "2000"
    dim_size = "3"
    grid_size = "5"
    k = "30"

    # Jumlah Sites
    if effect == C.KEY_SITE_NUM:
        x_label = "Jumlah Sites"
        x = [2, 3, 4, 5, 6] # variable manipulasi 
        y1 = [log.read(C.KMPPD, data_type, data_num, dim_size, grid_size, metric, str(i), k) for i in x]
        y2 = [log.read(C.NAIVE_KMPP, data_type, data_num, dim_size, grid_size, metric, str(i), k) for i in x]
        # if metric == 3:
        #     y3 = [log.read(C.NAIVE, data_type, data_num, dim_size, grid_size, metric, str(i), k) for i in x]
        if metric == 3:
            ylim = [0, 2000] # sek gatau
    # Jumlah Data Per Site
    elif effect == C.KEY_DATA_NUM:
        x_label = "Jumlah Data Per Site"
        # x = [500, 1000, 2000, 5000, 10000]
        x = [500, 1000, 2000]

        y1 = [log.read(C.KMPPD, data_type, str(i), dim_size, grid_size, metric, site_num, k, True) for i in x]
        y2 = [log.read(C.NAIVE_KMPP, data_type, str(i), dim_size, grid_size, metric, site_num, k, True) for i in x]
        if metric == 3:
            if data_type == 1:
                y3 = [log.read(C.NAIVE, data_type, str(i), dim_size, grid_size, metric, site_num, k, True) for i in x]
            ylim = [0, 5000] # sek gatau
            # ylim = [0, 3000] # sek gatau
        if metric == 1:
            ylim = [0, 10] # sek gatau
        elif metric == 2:
            ylim = [0, 1000] # sek gatau
        elif metric == 5:
            ylim = [0, 500] # sek gatau
        
    # Jumlah Dimensi Data
    elif effect == C.KEY_DIM:
        x_label = "Jumlah Dimensi Data"
        x = [2, 3, 4]
        y1 = [log.read(C.KMPPD, data_type, data_num, str(i), grid_size, metric, site_num, k) for i in x]
        y2 = [log.read(C.NAIVE_KMPP, data_type, data_num, str(i), grid_size, metric, site_num, k) for i in x]
        if metric == 1:
            ylim = [0, 10] # sek gatau
        elif metric == 2:
            ylim = [0, 5000] # sek gatau
        elif metric == 5:
            ylim = [0, 1500] # sek gatau
        if metric == 3:
            ylim = [0, 8000] # sek gatau

        # if metric == 3:
        #     y3 = [log.read(C.NAIVE, data_type, data_num, str(i), grid_size, metric, site_num, k) for i in x]
        # limit
        # ylim = [0, 25000] # sek gatau
    
    # Jumlah Grid
    elif effect == C.KEY_GRID:
        x_label = "Jumlah Grid"
        x = [3, 4, 5, 6, 7]
        y1 = [log.read(C.KMPPD, data_type, data_num, dim_size, str(i), metric, site_num, k) for i in x]
        y2 = [log.read(C.NAIVE_KMPP, data_type, data_num, dim_size, str(i), metric, site_num, k) for i in x]
        if metric == 1:
            ylim = [0, 10] # sek gatau
        elif metric == 2:
            ylim = [0, 5000] # sek gatau
        elif metric == 5:
            ylim = [0, 1000] # sek gatau
        if metric == 3:
            ylim = [0, 5000] # sek gatau
        # if metric == 3:
        #     y3 = [log.read(C.NAIVE, data_type, data_num, dim_size, str(i), metric, site_num, k) for i in x]
        # limit
        # ylim = [0, 25000] # sek gatau
    
    # Jumlah k
    elif effect == C.KEY_K:
        x_label = "Jumlah k"
        x = [10, 20, 30, 40, 50]
        y1 = [log.read(C.KMPPD, data_type, data_num, dim_size, grid_size, metric, site_num, str(i)) for i in x]
        y2 = [log.read(C.NAIVE_KMPP, data_type, data_num, dim_size, grid_size, metric, site_num, str(i)) for i in x]
        # if metric == 3:
        #     y3 = [log.read(C.NAIVE, data_type, data_num, dim_size, grid_size, metric, site_num, str(i)) for i in x]
        # limit
        # ylim = [0, 25000] # sek gatau
        if metric == 3:
            ylim = [0, 3000] # sek gatau

    # plotting the line 1  
    plt.plot(x, y2, label = "C.KMPPD", color='blue', linestyle='dashed', marker='v',
             markerfacecolor='blue', markersize=5)
    # plotting the line 2  
    plt.plot(x, y1, label = "C.KMPPD-RiG", color='coral', linestyle='dashed', marker='o',
             markerfacecolor='coral', markersize=5)
    # plotting the line 3  
    if 'y3' in locals():
        plt.plot(x, y3, label = "Naive", color='forestgreen', linestyle='dashed', marker='s',
                 markerfacecolor='forestgreen', markersize=5)

    # limit the y axis
    if 'ylim' in locals():
        plt.ylim(ylim)
    
    # naming the x axis and y axis
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # show a legend on the plot
    plt.legend()
    
    # # function to show the plot
    # plt.show()

    # generate filename 
    metric_desc = y_label.lower().split(" (")[0].replace(" ", "_")
    effect_desc = x_label.lower().replace(" ", "_")
    filename = "_".join([data_type, metric_desc, effect_desc]) + EXT

    # save the plot 
    graph_path = getter.graph_path(graph_type=GRAPH_TYPE,
                                   opt="/".join([effect_desc, metric_desc]))
    io.export_graph(graph_path, filename, plt, EXT, DPI)
