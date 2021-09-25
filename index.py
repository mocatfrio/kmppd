

import getopt
import sys
import system.core.dataset as dataset
import system.core.line_graph as line_graph
import system.core.scatterplot as scatterplot
import system.core.simulation as simulation
import system.core.accuracy as accuracy
import application.helpers.constant as C

# command 
GEN_DATASET = 'generate_dataset'
PRECOMPUTE = 'precompute'
RUN_QUERY = 'run_query'
RESET_SIM = 'reset_simulation'
GEN_LINE_GRAPH = 'generate_line_graph'
GEN_SCATTERPLOT = 'generate_scatterplot'
CHECK_ACCURACY = 'check_accuracy'


def main(argv):
    pfile = None
    cfile = None
    del_logs = False

    # get arguments 
    short_command = 'ho:s:t:n:d:m:k:g:x:p:c:e:i:y:'
    long_command = ['help', 'option=', 'site=', 'type=', 'num=', 'dim=', 'method=', 'k=', 'grid=', 'sim_name=', 'pfile=', 'cfile=', 'effect=', 'metric=', 'del_logs=']
    try:
        opts, args = getopt.getopt(argv, short_command, long_command)
    except getopt.GetoptError:
        print("index.py -s <number of site> -t <dataset type> -n <number of data> -d <dim size> -m <method> -k <k> -g <grid size> -x <simulation name> -p <product filename> -c <customer filename> -e <effect> -i <metric> -y <delete_logs>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("index.py -s <number of site> -t <dataset type> -n <number of data> -d <dim size> -m <method> -k <k> -g <grid size> -x <simulation name> -p <product filename> -c <customer filename> -e <effect> -i <metric> -y <delete_logs>")
            sys.exit()
        elif opt in ("-o", "--option"):
            command = arg
        elif opt in ("-s", "--site"):
            site_num = int(arg)
        elif opt in ("-t", "--type"):
            data_type = arg
        elif opt in ("-n", "--num"):
            data_num = int(arg)
        elif opt in ("-d", "--dim"):
            dim_size = int(arg)
        elif opt in ("-m", "--method"):
            method = arg
        elif opt in ("-k", "--k"):
            k = int(arg)
        elif opt in ("-g", "--grid"):
            grid_size = int(arg)
        elif opt in ("-x", "--sim_name"):
            sim_name = arg
        elif opt in ("-p", "--pfile"):
            pfile = arg
        elif opt in ("-c", "--cfile"):
            cfile = arg
        elif opt in ("-e", "--effect"):
            effect = arg
        elif opt in ("-i", "--metric"):
            metric = arg
        elif opt in ("-y", "--del_logs"):
            if arg == str(0):
                del_logs = True
            else:
                del_logs = False

    # try:
    if command == GEN_DATASET:
        # python3 index.py -o generate_dataset -s 3 -t ind -n 500 -d 2 
        dataset.generate(site_num, data_type, data_num, dim_size)
        print('Data generation successfully done!')
    
    elif command == PRECOMPUTE:
        # python3 index.py -o precompute -s 3 -t ind -n 500 -d 2 -m kmppd -g 5
        if method == C.NAIVE:
            print('Naive approach cant be precomputed')
            sys.exit(0)
        simulation.precompute(site_num, method, data_type, data_num, dim_size, grid_size)
        print('Data precomputing successfully done!')
    
    elif command == RUN_QUERY:
        # python3 index.py -o run_query -k 10 -s 3 -m kmppd -t ind -n 500 -d 2 -g 5
        simulation.run_query(k, site_num, method, data_type, data_num, dim_size, grid_size)
        print('Query processing successfully done!')
    
    elif command == RESET_SIM:
        # python3 index.py -o reset_simulation -t ind -n 500 -d 2 -m kmppd -g 5 -y 0
        # python3 index.py -o reset_simulation -x kmppd_ind_500_2_5 -y 0
        if 'sim_name' in locals():
            simulation.reset(sim_name=sim_name, delete_logs=del_logs)
        else:
            simulation.reset(method, data_type, data_num, dim_size, grid_size, delete_logs=del_logs)
        print('Simulation reset successfully done!')

    elif command == GEN_LINE_GRAPH:
        line_graph.generate(effect, data_type, metric)
    
    elif command == GEN_SCATTERPLOT:
        # python3 index.py -o generate_scatterplot -s 1 -p fc_500_2_product.csv -c fc_500_2_customer.csv
        scatterplot.generate(pfile, cfile, site_num)
    
    elif command == CHECK_ACCURACY:
        site_id = site_num
        accuracy.check(site_id, pfile, cfile, grid_size, method)
    
    # except Exception as e:
    #     print(e)


if __name__ == '__main__':
    main(sys.argv[1:])
