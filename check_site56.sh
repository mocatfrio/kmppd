#!/bin/sh
## declare an array variable
declare -a arr=("kmppd_2a23f460-102a-4561-aa4c-db203d3ebc62"
                "kmppd_48b88f94-3111-4767-b92b-ac6fec4af49f"
                "kmppd_d4a8a3f9-2214-4ecc-9a3f-62682f87c70d"
                "optimized_kmppd_7242a22b-e8ea-4bdf-8984-7e94eb755500"
                "optimized_kmppd_cf3dd718-ef74-49f3-b0f5-a176032f271c"
                "optimized_kmppd_bd22d281-b942-4aa8-9542-0cb455716284"
                )


echo -e "\nEnter site:"
read SITE_NUM

## now loop through the above array
a=0
for i in "${arr[@]}"
do
  if [[ -d ~/database_cardinality/site_$SITE_NUM/$i/ ]]
  then
    a=$((a + 1))
    echo "~/database_cardinality/site_${SITE_NUM}/${i} exists on your filesystem."
  else
    echo "~/database_cardinality/site_${SITE_NUM}/${i} NOT exists on your filesystem."
  fi
done

echo $a
if [[ $a -eq ${#arr[@]} ]]
then
  echo 'All files is exist!'
else
  echo 'Not all files is exist!'
fi