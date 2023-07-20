FROM python:3.7.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
RUN apt-get update && apt-get install -y vim
COPY requirements.txt /code/
RUN apt-get install -y python3-dev build-essential
RUN apt-get install -y default-libmysqlclient-dev
RUN pip install -r requirements.txt
COPY . /code/
EXPOSE 8000
