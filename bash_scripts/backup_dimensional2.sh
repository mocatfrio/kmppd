#!/bin/sh
## declare an array variable
declare -a arr=(
                #"kmppd_7ba78e17-7f45-40e8-999d-eb7008fc743e"
                "kmppd_1551e5e1-52cb-43cb-9d71-4589f71d7ded"
                #"kmppd_99a0e286-bb6d-4785-90ee-1aa81e99b29c"
                #"kmppd_b8b13998-4ddd-4e3d-9267-9ee5980daeba"
                #"kmppd_765de84e-d0bf-41cc-9843-a35d5f9f5f76"
                "kmppd_b13fda81-b198-4ff1-8959-99fc662b826c"
                #"optimized_kmppd_8fca3d34-a80a-4cbc-90d2-26b85faffcbb"
                "optimized_kmppd_10ee3807-2c89-4034-89a3-21d18974aa05"
                #"optimized_kmppd_323927ef-a174-4a48-b4b7-52f64a22217b"
                #"optimized_kmppd_cda7da06-0df0-4268-a5ea-d9f57b189957"
                #"optimized_kmppd_ee2cc36d-d409-4622-bc50-4bba2855b76c"
                #"optimized_kmppd_9953edad-08e3-4b63-a9d5-71816dbb52e3"
                )

read -s -p "Enter ssh password : " PASSWORD_SSH;
echo -e "\nEnter site:"
read SITE_NUM

## now loop through the above array
for i in "${arr[@]}"
do
  sshpass -p $PASSWORD_SSH scp -r root@178.128.122.179:~/kmppd/system/database/site_$SITE_NUM/$i/ ~/database_dimensional/site_$SITE_NUM
  if [ $? -eq 0 ];
  then
      echo -e "${i} is successfully exported from site ${SITE_NUM}\n"
  else
      echo -e "${i} is NOT successfully exported from site ${SITE_NUM}\n"
  fi
done
echo 'done'
