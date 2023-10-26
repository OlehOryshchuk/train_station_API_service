FROM python:3.11.1-alpine

LABEL maintainer="olehoryshshuk@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR train_station/

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ..

RUN mkdir -p /media

RUN adduser \
        --disabled-password \
        --no-create-home \
        train_admin

RUN chown -R train_admin:train_admin /media/
RUN chmod -R 755 /media/

USER train_admin
