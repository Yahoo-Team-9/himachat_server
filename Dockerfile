FROM python:3.8
WORKDIR /app
COPY . .
RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm
ENV SECRET_KEY "B0xeu8qehf[of-21rfo2rj3ojfgj2ojfs2o-ik"

ENV MYSQL_USER b644c34d917430
ENV MYSQL_DATABASE heroku_60c5e0a606ac3df
ENV DATABASE_HOST us-cdbr-east-05.cleardb.net
ENV DATABASE_PASS 0c349e4e
ENV REDIS_URL "redis://:pb62b02e6fba023fb42087df041b8c1d421b62df1c5124397b2a466b572d4f51d@ec2-52-207-67-190.compute-1.amazonaws.com:24379"


RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN python -m pip install flask
RUN python -m pip install -r requirements.txt



 ENTRYPOINT[ "/bin/sh", "-c","cd"," /app" ,"&&" ,"gunicorn", "--worker-class", "eventlet" ,"-w", "1","--threads", "10", "--bind" ,"0.0.0.0:${PORT}" ,"application.app:app" ]
