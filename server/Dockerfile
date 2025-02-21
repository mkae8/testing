
FROM python:3.13

COPY ./server /app
COPY requirements.txt /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
