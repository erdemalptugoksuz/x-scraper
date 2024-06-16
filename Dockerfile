FROM python:3.12-slim

RUN apt-get update && apt-get install -y git
RUN pip install --upgrade pip

WORKDIR /app

COPY . .

COPY requirements.txt ./

RUN pip install -r requirements.txt --no-cache-dir
