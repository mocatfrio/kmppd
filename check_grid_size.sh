#!/bin/sh
## declare an array variable
declare -a arr=(
                "kmppd_a12ebb0a-2e55-4371-b99f-f85685e18717"
                "kmppd_e22d40f7-850b-43d1-b9f7-b2f73fa48463"
                "optimized_kmppd_4838f3a9-aa77-4c62-a165-9b7f58343118"
                "optimized_kmppd_e3bef73d-280f-4eb9-873b-c39046761a37"
                )


echo -e "\nEnter site:"
read SITE_NUM

## now loop through the above array
a=0
for i in "${arr[@]}"
do
  if [[ -d ~/kmppd/system/database/site_$SITE_NUM/$i/ ]]
  then
    a=$((a + 1))
    echo "~/kmppd/system/database/site_${SITE_NUM}/${i} exists on your filesystem."
  else
    echo "~/kmppd/system/database/site_${SITE_NUM}/${i} NOT exists on your filesystem."
  fi
done

echo $a
if [[ $a -eq ${#arr[@]} ]]
then
  echo 'All files is exist!'
else
  echo 'Not all files is exist!'
fi
