FROM python:3.11

LABEL maintainer="Misha00025<misha00025@mail.ru>"

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
WORKDIR /app

COPY . .
RUN pip install -r req.txt

CMD python main.py