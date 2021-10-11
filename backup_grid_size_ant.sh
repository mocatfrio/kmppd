#!/bin/sh
## declare an array variable
declare -a arr=(
                "kmppd_3a17399a-44f3-4246-a491-5999813f0d53"
                "kmppd_cb7be7b0-af67-4507-b3aa-be311e183402"
                "kmppd_a9962881-424c-47e7-b4ee-ab0bdd377669"
                "kmppd_dbf305ff-435d-4a51-8a33-06d8559a2fc1"
                "optimized_kmppd_bc57c1ec-e90f-4a42-8ed0-50b539688e0a"
                "optimized_kmppd_731d0223-8940-42ea-84c0-0d0ee7d64d94"
                "optimized_kmppd_3318e352-641a-49c2-9dd3-22a00c67dfe1"
                "optimized_kmppd_fa2a55e1-8b87-457c-a4ed-b60d0e2aec3e"
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
