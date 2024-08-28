FROM python:3.11

MAINTAINER Misha00025<misha00025@mail.ru>

ENV TZ=Europe/Moscow

RUN apt-get update
RUN apt install -y wget && apt install -y zip 

WORKDIR /root
ENV BOT_VERSION=Arkadia-0-8-0-hotfix
RUN wget "https://github.com/Misha00025/RPChatBotVK/archive/$BOT_VERSION.zip" && unzip $BOT_VERSION.zip
RUN mv /root/RPChatBotVK-$BOT_VERSION /root/RPChatBotVK

WORKDIR /root/RPChatBotVK
RUN python3 -m venv venv
RUN ./venv/bin/pip install -r req.txt
RUN chmod 777 main.py && mkdir ./configs && mkdir ./saves 

CMD ./main.py