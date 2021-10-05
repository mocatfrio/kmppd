#! /bin/bash

# LOCAL PROCESSING
# python3 index.py -o precompute -s <site_num> -t <dataset_type> -n <data_num> -d <dim_size> -m <method> -g <grid_size>

# example:
# python3 index.py -o precompute -s 3 -t ind -n 500 -d 2 -m kmppd -g 5

# DIMENSIONALITY
python3 index.py -o precompute -s 6 -t ind -n 5000 -d 2 -m optimized_kmppd -g 5
#python3 index.py -o precompute -s 6 -t ind -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o precompute -s 6 -t ind -n 5000 -d 4 -m optimized_kmppd -g 5

python3 index.py -o precompute -s 6 -t ant -n 5000 -d 2 -m optimized_kmppd -g 5
#python3 index.py -o precompute -s 6 -t ant -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o precompute -s 6 -t ant -n 5000 -d 4 -m optimized_kmppd -g 5

python3 index.py -o precompute -s 6 -t fc -n 5000 -d 2 -m optimized_kmppd -g 5
#python3 index.py -o precompute -s 6 -t fc -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o precompute -s 6 -t fc -n 5000 -d 4 -m optimized_kmppd -g 5

