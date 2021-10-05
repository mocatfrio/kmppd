#! /bin/bash

# GLOBAL PROCESSING
# python3 index.py -o run_query -k <k> -s <site_num> -t <dataset_type> -n <data_num> -d <dim_size> -m <method> -g <grid_size>

# example:
# python3 index.py -o run_query -k 10 -s 3 -t ind -n 500 -d 2 -m kmppd -g 5

# SITE NUM
python3 index.py -o run_query -k 30 -s 2 -t ind -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 30 -s 3 -t ind -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 30 -s 4 -t ind -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 30 -s 5 -t ind -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 30 -s 6 -t ind -n 5000 -d 3 -m kmppd -g 5

python3 index.py -o run_query -k 30 -s 2 -t ant -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 30 -s 3 -t ant -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 30 -s 4 -t ant -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 30 -s 5 -t ant -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 30 -s 6 -t ant -n 5000 -d 3 -m kmppd -g 5

python3 index.py -o run_query -k 30 -s 2 -t fc -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 30 -s 3 -t fc -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 30 -s 4 -t fc -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 30 -s 5 -t fc -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 30 -s 6 -t fc -n 5000 -d 3 -m kmppd -g 5

python3 index.py -o run_query -k 30 -s 2 -t ind -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 30 -s 3 -t ind -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 30 -s 4 -t ind -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 30 -s 5 -t ind -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 30 -s 6 -t ind -n 5000 -d 3 -m optimized_kmppd -g 5

python3 index.py -o run_query -k 30 -s 2 -t ant -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 30 -s 3 -t ant -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 30 -s 4 -t ant -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 30 -s 5 -t ant -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 30 -s 6 -t ant -n 5000 -d 3 -m optimized_kmppd -g 5

python3 index.py -o run_query -k 30 -s 2 -t fc -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 30 -s 3 -t fc -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 30 -s 4 -t fc -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 30 -s 5 -t fc -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 30 -s 6 -t fc -n 5000 -d 3 -m optimized_kmppd -g 5