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
                "optimized_kmppd_1d74eac3-b20a-4503-a491-420d1c4269eb"
                "kmppd_765de84e-d0bf-41cc-9843-a35d5f9f5f76"
                "kmppd_606733cf-ce43-4334-a91d-a91614b626e5"
                "kmppd_a12ebb0a-2e55-4371-b99f-f85685e18717"
                "kmppd_e22d40f7-850b-43d1-b9f7-b2f73fa48463"
                "kmppd_f955c67b-7674-4900-b39c-468069addace"
                "optimized_kmppd_4838f3a9-aa77-4c62-a165-9b7f58343118"
                "optimized_kmppd_e3bef73d-280f-4eb9-873b-c39046761a37"
                "optimized_kmppd_3b92fc27-91b9-48b9-ad3f-858b836874e2"
                )


read -s -p "Enter ssh password : " PASSWORD_SSH;
echo -e "\nEnter site:"
read SITE_NUM

## now loop through the above array
for i in "${arr[@]}"
do
  sshpass -p $PASSWORD_SSH scp -r root@178.128.122.179:~/kmppd/system/database/site_$SITE_NUM/$i/ ~/database/site_$SITE_NUM
  if [ $? -eq 0 ];
  then
      echo -e "${i} is successfully exported from site ${SITE_NUM}\n"
  else
      echo -e "${i} is NOT successfully exported from site ${SITE_NUM}\n"
  fi
done
echo 'done'