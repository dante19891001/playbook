#/bin/bash
docker stop nginx_frontend_crm 
docker rm nginx_frontend_crm
docker rmi reg.easydevops.net/nginx:crm-frontend-product
docker-compose -f /home/docker-data/docker-compose-crm-nginx.yml  up -d
docker restart nginx