FROM mysql:latest

MAINTAINER dream <zcx00439@gmail.com>

#####################################
# Set Timezone
#####################################

RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo Asia/Shanghai > /etc/timezone

RUN chown -R mysql:root /var/lib/mysql/

COPY config/my.cnf /etc/mysql/conf.d/my.cnf

CMD ["mysqld"]

EXPOSE 3306