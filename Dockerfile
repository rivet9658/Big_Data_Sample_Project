FROM python:3.7.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SUPERUSER_USERNAME=superadmin
ENV DJANGO_SUPERUSER_PASSWORD=1qaz@WSX3edc
RUN mkdir /big_data_sample_project
WORKDIR /big_data_sample_project
RUN apt-get update && apt-get install -y vim
COPY requirements.txt /big_data_sample_project/
RUN apt-get install -y python3-dev build-essential
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y default-mysql-client
RUN pip install -r requirements.txt
COPY . /big_data_sample_project/
EXPOSE 8000
