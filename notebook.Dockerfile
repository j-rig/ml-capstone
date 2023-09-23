FROM python:3.9-slim-buster
#FROM python:3.7-slim-buster
RUN apt-get -y update
RUN apt-get -y install build-essential libssl-dev ca-certificates
RUN pip install --upgrade pip
RUN pip install wheel
COPY notebook.req.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
#COPY data/model.lr.joblib /var/model.lr.joblib
