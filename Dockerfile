FROM ubuntu:20.04
LABEL authors="Dmitry Chavdar"
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN apt-get install supervisor
COPY . /simple_http_server
WORKDIR /simple_http_server
RUN pip3 install -r requirements.txt
RUN cp simple_http_server.conf /etc/supervisor/conf.d/
RUN touch /var/run/supervisor.sock && chmod 777 /var/run/supervisor.sock && service supervisor restart
CMD supervisord -c /etc/supervisor/supervisord.conf && supervisorctl -c /etc/supervisor/supervisord.conf
