#!/bin/sh
## declare an array variable
declare -a arr=("kmppd_f4bb9067-385f-46a0-b0ed-653a8afc67df"
                "kmppd_66e540f0-0de3-4834-a3ba-9b93f6263636"
                "kmppd_bee86b91-5390-474c-b68d-e93eea04e176"
                "kmppd_2a23f460-102a-4561-aa4c-db203d3ebc62"
                "kmppd_15001ea2-afbb-41cc-b364-91c2b4f6ac68"
                "optimized_kmppd_06b7b44d-6254-41f7-8df3-a04c92df92e9"
                "optimized_kmppd_2ff7ee19-1990-4aac-99c5-c721e99720bf"
                "optimized_kmppd_0c8af534-49c9-48d7-b93c-f7f1e70c10ad"
                "kmppd_dba513a8-7143-44ac-9ef8-9f3050f3391a"
                "kmppd_e6bcf9e0-a630-4a94-bc03-9d9acacf30fa"
                "kmppd_455ca971-e5b1-4256-ad2a-3951707a6671"
                "kmppd_48b88f94-3111-4767-b92b-ac6fec4af49f"
                "kmppd_44e17a9e-586c-450e-8138-2d9b6be1beb2"
                "optimized_kmppd_f54abe93-49a4-4599-983e-a769c9ec0b22"
                "optimized_kmppd_c41f99df-eb68-4b14-b496-15273579739a"
                "optimized_kmppd_e1e70694-cd3f-4c8b-b11b-7ce1de1dfdfd"
                "optimized_kmppd_cf3dd718-ef74-49f3-b0f5-a176032f271c"
                "optimized_kmppd_0d2d857b-4898-44d8-9c04-62d47094d27d"
                "kmppd_6c6d2cb1-17d8-4cb0-8bfd-60be1778f1d3"
                "kmppd_043353a3-e7ab-458c-81df-4a4f66f309db"
                "kmppd_a8f409f8-81f1-4671-abd1-6e0009dcc535"
                "kmppd_d4a8a3f9-2214-4ecc-9a3f-62682f87c70d"
                "kmppd_e399ded8-1bf4-43b8-93ec-1e1fd1d33097"
                "optimized_kmppd_f466262c-7eeb-4d0d-a4c6-960130c76d36"
                "optimized_kmppd_d0413e69-91eb-4243-86a0-c34e6113cb99"
                "optimized_kmppd_fdf20f3c-f2dc-43e0-ad22-058fba179525"
                "optimized_kmppd_bd22d281-b942-4aa8-9542-0cb455716284"
                )


echo -e "\nEnter site:"
read SITE_NUM

## now loop through the above array
for i in "${arr[@]}"
do
  rm -r ~/kmppd/system/database/site_$SITE_NUM/$i/
  if [ $? -eq 0 ];
  then
      echo -e "${i} is successfully deleted from site ${SITE_NUM}\n"
  else
      echo -e "${i} is NOT successfully deleted from site ${SITE_NUM}\n"
  fi
done
echo 'done'