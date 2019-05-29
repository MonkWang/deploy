FROM golang:1.10.1

WORKDIR /go/src

# 安装supervisor
RUN apt-get update && apt-get install -y supervisor


RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
COPY ./supervisord.conf /etc/supervisor/supervisord.conf

CMD ["/usr/bin/supervisord","-c","/etc/supervisor/supervisord.conf"]