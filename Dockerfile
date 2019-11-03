FROM python:3-alpine

RUN apk update && apk add build-base jpeg-dev zlib-dev bash && \
    apk add --virtual .build-deps postgresql-dev zlib-dev libffi-dev \
        linux-headers pkgconfig fontconfig-dev

RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo pango-dev gdk-pixbuf

RUN mkdir -p /data/web
WORKDIR /data/web
COPY ./requirements.txt .

RUN pip3 install -U pip
RUN pip3 install -r requirements.txt

COPY . .
