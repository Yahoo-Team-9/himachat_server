FROM python:3
WORKDIR /app

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN python -m pip install flask
RUN python -m pip install mysql
RUN python -m pip install mysql
RUN python -m pip install flask-socketio
ENV SECRET_KEY `cat /dev/urandom | base64 | fold -w 32 | head -n 1`


CMD [ "flask", "run", "--host=0.0.0.0", "--debugger", "--reload" ]
