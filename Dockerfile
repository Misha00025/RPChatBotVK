FROM python:3.11

MAINTAINER Misha00025<misha00025@mail.ru>

ENV TZ=Europe/Moscow

RUN apt-get update
RUN apt install -y wget && apt install -y zip && apt install -y git

WORKDIR /root
RUN git clone https://github.com/Misha00025/RPChatBotVK/ ./RPChatBotVK

WORKDIR /root/RPChatBotVK
RUN python3 -m venv venv
RUN ./venv/bin/pip install -r req.txt
RUN chmod 777 main.py && mkdir ./configs && mkdir ./saves 

CMD ./main.py