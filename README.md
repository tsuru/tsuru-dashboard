# tsuru-dashboard

[![Build Status](https://secure.travis-ci.org/tsuru/tsuru-dashboard.png?branch=master)](http://travis-ci.org/tsuru/tsuru-dashboard)

tsuru-dashboard is a Django-based project aimed at providing a Web-based dashboard for tsuru.

For issue tracking:

* https://github.com/tsuru/tsuru-dashboard/issues

# Deploying to tsuru

tsuru-dashboard can be deployed to tsuru like any other app.
 All you need to do is create a python app and deploy to tsuru using `git push` or `tsuru app-deploy`.

# Setting up a development environment

For local development, first create a virtualenv and install the deps:

    $ make deps

If all is well you should able to run the local server:

    $ export TSURU_HOST=http://tsuru-api-endpoint.com
    $ make run

## Browserifying jsx files

To generate all javascript files based on `js` file you can use the command:

    $ make build-js

# Running tests

## Running all tests

    $ make test

## Running python tests

    $ make python-test

## Running javascript tests

    $ make node-test

# Links

- Full tsuru documentation: http://docs.tsuru.io
- How to Contribute: http://docs.tsuru.io/en/latest/contributing
- Repository & Issue Tracker: https://github.com/tsuru/tsuru-dashboard
- Talk to us on Gitter: https://gitter.im/tsuru/tsuru
