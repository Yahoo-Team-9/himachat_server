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
ENV PORT  5000
ENV MYSQL_USER himachat_adomin2132
ENV MYSQL_DATABASE himachat
ENV DATABASE_HOST himachatdb.mysql.database.azure.com
ENV DATABASE_PASS qigkaz-depgYs-wetwy4
ENV REDIS_URL "redis://:s4dZNaVC8hsaId8sxB4Kkh2pxrOq7DOvIAzCaM87VTI=@himaching.redis.cache.windows.net:6379"


RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN python -m pip install flask
RUN python -m pip install -r requirements.txt


CMD [ "gunicorn", "--worker-class", "eventlet" ,"-w", "1","--threads", "10", "application.app:app" ]
