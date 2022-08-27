FROM node:18.8.0-buster-slim

COPY service/. service/
WORKDIR /service

RUN npm install

ENTRYPOINT npm start