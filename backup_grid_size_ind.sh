#!/bin/sh
## declare an array variable
declare -a arr=(
                "kmppd_a12ebb0a-2e55-4371-b99f-f85685e18717"
                "kmppd_e22d40f7-850b-43d1-b9f7-b2f73fa48463"
                "kmppd_fe43592b-e11b-4245-8c2c-f00b51af9369"
                "kmppd_ac51bc5f-8bff-4af6-836d-0c0a44547345"
                "optimized_kmppd_4838f3a9-aa77-4c62-a165-9b7f58343118"
                "optimized_kmppd_e3bef73d-280f-4eb9-873b-c39046761a37"
                "optimized_kmppd_87d2ab7d-abcb-4cdc-a0fa-d8e67aa1d7c0"
                "optimized_kmppd_950b6c2e-f2aa-45e8-9ba7-d01bf3b8c021"
                )


read -s -p "Enter ssh password : " PASSWORD_SSH;
echo -e "\nEnter site:"
read SITE_NUM

## now loop through the above array
for i in "${arr[@]}"
do
  sshpass -p $PASSWORD_SSH scp -r root@178.128.122.179:~/kmppd/system/database/site_$SITE_NUM/$i/ ~/database_grid_size/site_$SITE_NUM
  if [ $? -eq 0 ];
  then
      echo -e "${i} is successfully exported from site ${SITE_NUM}\n"
  else
      echo -e "${i} is NOT successfully exported from site ${SITE_NUM}\n"
  fi
done
echo 'done'
