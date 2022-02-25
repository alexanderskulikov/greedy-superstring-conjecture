FROM python:3-bullseye
MAINTAINER Aleksey Lobanov 'alex_github@likemath.ru'
RUN apt-get update -y && apt-get install -y libgraphviz-dev build-essential
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt

WORKDIR /app/web
ENV FLASK_APP=csc.py
CMD flask run --host=0.0.0.0

