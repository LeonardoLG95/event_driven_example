FROM python:3.9.13-buster

COPY service/. service/
WORKDIR /service

ENV PYTHONPATH="/"

RUN pip install -r requirements.txt

ENTRYPOINT uvicorn api:APP --reload --host "0.0.0.0" --port "8000"