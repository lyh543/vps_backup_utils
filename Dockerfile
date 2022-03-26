FROM python:3.7-buster
RUN wget -O /etc/apt/sources.list https://mirrors.cloud.tencent.com/repo/debian10_sources.list
RUN apt update && \
    apt install -y ssh rsync tar gzip default-mysql-client postgresql-client-common