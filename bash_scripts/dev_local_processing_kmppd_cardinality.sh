#! /bin/bash

# LOCAL PROCESSING
# python3 index.py -o precompute -s <site_num> -t <dataset_type> -n <data_num> -d <dim_size> -m <method> -g <grid_size>

# example:
# python3 index.py -o precompute -s 3 -t ind -n 500 -d 2 -m kmppd -g 5

# CARDINALITY
python3 index.py -o precompute -s 3 -t ind -n 100 -d 3 -m kmppd -g 5
python3 index.py -o precompute -s 3 -t ind -n 500 -d 3 -m kmppd -g 5
python3 index.py -o precompute -s 3 -t ind -n 1000 -d 3 -m kmppd -g 5

python3 index.py -o precompute -s 3 -t ant -n 100 -d 3 -m kmppd -g 5
python3 index.py -o precompute -s 3 -t ant -n 500 -d 3 -m kmppd -g 5
python3 index.py -o precompute -s 3 -t ant -n 1000 -d 3 -m kmppd -g 5

python3 index.py -o precompute -s 3 -t fc -n 100 -d 3 -m kmppd -g 5
python3 index.py -o precompute -s 3 -t fc -n 500 -d 3 -m kmppd -g 5
python3 index.py -o precompute -s 3 -t fc -n 1000 -d 3 -m kmppd -g 5

