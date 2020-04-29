#!/usr/bin/env bash

env=test
root=/root/deploy/docker
www_dir=/data/www
php_dir=/var/www/html
data_dir=/data/docker-data
etc_dir=${data_dir}/nginx/conf.d
cd $root


# 运行nginx
docker stop nginx
docker rm nginx
docker run  -d --net=host  --name=nginx  --restart=always \
  -v ${data_dir}:/data/ \
  -v ${php_dir}:/var/www/html \
  -v ${www_dir}:/var/www/ \
  -v /etc/letsencrypt:/etc/letsencrypt \
  -v ${etc_dir}:/etc/nginx/sites-available \
   nginx:0.0.1


# 运行php-web
docker stop php-web
docker rm php-web
docker run -d   --net=host  --name=php-web  --restart=always \
  -v ${data_dir}:/data/ \
  -v ${php_dir}:/var/www/html \
  -v /etc/supervisord.web:/etc/supervisor/conf.d \
  -v /etc/zabbix:/etc/zabbix \
   php:0.0.1

# 运行php-cli
docker stop php-cli
docker rm php-cli
docker run  -d  --net=host  --name=php-cli  --restart=always \
  -v ${data_dir}:/data/ \
  -v ${php_dir}:/var/www/html \
  -v /etc/supervisord.cli:/etc/supervisor/conf.d \
   php:0.0.1


# 运行mysql
docker stop mysql
docker rm mysql
docker run --net=host -d --restart=always -e MYSQL_ROOT_PASSWORD=dev  --name=mysql -v /var/lib/mysql:/var/lib/mysql mysql:0.0.1
#
## 运行redis
docker stop redis
docker rm redis
docker run --net=host  --restart=always --name=redis -d redis:0.0.1