FROM python:3

ENV PYTHONUNBUFFERED 1
RUN  mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

RUN apt-get -y update && apt-get install -y mysql-server