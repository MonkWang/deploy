FROM php:7.2-fpm

MAINTAINER dream <zcx00439@gmail.com>

RUN apt-get update

# 安装gd
RUN apt-get install -y  libjpeg-dev && apt-get install -y libpng-dev && apt-get install -y libfreetype6-dev && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install -j$(nproc) gd
# 安装redis，swoole，opcache
RUN pecl install redis-4.0.1 && docker-php-ext-enable redis && pecl install swoole && docker-php-ext-enable swoole && \
 docker-php-ext-enable opcache
# 安装pdo mysql
RUN docker-php-ext-configure pdo_mysql && docker-php-ext-install -j$(nproc) pdo_mysql

# 安装zip
RUN docker-php-ext-install zip

# 安装supervisor
RUN apt-get update && apt-get install -y supervisor

RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
#
COPY config/*.ini $PHP_INI_DIR/conf.d/
COPY php-fpm.d/*.conf $PHP_INI_DIR/../php-fpm.d/
COPY ./start.sh /start.sh
COPY ./supervisord.conf /etc/supervisor/supervisord.conf
RUN chmod +x /start.sh

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

EXPOSE 9000 1215

CMD ["/usr/bin/supervisord","-c","/etc/supervisor/supervisord.conf"]