from ubuntu:18.04

workdir /app
run apt-get update
run apt-get install -y  software-properties-common
COPY pull_up.py .
COPY deploy.py .
COPY deploy_settings.json .
cmd ["python3","pull_up.py"]

