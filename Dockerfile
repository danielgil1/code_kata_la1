# base image

FROM python:3.7

USER root

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		locales \
		wget \
		ca-certificates \
		fonts-texgyre \
        python-pip \
        python-setuptools \
		python-dev \
	&& rm -rf /var/lib/apt/lists/*

# setup location
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
	&& locale-gen en_US.utf8 \
	&& /usr/sbin/update-locale LANG=en_US.UTF-8


ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV PYTHONPATH=".:src/"

# Sets time zone
ENV TZ Australia/Melbourne

RUN pip install --upgrade pip

# Creates working directory inside Docker container
# use -v <local-path>:/workdir to share the volume between host and Docker container
RUN mkdir /workdir

# Sets working directory (overwrite using -w if needed)
WORKDIR /workdir

# Copies Python dependency list from host to Docker container
COPY . /workdir

# pip install
RUN pip install -r requirements.txt --compile --progress-bar pretty

CMD ["python","run.py","-s","spec.json"]