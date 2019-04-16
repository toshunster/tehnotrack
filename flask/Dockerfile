FROM ubuntu:16.04

ADD . /app
WORKDIR /app

RUN adduser flask --disabled-password --disabled-login

RUN apt-get update && apt-get -y install python3 python3-pip python3-venv git virtualenv

RUN python3 -m venv venv

RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r /app/requirements.txt
RUN venv/bin/pip install gunicorn

USER flask

ENV FLASK_APP run.py

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]

