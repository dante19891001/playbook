#!/bin/bash
# nginx安装脚本
# 版本：1.12.1
# MD5：e8f5f4beed041e63eb97f9f4f55f3085 

# move the download to ansible logic
#download_url='http://69.172.86.99:998'

nginx_version='nginx-1.12.1'
nginx_tar=$nginx_version.tar.gz

if [ -d /usr/local/nginx ];then
  echo "Warning :nginx is existed "
else
  yum install gcc gcc-c++ cmake ncurses-devel -y
  yum install -y pcre-devel openssl openssl-devel
  cd /usr/local/src/
  
  # www账号需要找IDC组
  #groupadd www
  #useradd -g www www
  
  tar zxvf $nginx_tar
  cd $nginx_version
  ./configure --user=www --group=www --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module --with-pcre --with-http_realip_module 
  make
  make install
fi