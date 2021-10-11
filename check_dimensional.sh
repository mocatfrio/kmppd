#!/bin/sh
## declare an array variable
declare -a arr=(
                "kmppd_7ba78e17-7f45-40e8-999d-eb7008fc743e"
                "kmppd_1551e5e1-52cb-43cb-9d71-4589f71d7ded"
                "optimized_kmppd_8fca3d34-a80a-4cbc-90d2-26b85faffcbb"
                "optimized_kmppd_10ee3807-2c89-4034-89a3-21d18974aa05"
                "kmppd_99a0e286-bb6d-4785-90ee-1aa81e99b29c"
                "kmppd_b8b13998-4ddd-4e3d-9267-9ee5980daeba"
                "optimized_kmppd_323927ef-a174-4a48-b4b7-52f64a22217b"
                "kmppd_765de84e-d0bf-41cc-9843-a35d5f9f5f76"
                )


echo -e "\nEnter site:"
read SITE_NUM

## now loop through the above array
a=0
for i in "${arr[@]}"
do
  if [[ -d ~/database/site_$SITE_NUM/$i/ ]]
  then
    a=$((a + 1))
    echo "~/database/site_${SITE_NUM}/${i} exists on your filesystem."
  else
    echo "~/database/site_${SITE_NUM}/${i} NOT exists on your filesystem."
  fi
done

echo $a
if [[ $a -eq ${#arr[@]} ]]
then
  echo 'All files is exist!'
else
  echo 'Not all files is exist!'
fi