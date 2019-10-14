FROM       python:3.6.4
COPY        . /srv/project

RUN         apt-get -y update
RUN         apt-get -y dist-upgrade
RUN         apt-get -y install supervisor
RUN         apt-get -y install libaio1

WORKDIR     /srv/project/wonyoung_narajangteo
RUN         pip install -r ./requirements.txt

RUN         cp /srv/project/.config/supervisor.conf /etc/supervisor/conf.d/
CMD         supervisord -n



