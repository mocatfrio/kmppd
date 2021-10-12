#!/bin/sh
## declare an array variable
declare -a arr=(
                "kmppd_9d209436-eb63-4baf-829b-a9f655bbe0d8"
                "kmppd_30a118ca-ec58-48a4-962f-86cd2f21cdca"
                "kmppd_4b413f9a-f49e-4cf4-b087-3f39042adca6"
                "kmppd_b0870f05-1898-4e67-b64b-ff0007e3cdfc"
                "optimized_kmppd_d3ba0583-9d04-46df-a754-62f9052f3efe"
                "optimized_kmppd_ce754671-8283-40e4-9a53-59233627f0a4"
                "optimized_kmppd_5bfeb640-d45e-4210-b66f-d96ae2ced9ed"
                "optimized_kmppd_153f2e39-de47-42d8-bd4d-4333925684d3"
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
