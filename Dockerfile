FROM python:3.11

USER root

RUN apt-get update && apt-get install -y git
RUN pip install --upgrade pip

HEALTHCHECK NONE

WORKDIR /code

COPY . .

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app .

EXPOSE 8080
