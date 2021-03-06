# pull official base image
FROM python:3.6-slim

# set work directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./apt_req /usr/src/app/apt_req
#install application
RUN apt-get update && \
    apt-get install -y $(cat ./apt_req) && \
    apt-get clean

# install dependencies

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip
RUN gdal-config --version
RUN pip install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==`gdal-config --version`
RUN pip install -r requirements.txt && pip install gunicorn



