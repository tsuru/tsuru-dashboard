from tsuru/python
copy requirements.apt /tmp
copy requirements.txt /tmp
run cat /tmp/requirements.apt | xargs sudo apt-get install -y --force-yes
run pip install -r /tmp/requirements.txt
entrypoint gunicorn --access-logfile - -b 0.0.0.0:$PORT -w 2 abyss.wsgi -k gevent
