#! /bin/bash

# 更新源
yum -y update

# 安装rz sz
yum -y install lrzsz

#安装vim
yum -y install vim

#安装gcc
yum -y install gcc gcc-c++

#安装git
yum -y install git

#安装php
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm
yum -y install php72w php72w-cli php72w-devel php72w-common php72w-mysqlnd php72w-gd php72w-xml php72w-zip php72w-fpm php72w-mbstring php72w-pear php72w-devel php72w-opcache
#yum -y install php72w php72w-cli php72w-devel php72w-common php72w-mysql php72w-gd php72w-xml php72w-zip php72w-fpm php72w-mbstring php72w-pear php72w-devel
#//yum install -y php73-php-fpm php73-php-cli php73-php-bcmath php73-php-gd php73-php-json php73-php-mbstring php73-php-mcrypt php73-php-mysqlnd php73-php-opcache php73-php-pdo php73-php-pecl-crypto php73-php-pecl-mcrypt php73-php-pecl-geoip php73-php-recode php73-php-snmp php73-php-soap php73-php-xmll php73-php-zip php73-php-dom php73-php-swoole php73-php-devel

# composer
cd ~
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php -r "if (hash_file('sha384', 'composer-setup.php') === '93b54496392c062774670ac18b134c3b3a95e5a5e5c8f1a9f115f203b75bf9a129d5daa8ba6a13e2cc8a1da0806388a8') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"
mv composer.phar /usr/bin/composer

#安装mysql
rpm -Uvh https://repo.mysql.com//mysql80-community-release-el7-1.noarch.rpm
yum -y install mysql-community-server

#安装openresty/nginx
sudo yum -y install yum-utils
sudo yum-config-manager --add-repo https://openresty.org/package/centos/openresty.repo
sudo yum -y install openresty

#安装redis
cd ~
wget http://download.redis.io/releases/redis-5.0.2.tar.gz
tar -xvf redis-5.0.2.tar.gz
cd redis-5.0.2
make
make install

#安装node
#cd ~
#wget https://nodejs.org/dist/v10.14.0/node-v10.14.0.tar.gz
#tar -xvf node-v10.14.0.tar.gz
#cd node-v10.14.0
#./configure
#make
#make install
