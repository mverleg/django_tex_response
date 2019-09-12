
FROM alpine:3.10.2
# FROM ubuntu:19.10

WORKDIR /app

RUN set -o pipefail && \
    apk update && \
    apk add texlive-full && \
    rm -rf /var/lib/apt/lists/*

RUN set -o pipefail && \
    apk add --no-cache python3 && \
    pip3 install -U pip && \
    rm -rf /var/lib/apt/lists/*
# not sure clearing apt-get cache makes sense in alpine... but can't hurt

COPY requirements.pip .

RUN pip3 install -r requirements.pip

COPY source .

CMD python3 manage.py runserver --nothreading --noreload "localhost:8132"

