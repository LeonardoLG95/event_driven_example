#!/bin/bash

docker build back_end/. -t api:latest
docker build front_end/. -t ui:latest

docker-compose up