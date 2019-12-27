FROM ubuntu:18.04

WORKDIR /app
RUN apt-get update
RUN apt-get install -y  software-properties-common
COPY pull_up.py .
COPY deploy.py .
COPY deploy_settings.json .
CMD ["python3","pull_up.py"]

