#! /bin/bash

# GLOBAL PROCESSING
# python3 index.py -o global_precompute -s <site_num> -t <dataset_type> -n <data_num> -d <dim_size> -m <method> -g <grid_size>

# example:
# python3 index.py -o global_precompute -s 3 -t ind -n 500 -d 2 -m kmppd -g 5

# Dimensional
# python3 index.py -o global_precompute -s 4 -t ind -n 5000 -d 2 -m kmppd -g 5
# python3 index.py -o global_precompute -s 4 -t ind -n 5000 -d 4 -m kmppd -g 5
# python3 index.py -o global_precompute -s 4 -t ant -n 5000 -d 2 -m kmppd -g 5
# python3 index.py -o global_precompute -s 4 -t ant -n 5000 -d 4 -m kmppd -g 5
python3 index.py -o global_precompute -s 4 -t fc -n 5000 -d 2 -m kmppd -g 5
# python3 index.py -o global_precompute -s 4 -t fc -n 5000 -d 4 -m kmppd -g 5

# python3 index.py -o global_precompute -s 4 -t ind -n 5000 -d 2 -m optimized_kmppd -g 5
python3 index.py -o global_precompute -s 4 -t ind -n 5000 -d 4 -m optimized_kmppd -g 5
## python3 index.py -o global_precompute -s 4 -t ant -n 5000 -d 2 -m optimized_kmppd -g 5
# python3 index.py -o global_precompute -s 4 -t ant -n 5000 -d 4 -m optimized_kmppd -g 5
# python3 index.py -o global_precompute -s 4 -t fc -n 5000 -d 2 -m optimized_kmppd -g 5
# python3 index.py -o global_precompute -s 4 -t fc -n 5000 -d 4 -m optimized_kmppd -g 5
