FROM python:3.7.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /big_data_sample_project
RUN apt-get update && apt-get install -y vim dos2unix
COPY requirements.txt /big_data_sample_project/
RUN apt-get install -y python3-dev build-essential
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y default-mysql-client
RUN pip install -r requirements.txt
COPY . /big_data_sample_project/
COPY entrypoint.sh /big_data_sample_project/entrypoint.sh
RUN dos2unix /big_data_sample_project/entrypoint.sh
RUN chmod +x /big_data_sample_project/entrypoint.sh
SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["/big_data_sample_project/entrypoint.sh"]
EXPOSE 8000
