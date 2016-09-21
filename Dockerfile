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
RUN apt-get install python python-pip curl httpie wget git zsh sudo -yq
# RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN useradd -ms /bin/bash fuckccnu
RUN echo "fuckccnu ALL=(ALL) NOPASSWD: ALL"  >> /etc/sudoers
RUN echo "fuckccnu:fuckccnu" | chpasswd
USER fuckccnu
workdir /home/fuckccnu
RUN mkdir /home/fuckccnu/.pip
RUN echo '[global]\nindex-url=http://pypi.doubanio.com/simple/\n\n[install]\ntrusted-host=pypi.doubanio.com\n' > /home/fuckccnu/.pip/pip.conf
RUN pip install shadowsocks
RUN sudo ssserver -p 443 -k password -m aes-256-cfb --user nobody -d start
# RUN git config --global http.proxy http://14649:da1a126a@p.tmdns.net/3885/da1a126a-jp2-ssl.pac
# RUN git config --global http.proxy http://47.89.28.131:8123/
RUN git clone https://github.com/Muxi-Studio/restccnu
RUN cd /home/fuckccnu/restccnu && pip install --index-url http://pypi.python.org/simple/ -r requirements.txt --trusted-host pypi.python.org

EXPOSE 9000 3141 22 5000
