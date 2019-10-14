FROM        base:latest

RUN         mkdir /var/log/celery
RUN         cp /srv/project/.config/supervisord.conf /etc/supervisor/conf.d/
CMD         supervisord -n



