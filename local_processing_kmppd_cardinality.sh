#! /bin/bash

# LOCAL PROCESSING
# python3 index.py -o local_precompute -s <site_num> -t <dataset_type> -n <data_num> -d <dim_size> -m <method> -g <grid_size>

# example:
# python3 index.py -o local_precompute -s 3 -t ind -n 500 -d 2 -m kmppd -g 5

# CARDINALITY
# python3 index.py -o local_precompute -s 6 -t ind -n 500 -d 3 -m kmppd -g 5
# python3 index.py -o local_precompute -s 6 -t ind -n 1000 -d 3 -m kmppd -g 5
# python3 index.py -o local_precompute -s 6 -t ind -n 2000 -d 3 -m kmppd -g 5
# python3 index.py -o local_precompute -s 6 -t ind -n 5000 -d 3 -m kmppd -g 5
# python3 index.py -o local_precompute -s 6 -t ind -n 10000 -d 3 -m kmppd -g 5

# python3 index.py -o local_precompute -s 6 -t ant -n 500 -d 3 -m kmppd -g 5
# python3 index.py -o local_precompute -s 6 -t ant -n 1000 -d 3 -m kmppd -g 5
# python3 index.py -o local_precompute -s 6 -t ant -n 2000 -d 3 -m kmppd -g 5
# python3 index.py -o local_precompute -s 6 -t ant -n 5000 -d 3 -m kmppd -g 5
# python3 index.py -o local_precompute -s 6 -t ant -n 10000 -d 3 -m kmppd -g 5

# python3 index.py -o local_precompute -s 6 -t fc -n 500 -d 3 -m kmppd -g 5
# python3 index.py -o local_precompute -s 6 -t fc -n 1000 -d 3 -m kmppd -g 5
# python3 index.py -o local_precompute -s 6 -t fc -n 2000 -d 3 -m kmppd -g 5
# python3 index.py -o local_precompute -s 6 -t fc -n 5000 -d 3 -m kmppd -g 5
# python3 index.py -o local_precompute -s 6 -t fc -n 10000 -d 3 -m kmppd -g 5

