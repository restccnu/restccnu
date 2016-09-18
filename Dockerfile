FROM ubuntu:16.04

MAINTAINER neo1218 <neo1218@yeah.net>
ENV DEBIAN_FRONTEND noninteractive

RUN echo 'deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse\n\
    ' > /etc/apt/sources.list
RUN apt-get update
RUN apt-get install python curl httpie git zsh sudo -yq
RUN useradd -ms /bin/bash fuckccnu
RUN echo "fuckccnu ALL=(ALL) NOPASSWD: ALL"  >> /etc/sudoers
RUN echo "fuckccnu:fuckccnu" | chpasswd
USER fuckccnu
workdir /home/fuckccnu
RUN git clone https://github.com/Muxi-Studio/restccnu
RUN cd /home/fuckccnu/restccnu

EXPOSE 9000 3141 22 5000
