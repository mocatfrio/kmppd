

import getopt
import sys
import system.core.dataset as dataset
import system.core.line_graph as line_graph
import system.core.scatterplot as scatterplot
import system.core.simulation as simulation
import system.core.accuracy as accuracy
import system.core.scenario as scenario
import system.core.test_result as test_result
import application.helpers.constant as C


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
        print_help()
        sys.exit(2)
    if not opts:
        print_help()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
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
    if command == C.GEN_DATASET:
        # python3 index.py -o generate_dataset -s 3 -t ind -n 500 -d 2 
        dataset.generate(site_num, data_type, data_num, dim_size)
        print('Data generation successfully done!')
    
    elif command == C.LOCAL_PRECOMPUTE:
        # python3 index.py -o local_precompute -s 3 -t ind -n 500 -d 2 -m kmppd -g 5
        if method == C.NAIVE:
            print('Naive approach cant be precomputed')
            sys.exit(0)
        simulation.local_precompute(site_num, method, data_type, data_num, dim_size, grid_size)
        print('Local precomputing successfully done!')
    
    elif command == C.GLOBAL_PRECOMPUTE:
        # python3 index.py -o global_precompute -s 3 -t ind -n 500 -d 2 -m kmppd -g 5
        if method == C.NAIVE:
            print('Naive approach cant be precomputed')
            sys.exit(0)
        simulation.global_precompute(site_num, method, data_type, data_num, dim_size, grid_size)
        print('Global precomputing successfully done!')

    elif command == C.RUN_QUERY:
        # python3 index.py -o run_query -k 10 -s 3 -m kmppd -t ind -n 500 -d 2 -g 5
        simulation.run_query(k, site_num, method, data_type, data_num, dim_size, grid_size)
        print('Query processing successfully done!')
    
    elif command == C.RESET_SIM:
        # python3 index.py -o reset_simulation -t ind -n 500 -d 2 -m kmppd -g 5 -y 0
        # python3 index.py -o reset_simulation -x kmppd_ind_500_2_5 -y 0
        if 'sim_name' in locals():
            simulation.reset(sim_name=sim_name, delete_logs=del_logs)
        else:
            simulation.reset(method, data_type, data_num, dim_size, grid_size, delete_logs=del_logs)
        print('Simulation reset successfully done!')

    elif command == C.GEN_LINE_GRAPH:
        line_graph.generate(effect, data_type, metric)
    
    elif command == C.GEN_SCATTERPLOT:
        # python3 index.py -o generate_scatterplot -s 1 -p fc_500_2_product.csv -c fc_500_2_customer.csv
        scatterplot.generate(pfile, cfile, site_num)
    
    elif command == C.CHECK_ACCURACY:
        site_id = site_num
        accuracy.check(site_id, pfile, cfile, grid_size, method)

    elif command == C.GEN_SCENARIO:
        scenario.generate()

    elif command == C.GEN_TEST_RESULT:
        test_result.generate()
    
    # except Exception as e:
    #     print(e)

def print_help():
    lst_of_command = [C.GEN_DATASET, C.PRECOMPUTE, C.RUN_QUERY, C.RESET_SIM, C.GEN_LINE_GRAPH, C.GEN_SCATTERPLOT, C.CHECK_ACCURACY, C.GEN_TEST_RESULT, C.GEN_SCENARIO]
    lst_of_dataset_type = [C.IND, C.ANT, C.FC]
    lst_of_method = [C.KMPPD, C.OKMPPD, C.NAIVE]

    print("usage: python3 index.py [-ostndmkgxpceiy] [parameter...]")
    print("-------------------options-------------------")
    print("-o \t : command, i.e.:")
    for com in lst_of_command:
        print("\t   -", com)
    print("-s \t : number of site")
    print("-t \t : dataset type, i.e.:")
    for dt in lst_of_dataset_type:
        print("\t   -", dt)
    print("-n \t : number of data row")
    print("-d \t : number of data dimension")
    print("-m \t : method")
    for met in lst_of_method:
        print("\t   -", met)
    print("-k \t : number of query result")
    print("-g \t : grid size")
    print("-x \t : simulation name")
    print("-p \t : product filename")
    print("-c \t : customer filename")
    print("-e \t : effect of")
    print("-i \t : metric")
    print("-y \t : delete logs?")

if __name__ == '__main__':
    main(sys.argv[1:])
