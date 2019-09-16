
# Container with a process to compile latex documents
# Usage note:
# - docker build -t docgen .
# - docker run --rm -p 8132:8132 --name c-docgen docgen
# - curl -X POST localhost:8132 -F "key=A54eAg@lpPZ94vBzI%7Qd0RC_P0wQR6$" -F "latex=@latex_example.tex"

FROM python:3.7.4-alpine3.10
# FROM alpine:3.10.2
# FROM ubuntu:19.10

WORKDIR /app

RUN set -o pipefail && \
    apk update && \
    apk add texlive-full texlive-luatex curl && \
    rm -rf /var/lib/apt/lists/*
# not sure clearing apt-get cache makes sense in alpine... but can't hurt

RUN curl https://bootstrap.pypa.io/get-pip.py | python3

COPY requirements.pip .

#TODO @mark: TEMPORARY! REMOVE THIS!
RUN pip3 install django
COPY ./tex_response/ tex_response

#RUN pip3 install -r requirements.pip

COPY source .

CMD python3 manage.py runserver --nothreading --noreload "0.0.0.0:8132"

