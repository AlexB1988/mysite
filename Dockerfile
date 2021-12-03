FROM python:3.8

WORKDIR /usr/src/mysite

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install netcat -y

#RUN apk update && apk upgrade -y && apk add postgresql-dev gcc python3-dev musl-dev

COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/mysite

ENTRYPOINT ["/mysite/entrypoint.sh"]