FROM nvidia/cuda:11.8.0-base-ubuntu22.04

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

# set work directory
ENV APP_HOME=/usr/src/app
WORKDIR $APP_HOME

COPY . $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends\
    gcc \
    g++\ 
    make\
    python3\ 
    python3-dev\
    python3-pip\
    python3-venv\
    python3-wheel\
    espeak\
    libespeak-dev\
    libsndfile1-dev
RUN rm -rf /var/lib/apt/lists/*
RUN pip3 install llvmlite --ignore-installed
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 5000