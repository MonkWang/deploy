FROM nginx:alpine

MAINTAINER dream <zcx00439@gmail.com>

COPY nginx.conf /etc/nginx/
COPY php-fpm /etc/nginx/

RUN mkdir -p /etc/letsencrypt/live && chmod -R 755 /etc/letsencrypt/live

# 设置阿里云镜像
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/' /etc/apk/repositories

RUN apk update \
    && apk upgrade \
    && apk add --no-cache bash \
    && adduser -D -H -u 1000 -s /bin/bash www-data

# 如果使用swoole启动php则不需要使用php-fpm，此步是为了兼容除了和+之外的项目
RUN echo "upstream php-upstream { server 127.0.0.1:9000; }" > /etc/nginx/conf.d/upstream.conf \
    && rm /etc/nginx/conf.d/default.conf

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

CMD ["nginx"]

EXPOSE 80 443
