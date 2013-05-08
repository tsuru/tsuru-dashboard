#Abyss (Tsuru Dashboard)

[![Build Status](https://secure.travis-ci.org/globocom/abyss.png?branch=master)](http://travis-ci.org/globocom/abyss)
[![Build Status](https://drone.io/github.com/globocom/abyss/status.png)](https://drone.io/github.com/globocom/abyss/latest)

Abyss is a django-base project aimed to providing a tsuru dashboard.


For issue tracking:

    * https://github.com/globocom/abyss/issues

#Getting Started

For local development, first create a virtualenv and install the deps:

    $ make deps

If all is well you should able to run the local server:

    $ export TSURU_HOST=http://tsuru-api-endpoint.com
    $ ./manage.py runserver

#Running tests

    $ make test
