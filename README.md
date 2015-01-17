# tsuru-dashboard





[![Build Status](https://secure.travis-ci.org/tsuru/tsuru-dashboard.png?branch=master)](http://travis-ci.org/tsuru/tsuru-dashboard)
[![Build Status](https://drone.io/github.com/tsuru/tsuru-dashboard/status.png)](https://drone.io/github.com/tsuru/tsuru-dashboard/latest)

tsuru-dashboard is a Django-based project aimed at providing a Web-based dashboard for tsuru.

For issue tracking:

* https://github.com/tsuru/tsuru-dashboard/issues

# Deploying to tsuru

tsuru-dashboard can be deployed to tsuru like any other app.

# Setting up a development environment

For local development, first create a virtualenv and install the deps:

    $ make deps

If all is well you should able to run the local server:

    $ export TSURU_HOST=http://tsuru-api-endpoint.com
    $ ./manage.py runserver

# Running tests

    $ make test

Links:

- Full tsuru documentation: http://docs.tsuru.io
- How to Contribute: http://docs.tsuru.io/en/latest/contributing
- Repository & Issue Tracker: https://github.com/tsuru/tsuru-dashboard
- Gitter: https://gitter.im/tsuru/tsuru
- IRC: Freenode, channel #tsuru
