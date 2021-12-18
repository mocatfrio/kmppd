#!/bin/sh

# Simulation that must be exist on site 5 and 6
declare -a arr=(
                "kmppd_2a23f460-102a-4561-aa4c-db203d3ebc62"
                "kmppd_48b88f94-3111-4767-b92b-ac6fec4af49f"
                "kmppd_d4a8a3f9-2214-4ecc-9a3f-62682f87c70d"
                "optimized_kmppd_7242a22b-e8ea-4bdf-8984-7e94eb755500"
                "optimized_kmppd_cf3dd718-ef74-49f3-b0f5-a176032f271c"
                "optimized_kmppd_bd22d281-b942-4aa8-9542-0cb455716284"
                )
declare -a sites=("5" "6")

for i in "${sites[@]}"
do
  for entry in ~/database/site_$i/*
  do
    echo $entry
    arr_entry=(${entry//// })
    filename=${arr_entry[${#arr_entry[@]}-1]}

    if [[ ! "${arr[*]}" =~ "${filename}" ]]
    then
      mv "${entry}" ~/database_cardinality_deleted/site_$i
      if [ $? -eq 0 ];
      then
          echo -e "${entry} is successfully moved\n"
      else
          echo -e "${entry} is NOT successfully moved\n"
      fi
    fi
  done
done
