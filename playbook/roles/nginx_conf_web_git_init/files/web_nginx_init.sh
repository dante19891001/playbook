#!/bin/bash
brand=$1
cd /usr/local/nginx/conf
git init
git config --global user.email "dante@sk.com"
git config --global user.name "dante"
touch vhost/.gitignore
echo "upstream" >  vhost/.gitignore
git remote add -f origin http://dante:w123c1QWE@git.it-om.net/web/B2C/configuration/nginx-conf-web-${brand}.git
git config core.sparsecheckout true 
echo "/crt" > .git/info/sparse-checkout
echo "/vhost" >> .git/info/sparse-checkout
echo "/common_files" >> .git/info/sparse-checkout