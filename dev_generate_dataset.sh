#! /bin/bash

# GENERATE DATA
# python3 index.py -o generate_dataset -s <site_num> -t <dataset_type> -n <data_num> -d <dim_size>

# example:
# python3 index.py -o generate_dataset -s 6 -t ind -n 500 -d 2

python3 index.py -o generate_dataset -s 3 -t ind -n 100 -d 2
python3 index.py -o generate_dataset -s 3 -t ind -n 500 -d 2
python3 index.py -o generate_dataset -s 3 -t ind -n 1000 -d 2

python3 index.py -o generate_dataset -s 3 -t ind -n 100 -d 3
python3 index.py -o generate_dataset -s 3 -t ind -n 500 -d 3
python3 index.py -o generate_dataset -s 3 -t ind -n 1000 -d 3

python3 index.py -o generate_dataset -s 3 -t ind -n 100 -d 4
python3 index.py -o generate_dataset -s 3 -t ind -n 500 -d 4
python3 index.py -o generate_dataset -s 3 -t ind -n 1000 -d 4


python3 index.py -o generate_dataset -s 3 -t ant -n 100 -d 2
python3 index.py -o generate_dataset -s 3 -t ant -n 500 -d 2
python3 index.py -o generate_dataset -s 3 -t ant -n 1000 -d 2

python3 index.py -o generate_dataset -s 3 -t ant -n 100 -d 3
python3 index.py -o generate_dataset -s 3 -t ant -n 500 -d 3
python3 index.py -o generate_dataset -s 3 -t ant -n 1000 -d 3

python3 index.py -o generate_dataset -s 3 -t ant -n 100 -d 4
python3 index.py -o generate_dataset -s 3 -t ant -n 500 -d 4
python3 index.py -o generate_dataset -s 3 -t ant -n 1000 -d 4


python3 index.py -o generate_dataset -s 3 -t fc -n 100 -d 2
python3 index.py -o generate_dataset -s 3 -t fc -n 500 -d 2
python3 index.py -o generate_dataset -s 3 -t fc -n 1000 -d 2

python3 index.py -o generate_dataset -s 3 -t fc -n 100 -d 3
python3 index.py -o generate_dataset -s 3 -t fc -n 500 -d 3
python3 index.py -o generate_dataset -s 3 -t fc -n 1000 -d 3

python3 index.py -o generate_dataset -s 3 -t fc -n 100 -d 4
python3 index.py -o generate_dataset -s 3 -t fc -n 500 -d 4
python3 index.py -o generate_dataset -s 3 -t fc -n 1000 -d 4


