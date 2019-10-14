FROM        base:latest

RUN         mkdir /var/log/celery

WORKDIR     /srv/project/wonyoung_narajangteo
RUN         mkdir /srv/project/static
RUN         python manage.py -y collectstatic --noinput

RUN         cp /srv/project/.config/supervisord.conf /etc/supervisor/conf.d/
CMD         supervisord -n



