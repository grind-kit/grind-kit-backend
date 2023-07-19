FROM python:3.9

EXPOSE 8002

RUN apt-get update
RUN apt-get install -y vim
RUN pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY .docker/requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/