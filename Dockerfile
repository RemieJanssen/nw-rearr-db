FROM ubuntu:focal
ARG DEBIAN_FRONTEND=noninteractive

# system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
	locales \
	build-essential \
	python3-dev \
	python3-pip \
	python3-venv \
	python3-wheel \
	gettext \
	git \
    libmagic-dev \
	postgresql-client \
&& apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8
RUN pip3 install --upgrade setuptools pip wheel

COPY . /code/
WORKDIR /code
RUN python3 -m venv .
RUN bin/pip install -r requirements/requirements.txt

RUN mkdir -p var/static var/media
RUN bin/python3 manage.py collectstatic --noinput --clear
