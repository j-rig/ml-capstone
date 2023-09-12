FROM python:3.9-slim-buster
# https://www.pythonanywhere.com/batteries_included/
RUN apt-get -y update
RUN apt-get -y install build-essential libssl-dev ca-certificates
RUN pip install --upgrade pip
RUN pip install wheel
COPY /src /var/app
RUN pip install --compile -e /var/app
