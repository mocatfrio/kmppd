#! /bin/bash

# GLOBAL PROCESSING
# python3 index.py -o run_query -k <k> -s <site_num> -t <dataset_type> -n <data_num> -d <dim_size> -m <method> -g <grid_size>

# example:
# python3 index.py -o run_query -k 10 -s 3 -t ind -n 500 -d 2 -m kmppd -g 5

# K
python3 index.py -o run_query -k 10 -s 4 -t ind -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 20 -s 4 -t ind -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 40 -s 4 -t ind -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 50 -s 4 -t ind -n 5000 -d 3 -m kmppd -g 5

python3 index.py -o run_query -k 10 -s 4 -t ant -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 20 -s 4 -t ant -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 40 -s 4 -t ant -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 50 -s 4 -t ant -n 5000 -d 3 -m kmppd -g 5

python3 index.py -o run_query -k 10 -s 4 -t fc -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 20 -s 4 -t fc -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 40 -s 4 -t fc -n 5000 -d 3 -m kmppd -g 5
python3 index.py -o run_query -k 50 -s 4 -t fc -n 5000 -d 3 -m kmppd -g 5

python3 index.py -o run_query -k 10 -s 4 -t ind -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 20 -s 4 -t ind -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 40 -s 4 -t ind -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 50 -s 4 -t ind -n 5000 -d 3 -m optimized_kmppd -g 5

python3 index.py -o run_query -k 10 -s 4 -t ant -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 20 -s 4 -t ant -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 40 -s 4 -t ant -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 50 -s 4 -t ant -n 5000 -d 3 -m optimized_kmppd -g 5

python3 index.py -o run_query -k 10 -s 4 -t fc -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 20 -s 4 -t fc -n 5000 -d 3 -m optimized_kmppd -g 5
python3 index.py -o run_query -k 40 -s 4 -t fc -n 5000 -d 3 -m optimized_kmppd -g 5
<<<<<<< HEAD
python3 index.py -o run_query -k 50 -s 4 -t fc -n 5000 -d 3 -m optimized_kmppd -g 5
=======
python3 index.py -o run_query -k 50 -s 4 -t fc -n 5000 -d 3 -m optimized_kmppd -g 5
>>>>>>> 3feba915d88ffa454d28baa74e223d4eb46e9b2a
