FROM node:8 as builder
COPY . /build
WORKDIR /build
RUN make build-js

FROM tsuru/python
ENV PORT 8000
COPY . /home/application/current
WORKDIR /home/application/current
COPY --from=builder /build/tsuru_dashboard/static /home/application/current/tsuru_dashboard/static/
RUN sudo chown -R ubuntu:ubuntu /home/application/current
RUN pip install pipenv && pipenv install --system --deploy && pyenv rehash
RUN python manage.py migrate --noinput
RUN python manage.py createcachetable
RUN python manage.py collectstatic --noinput
ENTRYPOINT gunicorn --access-logfile - -b 0.0.0.0:$PORT -w 2 abyss.wsgi -k gevent
