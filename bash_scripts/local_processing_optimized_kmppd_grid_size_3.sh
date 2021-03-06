#! /bin/bash

# LOCAL PROCESSING
# python3 index.py -o local_precompute -s <site_num> -t <dataset_type> -n <data_num> -d <dim_size> -m <method> -g <grid_size>

# example:
# python3 index.py -o local_precompute -s 3 -t ind -n 500 -d 2 -m kmppd -g 5

# GRID SIZE
# python3 index.py -o local_precompute -s 4 -t ind -n 5000 -d 3 -m optimized_kmppd -g 3
# python3 index.py -o local_precompute -s 4 -t ind -n 5000 -d 3 -m optimized_kmppd -g 4
# python3 index.py -o local_precompute -s 4 -t ind -n 5000 -d 3 -m optimized_kmppd -g 6
# python3 index.py -o local_precompute -s 4 -t ind -n 5000 -d 3 -m optimized_kmppd -g 7

# python3 index.py -o local_precompute -s 4 -t ant -n 5000 -d 3 -m optimized_kmppd -g 3
# python3 index.py -o local_precompute -s 4 -t ant -n 5000 -d 3 -m optimized_kmppd -g 4
# python3 index.py -o local_precompute -s 4 -t ant -n 5000 -d 3 -m optimized_kmppd -g 6
# python3 index.py -o local_precompute -s 4 -t ant -n 5000 -d 3 -m optimized_kmppd -g 7

# python3 index.py -o local_precompute -s 4 -t fc -n 5000 -d 3 -m optimized_kmppd -g 3
python3 index.py -o local_precompute -s 4 -t fc -n 5000 -d 3 -m optimized_kmppd -g 4
python3 index.py -o local_precompute -s 4 -t fc -n 5000 -d 3 -m optimized_kmppd -g 6
python3 index.py -o local_precompute -s 4 -t fc -n 5000 -d 3 -m optimized_kmppd -g 7

