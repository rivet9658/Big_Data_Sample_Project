FROM python:3.7.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir /big_data_sample_project
WORKDIR /big_data_sample_project
RUN apt-get update && apt-get install -y vim
COPY requirements.txt /big_data_sample_project/
RUN apt-get install -y python3-dev build-essential
RUN apt-get install -y default-libmysqlclient-dev
RUN pip install -r requirements.txt
COPY . /big_data_sample_project/
EXPOSE 8000
