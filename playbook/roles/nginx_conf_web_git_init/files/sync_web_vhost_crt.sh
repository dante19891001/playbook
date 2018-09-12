#!/bin/bash
operation=$1
function sync_web_vhost_crt() {
	if [[ ${operation} == "update" ]]
	then 
		cd /usr/local/nginx/conf
		git fetch --all
		git reset --hard origin/master
	else
		cd /usr/local/nginx/conf
		git pull origin master
		git add vhost crt common_files
		v_date=`date +%Y%m%d%H%M`
		git commit -m "update  ${brand} vhost crt ${v_date}"
		git push -u origin master
	fi
}
sync_web_vhost_crt