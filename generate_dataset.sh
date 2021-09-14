#!/bin/bash

# GENERATE DATA
# python3 generate_dataset.py -s <number_of_site> -t <dataset_type> -n <data_num> -d <dim_size>

# Dim 2 
python3 index.py -o generate_dataset -s 3 -t ind -n 500 -d 2
python3 index.py -o generate_dataset -s 3 -t ant -n 500 -d 2
python3 index.py -o generate_dataset -s 3 -t fc -n 500 -d 2