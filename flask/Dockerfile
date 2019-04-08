FROM ubuntu:16.04
RUN adduser --disabled-password --disabled-login flask
ADD . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -y python3.5 python3-pip python3-venv git virtualenv

RUN python3 -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r /app/requirements.txt
RUN venv/bin/pip install gunicorn

#RUN pip3 install -r /app/requirements.txt
USER flask

ENV FLASK_APP run.py

#RUN chown -R flask:run ./

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]

