#!/bin/sh

# Restore dimensionality simulation from local to server 

# "kmppd_7ba78e17-7f45-40e8-999d-eb7008fc743e"
# "kmppd_1551e5e1-52cb-43cb-9d71-4589f71d7ded"
# "optimized_kmppd_8fca3d34-a80a-4cbc-90d2-26b85faffcbb"
### "optimized_kmppd_10ee3807-2c89-4034-89a3-21d18974aa05"
# "kmppd_99a0e286-bb6d-4785-90ee-1aa81e99b29c"
# "kmppd_b8b13998-4ddd-4e3d-9267-9ee5980daeba"
# "optimized_kmppd_323927ef-a174-4a48-b4b7-52f64a22217b"
# "kmppd_765de84e-d0bf-41cc-9843-a35d5f9f5f76"

SIM="optimized_kmppd_10ee3807-2c89-4034-89a3-21d18974aa05"
declare -a sites=("1" "2" "3" "4")

read -s -p "Enter ssh password : " PASSWORD_SSH;


## now loop through the above array
for i in "${sites[@]}"
do  
  sshpass -p $PASSWORD_SSH scp -r ~/database/site_$i/$SIM/ root@178.128.122.179:~/kmppd/system/database/site_$i/$SIM/ 
  if [ $? -eq 0 ];
  then
      echo -e "${SIM} is successfully exported from site ${i}\n"
  else
      echo -e "${SIM} is NOT successfully exported from site ${i}\n"
  fi

  rm -r ~/database/site_$i/$SIM/
  if [ $? -eq 0 ];
  then
      echo -e "${SIM} is successfully deleted from site ${i}\n"
  else
      echo -e "${SIM} is NOT successfully deleted from site ${i}\n"
  fi
done
echo 'done'

