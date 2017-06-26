FROM tsuru/python
ADD . /home/application/current
WORKDIR /home/application/current
USER ubuntu
RUN cat requirements.apt | xargs sudo apt-get install -y --force-yes
RUN pip install -r requirements.txt
RUN python manage.py migrate --noinput
RUN python manage.py createcachetable
RUN python manage.py collectstatic --noinput
ENTRYPOINT gunicorn --access-logfile - -b 0.0.0.0:$PORT -w 2 abyss.wsgi -k gevent
